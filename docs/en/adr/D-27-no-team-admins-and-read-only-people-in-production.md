# D-27: Use no team admins, and give people only read-only roles in production

| Field | Value |
|---|---|
| Decision ID | D-27 |
| Status | Proposed |
| Date | 2026-11-20 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Platform engineering |
| Decided by | Platform lead and Security / SOC (pending approval of 02) |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.2 |
| Supersedes | — |

## 1. Context

The comparison has team admins create team and service-account keys [CMP §2.3.5], but routes production changes through CI [CMP §2.3, §2.9]. R-25 records the conflict. A check of the LiteLLM v1.95.0 source on 2026-11-20 found:

- **Team admins.** They need the Enterprise licence, and Entra cannot assign them ([`ui_sso.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/ui_sso.py)). They can add and remove members, change budgets and model access, and add logging callbacks for their team ([`team_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/team_endpoints.py)).
- **Standing `proxy_admin`.** Through `/config/update` it can change runtime settings, including `store_prompts_in_spend_logs` and pass-through routes, whatever `store_model_in_db` is set to ([`proxy_server.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/proxy_server.py)).

Who may change the production gateway must be decided before 04 and 05 are written.

## 2. Decision drivers

| Driver | Source |
|---|---|
| Team membership comes only from Entra groups | 01 TEN-004 |
| Production changes to teams, budgets, models and service-account keys go through CI | 01 OPS-003; [CMP §2.3, §2.9] |
| Service-account keys and keys for other users come only from CI | 01 TEN-002 |
| People hold only read-only roles in the production gateway | 01 IAM-013 |
| Admin roles come from Entra app roles | 01 IAM-004 |
| Every admin action that changes a key, team, budget or model is audited | 01 OBS-001 |
| No prompt content is stored outside the approved stores | 01 PRV-001; 02 §7.3 |
| Team leads see their team's spend and get budget alerts | 01 UC-3, CST-010 |
| Access to per-user reports is agreed with the privacy office | 01 PRV-003 |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| **Roles:** no LiteLLM team admins; team leads are ordinary team members and request changes through a CI pull request; people hold `proxy_admin_viewer` in production. **Admin keys:** `proxy_admin` is held only by the CI identity (a key whose `allowed_routes` covers just the management routes it uses) and by break-glass (D-28); the sync job (D-30) has its own limited key. **Database:** people get read-only IAM DB authentication; writes only through break-glass; pgAudit logs people's sessions to the SIEM. | — | A pull request and a pipeline run for every team, budget, model or workload-key change. Two limited admin keys to manage. pgAudit to set up. | A CI outage delays changes. The CI key can create a key for any user until it is rotated. | Chosen |
| LiteLLM team admins, assigned by hand | TEN-004: admins can change members. TEN-002: admins can create service-account keys. OPS-003: changes bypass CI. IAM-004: the role does not come from Entra. | Enterprise licence. A manual assignment per team, with no Entra mapping. | A team logging callback can send prompts to a destination outside the approved stores (PRV-001) | Rejected |
| Platform engineers hold `proxy_admin` permanently in production | IAM-013, OPS-003 | None | `/config/update` can turn on prompt storage or pass-through routes at runtime. The v1.95.0 audit log does not record guardrail changes ([`audit_logs.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_helpers/audit_logs.py)). | Rejected |
| Platform engineers activate `proxy_admin` through Entra PIM for Groups | — | Entra ID P2 or ID Governance licences ([PIM for Groups](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups)) | Ending the activation does not end access. LiteLLM keeps the role until the next sign-in or sync, and an open session lasts until it expires (D-28). | Rejected for now; see §6 |

## 4. Decision

The production gateway has no LiteLLM team admins. A team lead is an ordinary team member: they see the team's spend in the Admin UI and in Grafana. They request workload keys, budgets, members and models through a CI pull request.

Who holds which role in production:

- **People** hold `proxy_admin_viewer` only.
- **CI** holds `proxy_admin` with a key whose `allowed_routes` covers just the management routes CI uses. That key is released only to protected-branch jobs, on runners with a dedicated egress IP.
- **Break-glass** can also act as `proxy_admin` (D-28).
- **The sync job** has its own admin key, limited to the routes it needs (D-30).

People reach the LiteLLM database only through a read-only IAM DB authentication role. Writes go only through break-glass, and pgAudit sends people's database sessions to the SIEM.

This beats team admins assigned by hand: Entra stays the only source of team membership, and every production change has a reviewed record in Git.

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §2, §2.1, §6.2 | "Team admin" becomes "Team lead"; UC-10 and UC-11 added; IAM-013 added |
| 02 Architecture and design | §4.1, §4.2, §4.3, §4.6 | CI key row; role mapping without team admins; database access for people; scenarios S3 to S9 |
| 02 Architecture and design | §7.1, §10, §13, §14 | Read-only database access; production changes through CI; D-27 row; R-25 mitigated |
| 05 User guide | §3, §5 | Team lead tasks done through CI pull requests |
| 11 Appendices | §A | "Team lead" replaces "Team admin" |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | Entra groups stay the only source of team membership, and no person can write to the production gateway outside CI or break-glass | T-078, V-12 |
| Benefit | Workload keys have one path, through CI, which closes the conflict recorded in R-25 | R-25 |
| Cost | Team leads wait for a reviewed pipeline run to change a budget, member, model or workload key | — |
| Cost | The CI key can create a key for any user, so it can impersonate users. Its use is audited, and its rotation schedule is open. | R-48 |
| Cost | Every team member, including the team lead, sees each member's spend in the Admin UI ([`team_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/team_endpoints.py)) | R-52 |
| Cost | A `proxy_admin` (CI or break-glass) can still change runtime settings. The WAF refuses `/config/*` (D-31), and the v1.95.0 audit log does not record guardrail changes. | R-55 |
| Follow-up | Runners that hold the CI key need a dedicated egress IP. Standard GitHub-hosted runners use shared IP ranges ([GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)). The CI system is not chosen. | R-58 |
| Follow-up | Database Activity Streams are not available on Aurora Serverless v2 ([Database Activity Streams](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/DBActivityStreams.html)), so pgAudit is the source; provisioned or Serverless v2 is still open | R-23 |

## 6. Verification and review

- **Verified by:** V-12, T-013, T-021, T-069, T-078, T-083
- **Revisit when:** CI-only changes become a bottleneck for the number of teams or change requests; or LiteLLM can map team roles from Entra and remove roles when Entra does (then team admins or PIM for Groups can be reconsidered); or the sync job (D-30) resets roles fast enough to end a PIM activation window.

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | Proposed | Proposed |
