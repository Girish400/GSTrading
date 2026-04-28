# Design Document

## Objective

Build a reliable trading system around Interactive Brokers that can consume live market data, evaluate a large rules checklist, manage risk, and support paper or live execution with auditability.

## Architectural Direction

### Phase 1: Market Data Foundation

- Connect to TWS or IB Gateway using `ibapi`
- Normalize tick events into application snapshots
- Expose an `asyncio`-friendly consumption model
- Persist optional structured outputs for later replay and analysis

### Phase 2: Rule Evaluation

- Create a rules engine that groups rules by domain:
  - Entry timing
  - Liquidity and spread
  - ORB setup logic
  - Momentum logic
  - Market context
  - Risk gating
  - Execution gating
- Represent each rule as a testable unit with a boolean result and explanation

### Phase 3: Execution and Risk

- Add order intent generation
- Add risk sizing and max-loss enforcement
- Add cooldown and duplicate-trade suppression
- Add stop, target, and exit policy management

### Phase 4: Operations

- Persist trade and rule evaluation logs
- Add dashboards and alerting hooks
- Add deployment profiles for development, paper, and production

## Non-Functional Requirements

- Deterministic logging for every trade decision
- Clear failure behavior on API disconnects and timeouts
- Testability without requiring live market connectivity
- Configuration through CLI and environment-friendly settings
- CI pipelines that lint, test, build, and package the software

## Current Implementation Decision

The repository currently implements a focused market data client rather than the full rules engine. This is intentional: the rules document depends on trustworthy, structured market data first. The current package therefore isolates connectivity and streaming so strategy logic can be layered in without rewriting the application entry point.

## Risks

- `ibapi` is callback-driven and not natively asyncio-first, so thread and event-loop boundaries must stay disciplined.
- Many checklist items require data not yet sourced by the current application, such as breadth, sector, VIX, ATR, RSI, and calendar events.
- Production deployment will need secret handling, environment-specific configuration, and stronger runtime health checks before live execution is enabled.
