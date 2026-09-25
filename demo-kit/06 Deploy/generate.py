#!/usr/bin/env python3
"""
Mill River Mechanical demo kit: date generator.

Takes the Monday of your demo week (S) and writes a dated deployment pack:
  - specs/*.md          one instruction file per system, for Claude to execute via connectors
  - zoho-import/*.csv   Zoho Books import files (paid-bill expenses, recurring invoices)
  - drive/*.csv         AR aging and AP aging snapshots for 03 Finance/
  - MANUAL STEPS.md     the hand steps, with this run's exact dates and amounts
  - CLAUDE PROMPTS.md   the prompts to paste into Claude

Usage:  python3 generate.py 2026-10-05        (must be a Monday)
Output: ./out-2026-10-05/

Standard library only. Reads the customer, vendor, invoice and bill tables
from "../02 Seed data.md", so edit amounts there, not here.
"""
import csv, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
SEED = os.path.join(KIT, "02 Seed data.md")

# ---------------------------------------------------------------- args
if len(sys.argv) != 2:
    sys.exit("usage: python3 generate.py YYYY-MM-DD   (the Monday of your demo week)")
S = dt.date.fromisoformat(sys.argv[1])
if S.weekday() != 0:
    sys.exit(f"{S} is a {S:%A}. S must be a Monday: the story needs S+3 to be Thursday and S+4 Friday.")
OUT = os.path.join(HERE, f"out-{S}")
for sub in ("specs", "zoho-import", "drive"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

def d(o):   return S + dt.timedelta(days=int(o))
def iso(o): return d(o).isoformat()
def mdy(x): return x.strftime("%m/%d/%y")
def nice(o):return d(o).strftime("%a %b %-d, %Y")
def ordinal(n): return f"{n}{'th' if 11<=n%100<=13 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
UNTIL = d(365).strftime("%Y%m%dT235959Z")

# ---------------------------------------------------------------- seed tables
seed = open(SEED, encoding="utf-8").read()
def block(heading):
    i = seed.index(heading); j = seed.index("```csv", i) + 7; k = seed.index("```", j)
    rows = list(csv.reader(seed[j:k].strip().splitlines()))
    return rows[0], rows[1:]

_, cust_rows = block("### Customers")
_, vend_rows = block("### Vendors")
_, closed = block("### 2a")
_, openb = block("### 2b")
_, open_bills = block("### Open vendor bills")
_, paid_bills = block("### Paid bills")

invoices = []
for n, c, i, du, p, a in closed:
    invoices.append(dict(no=n, customer=c, date=iso(i), due=iso(du), paid=iso(p), amount=float(a)))
for n, c, i, du, _dp, a in openb:
    invoices.append(dict(no=n, customer=c, date=iso(i), due=iso(du), paid=None, amount=float(a)))

ACCT = {"Valley Supply Co.": "Cost of Goods Sold", "Nutmeg Sheet Metal": "Cost of Goods Sold",
        "Berkshire Truck & Fleet": "Vehicle Expense", "Dalton Fuel & Propane": "Fuel",
        "Crowley Insurance Agency": "Insurance"}
DESC = {"Valley Supply Co.": "HVAC and plumbing materials", "Berkshire Truck & Fleet": "Van service and tires",
        "Dalton Fuel & Propane": "Shop heat and vehicle fuel", "Crowley Insurance Agency": "GL, auto and workers comp premium",
        "Nutmeg Sheet Metal": "Custom duct and fabrication"}
TERMS = {"Dalton Fuel & Propane": "Net 15"}
bills = []
for n, v, b, du, a, acc in open_bills:
    bills.append(dict(no=n, vendor=v, date=iso(b), due=iso(du), paid=None, amount=float(a), account=acc))
for n, v, b, du, p, a in paid_bills:
    n = n.replace("VSC-87too", "VSC-87840")          # known typo in the seed table
    bills.append(dict(no=n, vendor=v, date=iso(b), due=iso(du), paid=iso(p), amount=float(a), account=ACCT[v]))

open_inv = [x for x in invoices if not x["paid"]]
paid_bill_total = sum(b["amount"] for b in bills if b["paid"])
closed_total = sum(x["amount"] for x in invoices if x["paid"])
BANK = 38900.00
OPENING = BANK + paid_bill_total                      # opening bank so that bank = 38,900 after paid bills
earliest_paid_bill = min(dt.date.fromisoformat(b["paid"]) for b in bills if b["paid"])
OPENING_DATE = (earliest_paid_bill - dt.timedelta(days=1)).isoformat()
CLEAR_DATE = iso(-1)

json.dump(invoices, open(os.path.join(OUT, "specs", "invoices.json"), "w"), indent=1)

# ---------------------------------------------------------------- Drive CSVs
def bucket(dp): return "Current" if dp == 0 else ("1-30" if dp <= 30 else ("31-60" if dp <= 60 else "61+"))
with open(os.path.join(OUT, "drive", "AR aging.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["invoice_no","customer","issue_date","due_date","days_past_due","amount_usd","aging_bucket"])
    for x in open_inv:
        dp = max(0, (S - dt.date.fromisoformat(x["due"])).days)
        w.writerow([x["no"], x["customer"], x["date"], x["due"], dp, f'{x["amount"]:.2f}', bucket(dp)])
with open(os.path.join(OUT, "drive", "AP aging.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["bill_no","vendor","bill_date","due_date","days_past_due","amount_usd","account","terms","status"])
    for b in bills:
        if b["paid"]: continue
        dp = max(0, (S - dt.date.fromisoformat(b["due"])).days)
        w.writerow([b["no"], b["vendor"], b["date"], b["due"], dp, f'{b["amount"]:.2f}', b["account"], TERMS.get(b["vendor"], "Net 30"), "open"])

# ---------------------------------------------------------------- Zoho import CSVs (Zoho's own sample templates)
EXP_HDR = "Entry Number,Expense Date,Expense Account,Paid Through,Vendor,Expense Description,Currency Code,Exchange Rate,Expense Amount,Is Billable,Customer Name,Reference#,Project Name,Mileage Rate,Distance,Start Odometer Reading,End Odometer Reading,Mileage Unit,Mileage Type,Employee Email,Expense Reference ID".split(",")
with open(os.path.join(OUT, "zoho-import", "expenses - paid bill history.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(EXP_HDR)
    for i, b in enumerate(sorted([b for b in bills if b["paid"]], key=lambda b: b["paid"]), 1):
        r = dict.fromkeys(EXP_HDR, "")
        r.update({"Entry Number": i, "Expense Date": mdy(dt.date.fromisoformat(b["paid"])), "Expense Account": b["account"],
                  "Paid Through": "Mill River Operating", "Vendor": b["vendor"], "Expense Description": f'{DESC[b["vendor"]]} — bill {b["no"]}',
                  "Currency Code": "USD", "Exchange Rate": 1, "Expense Amount": f'{b["amount"]:.2f}', "Is Billable": "FALSE",
                  "Reference#": b["no"], "Mileage Rate": 0, "Mileage Type": "NonMileage"})
        w.writerow([r[h] for h in EXP_HDR])

REC_HDR = ["Recurring Invoice Name","Start Date","End Date","Purchase Order","Recurrence Frequency","Repeat Every","Customer Name","Branch Name","Template Name","Currency Code","Exchange Rate","Item Name","SKU","Item Desc","Discount(%)","Quantity","Item Price","Item Tax","Item Tax %","Item Tax Authority","Item Tax Exemption Reason","Notes","Terms & Conditions","PayPal","Authorize.Net","Google Checkout","Invoice Level Tax","Invoice Level Tax %","Invoice Level Tax Authority","Invoice Level Tax Exemption Reason","Project Name","CF.Transporter_Name"]
RECURRING = [  # name, customer, amount, start offset, item description
    ("Northgate — building systems maintenance", "Northgate Mill Properties LLC", 4850, 22, "Building systems maintenance, Bldgs 1 & 2 — monthly, under MSA"),
    ("Whitcomb — RTU service agreement", "Whitcomb Regional Charter School", 2000, 15, "RTU service agreement — monthly"),
    ("Braided River — quarterly service plan", "Braided River Brewing Co.", 1650, 18, "Service plan — monthly"),
    ("Loomis Block — six-building PM", "Loomis Block Property Management", 2280, 12, "Six-building preventive maintenance — monthly"),
    ("Birchwood — dental suite PM", "Birchwood Family Dental", 790, 9, "Dental suite preventive maintenance — monthly")]
def add_months(x, n):
    m = x.month - 1 + n; y = x.year + m // 12; m = m % 12 + 1
    import calendar; return x.replace(year=y, month=m, day=min(x.day, calendar.monthrange(y, m)[1]))
with open(os.path.join(OUT, "zoho-import", "recurring invoices.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(REC_HDR)
    for name, cust, amt, off, desc in RECURRING:
        r = dict.fromkeys(REC_HDR, "")
        r.update({"Recurring Invoice Name": name, "Start Date": mdy(d(off)), "End Date": mdy(add_months(d(off), 11)),
                  "Recurrence Frequency": "Month", "Repeat Every": 1, "Customer Name": cust, "Currency Code": "USD", "Exchange Rate": 1,
                  "Item Name": "Commercial service — maintenance & repair", "Item Desc": desc, "Discount(%)": 0, "Quantity": 1,
                  "Item Price": f"{amt:.2f}", "Notes": "Thanks for your business.", "Terms & Conditions": "Net 15",
                  "PayPal": "FALSE", "Authorize.Net": "FALSE", "Google Checkout": "FALSE"})
        w.writerow([r[h] for h in REC_HDR])

# ---------------------------------------------------------------- spec: Zoho (connector part)
cust_csv = "\n".join(",".join(f'"{c}"' if "," in c else c for c in r) for r in cust_rows)
vend_csv = "\n".join(",".join(f'"{c}"' if "," in c else c for c in r) for r in vend_rows)
open(os.path.join(OUT, "specs", "zoho.md"), "w").write(f"""# Zoho Books seed spec (connector part). Anchor S = Mon {S}.
Throwaway demo org for an invented company. The owner has approved every write in this file.
NEVER use send=true and never email a contact. First call list_organizations and use the org named "Mill River Mechanical".
Check for existing records (list_contacts / list_invoices) and skip anything already there, so a re-run doesn't duplicate.

## 1. Contacts (create_contact)
Customers: contact_type customer. Companies: customer_sub_type business, payment_terms 15, label "Net 15".
Residential: customer_sub_type individual, payment_terms 0, label "Due on Receipt".
contact_name = Company Name if present, else the person's name. Put the person in contact_persons
(first/last/email/phone, is_primary_contact true). billing_address from the row, country "U.S.A". notes = Notes column.
Contact Name,Company Name,Contact Type,Email,Phone,Payment Terms,Billing Street,Billing City,Billing State,Billing Code,Notes
{cust_csv}

Vendors: contact_type vendor (send NO customer-only fields), contact_name = Company Name, person in contact_persons,
payment_terms 30 "Net 30" except Dalton Fuel & Propane 15 "Net 15". notes = Notes.
Contact Name,Company Name,Contact Type,Email,Phone,Payment Terms,Notes
{vend_csv}

## 2. Items (create_item: item_type sales, product_type service, rate 0, default "Sales" income account)
- "Commercial service — maintenance & repair": every commercial invoice except INV-2588. The recurring-invoice import also uses this item by name.
- "Residential service & repair": every residential invoice
- "Equipment — installed": INV-2588 only (Braided River glycol system upgrade)

## 3. Invoices (create_invoice with query ignore_auto_number_generation=true, send false)
One line, quantity 1, rate = amount. date and due_date exactly as given. All 47 are in specs/invoices.json
(paid = payment date; null = still open). Invoices come out as DRAFT; the connector cannot mark them sent. That is expected,
because the owner marks the 13 open ones sent by hand afterward.

## 4. Payments for the 34 paid invoices (create_customer_payment)
Zoho accepts a payment on a draft invoice and flips it to paid. date = paid date, amount = amount_applied = invoice amount,
invoices=[{{invoice_id, amount_applied}}], plus invoice_id and customer_id. account_id = the "Undeposited Funds" account
(list_bank_accounts). payment_mode: commercial "check" (Birchwood Family Dental "autotransaction"), residential "creditcard".

## 5. Verify and report
list_invoices response_option 1: 47 invoices, total {sum(x['amount'] for x in invoices):,.2f}; the 13 open ones total
{sum(x['amount'] for x in open_inv):,.2f} (Northgate {sum(x['amount'] for x in open_inv if x['customer'].startswith('Northgate')):,.2f}).
Undeposited Funds will show {closed_total:,.2f}. That's expected, and a journal clears it later.
Report counts, totals, ids and anything that failed.
""")

# ---------------------------------------------------------------- spec: HubSpot
open(os.path.join(OUT, "specs", "hubspot.md"), "w").write(f"""# HubSpot seed spec. Anchor S = Mon {S}.
Throwaway free portal for an invented company. The owner has approved every write here: pass confirmationStatus "CONFIRMED".
Order: companies → contacts (with company association) → deals → notes (so notes can attach to deals at creation).
First: get_user_details; search_properties for the exact internal values of company `industry`, contact `lifecyclestage`,
`hs_lead_status`, and the default pipeline's `dealstage`. Max 10 objects per request. Search first to avoid duplicates.

Known behaviour (don't fight it):
- `createdate` is read-only, so every contact shows the seeding day as its create date. Leave it.
- HubSpot rejects `.example` contact emails as invalid, so leave email off those three business contacts. @example.com is accepted.
- HubSpot auto-creates a company "example.com" from the homeowners' emails. The connector can't delete it, so the owner deletes it by hand.
- Creating a deal bumps its contact to Opportunity. Set lifecycle back to the value below afterwards.
- Store deal close dates at 12:00 America/New_York so they land on the right day.

## Companies (name | industry | employees | city | domain), all state MA
Northgate Mill Properties LLC | Real Estate | 7 | Easthampton | northgatemill.example
Whitcomb Regional Charter School | Education Management | 44 | Easthampton | whitcombcharter.example
Braided River Brewing Co. | Food & Beverages | 9 | Easthampton | braidedriverbrew.example
Loomis Block Property Management | Real Estate | 4 | Easthampton | loomisblock.example
Birchwood Family Dental | Hospital & Health Care | 8 | Easthampton | birchwooddental.example
Serra Orthodontics | Hospital & Health Care | 11 | Northampton | serraortho.example
Tessier Auto Body | Automotive | 6 | Holyoke | tessierauto.example
Hadley Grove Assisted Living | Hospital & Health Care | 34 | Hadley | hadleygrove.example

## Contacts (first,last,email,company,lifecycle,lead status,job title), residential city Easthampton MA
Dominic,Serra,dserra@serraortho.example,Serra Orthodontics,MQL,Open,Practice Owner
Ellen,Pomeroy,epomeroy@example.com,,Lead,Open Deal,Homeowner
Aliyah,Ferrand,aferrand@example.com,,Lead,New,Homeowner
Nina,Oyelaran,noyelaran@hadleygrove.example,Hadley Grove Assisted Living,MQL,Open,Facilities Director
Ray,Tessier,ray@tessierauto.example,Tessier Auto Body,Lead,Open,Owner
Carl,Brissette,cbrissette@example.com,,Lead,New,Homeowner
Marisol,Da Silva,mdasilva@example.com,,Lead,Open,Homeowner
Peter,Lapointe,plapointe@example.com,,Lead,New,Homeowner
Joanne,Fitzgerald,jfitzgerald@example.com,,MQL,Open,Homeowner
Oscar,Okonjo,ookonjo@example.com,,Lead,New,Homeowner

## Deals (default Sales Pipeline)
Heat pump conversion - Pomeroy residence | contact Ellen Pomeroy | 34500 | Presentation Scheduled | close {iso(9)}
Rooftop replacement - 4 units | Serra Orthodontics + Dominic Serra | 58000 | Qualified To Buy | close {iso(45)}
Bldg 2 boiler replacement | Northgate Mill Properties LLC | 86000 | Appointment Scheduled | close {iso(120)}
FY27 RTU service contract renewal | Whitcomb Regional Charter School | 24000 | Contract Sent | close {iso(14)}
Mini-split install | Tessier Auto Body + Ray Tessier | 11200 | Appointment Scheduled | close {iso(-5)}   <- in the past while open, on purpose
Glycol system upgrade | Braided River Brewing Co. | 19800 | Closed Won | close {iso(-20)}

## Notes (hs_note_body verbatim; hs_timestamp = date at 10:00 America/New_York). These drive "last activity".
Dominic Serra (+Serra company +Serra deal) | {iso(-3)} | Four rooftop units, two at end of life. Budget approved for Q4 — wants a number before the board meets on the 18th.
Ellen Pomeroy (+Pomeroy deal) | {iso(-11)} | Quote sent for full heat pump conversion, $34,500. Asked whether any state or utility rebates apply. Still unanswered.
Aliyah Ferrand | {iso(-1)} | Website form: furnace making a grinding noise, house is cold. Wants someone out this week.
Nina Oyelaran (+Hadley Grove company) | {iso(-6)} | Walked the building with facilities. Four zones, aging boilers. No deadline given.
Ray Tessier (+Tessier company +Tessier deal) | {iso(-41)} | Form fill for a mini-split. No response to two follow-ups.
Joanne Fitzgerald | {iso(-24)} | Asked about water heater replacement in spring. Not urgent, wants a ballpark.
Northgate deal | {iso(-7)} | Walked Bldg 2 boiler room with Karen Vostok. Two cast-iron boilers original to the building. Budgeting for next fiscal year.
Whitcomb deal | {iso(-3)} | Renewal agreement sent to Paula Rennick. Business office cuts the PO after the October board consent agenda.
Braided River deal | {iso(-20)} | Glycol upgrade signed. Deposit received.

## Verify and report
8 companies (+ the auto "example.com" = 9), 10 contacts, 6 deals, 9 notes; associations; stages, amounts, close dates; lifecycle stages.
""")

# ---------------------------------------------------------------- spec: Calendar
def first_on_or_after(start, weekday):
    return start + dt.timedelta(days=(weekday - start.weekday()) % 7)
def nth_weekday(y, m, weekday, n):
    x = dt.date(y, m, 1); x = first_on_or_after(x, weekday); return x + dt.timedelta(weeks=n - 1)
def last_weekday_of_month(y, m):
    import calendar; x = dt.date(y, m, calendar.monthrange(y, m)[1])
    while x.weekday() > 4: x -= dt.timedelta(days=1)
    return x
base = d(-28)
def next_monthly(fn):
    y, m = base.year, base.month
    while True:
        x = fn(y, m)
        if x >= base: return x
        m += 1; y += (m - 1) // 12; m = (m - 1) % 12 + 1
MO, TU, WE, TH, FR = range(5)
series = [
    ("Northgate Mill - building systems service Bldgs 1 & 2", first_on_or_after(base, TH), "09:00", "12:00", f"RRULE:FREQ=WEEKLY;BYDAY=TH;UNTIL={UNTIL}", "240 Ferry St, Easthampton MA", "Gene + Luis. Standing maintenance under MSA"),
    ("Crew huddle - shop", first_on_or_after(base, MO), "07:30", "07:50", f"RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL={UNTIL}", "Shop", "Jobs board and truck assignments"),
    ("Service dispatch - residential", first_on_or_after(base, MO), "08:00", "12:00", f"RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;UNTIL={UNTIL}", "Field", "Residential service calls block"),
    ("Carol - bookkeeping check-in", first_on_or_after(base, TU), "15:00", "15:30", f"RRULE:FREQ=WEEKLY;BYDAY=TU;UNTIL={UNTIL}", "Phone", "Coding questions and AR review"),
    ("Whitcomb Charter - RTU rounds", d(-27), "08:00", "11:00", f"RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TU;UNTIL={UNTIL}", "88 Loudville Rd, Easthampton MA", "Gene + 2. Under service agreement"),
    ("Braided River - rooftop unit check", d(-17), "11:00", "12:30", f"RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=FR;UNTIL={UNTIL}", "17 Union St, Easthampton MA", "Recurring complaint. See Gene's email"),
    ("Commercial site assessment - quote visit", first_on_or_after(base, WE), "10:00", "12:00", f"RRULE:FREQ=WEEKLY;BYDAY=WE;UNTIL={UNTIL}", "Varies", "Dana. New install quotes originate here"),
    ("Crew huddle - shop", first_on_or_after(base, FR), "07:30", "07:50", f"RRULE:FREQ=WEEKLY;BYDAY=FR;UNTIL={UNTIL}", "Shop", "Week close and next week's schedule"),
    ("Payroll clears", d(-24), "ALL-DAY", "", f"RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=FR;UNTIL={UNTIL}", "", f"All-day marker. $31,600 biweekly payroll clears. Next: Fri {iso(4)}"),
    ("Valley Supply rep - check-in", next_monthly(lambda y, m: nth_weekday(y, m, WE, 1)), "14:00", "14:45", f"RRULE:FREQ=MONTHLY;BYDAY=1WE;UNTIL={UNTIL}", "Shop", "Pricing and backorders"),
    ("Month-end close with Carol", next_monthly(last_weekday_of_month), "13:00", "15:00", f"RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1;UNTIL={UNTIL}", "Office", "Reconcile and code"),
    ("Crowley Insurance - policy & comp review", next_monthly(lambda y, m: nth_weekday(y, m, TH, 2)), "09:00", "10:00", f"RRULE:FREQ=MONTHLY;INTERVAL=3;BYDAY=2TH;UNTIL={UNTIL}", "Office", "GL auto and workers comp"),
]
rows = "\n".join(f"| {i} | {s} | {st} {a} | {b} | {r} | {loc} | {desc} |" for i, (s, st, a, b, r, loc, desc) in enumerate(series, 1))
open(os.path.join(OUT, "specs", "calendar.md"), "w").write(f"""# Google Calendar seed spec. Anchor S = Mon {S}.
Primary calendar of the demo account. The calendar's own time zone may be UTC, so ALWAYS pass timeZone "America/New_York".
No attendees (invites to invented addresses bounce into the demo inbox). notificationLevel NONE.
Check list_events first to avoid duplicates. Create #1 (Northgate) FIRST and confirm it has occurrences on Thu {iso(3)}
and on a Thursday about six months out, before creating the rest.

| # | summary | first start (local) | end | recurrence | location | description |
|---|---|---|---|---|---|---|
{rows}

Payroll (#9) must land on Fri {iso(4)}. It's all-day: allDay true, end = start + 1 day.

Also create ONE single all-day event (not recurring), availability FREE:
"Valley Supply VSC-88142 due — $12,400" on Thu {iso(3)}. Description: "Valley Supply Co. statement, account 4471. Invoice VSC-88142,
Net 30, balance $12,400. Payroll ($31,600) clears the next day." (Zoho Free has no Bills, so the calendar and Drive carry the payable.)

Verify: list_events for {iso(0)}..{iso(6)} and report every occurrence. Thu {iso(3)} must show Northgate 9–12 and the Valley Supply marker;
Fri {iso(4)} must show Payroll clears.
""")

# ---------------------------------------------------------------- spec: Gmail
msgs = [
 (-18, "Karen Vostok, Northgate Mill Properties <kvostok@northgatemill.example>", "Rosa Delgado", "Re: Invoice 2618",
  "Rosa — got your note. We're waiting on the tenant in Building 1 to settle their side before we can release this one. Should be sorted shortly. I'll come back to you.\n\nKaren"),
 (-11, "Ellen Pomeroy <epomeroy@example.com>", "Dana Mercier", "Question about the quote",
  "Hi Dana — thanks for getting the quote over so quickly. Before we decide, do any state or utility rebates apply to this kind of conversion? It makes a real difference to us at that number.\n\nThanks, Ellen"),
 (-7, "Crowley Insurance Agency <billing@crowleyins.example>", "Dana Mercier", "Workers comp audit — scheduling",
  f"Dana, the carrier has scheduled your annual workers comp premium audit. Our auditor will need payroll records by class code and your subcontractor certificates for the policy year. We've put you down for the morning of the {ordinal(d(11).day)} — let us know if that doesn't work.\n\nMartin Crowley\nCrowley Insurance Agency"),
 (-6, "Valley Supply Co. AR <ar@valleysupply.example>", "Accounts payable", "Statement — account 4471",
  f"Attached is your statement for the period. Balance due $12,400 on invoice VSC-88142, terms Net 30, due {d(3):%B} {d(3).day}, {d(3).year}. Please remit by the due date to keep your account current. Questions, call the AR desk at 413-555-0301.\n\nValley Supply Co. — Accounts Receivable"),
 (-5, "Google Business Profile (demo seed) <notifications@business.example>", "Mill River Mechanical", "You have a new 2-star review",
  "Mill River Mechanical received a new review.\n\nRating: 2 of 5 stars\nReviewer: S. Brissette\n\n\"Booked a window between 8 and 12, nobody came and nobody called. Second time. The work is fine when they turn up.\"\n\nReply to this review from your Business Profile."),
 (-4, "Tyler Nowak <tnowak.mrm@example.com>", "Dana Mercier", "Notice",
  "Dana — this is hard to write. I've taken a position with a mechanical outfit in Springfield, closer to home and better hours for the kids. My last day would be two weeks from Friday. I'll finish the Whitcomb startup and write up the units I've been carrying so nothing gets lost. Thanks for six years.\n\nTyler"),
 (-4, "HVAC Weekly <digest@hvacweekly.example>", "Mill River Mechanical", "HVAC Weekly — your digest",
  "This week in HVAC Weekly: refrigerant transition timelines, shoulder-season service marketing ideas, and a roundup of new cold-climate heat pump models. Read the full issue online.\n\nYou are receiving this because you subscribed to HVAC Weekly. Unsubscribe | Manage preferences"),
 (-3, "Paula Rennick, Whitcomb Regional Charter School <prennick@whitcombcharter.example>", "Rosa Delgado", "FY27 service contract — our PO process",
  "Rosa, following up on the renewal. Our business office cuts the PO after the board's consent agenda, then AP runs a 45-day cycle from receipt — that's district policy, not us dragging our feet. If you send the countersigned agreement this week it'll be in the October board packet. The invoices you have outstanding are queued and will pay in order.\n\nPaula Rennick\nBusiness Office, Whitcomb Regional Charter School"),
 (-3, "Dominic Serra, Serra Orthodontics <dserra@serraortho.example>", "Dana Mercier", "Re: rooftop units — we have budget approved",
  "Dana — good news, the board approved the capital line for the rooftop work. Four units, two of them on their last legs. I need a real number before the next board meeting on the 18th. What do you need from me to get there?\n\nDominic"),
 (-3, "Marisol Da Silva <mdasilva@example.com>", "Rosa Delgado", "Re: annual tune-up scheduling",
  "Hi Rosa — is it time for our annual again? Last year you came in October I think. Any weekday afternoon is fine.\n\nMarisol"),
 (-2, "Gene Kowalczyk, Service Manager <gene.mrm@example.com>", "Dana Mercier", "Braided River RTU — this one is going to fail",
  "Dana, the rooftop unit at Braided River is short-cycling again. Third time we've been out and third time they've asked us to patch it rather than quote a replacement. Compressor is drawing high and the contactor is pitted. If it goes on a Friday night in the middle of service they're going to lose a weekend of product and it'll be our phone ringing.\n\nI'd like to put a number in front of Andre before that happens.\n\nGene"),
 (-2, "Peter Lapointe <plapointe@example.com>", "Mill River Mechanical", "Water heater — can someone come out?",
  "Water heater is leaking from the bottom, not a lot but steady. It's about twelve years old. Do you replace these or is it worth fixing?\n\nPeter Lapointe, 33 Pleasant Street"),
 (-2, "Valley Pro Supply Deals <promo@valleyprodeals.example>", "Mill River Mechanical", "Fall promo — 20% off fittings",
  "FALL INTO SAVINGS! 20% off all brass and PEX fittings through October 31. Stock up before heating season. Use code FALL20 at checkout. Free delivery on orders over $500.\n\nYou're receiving this email because you're a registered trade customer. Unsubscribe | View in browser"),
 (-1, "Carol Innis <carol.innis.books@example.com>", "Dana Mercier", "September close — need the Northgate coding",
  "Dana, I can't close September until you tell me how to code the Northgate work. Three invoices and I don't know which are under the maintenance agreement and which are billable extras. Ten minutes on the phone and I'm done. Tuesday works.\n\nCarol"),
 (-1, "Aliyah Ferrand <aferrand@example.com>", "Mill River Mechanical", "Website enquiry — furnace noise",
  "Our furnace is making a grinding noise and the house isn't holding heat. We're at 41 Maple. Can someone come out this week? Mornings are better.\n\nAliyah Ferrand"),
]
parts = [f"""# Gmail seed spec. Anchor S = Mon {S}.
Gmail can't send as someone else and can't backdate. So: send each message with send_message TO THE DEMO MAILBOX ITSELF
(the account's own address, from list_labels/search) and to no one else, one at a time, in this order, as plain text `body`.
Each body starts with a 3-line seed header (From / To / Sent) so skills can see the real sender and date.
Keep subjects exactly as written. Before sending, search for self-sent mail with these subjects to avoid duplicates.
Afterwards confirm all 15 are in INBOX and list their ids. Do nothing special with the two noise messages (#7, #13).
"""]
for n, (o, frm, to, subj, body) in enumerate(msgs, 1):
    parts.append(f"---\n## {n}. Subject: {subj}\nBODY:\nFrom: {frm}\nTo: {to}\nSent: {nice(o)}\n\n{body}\n")
open(os.path.join(OUT, "specs", "gmail.md"), "w").write("\n".join(parts))

# ---------------------------------------------------------------- spec: Drive
P = os.path.join(KIT, "05 Drive payload")
open(os.path.join(OUT, "specs", "drive.md"), "w").write(f"""# Google Drive seed spec. Anchor S = Mon {S}.
Build this tree in My Drive of the demo account under a new top-level folder "Mill River Mechanical". Names EXACTLY as written
(em dashes, parentheses). Search first so nothing duplicates. Folders: mimeType application/vnd.google-apps.folder.
Upload with create_file, disableConversionToGoogleType TRUE for every file (keep .md/.csv/.txt/.pdf/.docx/.xlsx native).
Text files: textContent + contentMimeType (text/markdown, text/csv, text/plain). Binary: base64Content from `base64 -w0 "<path>"`.
After each binary upload, compare fileSize in the response to the local byte count and re-upload on mismatch
(an .xlsx came back corrupted twice on the first build; trash the bad copy).
Images (logo, photos, ~0.5–2.5 MB) are too large to pass through the connector, so skip them; the owner drags them in by hand.

Kit root: {KIT}
Mill River Mechanical/
  CLAUDE.md                          <- "{P}/CLAUDE.md"
  00 Brand/
    Brand kit.md                     <- "{KIT}/04 Brand/Brand kit.md"
    Email signature.txt              <- "{KIT}/03 Setup/Email signature.txt"
    Photos/                          (empty; owner uploads images by hand)
  01 Customers/
    Northgate Mill Properties/       <- the 4 files in "{P}/01 Customers/Northgate Mill Properties/"
    Whitcomb Regional Charter School/<- the 2 files in "{P}/01 Customers/Whitcomb Regional Charter School/"
    Braided River Brewing/           <- the 1 file in "{P}/01 Customers/Braided River Brewing/"
    Birchwood Family Dental/         (empty)
    Loomis Block Property Management/(empty)
  02 Jobs/2026/
    J-2601 Pomeroy heat pump conversion/  <- the quote PDF in "{P}/02 Jobs/2026/J-2601 Pomeroy heat pump conversion/", plus empty "Site photos/"
    J-2588 Braided River glycol upgrade/  (empty)
  03 Finance/
    CLAUDE.md                        <- "{P}/03 Finance/CLAUDE.md"
    Revenue history 24mo.csv         <- "{P}/03 Finance/Revenue history 24mo.csv"
    AR aging.csv                     <- "{OUT}/drive/AR aging.csv"   (dated for this run; NOT the payload copy)
    AP aging.csv                     <- "{OUT}/drive/AP aging.csv"   (open bills live here; Zoho Free has no Bills)
  04 Vendors/Valley Supply Co./      (empty)
  05 Team/Job descriptions/Service Technician.docx <- "{P}/05 Team/Job descriptions/Service Technician.docx"

Verify: list every folder's contents, and read the Northgate MSA PDF and quote the sentence with its end date (March 14, 2027).
Report the top folder link.
""")

# ---------------------------------------------------------------- manual steps + prompts
nor = sum(x["amount"] for x in open_inv if x["customer"].startswith("Northgate"))
open(os.path.join(OUT, "MANUAL STEPS.md"), "w").write(f"""# Manual steps for S = Mon {S}

Do these after Claude finishes the connector phase. About 30 minutes in total.

## Zoho Books (in order)
1. **Mark the 13 open invoices as sent.** Sales → Invoices → filter Draft → select all → Mark as Sent.
   (The 34 historical invoices are already Paid. Only the 13 open ones are drafts.)
2. **Chart of accounts.** Accountant → Chart of Accounts → New:
   - Income: Equipment — Installed, Service & Repair, Service Agreements
   - Expense: Fuel
3. **Bank account.** Banking → Add Bank Account → manual, "Mill River Operating", checking. No bank feed.
4. **Opening journal.** Accountant → Manual Journals → New, dated **{OPENING_DATE}**:
   debit Mill River Operating **${OPENING:,.2f}**, credit Opening Balance Adjustments. Note: "Opening balance at migration".
5. **Import paid-bill history as expenses.** Purchases → Expenses → ⋯ → Import → `zoho-import/expenses - paid bill history.csv`.
   Date format MM/DD/YY. 7 rows, ${paid_bill_total:,.2f}. The bank then reads **${BANK:,.2f}**.
6. **Clear Undeposited Funds.** Manual journal dated **{CLEAR_DATE}**: debit Opening Balance Adjustments **${closed_total:,.2f}**,
   credit Undeposited Funds. Note: "Pre-migration receipts, deposited in legacy books".
   Without it, Zoho reports the historical payments as ~${closed_total/1000:,.0f}K of extra cash and the payroll story breaks.
   A journal dated in the future only takes effect on its date.
7. **Import recurring invoices.** Sales → Recurring Invoices → ⋯ → Import → `zoho-import/recurring invoices.csv`
   (5 profiles, monthly, starting {mdy(d(9))}–{mdy(d(22))}).
8. **Bills: skip.** The Free plan has no Bills module. Open payables live in Drive `03 Finance/AP aging.csv` plus a calendar marker.

Check (or ask Claude to check via the connector): open AR **${sum(x['amount'] for x in open_inv):,.2f}**, Northgate **${nor:,.2f}**,
Mill River Operating **${BANK:,.2f}**, Undeposited Funds **$0.00** (once step 6's date has passed).

## HubSpot
- Delete the auto-created company **example.com** (Contacts → Companies). HubSpot makes it from the homeowners' @example.com emails.

## Google
- Gmail → Settings → General → Signature: paste `03 Setup/Email signature.txt`, set as default for new mail and replies.
- Drive: drag `04 Brand/mill-river-mechanical-logo.png` into `00 Brand/`, and the four photos into `00 Brand/Photos/`.
- Drive trash: empty it if Claude trashed any bad uploads.

## Claude settings (demo account only)
- Settings → Profile → Global Instructions: paste `03 Setup/Global instructions.txt`.
- Settings → Cowork → Cowork Instructions: paste `03 Setup/Cowork instructions.txt`.
- Run `smb-onboard` and store the Business Context block from `01 Company bible.md`. Set Onboarded to your workshop date.
""")

open(os.path.join(OUT, "CLAUDE PROMPTS.md"), "w").write(f"""# Prompts for Claude (Cowork), S = Mon {S}

Unzip the kit, attach the whole `out-{S}` folder (or the zip) to a Cowork session on the demo account, and paste:

---
I'm seeding a throwaway demo account for an invented company (Mill River Mechanical; every person, customer and figure is fictional).
All five connectors (Gmail, Google Calendar, Google Drive, HubSpot, Zoho Books) are signed in as the demo account.
First, confirm each connector's signed-in identity and that the systems are empty. Then run five parallel subagents, one per system,
each following its spec file in `specs/` exactly: zoho.md (with invoices.json), hubspot.md, calendar.md, gmail.md, drive.md.
I approve every write described in those specs. Never email anyone except the demo mailbox itself, never set send=true in Zoho,
and don't touch any system outside those five. When they finish, give me one summary table of what landed and anything that failed.
---

After the manual steps, paste:

---
Verify the demo: Zoho open AR is $61,000 (Northgate $23,765), Mill River Operating is $38,900 and Undeposited Funds is $0.
HubSpot has 8 companies, 10 contacts, 6 deals and 9 notes. Calendar shows Northgate Thu {iso(3)} 9–12 and payroll Fri {iso(4)}.
Gmail has the 15 seed messages. Drive `03 Finance/` has AR aging, AP aging, revenue history and CLAUDE.md. Report any mismatch.
---
""")

print(f"Wrote {OUT}")
print(f"  open AR {sum(x['amount'] for x in open_inv):,.2f} | Northgate {nor:,.2f} | closed history {closed_total:,.2f}")
print(f"  opening journal {OPENING:,.2f} on {OPENING_DATE} | paid bills {paid_bill_total:,.2f} | bank {BANK:,.2f}")
print(f"  Thu {iso(3)} Northgate + Valley Supply due | Fri {iso(4)} payroll")
