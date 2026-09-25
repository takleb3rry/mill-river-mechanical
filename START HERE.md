# Mill River Mechanical — demo kit

A ready-made practice business for Claude SMB trainings. It's a 14-person HVAC and plumbing contractor in Easthampton, MA,
seeded across Gmail, Google Calendar, Google Drive, HubSpot and Zoho Books so the SMB plugin's skills have real data to join.
Mill River Mechanical is invented. No person, customer or figure in this kit is real.

**Time to deploy: about 1.5 hours.** Accounts take 20 minutes, Claude's connector phase about 30 (Drive is the slowest part),
and the manual steps another 30. After that, re-seeding for a new date takes about 45 minutes.

## What's in here

| Item | What it is |
| --- | --- |
| `01 Company bible.md` | The company, the story, the demo run sheet, the trainer flags. Read it once. |
| `02 Seed data.md` | Every record, as day-offsets from S. Change amounts or names here. |
| `03 Setup/` | Text for Claude settings and the Gmail signature. |
| `04 Brand/` | Logo, palette and four job-site photos. |
| `05 Drive payload/` | Contracts, CLAUDE.md files and CSVs that go into Drive. |
| `06 Deploy/generate.py` | Takes your demo Monday and writes a dated pack: Claude specs, Zoho import files, Drive CSVs, and your manual steps with exact amounts. |

## Before you start (5 minutes)

1. **Use throwaway accounts only.** You need one Google account (Gmail, Calendar and Drive all hang off it), a HubSpot free CRM
   portal, and a Zoho Books Free organization (United States, USD, fiscal year ending December). Claude can't create accounts for you.
   Use a Claude account set aside for demos.
2. **Pick S, the Monday of your demo week.** Every date in the kit is an offset from S. The story needs Thursday (S+3) to hold the
   Northgate site visit and the $12,400 supply bill, and Friday (S+4) to hold payroll. Seed a few days before S, not weeks before:
   invoice ages count from today, so Northgate's "47 days overdue" is only true on S itself.
3. **Generate the dated pack.** Run `python3 "06 Deploy/generate.py" YYYY-MM-DD` (Python 3, no installs needed). You get
   `06 Deploy/out-YYYY-MM-DD/`. If you don't have Python, attach the kit to Cowork and ask Claude to run it.
4. **Connect the five connectors** in Claude: Gmail, Google Calendar, Google Drive, HubSpot, Zoho Books. Sign each one in with
   the demo accounts, not your own.

## Deploy

### Phase 1: Claude does it (about 30 minutes, runs in parallel)

Attach the `out-YYYY-MM-DD` folder to a Cowork session and paste the first prompt from `CLAUDE PROMPTS.md`. Claude first checks
that every connector is signed in as the demo account and that the systems are empty. It then runs one subagent per system:

| System | What gets seeded |
| --- | --- |
| Zoho Books | 15 customers, 5 vendors, 3 items, 47 invoices ($248,650), 34 payments. The 13 open invoices total $61,000. |
| HubSpot | 8 companies, 10 contacts, 6 deals, 9 notes, with last-activity dates spread out so lead scoring has range |
| Calendar | 12 recurring series from S-28 to S+365, plus a one-off marker for the supply bill due Thursday |
| Gmail | 15 messages, sent to the demo mailbox itself, oldest first |
| Drive | The full folder tree, both CLAUDE.md files, contracts, and the revenue, AR aging and AP aging CSVs |

### Phase 2: you do it (about 30 minutes)

Follow `MANUAL STEPS.md` in your pack. It has this run's exact dates and amounts. In short:

- **Zoho:** mark the 13 draft invoices as sent, add 4 accounts and the "Mill River Operating" bank account, post two journals,
  and import two CSVs (paid-bill history as expenses, and the 5 recurring invoice profiles).
- **HubSpot:** delete the auto-created "example.com" company.
- **Google:** set Dana's Gmail signature, and drag the logo and photos into Drive `00 Brand/`.
- **Claude:** paste the Global and Cowork instructions, then run `smb-onboard` with the Business Context block from the bible.

### Phase 3: verify

Paste the second prompt from `CLAUDE PROMPTS.md`. Then run the three demo checks:

| Prompt | What good looks like |
| --- | --- |
| "what do I need to know this week" | Names Northgate, $14,850, the days overdue **and** Thursday's site visit, without being told to look at the calendar |
| "who owes me money" | The Northgate draft is firmer than the Whitcomb one, and cites the school's 45-day PO cycle as the reason |
| "who should I call first" | Serra ranks first on "budget approved"; Tessier sinks to the bottom |

Target numbers: open AR **$61,000** (Northgate $23,765), bank **$38,900**, Undeposited Funds **$0**. Thursday's arithmetic is
$38,900 − $31,600 payroll − $12,400 bill = **−$5,100**.

## What the tools can't do, and the workaround built into this kit

| Limitation | Workaround in the kit |
| --- | --- |
| **Zoho Free has no Bills module.** | Open payables live in Drive `03 Finance/AP aging.csv`, and its CLAUDE.md says so. Thursday's bill is also a calendar event and a vendor email. Paid bill history goes into Zoho as expenses. |
| The Zoho connector can't mark invoices sent, create bank accounts, post journals, add chart-of-accounts entries or create recurring profiles. | Invoices are created as drafts and you bulk-mark them sent. Everything else is either a UI step or an import CSV in Zoho's own template. |
| Zoho puts historical customer payments in **Undeposited Funds**, which it counts as cash (+$187,650). | A clearing journal dated S-1 empties it. A journal dated in the future only takes effect on its date. |
| The bank balance can't be typed in directly. | An opening journal ($87,090) minus the imported paid bills ($48,190) leaves exactly $38,900. |
| Browser automation of Zoho was blocked partway (Claude's safety check stopped it reading the page's session tokens). | Don't plan on it. The manual steps are quicker than steering a browser anyway. |
| **Gmail can't send as another person or backdate a message.** | Messages go to the mailbox itself. Each body starts with a From / To / Sent header naming the invented sender and the story date, and skills read it. All messages show the day you seeded. |
| HubSpot rejects `.example` contact emails. | The three business contacts have no email; homeowners use @example.com, which HubSpot accepts. |
| HubSpot auto-creates a company "example.com" from homeowner emails, and the connector can't delete it. | Delete it in the UI, or the company count reads 9 instead of 8. |
| HubSpot `createdate` is read-only. | Every contact shows the seeding day as its create date. Recency comes from note timestamps instead, and those can be backdated. |
| Creating a deal bumps its contact to Opportunity. | The spec resets lifecycle stages afterwards. |
| The Drive connector can't carry images (logo 0.5 MB, photos ~2.3 MB), and a binary upload came back corrupted once. | Images are dragged in by hand. The spec checks every upload's size and retries on a mismatch. |
| The Drive connector can't edit a file in place. | To change a file, upload a new one and trash the old. |
| The demo calendar may be set to UTC. | Every event passes America/New_York explicitly. |
| Zoho Free states a $50K revenue limit, and the seeded books hold ~$249K. How Zoho enforces this is unknown. | Seed early and watch for an upgrade prompt. If it trips, move the ledger to a Xero demo company and change nothing else. |
| The kit's original `AR aging.csv` was dated for one fixed Monday. | The generator writes AR and AP aging for your S. |

## Things to know before the room

- **No Google Business Profile.** The 2-star review is an email in the inbox, which is enough for `review-reputation`.
- **No rebate facts, anywhere.** Ellen Pomeroy's unanswered rebate question is the asset. Don't seed an answer.
- **The deck says QuickBooks; the demo runs on Zoho.** Say so out loud. The plugin treats the ledgers as peers.
- **Check the invented names** against real businesses in your region before the first session.
- **Re-seeding for a new date:** run the generator for the new S and seed into fresh accounts, or delete the old records first.
  Everything in the kit is relative to S, so nothing needs rewriting by hand.
