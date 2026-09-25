# Seed data

Everything to load, system by system. Built to be seeded once and left alone for twelve months.

## The rolling design

**S** is the day you load this data. Every date below is an offset in days from S, so one fill-down in a spreadsheet turns the whole set into real dates. Seed once, then leave it.

The calendar, Drive and Gmail are genuinely static for twelve months. The ledger is the one system where an invoice's age is computed from today, so it needs a design rather than a snapshot. This is it:

1. **Twelve months of closed history**, S-365 to S-60, issued *and* paid. This never changes and it is what `invoice-chase` scores payment behaviour on — Northgate averaging 39 days, Whitcomb 44 but never beyond, Birchwood 6.
2. **Thirteen open invoices**, S-61 to S-8, which produce the aging story on day one.
3. **Recurring invoice profiles** in Zoho, monthly per commercial customer, so fresh invoices keep arriving all year without you touching anything.

### What happens over twelve months, and why it is fine

Open AR grows, because nothing new gets marked paid. That sounds like decay and is actually a correction. A contractor billing $3.3M a year should carry $300–400K of receivables at normal payment terms; $61,000 is about six days of sales outstanding, which is unrealistically tidy. As the year runs, AR drifts from too-low toward about-right.

The story degrades gracefully too. Seeded at 47 days overdue, Northgate reads 137 days overdue by month three. `invoice-chase` still ranks it first, still writes it a firmer letter than it writes the school, and the line *"this is what happens when nobody chases"* lands harder with a room of contractors, not softer.

If you ever want the aging tight again, it is four clicks: filter the invoice list to the oldest cohort and bulk **Mark as paid**. Five minutes a quarter, optional, never before a session.

### The one inconsistency, named

A $3.3M contractor with $61K of AR does not add up on close inspection. The reconciliation is in the dataset: Mill River moved to Zoho Books eight weeks before S and brought only open balances across, which is what every small business actually does in a ledger migration. The twelve months of closed history sit in the Drive CSV, not the ledger. That keeps the seeded book small, keeps the Zoho threshold exposure to roughly $120–150K rather than $3.3M, and gives a true answer if anyone in the room asks why the books look thin.

The alternative is to shrink Mill River to six people and about $850K, where $61K of AR is simply correct and no explanation is needed. That is a cleaner dataset and arguably a more representative Easthampton business. It is a real decision — flag it if you want it, and I will rescale every figure in both tabs.

## Zoho slice 1 — customers and vendors

Load these first; invoices and bills reference them by name. Zoho's contact import maps these headers directly. Set the organization to United States, USD, financial year ending 31 December before importing anything.

### Customers

```csv
Contact Name,Company Name,Contact Type,Email,Phone,Payment Terms,Billing Street,Billing City,Billing State,Billing Code,Notes
Karen Vostok,Northgate Mill Properties LLC,Customer,kvostok@northgatemill.example,413-555-0182,Net 15,240 Ferry Street,Easthampton,MA,01027,Two buildings 41 units. Standing Thursday maintenance. Pays when tenants pay
Paula Rennick,Whitcomb Regional Charter School,Customer,prennick@whitcombcharter.example,413-555-0143,Net 15,88 Loudville Road,Easthampton,MA,01027,K-8 310 students. PO cycle runs 45 days. Never misses
Andre Sokol,Braided River Brewing Co.,Customer,andre@braidedriverbrew.example,413-555-0119,Net 15,17 Union Street,Easthampton,MA,01027,Taproom and production. Pays after good weekends
Theresa Loomis,Loomis Block Property Management,Customer,tloomis@loomisblock.example,413-555-0167,Net 15,61 Cottage Street,Easthampton,MA,01027,Six small commercial buildings. Pays on time
Dr. Nadia Cruz,Birchwood Family Dental,Customer,office@birchwooddental.example,413-555-0155,Net 15,9 Northampton Street,Easthampton,MA,01027,Three operatories. Autopay on file
Robert Kaczmarek,,Customer,rkaczmarek@example.com,413-555-0203,Due on Receipt,14 Parsons Street,Easthampton,MA,01027,Residential. First job
Diana Alvarez,,Customer,dalvarez@example.com,413-555-0211,Due on Receipt,52 Holyoke Street,Easthampton,MA,01027,Residential
Marc Bouchard,,Customer,mbouchard@example.com,413-555-0228,Due on Receipt,7 Clark Street,Easthampton,MA,01027,Residential
Susan Brissette,,Customer,sbrissette@example.com,413-555-0234,Due on Receipt,120 Main Street,Easthampton,MA,01027,Residential. Left a 2-star review over a missed window
Peter Lapointe,,Customer,plapointe@example.com,413-555-0240,Due on Receipt,33 Pleasant Street,Easthampton,MA,01027,Residential
Marisol Da Silva,,Customer,mdasilva@example.com,413-555-0247,Due on Receipt,18 Parsons Street,Easthampton,MA,01027,Residential
Joanne Fitzgerald,,Customer,jfitzgerald@example.com,413-555-0252,Due on Receipt,95 East Street,Easthampton,MA,01027,Residential
Oscar Okonjo,,Customer,ookonjo@example.com,413-555-0259,Due on Receipt,4 Adams Street,Easthampton,MA,01027,Residential
Ellen Pomeroy,,Customer,epomeroy@example.com,413-555-0266,Due on Receipt,71 Park Street,Easthampton,MA,01027,Residential. Open heat pump quote
Carl Brissette,,Customer,cbrissette@example.com,413-555-0271,Due on Receipt,140 Main Street,Easthampton,MA,01027,Residential
```

### Vendors

```csv
Contact Name,Company Name,Contact Type,Email,Phone,Payment Terms,Notes
Deb Marchetti,Valley Supply Co.,Vendor,ar@valleysupply.example,413-555-0301,Net 30,HVAC and plumbing wholesaler. The big one
Rick Tanaka,Berkshire Truck & Fleet,Vendor,billing@berkshirefleet.example,413-555-0318,Net 30,Van service and tires
Joan Whitcomb,Dalton Fuel & Propane,Vendor,accounts@daltonfuel.example,413-555-0325,Net 15,Shop heat and vehicle fuel
Martin Crowley,Crowley Insurance Agency,Vendor,billing@crowleyins.example,413-555-0332,Net 30,GL auto and workers comp
Alan Nutt,Nutmeg Sheet Metal,Vendor,shop@nutmegsheetmetal.example,413-555-0349,Net 30,Custom duct and fabrication
```

The five commercial customers carry the whole AR story; the ten residential contacts exist so the book does not look like it has five customers. Every email is on a `.example` domain or `example.com` and will not deliver — that is deliberate. If you later want `invoice-chase` to queue real drafts you can read, point two or three of them at addresses you control.

## Zoho slice 2 — the invoice book

Two files. The first is closed history and never changes. The second is the open book that produces the demo. Dates are day-offsets from **S**; in a spreadsheet, `=$S$1+offset` and fill down.

### 2a — Closed history, issued and paid

This is what `invoice-chase` reads to score each customer's payment behaviour. The `paid_offset` column is the payment date, and the lag it implies is the whole point: Northgate averages 39 days, Whitcomb 44 but never later, Braided River swings, Birchwood pays in a week.

```csv
invoice_no,customer,issue_offset,due_offset,paid_offset,amount_usd
INV-2402,Northgate Mill Properties LLC,-358,-343,-305,12400.00
INV-2411,Whitcomb Regional Charter School,-351,-336,-292,7850.00
INV-2418,Braided River Brewing Co.,-345,-330,-318,4900.00
INV-2424,Loomis Block Property Management,-338,-323,-320,3600.00
INV-2431,Birchwood Family Dental,-330,-315,-309,2180.00
INV-2447,Northgate Mill Properties LLC,-298,-283,-246,11750.00
INV-2455,Whitcomb Regional Charter School,-291,-276,-233,6400.00
INV-2462,Braided River Brewing Co.,-284,-269,-244,5310.00
INV-2469,Loomis Block Property Management,-277,-262,-259,3950.00
INV-2476,Birchwood Family Dental,-270,-255,-248,1920.00
INV-2491,Northgate Mill Properties LLC,-238,-223,-181,13100.00
INV-2498,Whitcomb Regional Charter School,-231,-216,-173,8600.00
INV-2505,Braided River Brewing Co.,-224,-209,-196,3780.00
INV-2512,Loomis Block Property Management,-217,-202,-199,4220.00
INV-2519,Birchwood Family Dental,-210,-195,-189,2450.00
INV-2534,Northgate Mill Properties LLC,-178,-163,-122,12900.00
INV-2541,Whitcomb Regional Charter School,-171,-156,-113,7200.00
INV-2548,Braided River Brewing Co.,-164,-149,-126,6150.00
INV-2555,Loomis Block Property Management,-157,-142,-139,3480.00
INV-2562,Birchwood Family Dental,-150,-135,-129,1760.00
INV-2577,Northgate Mill Properties LLC,-118,-103,-64,14200.00
INV-2584,Whitcomb Regional Charter School,-111,-96,-53,9100.00
INV-2591,Braided River Brewing Co.,-104,-89,-71,5640.00
INV-2598,Loomis Block Property Management,-97,-82,-79,4010.00
INV-2605,Birchwood Family Dental,-90,-75,-69,2290.00
INV-2588,Braided River Brewing Co.,-96,-81,-66,19800.00
INV-2609,Robert Kaczmarek,-88,-88,-86,1420.00
INV-2612,Diana Alvarez,-84,-84,-84,780.00
INV-2614,Marc Bouchard,-80,-80,-78,1150.00
INV-2616,Susan Brissette,-76,-76,-75,640.00
INV-2621,Peter Lapointe,-70,-70,-69,1890.00
INV-2625,Marisol Da Silva,-66,-66,-66,520.00
INV-2629,Joanne Fitzgerald,-64,-64,-62,970.00
INV-2633,Oscar Okonjo,-62,-62,-61,1340.00
```

### 2b — The open book

Thirteen invoices, unpaid at S. This is the aging table the demo runs on: $23,050 in the 31–60 bucket, $28,275 at 1–30, $9,675 not yet due, $61,000 total. Northgate holds $23,765 of it across three invoices — 39% of open AR in one customer, which is the concentration `business-pulse` should notice on its own.

```csv
invoice_no,customer,issue_offset,due_offset,days_past_due_at_S,amount_usd
INV-2618,Northgate Mill Properties LLC,-61,-47,47,14850.00
INV-2634,Whitcomb Regional Charter School,-48,-33,33,8200.00
INV-2651,Braided River Brewing Co.,-40,-25,25,6480.00
INV-2662,Loomis Block Property Management,-36,-21,21,4150.00
INV-2671,Northgate Mill Properties LLC,-33,-19,19,3900.00
INV-2688,Birchwood Family Dental,-27,-12,12,2340.00
INV-2694,Robert Kaczmarek,-25,-10,10,1875.00
INV-2701,Whitcomb Regional Charter School,-22,-7,7,5600.00
INV-2709,Braided River Brewing Co.,-19,-5,5,2970.00
INV-2715,Diana Alvarez,-17,-3,3,960.00
INV-2722,Loomis Block Property Management,-14,1,0,3420.00
INV-2728,Marc Bouchard,-11,4,0,1240.00
INV-2733,Northgate Mill Properties LLC,-8,7,0,5015.00
```

### 2c — Recurring profiles, so the book keeps itself alive

Create these once in Zoho under Sales → Recurring Invoices. They generate fresh invoices monthly for twelve months with no further input, which is what keeps a young aging bucket in the book all year instead of one frozen snapshot.

| Profile | Customer | Amount | Starts | Frequency |
| --- | --- | --- | --- | --- |
| Northgate — building systems maintenance | Northgate Mill Properties LLC | $4,850 | S+22 | Monthly, 12 |
| Whitcomb — RTU service agreement | Whitcomb Regional Charter School | $2,000 | S+15 | Monthly, 12 |
| Braided River — quarterly service plan | Braided River Brewing Co. | $1,650 | S+18 | Monthly, 12 |
| Loomis Block — six-building PM | Loomis Block Property Management | $2,280 | S+12 | Monthly, 12 |
| Birchwood — dental suite PM | Birchwood Family Dental | $790 | S+9 | Monthly, 12 |

Total recurring: $11,570 a month, so AR grows about $139K over the year if nothing is marked paid — landing near $200K, which is closer to right for this company than the $61,000 it starts at.

## Zoho slice 3 — bills, bank, accounts

### Open vendor bills

> **Zoho Free has no Bills module.** These five go into Drive `03 Finance/AP aging.csv` (written by the generator), not the ledger.

```csv
bill_no,vendor,bill_offset,due_offset,amount_usd,account
VSC-88142,Valley Supply Co.,-27,3,12400.00,Cost of Goods Sold
BTF-2209,Berkshire Truck & Fleet,-24,6,1890.00,Vehicle Expense
DFP-4471,Dalton Fuel & Propane,-6,9,2150.00,Fuel
CRW-10036,Crowley Insurance Agency,-18,12,2760.00,Insurance
NGD-771,Nutmeg Sheet Metal,-17,13,1020.00,Cost of Goods Sold
```

The Valley Supply bill at S+3 is deliberate. It falls on the same Thursday as the Northgate site visit and one day before payroll, which is what makes the cash question real rather than rhetorical.

### Paid bills, for history

> Imported into Zoho as **expenses** paid through Mill River Operating (generator file `expenses - paid bill history.csv`).

```csv
bill_no,vendor,bill_offset,due_offset,paid_offset,amount_usd
VSC-87too,Valley Supply Co.,-118,-88,-88,14900.00
VSC-87911,Valley Supply Co.,-88,-58,-57,11200.00
VSC-88031,Valley Supply Co.,-57,-27,-27,13650.00
BTF-2188,Berkshire Truck & Fleet,-85,-55,-55,2240.00
DFP-4402,Dalton Fuel & Propane,-66,-51,-51,1780.00
CRW-9980,Crowley Insurance Agency,-48,-18,-18,2760.00
NGD-742,Nutmeg Sheet Metal,-77,-47,-45,1660.00
```

Correct `VSC-87too` to `VSC-87840` on import — that is a typo, not a code.

### Bank

> You can't type the balance in. Post an opening journal of $87,090 and import the paid-bill expenses ($48,190) to land on $38,900; then clear Undeposited Funds with a journal (see Load order).

One account: **Mill River Operating**, checking, opening balance **$38,900** dated S. Do not connect a real bank feed; enter it as a manual account. A feed would overwrite the balance and take the cash story with it.

### Chart of accounts

Zoho's US default chart covers almost all of it. Add four:

| Account | Type | Why |
| --- | --- | --- |
| Equipment — Installed | Income | Separates install revenue from service |
| Service & Repair | Income | The 55% line |
| Service Agreements | Income | Where the recurring profiles post |
| Fuel | Expense | Dalton Fuel bills need somewhere to go |

### The payroll figure

Payroll does not go in Zoho — there is no Gusto in this stack and the free plan has no payroll module. `cash-flow-snapshot` reads it from the fixed-costs line in the Drive CSV and from the Business Context block. State it there: **$31,600 biweekly, clearing every other Friday, next on S+4.**

## HubSpot seed

Import in this order: companies, then contacts (so the association resolves), then notes, then deals. `lead-triage` reads industry and headcount off the **company** record, not the contact — a contact-only import scores every lead flat and the skill will refuse to present a ranking.

### Companies

```csv
Name,Industry,Number of Employees,City,State,Website
Northgate Mill Properties LLC,Real Estate,7,Easthampton,MA,northgatemill.example
Whitcomb Regional Charter School,Education Management,44,Easthampton,MA,whitcombcharter.example
Braided River Brewing Co.,Food & Beverages,9,Easthampton,MA,braidedriverbrew.example
Loomis Block Property Management,Real Estate,4,Easthampton,MA,loomisblock.example
Birchwood Family Dental,Hospital & Health Care,8,Easthampton,MA,birchwooddental.example
Serra Orthodontics,Hospital & Health Care,11,Northampton,MA,serraortho.example
Tessier Auto Body,Automotive,6,Holyoke,MA,tessierauto.example
Hadley Grove Assisted Living,Hospital & Health Care,34,Hadley,MA,hadleygrove.example
```

### Contacts

```csv
First Name,Last Name,Email,Associated Company,Lifecycle Stage,Lead Status,Job Title,Create Date (offset),Last Activity Date (offset),Email Opens,Last Replied (offset)
Dominic,Serra,dserra@serraortho.example,Serra Orthodontics,Marketing Qualified Lead,Open,Practice Owner,-21,-3,6,-3
Ellen,Pomeroy,epomeroy@example.com,,Lead,Open Deal,Homeowner,-19,-11,4,-11
Aliyah,Ferrand,aferrand@example.com,,Lead,New,Homeowner,-1,-1,1,
Nina,Oyelaran,noyelaran@hadleygrove.example,Hadley Grove Assisted Living,Marketing Qualified Lead,Open,Facilities Director,-14,-6,3,-6
Ray,Tessier,ray@tessierauto.example,Tessier Auto Body,Lead,Open,Owner,-52,-41,1,
Carl,Brissette,cbrissette@example.com,,Lead,New,Homeowner,-4,-4,0,
Marisol,Da Silva,mdasilva@example.com,,Lead,Open,Homeowner,-9,-9,2,
Peter,Lapointe,plapointe@example.com,,Lead,New,Homeowner,-2,-2,0,
Joanne,Fitzgerald,jfitzgerald@example.com,,Marketing Qualified Lead,Open,Homeowner,-31,-24,5,-24
Oscar,Okonjo,ookonjo@example.com,,Lead,New,Homeowner,-6,-6,1,
```

### Notes — attach to the contact, these carry the urgency signal

`lead-triage` scans note **bodies** for "urgent", "ASAP", "deadline" and "budget approved". A note count alone fires nothing, so these have to exist as real note records.

| Contact | Note body |
| --- | --- |
| Dominic Serra | Four rooftop units, two at end of life. Budget approved for Q4 — wants a number before the board meets on the 18th. |
| Ellen Pomeroy | Quote sent for full heat pump conversion, $34,500. Asked whether any state or utility rebates apply. Still unanswered. |
| Aliyah Ferrand | Website form: furnace making a grinding noise, house is cold. Wants someone out this week. |
| Nina Oyelaran | Walked the building with facilities. Four zones, aging boilers. No deadline given. |
| Ray Tessier | Form fill for a mini-split. No response to two follow-ups. |
| Joanne Fitzgerald | Asked about water heater replacement in spring. Not urgent, wants a ballpark. |

### Deals

```csv
Deal Name,Associated Company,Amount,Deal Stage,Close Date (offset),Last Activity (offset)
Heat pump conversion - Pomeroy residence,,34500,Presentation Scheduled,9,-11
Rooftop replacement - 4 units,Serra Orthodontics,58000,Qualified To Buy,45,-3
Bldg 2 boiler replacement,Northgate Mill Properties LLC,86000,Appointment Scheduled,120,-7
FY27 RTU service contract renewal,Whitcomb Regional Charter School,24000,Contract Sent,14,-3
Mini-split install,Tessier Auto Body,11200,Appointment Scheduled,-5,-41
Glycol system upgrade,Braided River Brewing Co.,19800,Closed Won,-20,-20
```

The Tessier deal closes at S-5 — a close date in the past while the deal is still open. That is a specific condition `business-pulse` hunts for, and it should surface unprompted. Two stalled deals at different severities (Pomeroy silent 11 days, Tessier silent 41) give the brief something to rank rather than one lonely flag.

**Stage names** above use HubSpot's default sales pipeline labels so the import does not need a custom pipeline.

## Gmail seed

Compose these into `millrivermech@gmail.com`. The three marked **core** carry the demo; the rest are texture, and the texture is what makes `inbox-manager` look like it is doing something. Send oldest first so the thread order is right.

To send from an invented address without setting up twelve accounts: write them as drafts in the demo mailbox, or use one spare account and change the display name per message. Neither is perfect on close inspection and neither matters on a projector.

### The three that matter

**1. Karen Vostok → Rosa, S-18. Subject: Re: Invoice 2618** — *core*

> Rosa — got your note. We're waiting on the tenant in Building 1 to settle their side before we can release this one. Should be sorted shortly. I'll come back to you.
>
> Karen

Nothing after it. This is the thread `invoice-chase` should find and cite when it justifies a firmer tone for Northgate — a promise made 18 days ago and not kept.

**2. Gene Kowalczyk → Dana, S-2. Subject: Braided River RTU — this one is going to fail** — *core*

> Dana, the rooftop unit at Braided River is short-cycling again. Third time we've been out and third time they've asked us to patch it rather than quote a replacement. Compressor is drawing high and the contactor is pitted. If it goes on a Friday night in the middle of service they're going to lose a weekend of product and it'll be our phone ringing.
>
> I'd like to put a number in front of Andre before that happens.
>
> Gene

**3. Ellen Pomeroy → Dana, S-11. Subject: Question about the quote** — *core*

> Hi Dana — thanks for getting the quote over so quickly. Before we decide, do any state or utility rebates apply to this kind of conversion? It makes a real difference to us at that number.
>
> Thanks, Ellen

**Unanswered.** Leave it that way. Do not seed a rebate program name, amount or eligibility rule anywhere in this dataset — if a skill repeats an invented incentive figure to a room of contractors, someone will know it is wrong and you will spend the next ten minutes on that instead of the demo. The unanswered question is the asset; the answer is a liability.

### The other twelve

| From | Subject | Offset | Role |
| --- | --- | --- | --- |
| Tyler Nowak | Notice | S-4 | Two weeks. Feeds `job-post-builder` |
| Valley Supply Co. | Statement — account 4471 | S-6 | The $12,400 due Thursday |
| Paula Rennick, Whitcomb | FY27 service contract — our PO process | S-3 | Explains the 45-day cycle. Justifies the gentle chase |
| Google Business Profile | You have a new 2-star review | S-5 | S. Brissette, missed appointment window |
| Carol Innis | September close — need the Northgate coding | S-1 | Bookkeeper waiting on Dana |
| Dominic Serra | Re: rooftop units — we have budget approved | S-3 | Mirrors the HubSpot note |
| Aliyah Ferrand | Website enquiry — furnace noise | S-1 | Inbound lead, also in HubSpot |
| Peter Lapointe | Water heater — can someone come out? | S-2 | Ordinary intake |
| Marisol Da Silva | Re: annual tune-up scheduling | S-3 | Ordinary intake |
| Crowley Insurance Agency | Workers comp audit — scheduling | S-7 | Audit lands S+11 |
| Supply vendor marketing blast | Fall promo — 20% off fittings | S-2 | Noise to be filed, not surfaced |
| Trade publication | HVAC Weekly — your digest | S-4 | Noise |

The 2-star review email is worth seeding properly, with the review text in the body: *"Booked a window between 8 and 12, nobody came and nobody called. Second time. The work is fine when they turn up."* That gives `review-reputation` something real to respond to, which matters because it is the substitute skill for the `/customer-pulse-check` that the deck promises and the plugin does not ship.

### The twelve bodies

Short on purpose. Each is one paragraph because that is what real small-business mail looks like.

**Tyler Nowak → Dana, S-4. Notice.** "Dana — this is hard to write. I've taken a position with a mechanical outfit in Springfield, closer to home and better hours for the kids. My last day would be two weeks from Friday. I'll finish the Whitcomb startup and write up the units I've been carrying so nothing gets lost. Thanks for six years. Tyler"

**Valley Supply Co. → accounts, S-6. Statement — account 4471.** "Attached is your statement for the period. Balance due $12,400 on invoice VSC-88142, terms Net 30. Please remit by the due date to keep your account current. Questions, call the AR desk."

**Paula Rennick, Whitcomb → Rosa, S-3. FY27 service contract — our PO process.** "Rosa, following up on the renewal. Our business office cuts the PO after the board's consent agenda, then AP runs a 45-day cycle from receipt — that's district policy, not us dragging our feet. If you send the countersigned agreement this week it'll be in the October board packet. The invoices you have outstanding are queued and will pay in order."

**Google Business Profile → the mailbox, S-5. You have a new 2-star review.** Review body: "Booked a window between 8 and 12, nobody came and nobody called. Second time. The work is fine when they turn up." — S. Brissette

**Carol Innis → Dana, S-1. September close — need the Northgate coding.** "Dana, I can't close September until you tell me how to code the Northgate work. Three invoices and I don't know which are under the maintenance agreement and which are billable extras. Ten minutes on the phone and I'm done. Tuesday works."

**Dominic Serra → Dana, S-3. Re: rooftop units — we have budget approved.** "Dana — good news, the board approved the capital line for the rooftop work. Four units, two of them on their last legs. I need a real number before the next board meeting on the 18th. What do you need from me to get there?"

**Aliyah Ferrand → the mailbox, S-1. Website enquiry — furnace noise.** "Our furnace is making a grinding noise and the house isn't holding heat. We're at 41 Maple. Can someone come out this week? Mornings are better."

**Peter Lapointe → the mailbox, S-2. Water heater — can someone come out?** "Water heater is leaking from the bottom, not a lot but steady. It's about twelve years old. Do you replace these or is it worth fixing?"

**Marisol Da Silva → Rosa, S-3. Re: annual tune-up scheduling.** "Hi Rosa — is it time for our annual again? Last year you came in October I think. Any weekday afternoon is fine."

**Crowley Insurance Agency → Dana, S-7. Workers comp audit — scheduling.** "Dana, the carrier has scheduled your annual workers comp premium audit. Our auditor will need payroll records by class code and your subcontractor certificates for the policy year. We've put you down for the morning of the 16th — let us know if that doesn't work."

**Vendor marketing blast, S-2. Fall promo — 20% off fittings.** Generic supplier promotion. Unsubscribe link, images, no human wrote it. Exists so `inbox-manager` has something to file rather than surface.

**HVAC Weekly → the mailbox, S-4. Your digest.** Trade newsletter. Same purpose.

The two noise messages matter more than they look. A mailbox where every message needs the owner is not an inbox, it is a to-do list, and `inbox-manager` sorting thirteen urgent things proves nothing. The demo lands when it files two and surfaces three.

## Google Calendar seed

Twelve recurring series, created once, each set to end twelve months after S. No guests — invitations to invented addresses bounce into the demo mailbox and pollute it.

```csv
Subject,Start Time,End Time,Recurrence,Location,Description
Crew huddle - shop,07:30,07:50,Weekly on Monday,Shop,Jobs board and truck assignments
Service dispatch - residential,08:00,12:00,Weekly Mon-Fri,Field,Residential service calls block
Northgate Mill - building systems service Bldgs 1 & 2,09:00,12:00,Weekly on Thursday,240 Ferry St,Gene + Luis. Standing maintenance under MSA
Carol - bookkeeping check-in,15:00,15:30,Weekly on Tuesday,Phone,Coding questions and AR review
Whitcomb Charter - RTU rounds,08:00,11:00,Every 2 weeks on Tuesday,88 Loudville Rd,Gene + 2. Under service agreement
Braided River - rooftop unit check,11:00,12:30,Every 2 weeks on Friday,17 Union St,Recurring complaint. See Gene's email
Commercial site assessment - quote visit,10:00,12:00,Weekly on Wednesday,Varies,Dana. New install quotes originate here
Crew huddle - shop,07:30,07:50,Weekly on Friday,Shop,Week close and next week's schedule
Payroll clears,,,Every 2 weeks on Friday,,All-day marker. $31600
Valley Supply rep - check-in,14:00,14:45,Monthly on the first Wednesday,Shop,Pricing and backorders
Month-end close with Carol,13:00,15:00,Monthly on the last weekday,Office,Reconcile and code
Crowley Insurance - policy & comp review,09:00,10:00,Quarterly on the second Thursday,Office,GL auto and workers comp
```

Set the **Northgate Thursday block first** and confirm it recurs weekly for the full twelve months before you build anything else. It is the only event the demo cannot run without: the ledger says Northgate is overdue, the calendar says Gene is standing in their boiler room on Thursday, and the sentence that joins them is the one the room remembers.

Add the prior four weeks of the same series so the calendar has history behind it rather than beginning abruptly at S. Google does this for free if you start the recurrence at S-28.

## Load order

Run `06 Deploy/generate.py` for your S first. It turns every offset below into real dates and writes the specs Claude
executes, plus the Zoho import files. `START HERE.md` has the full walkthrough; this is the short version.

1. **Accounts and connectors.** One throwaway Google account, a HubSpot free portal, and a Zoho Books Free org (US / USD /
   FY ending 31 December). Connect all five connectors in Claude as those accounts.
2. **Claude, in parallel:** Zoho contacts, items, 47 invoices and 34 payments; HubSpot companies, contacts, deals and notes;
   the 12 Calendar series plus the Thursday bill marker; the 15 Gmail messages; the Drive tree. Set the Northgate Thursday
   series first and confirm it recurs.
3. **You, in Zoho:** bulk-mark the 13 drafts as sent; add the four accounts and the Mill River Operating bank account; post the
   opening journal; import the paid-bill expenses; post the Undeposited Funds clearing journal; import the recurring profiles.
4. **You, elsewhere:** delete HubSpot's auto "example.com" company; set the Gmail signature; drag the logo and photos into
   Drive `00 Brand/`; paste the Global and Cowork instructions; run `smb-onboard`.
5. **Verify** with the three checks below, then rehearse the run sheet, timed.

### Changes from the original plan, learned on the first build

- **Bills are not in Zoho.** The Free plan has no Bills module. The five open bills live in Drive `03 Finance/AP aging.csv`
  (the Finance CLAUDE.md says so), and the Valley Supply bill also appears as a calendar marker on S+3. The seven paid bills
  are imported into Zoho as expenses paid from Mill River Operating.
- **The bank balance is built, not typed in.** An opening journal of $87,090 (dated the day before the first paid bill),
  minus $48,190 of paid-bill expenses, leaves $38,900.
- **Undeposited Funds has to be cleared.** Customer payments recorded through the connector land there, and Zoho counts that
  as cash (+$187,650). A journal dated S-1 moves it to Opening Balance Adjustments.
- **Gmail cannot backdate or send as others.** Each seeded message is sent to the demo mailbox with a From / To / Sent header
  in its body. The story dates are in the text; Gmail's own date is the seeding day.
- **HubSpot:** `.example` emails are rejected for contacts (the business contacts have none), `createdate` can't be set, and
  deals push contacts to Opportunity until the lifecycle stage is reset.
- **Recurring profiles** are imported from a CSV in Zoho's own template rather than typed in.

### The three things to verify before you trust it

| Check | Prompt | What good looks like |
| --- | --- | --- |
| The join works | *"what do I need to know this week"* | It names Northgate, the amount, the days overdue **and** the Thursday visit, without being told to look at the calendar |
| The tones separate | *"who owes me money"* | The Northgate draft is firmer than the Whitcomb draft, and it cites the 45-day PO cycle as the reason for the difference |
| The ranking discriminates | *"who should I call first"* | Serra ranks top on "budget approved", Tessier sinks. If everything scores flat, the company associations did not import |

If the first check fails, the calendar series is wrong or the ledger is not connected. Fix it before the session, not during.

### Answered on the first build

- **Zoho accepts a customer payment on a draft invoice** and marks it paid, so closed history needs no "mark sent" step.
- **Journals dated in the future** only take effect on their date. Date the clearing journal S-1 or earlier if you want it live immediately.
