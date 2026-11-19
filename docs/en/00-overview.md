# Internal LLM gateway: Overview

## Document control

| Field | Value |
|---|---|
| System name | Internal LLM gateway |
| Public endpoint | `https://llm.corp.example`: the working name used by the comparison [CMP A-15]; the production hostname is 01 Q-14 |
| Documentation owner | TBD (Product owner, 2026-12-18) (01 Q-1) |
| Technical owner | TBD (Platform engineering, 2026-12-18) (01 Q-1) |
| Status | Draft |
| Review cadence | Every quarter, on every LiteLLM upgrade, and before each model is onboarded |
| Next review | TBD (Product owner, 2026-12-18) (01 Q-1) |
| Source code / IaC | TBD (Platform engineering, 2027-01-29): none exists yet; the system is in the design phase (02 R-22) |
| Source analysis | llm-gateway-comparison commit `46699eb` (2026-11-17) |

**Approvals**

| Role | Name | Date |
|---|---|---|
| Platform engineering lead | TBD (Platform engineering, 2026-12-18) (01 Q-1) | Not approved |
| Security | TBD (Security / SOC, 2026-12-18) (01 Q-1) | Not approved |
| Legal / privacy (residency, content logging) | TBD (Legal / privacy, 2026-12-18) (01 Q-1) | Not approved |
| FinOps (chargeback) | TBD (FinOps, 2026-12-18) (01 Q-1) | Not approved |

Version history: system releases are in 10 Release notes. The two baselines keep their own change logs (01 §11, 02 §15).

## 1. System overview

Internal LLM gateway gives engineers and internal workloads one OpenAI- and Anthropic-compatible endpoint for large language models processed in Japan. Users sign in with Entra ID (Okta Verify MFA, Intune-compliant device) to create their own virtual key for their team; every call carries a virtual key, comes from an allowlisted office or DC network, is charged to a team, and is held to budgets and rate limits [CMP §2.3]. It runs on LiteLLM Proxy in AWS Tokyo, with Osaka for disaster recovery [CMP §7.2]. What it replaces is TBD (Product owner, 2026-12-18) (01 Q-2), and it serves about 5,000 employees, about 300 concurrent users at peak [CMP A-9]. The system is in the design phase: nothing is built yet.

### 1.1 Scope

- **In scope:** model access through the gateway, identity and team mapping, budgets and limits, chargeback data, guardrails, metadata logging
- **Out of scope this phase:** remote and home access; external model APIs that cannot prove in-Japan processing; response caching; model training and fine-tuning; private-line ingress; mTLS with device certificates, unless a launch gate requires it; endpoint families beyond chat, messages, responses and embeddings; residency of identity data. Each one is listed with its reason in 01 §1.3.

### 1.2 Key capabilities

| Capability | What it does | Primary users | Requirement IDs |
|---|---|---|---|
| Model access | One endpoint for the approved, Japan-resident models | Engineers, workloads | FUN-001 to FUN-009, MDL-001 to MDL-011, MDL-101 to MDL-105 |
| Identity | Entra sign-in (MFA, compliant device) to the Admin UI, where each user creates their own virtual key; every API call uses a virtual key | Engineers, workloads | IAM-001 to IAM-014, TEN-001 to TEN-008 |
| Cost control | Per-team budgets, rate and token limits, chargeback reports | Team leads, FinOps | CST-001 to CST-011 |
| Residency and privacy | All processing and logs in Japan; no prompt content stored by default | Legal, security | RES-001 to RES-007, PRV-001 to PRV-004 |
| Guardrails | PII masking, prompt-attack detection, run inside the VPC | Security | SEC-008, SEC-009 |

### 1.3 Stakeholders

Contact details for each role are in 11 §C. Team names are 01 Q-1.

| Role | Team | Responsibility |
|---|---|---|
| Product owner | TBD (Product owner, 2026-12-18) | Priorities, model catalog, roadmap |
| Platform engineering | TBD (Product owner, 2026-12-18) | Build, upgrade, operate |
| On-call | TBD (Product owner, 2026-12-18) | Production incidents |
| Security / SOC | TBD (Product owner, 2026-12-18) | Guardrails, audit review, incidents involving prompts |
| Legal / privacy | TBD (Product owner, 2026-12-18) | Residency and content-logging approvals |
| FinOps | TBD (Product owner, 2026-12-18) | Chargeback, reconciliation with AWS billing |
| Network | TBD (Product owner, 2026-12-18) | Egress IPs, allowlist, TLS-inspection exemption, proof that unmanaged devices cannot use our egress IPs |
| Identity | TBD (Product owner, 2026-12-18) | Entra app registration, Conditional Access, Okta MFA |
| Endpoint / Intune | TBD (Product owner, 2026-12-18) | Client configuration, the key helper, and certificates if mTLS becomes required |

### 1.4 Service levels

The targets are defined in 01. This table names them by ID, so that the two documents cannot disagree.

| Commitment | Defined in |
|---|---|
| Availability | AVL-M01 |
| Gateway latency overhead | PRF-M01 |
| Recovery from loss of the Tokyo region | AVL-M02 (RTO), AVL-M03 (RPO) |
| Support hours | OPS-006 |
| Upstream model availability | Not covered by the gateway SLO unless AVL-M01 says so |

### 1.5 Assumptions and constraints

The full list, with owners and confirmation dates, is in 01 §3–4. The ones a newcomer must know:

- Users are on the corporate network; access is limited to office and DC egress IPs [CMP A-13, A-14].
- Unmanaged devices cannot use those egress IPs; the choice of virtual keys without device certificates rests on this, and launch gate V-11 tests it [CMP A-16].
- Only models processed in Japan are allowed; availability changes, so it is re-checked before onboarding [CMP A-5, A-7].
- Prompt and response content is not stored by default [CMP A-10].
