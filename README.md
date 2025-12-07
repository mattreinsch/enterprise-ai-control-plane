enforce policy → notify"  
  - "Review document sensitivity → update tags → restrict access → log decision"  
- Captures **full observability**: runs, decisions, errors, and SLO status

It is intentionally **framework-light** so you can plug in:

- Atlas: `atlas-mlops-snowflake`  
- Intelligence Agent V2: `snowflake-intelligence-agent-v2`  
- Governance Autopilot concepts

---

##  High-Level Architecture

```text
                  ┌───────────────────────────┐
                  │   EXECUTIVE / SYSTEM INPUT │
                  │  (events, questions, SLOs) │
                  └──────────────┬────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │  CONTROL PLANE CORE    │
                    │ (registry + policies   │
                    │   + orchestrat            ▼
   ┌─────────────────────┐                    ┌──────────────────────┐
   │ GOVERNANCE AUTOPILOT│◄─tags / policies─►│ DATA & DOCS & ACTIONS │
   │ (PII, tags, access) │                    │ (SQL, docs, Slack…)  │
   └─────────────────────┘                    └──────────────────────┘

                    ▼
          ┌─────────────────────┐
          │ CONTROL PLANE RUN   │
          │ LOGS, METRICS, SLOs │
          └─────────────────────┘

 Project Layout
src/control_plane/

config.py — global configuration, environment flags

registry.py — in-memory / DB-backed registry for agents & workflows

agents.py — Control Plane view of external agents (Atlas, Intel Agent, etc.)

pod tasks

Call your Snowflake Intelligence Agent V2 from workflows

Plug in real governance rules from Governance Autopilot

 Design Goals

Snowflake-native first

Composable — Atlas, agents, and governance remain separate projects

Auditable — every workflow run is logged

Readable — designed as much as an architecture reference as a codebase

This is a V1: a strong foundation and narrative for enterprise AI leadership roles.

 License

MIT License. See LICENSE for details.

⭐ If This Is Useful

⭐ Star the repo on GitHub

 Use it as a template for your own Control Plane implementation

 Share your extensions (supply chain, compliance, finance)

 Connect with me on LinkedIn (mattreinsch) and subscribe to Data Drift for weekly deep dives on AI platforms & systems.