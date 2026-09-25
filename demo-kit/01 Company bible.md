# Mill River Mechanical — Demo Company Bible & Dataset Spec

2026-09-22 · @Jeff

The practice business for the Claude SMB Trainer Program workshop, Easthampton MA.

## How to use this

This is the practice business for the Claude SMB Trainer Program workshop, and the only account anything gets demoed from. Step 2 of the course is explicit: *"Never demo from your own email or calendar. Always use the practice business,"* and *"seed the practice business"* is a day-before task.

Everything below is invented. Mill River Mechanical does not exist, no person named here is real, and no figure came from a real company's books. Before the first workshop, check the five commercial customer names and the company name itself against live businesses in Hampshire and Hampden counties — the names were chosen to sound like the Valley, which is exactly what makes an accidental collision possible.

Dates are written as offsets from **M**, the Monday of the demo week, so the dataset can be re-seeded for any session without rewriting the story. M+3 is that Thursday; M-47 is forty-seven days before that Monday. Where a worked example helps, M = Monday 5 October 2026.

The audience this is built for: the deck's own room profile is \~80% owners of companies with 5–50 people, in construction, manufacturing, contracting, accounting and client services, whose stated priority is automating quoting, intake, follow-up and reporting. Mill River sits in the middle of that.

## The company

Mill River Mechanical Co. LLC is a 14-person HVAC and plumbing contractor at 112 Pleasant Street, Easthampton MA 01027, founded 2011, owner-operated by Dana Mercier, who took it over from her father in 2018. Calendar fiscal year, USD, United States.

Trailing twelve-month revenue is **$3.30M** across three lines:

| Line | Share | TTM revenue | What it is |
| --- | --- | --- | --- |
| Residential service & repair | 55% | $1.82M | Break-fix, tune-ups, water heaters. High volume, low ticket, paid on the spot or in days |
| Heat pump & boiler installs | 30% | $0.99M | $12k–$40k residential conversions. Quote-driven, long sales cycle |
| Light commercial contracts | 15% | $0.49M | Five accounts on annual service agreements. Where all the AR trouble lives |
|  |  |  |  |

### The people

| Name | Role | Why they matter to the demo |
| --- | --- | --- |
| Dana Mercier | Owner | The persona the room is standing in. Every approval gate is hers |
| Rosa Delgado | Office manager — dispatch, AR, the inbox | Owns the mailbox the demo reads |
| Gene Kowalczyk | Service manager | Sends the email that flags the failing brewery rooftop unit |
| Luis Cardona | Install crew lead | On the Thursday Northgate visit |
| Marcus Bell, Tyler Nowak, Priya Raman, Dev Okafor, Sam Trudeau | Service techs | Tyler gives notice at M-4 |
| Aaron Fitch, Nate Brzezinski, Kofi Mensah | Install crew | Payroll volume |
| Jess Lamoureux | Apprentice | — |
| Carol Innis | Bookkeeper, 10 hrs/week | Chases Dana for month-end coding |

Payroll runs biweekly and clears **Friday, M+4**, at $31,600.

### The seasonal shape

Two peaks and two troughs a year, which is what makes the cash forecast worth watching rather than a flat line. Heating work peaks December through February; cooling peaks July and August. The troughs are March–April and September–October — and the demo sits in the second one, after the summer cash has been spent and before the heating rush lands. That is the whole reason Friday is tight.

## Systems and accounts

Everything hangs off one throwaway Google identity. Suggested: `millrivermech@gmail.com`, display name "Mill River Mechanical." A plain Gmail address is right for a 14-person contractor and costs nothing.

| System | Plan | Seeded with | Feeds |
| --- | --- | --- | --- |
| Gmail | Free | \~15 threads | `inbox-manager`, `invoice-chase` drafts, `monday-brief` |
| Google Calendar | Free | 3 weeks of jobs | `monday-brief`, `call-list` |
| Google Drive | Free | Folder tree + contracts + CLAUDE.md | Step 14, Step 16, `contract-review` |
| HubSpot | Free CRM | 5 companies, 10 contacts, 6 deals | `lead-triage`, `business-pulse` |
| Zoho Books | Free | 13 open invoices, paid-bill expenses, one bank account (open bills in Drive AP aging) | `invoice-chase`, `cash-flow-snapshot`, `business-pulse` |
| Revenue history | CSV in Drive | 12 months | `cash-flow-snapshot` fallback, `report-builder` |

### Why Zoho Books, and the one thing to watch

Zoho publishes an official [Zoho Books connector](https://claude.com/connectors/zoho-books) for Claude with read and write, and it ships inside the SMB plugin's own server list — a tested path, not a workaround. The free tier is not API-gated: Zoho's docs put the limit at 100 requests per minute per organization with [1,000 API requests/day on the Free plan](https://www.zoho.com/books/api/v3/introduction/#api-call-limit). A full `business-pulse` run is on the order of a dozen calls.

The risk is eligibility, not permissions — and it is worth separating the two kinds of limit, because only one of them is a counter.

| Limit | Free plan | What Mill River seeds | Verdict |
| --- | --- | --- | --- |
| Invoices per year | 1,000 | \~60 | Nowhere near |
| Bills/expenses per year | 1,000 | \~10 | Nowhere near |
| Users | 1 + 1 accountant | 1 | Fine |
| API requests per day | 1,000 | \~12 per skill run | Fine |
| **Revenue for the financial year** | **$50K** | **\~$249K of invoiced revenue in the ledger** | **Over** |

Zoho's own FAQ states it as a condition on duration, not a metered cap: *"As long as your revenue for the financial year does not exceed the threshold of $50K, Zoho Books's Free Plan is available indefinitely."* Zoho does not publish how it measures that, or what happens when an account's books cross it. I could not find a source either way, so treat it as unresolved rather than settled.

Two things reduce the exposure. The $3.3M trailing-twelve-month figure **never enters Zoho** — it lives in the Drive CSV that `cash-flow-snapshot` reads. What the ledger actually carries is the open AR ($61,000) plus $187,650 of closed history behind it — $248,650 once the seed is loaded. That is about five times the threshold, not sixty-six.

**Do not try to shrink Mill River to fit.** There is no credible 5–50 person business with $50K of annual revenue, and a $3.3M contractor carrying $34K of receivables is a number a room full of contractors will notice in about four seconds. The internal consistency of the dataset is worth more than staying inside a threshold nobody in the room can see.

**Instead, test it empirically and early.** Create the org and seed it several weeks before the first session, then leave it alone and watch for an upgrade prompt. It costs nothing and it is the only way to get a real answer. If it trips, switch the ledger leg to Xero and change nothing else — the plugin treats them as peers, and every other connector in the dataset is untouched.

**The fallback, if the account gets prompted to upgrade:** a free Xero account's demo company. Xero's developer docs say it [connects to an application "the same as with any other Xero organisation"](https://developer.xero.com/documentation/development-accounts/), but it auto-resets 28 days after creation and arrives carrying Xero's own dummy data, which would mix into the AR aging. A Xero trial organisation is empty and clean but needs billing details after 30 days. QuickBooks has no free tier worth the effort: [Intuit's sandboxes](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes) are tied to an app you develop under your own keys, and the connector here is Intuit's published production app.

### Say the mismatch out loud

Slides 28 and 29 of the deck both name QuickBooks as the ledger. Nothing degrades on Zoho — the plugin treats MYOB, NetSuite, QuickBooks, Xero and Zoho Books as peers under its own connector-neutrality rule — but the screen will not match the slide. Name it: *"I built this on a free accounting tier because I wasn't going to pay for a demo."* Half the room is already wondering what this costs.

## The week

Every skill in the demo should land on the same sentence:

> **Northgate owes $14,850, it's 47 days out, and Gene is standing in their boiler room Thursday morning. Ask for the check in person.**

That line is the test of whether the dataset works. If `monday-brief` finds it without being told, the seeding is correct. It only works because the AR record, the calendar event and the email thread are three separate facts in three separate tools — which is the entire argument for connectors.

Five tensions run through the week, each feeding a different skill:

| # | Tension | The fact | Skill it feeds |
| --- | --- | --- | --- |
| 1 | Receivables | $61,000 open, $23,765 of it Northgate across three invoices — 39% of AR in one customer | `invoice-chase`, `business-pulse` |
| 2 | Cash | $38,900 in the bank. $31,600 payroll clears Friday, $12,400 supply bill due Thursday | `cash-flow-snapshot` |
| 3 | Pipeline | A $34,500 heat pump quote sent to Ellen Pomeroy 11 days ago, never followed up | `lead-triage`, `call-list` |
| 4 | Operations | Gene flags that Braided River's rooftop unit is failing and they've deferred three times | `inbox-manager`, `monday-brief` |
| 5 | People | Tyler Nowak gave notice at M-4. No job post up | `job-post-builder` |

### The arithmetic that makes Friday tight

$38,900 in the bank, minus $31,600 payroll Friday, minus the $12,400 Valley Supply bill Thursday, is **negative $5,100** before anything else moves. Northgate's oldest invoice alone covers it. That is not a contrived number — it is what a September shoulder month looks like for a contractor, and half the room has lived it.

### One deliberate omission

The demo does not run `pay-the-bills` or `ap-processor`. The deck's second operator case study (slide 19, Corey at Prospect Butcher Co.) is already an accounts-payable story, told twenty minutes earlier. Leading with AR instead of AP means the live demo extends the deck rather than repeating it.

## Zoho Books dataset

Open AR totals **$61,000**: $23,050 in the 31–60 day bucket, $28,275 at 1–30 days, $9,675 not yet due, nothing past 60. The payer profiles are the point — `invoice-chase` scores each customer and writes three different tones, and a room that sees a gentle note to the school beside a firm one to Northgate understands the skill instantly.

### Customers

| Customer | Type | TTM revenue | Payer profile | Why |
| --- | --- | --- | --- | --- |
| Northgate Mill Properties LLC | Commercial landlord, 2 buildings, 41 units | $142,000 | Repeat late | Pays when their own tenants pay. Biggest client, worst payer |
| Whitcomb Regional Charter School | K–8, 310 students | $96,400 | Good, slow by process | Never misses. Purchase-order cycle just takes 45 days |
| Braided River Brewing Co. | Taproom + production, 9 staff | $71,800 | Occasionally late | Cash-flow-driven, pays after good weekends |
| Loomis Block Property Management | 6 small commercial buildings | $58,200 | Good | Net 15, pays on time |
| Birchwood Family Dental | 3 operatories | $34,900 | Good | Autopay on file, rarely open |

### Open invoices at M

```csv
invoice_no,customer,issue_date,due_date,days_past_due,amount_usd,status
INV-2618,Northgate Mill Properties LLC,M-61,M-47,47,14850.00,overdue
INV-2634,Whitcomb Regional Charter School,M-48,M-33,33,8200.00,overdue
INV-2651,Braided River Brewing Co.,M-40,M-25,25,6480.00,overdue
INV-2662,Loomis Block Property Management,M-36,M-21,21,4150.00,overdue
INV-2671,Northgate Mill Properties LLC,M-33,M-19,19,3900.00,overdue
INV-2688,Birchwood Family Dental,M-27,M-12,12,2340.00,overdue
INV-2694,R. Kaczmarek,M-25,M-10,10,1875.00,overdue
INV-2701,Whitcomb Regional Charter School,M-22,M-7,7,5600.00,overdue
INV-2709,Braided River Brewing Co.,M-19,M-5,5,2970.00,overdue
INV-2715,D. Alvarez,M-17,M-3,3,960.00,overdue
INV-2722,Loomis Block Property Management,M-14,M+1,0,3420.00,open
INV-2728,M. Bouchard,M-11,M+4,0,1240.00,open
INV-2733,Northgate Mill Properties LLC,M-8,M+7,0,5015.00,open
```

Seed 30–40 **paid** invoices behind these, spread over the prior six months, so `invoice-chase` has payment history to score on. Northgate's should show an average of 39 days to pay; Whitcomb's 44 but never beyond; Birchwood's 6.

### Vendor bills due within 14 days

```csv
bill_no,vendor,due_date,amount_usd
VSC-88142,Valley Supply Co.,M+3,12400.00
BTF-2209,Berkshire Truck & Fleet,M+6,1890.00
DFP-4471,Dalton Fuel & Propane,M+9,2150.00
CRW-10036,Crowley Insurance Agency,M+12,2760.00
NGD-771,Nutmeg Sheet Metal,M+13,1020.00
```

### Bank and payroll

One checking account, **$38,900** at M. Biweekly payroll of **$31,600** clears M+4. Nothing else material leaves before M+7.

### Revenue history — `03 Finance/Revenue history 24mo.csv`

This is what `cash-flow-snapshot` reads for seasonality, and the fallback if the ledger is unavailable mid-demo. The file in the kit carries **24 months**, 2025-10 through 2027-09, so it stays current for a full year with no refresh. The twelve rows below are its first half. Two materials figures were corrected against the bank column — June and September 2026 — so the closing balance now chains correctly across all 24 rows.

```csv
month,revenue_usd,collections_usd,payroll_usd,materials_usd,other_opex_usd,bank_eom_usd
2025-10,215000,238000,158000,64000,31000,74200
2025-11,268000,229000,166000,81000,30000,26200
2025-12,312000,281000,174000,94000,33000,6200
2026-01,341000,318000,182000,102000,34000,6200
2026-02,318000,336000,174000,95000,32000,41200
2026-03,236000,289000,166000,71000,31000,62200
2026-04,198000,241000,158000,59000,30000,56200
2026-05,224000,207000,158000,67000,31000,7200
2026-06,289000,248000,166000,88000,32000,-30800
2026-07,334000,301000,182000,100000,34000,-45800
2026-08,321000,347000,174000,96000,33000,-1800
2026-09,244000,296000,166000,72000,31000,25200
```

The negative months are deliberate — Mill River runs a line of credit through the summer install season, which is both realistic and the thing `cash-flow-snapshot` should surface as a pattern rather than a surprise.

## HubSpot dataset

`lead-triage` scores on four dimensions — engagement, company fit, urgency, and a recency penalty — and it refuses to present a ranking if the top and bottom composites differ by less than 10 points. So the seed has to create real spread, not ten identical rows. Three things make that happen: **every lead needs an associated company** (industry and headcount are read off the company record, not the contact), **at least one note body must contain an urgency keyword** ("urgent", "ASAP", "deadline", "budget approved"), and **`notes_last_updated` must vary** or the recency penalty flattens everything.

### Companies

The five customers from the ledger, plus three prospects: Serra Orthodontics (healthcare, 11 employees), Tessier Auto Body (automotive, 6), and Hadley Grove Assisted Living (senior care, 34). Fill `industry` and `numberofemployees` on every one.

### Contacts — lifecycle stage Lead or MQL

```csv
firstname,lastname,email,company,lifecyclestage,hs_lead_status,jobtitle,createdate,notes_last_updated,hs_email_open,hs_sales_email_last_replied,num_associated_deals
Dominic,Serra,dserra@serraortho.example,Serra Orthodontics,MQL,Open,Practice Owner,M-21,M-3,6,M-3,1
Ellen,Pomeroy,epomeroy@example.com,,Lead,Open Deal,,M-19,M-11,4,M-11,1
Aliyah,Ferrand,aferrand@example.com,,Lead,New,,M-1,M-1,1,,0
Nina,Oyelaran,noyelaran@hadleygrove.example,Hadley Grove Assisted Living,MQL,Open,Facilities Director,M-14,M-6,3,M-6,0
Ray,Tessier,ray@tessierauto.example,Tessier Auto Body,Lead,Open,Owner,M-52,M-41,1,,1
Carl,Brissette,cbrissette@example.com,,Lead,New,,M-4,M-4,0,,0
Marisol,"Da Silva",mdasilva@example.com,,Lead,Open,,M-9,M-9,2,,0
Peter,Lapointe,plapointe@example.com,,Lead,New,,M-2,M-2,0,,0
Joanne,Fitzgerald,jfitzgerald@example.com,,MQL,Open,,M-31,M-24,5,M-24,0
Oscar,Okonjo,ookonjo@example.com,,Lead,New,,M-6,M-6,1,,0
```

### Note bodies — these carry the urgency signal

| Contact | Note body | Effect |
| --- | --- | --- |
| Dominic Serra | "Four rooftop units, two at end of life. Budget approved for Q4 — wants a number before the board meets." | Fires the +15 urgency keyword. Should rank #1 |
| Ellen Pomeroy | "Quote sent M-11. Asked whether any state or utility rebates apply to the conversion — still unanswered." | The open loop. Ranks high on deal attachment, penalized on staleness |
| Aliyah Ferrand | "Website form: furnace making a grinding noise, house is cold." | New and urgent, no history |
| Ray Tessier | "Form fill. No response to two follow-ups." | Should sink — proves the ranking discriminates |

### Deals

| Deal | Company | Amount | Stage | Close date | Last activity |
| --- | --- | --- | --- | --- | --- |
| Heat pump conversion — Pomeroy residence | — | $34,500 | Proposal Sent | M+9 | M-11 |
| Rooftop replacement — 4 units | Serra Orthodontics | $58,000 | Qualified to Buy | M+45 | M-3 |
| Bldg 2 boiler replacement | Northgate Mill Properties | $86,000 | Discovery | M+120 | M-7 |
| FY27 RTU service contract renewal | Whitcomb Regional Charter School | $24,000 | Contract Sent | M+14 | M-3 |
| Mini-split install | Tessier Auto Body | $11,200 | Discovery | **M-5** | M-41 |
| Glycol system upgrade | Braided River Brewing Co. | $19,800 | Closed Won | M-20 | M-20 |

The Tessier deal has a close date **in the past while still open** — that is a specific risk `business-pulse` looks for, and it should surface in the Monday brief without prompting. Two stalled-deal signals in one dataset (Pomeroy at 11 days silent, Tessier at 41) give the brief something to rank.

## Gmail dataset

Fifteen threads, sent from free accounts you control or composed directly into the mailbox. Three of them carry the demo; the rest are texture, and the texture matters — `inbox-manager` sorting five real emails is not a demo, sorting fifteen with three that need Dana is.

| # | From | Subject | Sent | What it does |
| --- | --- | --- | --- | --- |
| 1 | Karen Vostok, Northgate Mill Properties | Re: Invoice 2618 | M-18 | *"We're waiting on our own tenant — I'll get to it."* No reply since. The thread `invoice-chase` should find and cite |
| 2 | Gene Kowalczyk | Braided River RTU — this one is going to fail | M-2 | Compressor short-cycling, deferred three times. The operational flag |
| 3 | Ellen Pomeroy | Question about the quote | M-11 | Asks whether any rebates apply. **Unanswered.** The thing Dana owes someone |
| 4 | Tyler Nowak | Notice | M-4 | Two weeks. Triggers `job-post-builder` if you get that far |
| 5 | Valley Supply Co. | Statement — account 4471 | M-6 | The $12,400 due Thursday |
| 6 | Whitcomb business office | FY27 service contract — PO process | M-3 | Explains the 45-day cycle. Justifies the gentle tone in the chase |
| 7 | Google Business Profile | New 2-star review | M-5 | S. Brissette, missed appointment window. Feeds `review-reputation` |
| 8 | Carol Innis | September close — need the Northgate coding | M-1 | Bookkeeper waiting on Dana |
| 9 | Dominic Serra | Re: rooftop units — budget approved | M-3 | Mirrors the HubSpot note. Cross-tool consistency |
| 10–12 | Three residential customers | Service requests | M-1, M-2, M-3 | Ordinary intake |
| 13 | Crowley Insurance Agency | Workers comp audit — scheduling | M-7 | Audit set for M+11 |
| 14–15 | Two vendor marketing blasts | — | M-2, M-4 | Noise `inbox-manager` should file, not surface |

**Do not** put anything in the mailbox that looks like a real person's real address. Use `example.com` and `.example` domains throughout, and keep the display names invented.

One caution on thread 3: write Ellen's question as *"do any state or utility rebates apply to this?"* and leave it unanswered. Do not seed a specific program name, amount or eligibility rule into the dataset — if a skill later repeats a made-up incentive figure to a room of contractors, someone in that room will know it's wrong, and the demo loses the room. The unanswered question is the point; the answer is not.

## Google Calendar dataset

Seed once, for twelve months, using recurring series rather than individual events. Twelve series cover a full year, and Google's recurrence engine does the rest — roughly fifteen minutes of setup and then nothing to maintain.

The design change that makes this work: **the demo-critical events recur weekly, not monthly.** A monthly Northgate visit only lands in the demo week one month in twelve. A weekly Thursday service slot lands in every week of the year, so the demo works whenever you run it. A landlord with 41 units across two buildings on a standing Thursday maintenance slot is entirely ordinary.

### The twelve series

| Event | Recurrence | Time | Why |
| --- | --- | --- | --- |
| Crew huddle — shop | Every Mon | 7:30–7:50 | Opens the week |
| Service dispatch — residential | Every weekday | 8:00–12:00 | Density. One block, not forty calls |
| **Northgate Mill — building systems service, Bldgs 1 & 2** (Gene, Luis) | **Every Thu** | **9:00–12:00** | **The event the whole demo turns on** |
| Carol — bookkeeping check-in | Every Tue | 15:00–15:30 | The month-end thread has a home |
| Whitcomb Charter — RTU rounds (Gene +2) | Every other Tue | 8:00–11:00 | Ties the renewal deal to real work |
| Braided River — rooftop unit check | Every other Fri | 11:00–12:30 | Gene's failing-unit email has somewhere to land |
| Commercial site assessment — quote visit (Dana) | Every Wed | 10:00–12:00 | Where new install quotes come from |
| Crew huddle — shop | Every Fri | 7:30–7:50 | Closes the week |
| Payroll clears | Every other Fri | all-day | The deadline in the cash story |
| Valley Supply rep — check-in | 1st Wed monthly | 14:00–14:45 | Vendor texture |
| Month-end close with Carol | Last weekday monthly | 13:00–15:00 | Feeds `month-end-prep` if you ever demo it |
| Crowley Insurance — policy & comp review | Quarterly, 2nd Thu | 9:00–10:00 | Gives the quarter some weight |

Set every series to run twelve months from the seed date and stop. Decline-free, no guests — invitations to invented addresses will bounce and the bounces land in the demo mailbox.

### Why this one fact matters most

The Thursday Northgate block is the single most important row in this document. It is what turns *"Northgate is 47 days overdue"* into *"Gene is in their boiler room Thursday morning — ask for the check in person."* One fact lives in the ledger, the other in the calendar, and the skill joining them is the entire argument for connectors. Weekly recurrence is what guarantees it is always true on demo day.

### What still drifts

Calendar events do not go stale — a service call last March is simply history, and next March's is already there. The ledger is the one system that cannot be made fully static, because an invoice's age is computed from today. Seeded once at 47 days overdue, Northgate reads 137 days overdue three months later. The demo still runs, `invoice-chase` still finds it and still writes a firmer letter than it writes the school; only the tidy aging-bucket spread changes. The seed data tab handles this with rolling monthly invoice cohorts so the picture stays roughly constant — see it there rather than planning a re-seed.

## Google Drive dataset

The folder tree does double duty: it is the Step 14 project context and the Step 16 context-engineering exercise. Step 16's test prompt is *"Find the most recent contract for my biggest client and tell me when it expires"* — so there must be exactly one defensible answer. Northgate is the biggest client at $142,000 TTM, and their master service agreement is the most recent contract in the tree. The answer is **14 March 2027**.

```
Mill River Mechanical/
  CLAUDE.md
  00 Brand/
    mill-river-mechanical-logo.png
    Brand kit.md
    Email signature.txt
    Photos/                                (4 job-site images)
  01 Customers/
    Northgate Mill Properties/
      2026-03-15 Master Service Agreement — Northgate (term through 2027-03-14).pdf
      2025-11-02 Service Agreement — Northgate (superseded).pdf
      Bldg 1 equipment list.xlsx
      Bldg 2 equipment list.xlsx
    Whitcomb Regional Charter School/
      2024-07-01 RTU Service Contract — Whitcomb (expires 2026-06-30).pdf
      2026-09-08 Renewal proposal — Whitcomb FY27.docx
    Braided River Brewing/
      2025-06-12 Service Agreement — Braided River.pdf
    Birchwood Family Dental/
    Loomis Block Property Management/
  02 Jobs/
    2026/
      J-2601 Pomeroy heat pump conversion/
        2026-09-11 Quote — Pomeroy.pdf
        Site photos/
      J-2588 Braided River glycol upgrade/
  03 Finance/
    CLAUDE.md
    Revenue history 24mo.csv
    AR aging.csv
    AP aging.csv                           (open bills — Zoho Free has no Bills)
  04 Vendors/
    Valley Supply Co./
  05 Team/
    Job descriptions/
      Service Technician.docx
```

### Root CLAUDE.md

```markdown
# Mill River Mechanical — how to work in this folder

We are a 14-person HVAC and plumbing contractor in Easthampton, MA.
Dana Mercier owns the company; Rosa Delgado runs the office.

## How this folder is organized
- `01 Customers/` — one folder per customer. Contracts, equipment lists, correspondence.
- `02 Jobs/` — by year, then job number (J-####). Quotes, photos, sign-offs.
- `03 Finance/` — exports and working files. See its own CLAUDE.md.
- `04 Vendors/` — supplier agreements and price lists.
- `05 Team/` — job descriptions and hiring material. No personnel files here.

## Naming
Dated files start `YYYY-MM-DD`. Contracts carry their end date in the name.
A replaced contract is kept and marked `(superseded)` — never deleted.

## Always
- Quote the contract's own words when you tell me a term or a date.
- Say which file an answer came from.

## Never without asking
- Move or rename anything under `01 Customers/`.
- Write into `03 Finance/`.
- Draft anything addressed to a customer without showing me first.
```

### `03 Finance/CLAUDE.md`

```markdown
# Finance folder

Read-only. Exports from Zoho Books, refreshed monthly by Carol.

- `Revenue history 24mo.csv` — trailing twelve months. Bank balance is end of month.
- `AR aging.csv` — snapshot, not live. The ledger is the source of truth.
- `AP aging.csv` — open vendor bills. Source of truth for payables: Zoho Books (Free plan) has no Bills module.

Never edit a file here. If a number looks wrong, say so — do not correct it.
```

Two CLAUDE.md files, one nested, is exactly the Step 16 teaching point: Cowork reads the nearest one first as it goes deeper.

## The Business Context block

`smb-onboard` writes this to memory and every other skill in the plugin reads it by heading match. Step 11's trainer note is blunt about it: *"Do not skip smb-onboard. Without it the plugin stays generic and the demos fall flat."*

Run the interview live in front of the room the first time — it is good theatre and it is the step people skip. But have this ready to paste if the room is running long, and set `Onboarded` to the workshop date. Field names and the heading must not change.

```markdown
## Business context

- **Business:** HVAC and plumbing contractor — residential service and repair, heat pump and boiler installs, light commercial service contracts
- **Size:** 14 people including the owner
- **Top headaches:** commercial customers paying 40+ days late · quotes going out and never being followed up · making payroll in the shoulder months
- **Connected tools:** Gmail, Google Calendar, Google Drive, HubSpot, Zoho Books
- **Country:** US
- **Currency:** USD
- **Financial year end:** 31 December
- **Weekly cadence:** "Monday brief" every Monday at 7am
- **Website:** millrivermech.example
- **Brand colors:** deep navy #12365B with river blue #5D99C9 and a flame orange #E85A30 accent, on off-white
- **Logo:** 00 Brand/mill-river-mechanical-logo.png
- **Output preference:** visual artifacts
- **Onboarded:** <workshop date>
```

The three headaches are chosen deliberately. Each one maps to a skill you will run in the next ten minutes — `invoice-chase`, `lead-triage`, `cash-flow-snapshot` — so when the plugin recommends a starting stack, it recommends the demo you were about to give anyway. That is not a trick; it is what a real onboarding does when the answers are honest.

## Demo run sheet — Step 5

Step 5 caps this at ten minutes and says the point is the setup, not the show: *"the demo is the setup, not the show."* Three skills, one story, nothing sent.

| Time | What you do | What the room sees |
| --- | --- | --- |
| 0:00–0:30 | Frame it. *"This is not my business. This is Mill River Mechanical — 14 people, Easthampton, HVAC and plumbing. Real tools, real data, none of it mine."* | The premise. Say it once, clearly |
| 0:30–3:30 | `/monday-brief` | Cash, AR, pipeline, the week — converging on Northgate. Let it finish before you talk over it |
| 3:30–6:30 | Type *"who owes me money"* | Three drafts in three tones. Open the Northgate one beside the Whitcomb one and let them read the difference |
| 6:30–9:00 | Type *"will I make payroll Friday"*, then *"make me a visual of that"* | The $5,100 gap, then an artifact. This also pre-sells Step 13 |
| 9:00–9:30 | Close. *"Nothing was sent. Nothing was paid. Every one of those is a draft waiting on Dana. Your turn."* | Hand off to Step 6 |

### The three things to say while it runs

1. **On the Monday brief:** point at where the Northgate line came from. *"The invoice is in the accounting system. The Thursday site visit is in the calendar. Nobody typed that sentence — it joined them."* That is the connector argument, and it is the only moment in the day you get to make it with evidence on screen.
2. **On invoice-chase:** name why the tones differ. The school is not late, its purchase-order cycle is 45 days; Northgate is 47 days out for the fourth time this year. *"It read the payment history. Would you have sent the same email to both?"*
3. **On the cash forecast:** say the number out loud. Negative $5,100 before Northgate pays. Then stop talking — that number does the work.

### What not to do

Do not approve a send. Do not run a fourth skill because the room is enjoying it. Do not open the marketplace and browse — Step 11's trainer note warns that people get lost there. And do not demo `pay-the-bills`: Corey's accounts-payable story was twenty minutes ago on slide 19.

## Seeding checklist

> Superseded by `START HERE.md` and `06 Deploy/`, which reflect what actually worked on the first build. Kept for reference.

Build in this order — each step depends on the one above it. Budget a full working day for the first build and about 90 minutes to re-seed for a later session.

- [ ] Create `millrivermech@gmail.com`. Turn off notification sounds and sign out of every other Google account in that browser profile
  - [ ] Set up the signature line in Gmail settings — Dana Mercier's block, from `00 Brand/Email signature.txt`. Every draft `invoice-chase` queues inherits it, and an unsigned draft on screen reads as a toy
- [ ] Google Drive: build the folder tree, write both CLAUDE.md files, generate the contract PDFs (the Northgate MSA matters most — it must say 14 March 2027 in its own words)
- [ ] Drop `Revenue history 24mo.csv` and `AR aging.csv` into `03 Finance/`
- [ ] Zoho Books Free: create the organization, US/USD/31 December, the five commercial customers plus residential contacts, then the 13 open invoices and 30–40 paid ones, then the five vendor bills, then the bank balance
- [ ] HubSpot free portal: companies first (industry and headcount filled), then contacts with their associated company, then note bodies, then deals
- [ ] Google Calendar: three weeks of events. Thursday 9:00 Northgate first
- [ ] Gmail: fifteen threads, oldest first so the dates land right
- [ ] Connect all five connectors in Claude and confirm each returns data
- [ ] Run `smb-onboard`, paste or speak the Business Context block
- [ ] Rehearse the full run sheet end to end, timed. Step 2 says do this three days out, not the night before

### What decays

| Thing | Decays how | Fix |
| --- | --- | --- |
| Every date | The whole story is relative to M. Two weeks later, "47 days overdue" is 61 days and the aging buckets shift | Re-date invoices, calendar and email before each session. This is most of the 90 minutes |
| Zoho free tier | Seeded books exceed the stated $50K eligibility | Watch for an upgrade prompt. Xero demo company is the fallback |
| HubSpot engagement fields | Open counts and last-activity timestamps age | Touch a few records so the recency penalty still separates leads |
| The Gmail thread dates | Cannot be back-dated once sent | Send them fresh each cycle, or accept compressed spacing |

The re-dating is the real maintenance cost and it is worth automating early. Once the dataset is built once, a script that takes a new M and rewrites the invoice, calendar and deal dates turns a 90-minute chore into five minutes — and it is a good candidate for the `build-agent` demo if you ever want a fifth skill in the run sheet.

## Trainer flags

Four places where the material contradicts itself or the product. None are fatal; all of them will surface in a room if you do not get ahead of them.

| Flag | Where | What to do |
| --- | --- | --- |
| **`/customer-pulse-check` does not exist** | Deck slide 30 lists it among six commands under the claim *"Every one of these is a real Cowork command — pre-built, ready to run upon install."* Step 11's trainer tab also names it for service businesses. No such skill ships in the plugin (v1.35.1) | Fix the slide, or say the swap out loud before anyone types it. `review-reputation` is the substitute — *"what are customers saying"* |
| **Cowork is no longer a separate thing** | Deck slide 27 presents Chat / Code / Cowork as three products. Step 7 says Cowork's abilities are now built into Chat with no separate tab | Step 7 is newer. Teach it that way and correct the slide, or the room spends the morning hunting for a Cowork tab |
| **A missing step** | Step 15's trainer tab admits a renumbering (*"originally step 6"*), and the app's own internal section IDs jump from step5 to step7 | Cosmetic, but expect the deck's numbering and the app's to disagree. Don't reference step numbers out loud |
| **The assessment doesn't exist** | Step 16 closes by telling learners to take a Skilljar assessment, and the page itself flags that it hasn't been built | Do not read that closing line. Close on the two-week app window instead |

One more, not a defect: the deck's room profile (slide 6) is written for Tulsa — headcount mix, sectors, and *"Hello, Tulsa!"* on slide 2. Rewrite it for Easthampton before the first session. The sector list happens to fit your expected room almost exactly, so the substance stands; only the city and the partner logos need changing.
