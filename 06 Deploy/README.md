# 06 Deploy

`generate.py` turns the offsets in `02 Seed data.md` into a dated deployment pack for one demo Monday (S).

    python3 generate.py 2026-10-05

It writes `out-2026-10-05/`:

| File | Use |
| --- | --- |
| `CLAUDE PROMPTS.md` | Paste the first prompt into Cowork to seed everything the connectors can reach; paste the second to verify. |
| `specs/*.md`, `specs/invoices.json` | One instruction file per system. Claude runs one subagent per file in parallel. |
| `zoho-import/expenses - paid bill history.csv` | Zoho → Purchases → Expenses → Import. Zoho's own expense template, dates MM/DD/YY. |
| `zoho-import/recurring invoices.csv` | Zoho → Sales → Recurring Invoices → Import. Zoho's own recurring-profile template. |
| `drive/AR aging.csv`, `drive/AP aging.csv` | Dated snapshots for Drive `03 Finance/` (the Drive spec uploads them). |
| `MANUAL STEPS.md` | The hand steps, with this run's journal dates and amounts. |

The script refuses a date that isn't a Monday. It uses only the Python standard library. To change amounts, names or offsets,
edit the tables in `02 Seed data.md`. HubSpot, Calendar and Gmail content lives in the script itself.

Tested for S = 2026-09-28 (matches the first live build exactly) and S = 2027-01-11.
