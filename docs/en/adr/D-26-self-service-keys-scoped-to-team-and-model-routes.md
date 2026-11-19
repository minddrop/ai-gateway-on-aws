# D-26: Let users create their own keys, charged to their team and limited to model routes

| Field | Value |
|---|---|
| Decision ID | D-26 |
| Status | Proposed |
| Date | 2026-11-20 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Platform engineering |
| Decided by | Platform lead and Security / SOC (pending approval of 02) |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.2 |
| Supersedes | D-2 |

## 1. Context

D-2 let users create "personal keys" in the Admin UI, and left team and service-account keys to team admins or CI [CMP §2.3.5]. A check of the LiteLLM v1.95.0 source on 2026-11-20 found three problems with that wording:

- **The key would have no team.** In LiteLLM's terms a personal key is a key with no team ([`key_management_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/key_management_endpoints.py)), so a self-created key would be charged to no team.
- **Engineers could not create team keys.** By default a team member may only read the team's keys ([`team_member_permission_checks.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_helpers/team_member_permission_checks.py)).
- **A stolen key could mint new ones.** A key with no route limit carries its owner's management rights, so a stolen user key could create, change and delete keys without an Entra sign-in ([`route_checks.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/auth/route_checks.py)).

The issuance rules must be fixed before 04 §4.2 and gate V-2 are written.

## 2. Decision drivers

| Driver | Source |
|---|---|
| Every request is charged to a team that the platform assigns | 01 G-1, CST-001 |
| A user creates keys only for themselves, for a team they belong to, only for the model routes, within the upper bounds, and never with admin rights | 01 TEN-001 |
| Service-account keys and keys for other users come only from CI | 01 TEN-002, OPS-003 |
| A user in no team cannot create a key | 01 TEN-008 |
| Users create, renew and delete their own keys in a web UI | 01 FUN-008 |
| Each key is issued after an Entra sign-in with MFA and a compliant device | 01 IAM-001; [CMP §2.3.1, §2.3.5] |
| A credential that a prompt-injected agent can read must be limited in what it can do | [CMP §2.3.6 row 5] |
| A user without an admin role reads only their own data and their teams' data | 01 IAM-010 |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| Users create keys charged to one of their teams, and each key is an LLM-API key (`key_type: llm_api`) within the upper bounds. Keys with no team are refused. Team members are granted only `/key/generate`. A key policy hook rejects any user-created key that is not `llm_api`. | — | Settings in 04 §4.2. A small policy hook that we maintain across upgrades. LiteLLM v1.103.0 or later, the first version with `custom_key_policy` (R-47). | The hook fails open after an upgrade (R-51). Members are not granted `/key/update`, so renewal means creating a new key and deleting the old one. | Chosen |
| D-2 as written: personal keys with no team; team admins create team and service-account keys | CST-001: self-created keys are charged to no team. TEN-002: team admins can create service-account keys. TEN-001: keys are not limited to model routes. | Team admins need the Enterprise licence and manual assignment, because Entra cannot map them (D-27) | A stolen user key can create, change and delete keys, because nothing limits its routes ([`_types.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/_types.py)) | Rejected |
| Only platform admins issue keys | FUN-008: users cannot create their own keys. IAM-001: the user's device is not checked at issuance. | A platform admin issues every key and every renewal by hand | Keys are handed over outside the Admin UI, so they can be copied on the way [CMP §2.3.5] | Rejected |
| Users request keys through a workflow; CI issues them | FUN-008. IAM-001: no device check at issuance. | A ticket and a pipeline run for every key and renewal | The same hand-over exposure as admin-only issuance | Rejected; kept as the fallback if the Enterprise licence is not bought (AS-6, R-36) |

## 4. Decision

Users create their own keys in the Admin UI after an Entra sign-in. Each key:

- is owned by the user;
- is charged to one of the user's teams, which LiteLLM calls a team key with a user;
- is an LLM-API key: `key_type: llm_api` sets `allowed_routes: ["llm_api_routes"]`, so the key is refused on every management route ([`key_management_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/key_management_endpoints.py));
- stays within `upperbound_key_generate_params`, which LiteLLM enforces on generate, update and regenerate.

The settings that make this hold:

- `key_generation_settings.personal_key_generation.allowed_user_roles: ["proxy_admin"]` refuses keys with no team.
- `default_team_params.team_member_permissions: ["/key/generate"]` lets team members create keys. Members do not get `/key/update`, because it would let them edit any key in the team.
- A key policy hook, `custom_key_policy` (v1.103.0 or later), rejects any key a user creates that is not `llm_api`, on every key operation including regenerate.

Service-account keys, and keys for other users, come only from CI (D-27).

This beats D-2 because it keeps self-service and the device check at issuance, charges every key to a team, and stops a leaked key from creating new ones.

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §6.3 | TEN-001 and TEN-002 reworded; TEN-008 added |
| 02 Architecture and design | §4.5, §4.6 | Key lifecycle rows for keys users create; scenarios S1 and S2 |
| 02 Architecture and design | §11.2, §13 | Gate V-12 (authorization matrix); D-2 marked superseded by D-26 |
| 04 Configuration reference | §4.2 | Rows for `key_generation_settings`, `default_team_params.team_member_permissions`, `custom_key_policy` and `upperbound_key_generate_params` |
| 05 User guide | §3, §5 | Users create keys for their own team; renewal means creating a new key, then deleting the old one |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | Every key a user creates is charged to a team the user belongs to | V-7, V-12 |
| Benefit | A stolen or prompt-injected user key cannot create, change, list or delete keys. That shrinks what [CMP §2.3.6 row 5] leaves open. | V-12 |
| Cost | We write and maintain the key policy hook. If it fails open after an upgrade, user keys can again carry management rights. | R-51 |
| Cost | LiteLLM v1.103.0 or later is required: `custom_key_policy` is not in v1.95.0, and nothing there runs on `/key/regenerate` | R-47 |
| Cost | A user in two teams chooses the team when creating a key; which team should pay in that case is open | 01 Q-12 |
| Cost | Any team member can read every member's spend and the team's key details through `/team/info` and `/key/info` ([`team_endpoints.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/team_endpoints.py)) | R-52 |
| Cost | `llm_api_routes` includes the pass-through prefixes, so an `llm_api` key could call them; the WAF path allowlist refuses them at the edge | D-31, T-081 |
| Follow-up | V-2 tests the upper bounds on generate, update and regenerate, and V-12 tests every key operation, on each pinned version | R-47 |

## 6. Verification and review

- **Verified by:** V-2, V-7, V-12, T-008, T-021, T-080
- **Revisit when:** LiteLLM can enforce `llm_api` on keys users create without a custom hook (for example, a default route list that a request cannot bypass); or the role model in D-27 changes; or remote access is added (01 NG-1).

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | Proposed | Proposed |
