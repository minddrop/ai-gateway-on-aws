# D-30: Reconcile LiteLLM with Entra through a sync job instead of SCIM

| Field | Value |
|---|---|
| Decision ID | D-30 |
| Status | Proposed |
| Date | 2026-11-20 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Platform engineering |
| Decided by | Platform lead and Security / SOC (pending approval of 02) |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.2 |
| Supersedes | — |

## 1. Context

Entra is the source of truth for users, teams and roles (01 AS-1, TEN-004, IAM-004). LiteLLM v1.95.0 applies Entra only at sign-in, and only in one direction:

- it adds team memberships but never removes them;
- it keeps the stored role when the token carries no valid role ([`ui_sso.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/ui_sso.py)).

A leaver's or mover's keys therefore keep working until they are revoked [CMP §2.3.6 row 6]. The comparison proposes SCIM, plus an offboarding job if SCIM does not block keys [CMP §2.4].

SCIM has two problems here. When it deactivates a user, it blocks only the keys that user owns ([`scim_v2.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/scim/scim_v2.py)). And Entra's provisioning service connects from Microsoft's `AzureActiveDirectory` IP ranges ([SCIM provisioning](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups)), which the allowlisted ALB refuses.

## 2. Decision drivers

| Driver | Source |
|---|---|
| A disabled user's keys stop working within the target time | 01 IAM-006, Q-8 |
| A user who leaves a team loses that team's keys within the target time | 01 TEN-004, TEN-007 |
| An admin role removed in Entra stops granting admin rights | 01 IAM-004 |
| The allowlist holds only dedicated egress IPs of ours, with no shared ranges | 01 SEC-001, SEC-002; 02 D-6 |
| Egress goes only to allowlisted hostnames; Microsoft Graph is already on the list | 01 SEC-013; 02 §6 |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| A scheduled job in the gateway VPC reads Entra through Microsoft Graph (outbound, through Network Firewall). It calls the LiteLLM admin API inside the VPC with its own key, limited to the routes it uses. | — | We write, test and run the job. An application permission in Graph to read users and group memberships. One more limited admin key. | Changes take effect only on the job's next run, plus up to 60 s of key cache after a key is deleted (`user_api_key_cache_ttl`, [`team_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/team_endpoints.py)). If the job stops, access stays in place until someone notices. | Chosen |
| LiteLLM SCIM, with `/scim/*` opened to the `AzureActiveDirectory` ranges | SEC-002: the allowlist would admit Microsoft's service ranges, which are not dedicated egress IPs of ours | Enterprise licence. Security-group and WAF rules for ranges that Microsoft changes. The SCIM token is a key owned by the admin who created it. | Keys the user does not own keep working. Whether SCIM group updates remove team memberships has not been checked. | Rejected |
| Entra's on-premises SCIM provisioning agent ([on-premises SCIM provisioning](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/on-premises-scim-provisioning)), which connects outbound only | — | A Windows Server to run and patch, in the DC or in AWS; Entra ID P1 | The same LiteLLM SCIM limits as the option above | Rejected |
| Rely on sign-in and key expiry only | IAM-006, TEN-007, IAM-004 | None | Leavers' and movers' keys keep working for up to 90 days [CMP §2.3.6 row 6] | Rejected |

## 4. Decision

A scheduled sync job runs in the gateway VPC. It reads Entra through Microsoft Graph, over the outbound path through Network Firewall that is already allowed. It calls the LiteLLM admin API inside the VPC with its own key, which is limited to the routes it uses. On each run it does three things:

- blocks every key owned by a user whose Entra account is disabled;
- removes users from teams whose group they have left, with `/team/member_delete`, which deletes their keys for that team;
- resets roles that Entra no longer grants.

LiteLLM SCIM is not used. The job's interval and its blocking target come from 01 Q-8.

This beats SCIM because it needs no inbound path through the allowlist. It also handles team removals and role resets, which LiteLLM never does at sign-in.

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §2.1, §6.3 | UC-4 and UC-9; TEN-004 reworded; TEN-007 added |
| 02 Architecture and design | §2.1, §2.2 | Sync job added to the context diagram and the component table |
| 02 Architecture and design | §4.2, §4.5, §7.2 | Provisioning column; leaver and mover rows; how users and teams are removed |
| 02 Architecture and design | §6 | The tasks' security group also admits the sync job on port 4000 |
| 02 Architecture and design | §8.1, §11.1, §13, §14 | Leaver and mover threats; T-013, T-015 and T-020; D-30 row; R-35 and R-54 |
| 11 Appendices | §A | SCIM is used only for IAM Identity Center |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | Leavers, movers and role removals take effect without waiting for a sign-in, and without any inbound path to the ALB | T-013, T-015, T-020 |
| Cost | The job is custom code that must be retested on every LiteLLM upgrade, and its key is an admin key | R-54 |
| Cost | A key deleted by `/team/member_delete` or `/user/delete` may keep working for up to the key cache time (60 s by default). This was inferred from the code, not tested. | R-54 |
| Cost | Service-account keys have no person as owner, so blocking a user leaves them working. They are rotated by CI at least every 90 days. | 01 TEN-006 |
| Follow-up | Set the job's interval and the blocking target | 01 Q-8 |
| Follow-up | Alert when the job fails or cannot reach Graph | R-39 |
| Follow-up | Agree the Graph application permission for the job with Identity | TBD (Identity, 2026-12-18) (R-54) |
| Follow-up | Retest whether a later version's SCIM, or its sign-in, removes team memberships and blocks every affected key | R-35 |

## 6. Verification and review

- **Verified by:** T-013, T-015, T-020, V-12
- **Revisit when:** a pinned LiteLLM version removes team memberships and resets roles at sign-in or through SCIM, and passes T-015 and T-020.

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | Proposed | Proposed |
