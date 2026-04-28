# Project Tracker

## Status Legend

- `TODO`
- `IN PROGRESS`
- `DONE`
- `BLOCKED`

## Milestones

| ID | Work Item | Status | Notes |
|---|---|---|---|
| PT-001 | Create production-grade repository scaffold | DONE | Package, docs, tests, CI/CD, templates |
| PT-002 | Implement reliable AAPL market data ingestion | DONE | `ibapi` + `asyncio` baseline |
| PT-003 | Translate DOCX checklist into machine-readable rule definitions | TODO | Needed for rule engine |
| PT-004 | Add market context providers for VWAP, breadth, sector, and VIX | TODO | External data sources required |
| PT-005 | Add risk engine and trade journaling | TODO | Must precede order placement |
| PT-006 | Add paper trading execution adapter | TODO | Safer first deployment target |
| PT-007 | Add live trading guardrails and release controls | TODO | Requires operational review |

## Immediate Next Steps

1. Convert the checklist into grouped rule specifications.
2. Define market data interfaces needed for each rule group.
3. Add structured logging and replay fixtures from captured ticks.
