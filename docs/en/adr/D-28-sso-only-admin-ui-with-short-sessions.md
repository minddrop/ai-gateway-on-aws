# D-28: Allow only SSO sign-in to the Admin UI, with sessions of 8 hours or less

| Field | Value |
|---|---|
| Decision ID | D-28 |
| Status | Proposed |
| Date | 2026-11-20 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Platform engineering |
| Decided by | Platform lead and Security / SOC (pending approval of 02) |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.2 |
| Supersedes | — |

## 1. Context

Every user signs in to the Admin UI to create keys, and admins manage the gateway there [CMP §2.3.5, §2.9]. The comparison left one question open as V-3 (R-2): whether master-key login on `/ui` can be turned off while SSO is on [CMP §2.3.5]. A check of the LiteLLM v1.95.0 source on 2026-11-20 found:

- **Password sign-in still works with SSO on.** LiteLLM accepts `UI_USERNAME`/`UI_PASSWORD`, the master key as the password when `UI_PASSWORD` is unset, and database users' passwords ([`login_utils.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/auth/login_utils.py)).
- **The session ignores Entra's sign-in frequency.** It lasts 24 h by default ([`constants.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/constants.py)) and is never re-checked with Entra. Its cookie wraps a working LiteLLM key. Entra's sign-in frequency cannot end such a session ([session lifetime](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime)), so the 8 h limit in IAM-003 is not met.

LiteLLM also needs an emergency path for when Entra or CI is unavailable.

## 2. Decision drivers

| Driver | Source |
|---|---|
| The web UI accepts sign-in only through Entra, with MFA and a compliant device | 01 IAM-001 |
| Admins sign in again at least every 8 hours | 01 IAM-003 |
| A web UI session ends no later than 8 hours after sign-in, for every role | 01 IAM-011 |
| Every password sign-in on the web UI is off while SSO is configured, or its risk is accepted in writing | 01 SEC-011; [CMP V-3] |
| No person uses the master key for routine work, and everyone who can read it is reviewed | 01 SEC-010 |
| Break-glass admin access to LiteLLM does not depend on Entra, and every use raises an alert | 01 IAM-012 |
| While Entra is down, API traffic keeps working and UI sign-in fails clearly | 01 AVL-003; [CMP V-10] |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| SSO-only sign-in with short sessions, and master-key break-glass on the API (the settings are listed in §4) | — | LiteLLM v1.101.0 or later (R-47). Every user signs in again at least every 8 hours. | Until the session expires, its cookie works as a bearer key; v1.95.0 sets it without HttpOnly or Secure (R-53). Global Administrators bypass "Assignment required" ([application properties](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/application-properties)). | Chosen |
| Keep LiteLLM's defaults: 24 h sessions and password login | IAM-003, IAM-011, SEC-011 | None | `/ui` accepts the master key and database-user passwords from every allowlisted IP (R-2) | Rejected |
| A break-glass database user with a password, plus `disable_env_credential_login` (v1.102.0), which blocks only the configured credentials and the master key used as a password | SEC-011: a password sign-in stays on | One more credential to vault and rotate | A password sign-in on `/ui` from every allowlisted IP | Rejected |
| Turn the master key off entirely | n/a: not possible; the master key always works as an API Bearer token | — | — | Not possible |

## 4. Decision

The Admin UI accepts sign-in through Entra only. The settings:

- `general_settings.disable_password_login_when_sso_enabled: true`, available from v1.101.0, rejects every username and password sign-in once SSO is configured.
- `LITELLM_UI_SESSION_DURATION` is 8 hours or less, for every role. The exact value goes in 04 §4.2, set from 01 Q-15.
- The Entra enterprise app has "Assignment required" on.
- App roles are assigned only through groups, and each person is in exactly one role group. That matters because v1.95.0 uses the first valid role in the token, not the highest.
- `MICROSOFT_TENANT` is our tenant GUID.

LiteLLM break-glass is the master key, used as a Bearer token on the API from an allowlisted IP. Every read of its secret alerts Security, and the key is rotated after each use.

This beats keeping the defaults because it removes every password path to `/ui`. It also makes every session end within the 8 hours that Entra's sign-in frequency cannot enforce on LiteLLM.

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §6.2, §7.3 | IAM-011 and IAM-012 added; SEC-011 covers every password sign-in |
| 02 Architecture and design | §4.1, §4.5 | Admin UI session row and break-glass row; master key row |
| 02 Architecture and design | §7.4, §8.1 | Alert when the master-key secret is read; master-key login threat row |
| 02 Architecture and design | §13, §14 | D-28 row; R-2 and R-53 |
| 04 Configuration reference | §3, §4.2 | Master key readers and rotation after use; rows for `disable_password_login_when_sso_enabled`, `LITELLM_UI_SESSION_DURATION` and `MICROSOFT_TENANT` |
| 07 Operations runbook | §5 | Rotate the master key after every break-glass use |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | `/ui` has no password path once V-3 passes on the pinned version | R-2 |
| Benefit | Every role signs in again, with device and MFA checked, at least every 8 hours | T-076 |
| Cost | The session cookie wraps a LiteLLM key that works until the session ends. v1.95.0 sets the cookie without HttpOnly or Secure. Whether that key can call model routes, and which team it would be charged to, is untested. | R-53 |
| Cost | The session length is one global setting, so engineers sign in again as often as admins | — |
| Cost | Global Administrators can sign in without an assignment. With no app role they get `internal_user_viewer` ([`ui_sso.py`](https://github.com/BerriAI/litellm/blob/v1.95.0/litellm/proxy/management_endpoints/ui_sso.py)). V-12 checks that this role cannot create keys. | V-12 |
| Follow-up | Pin LiteLLM v1.101.0 or later: the password-login switch does not exist in v1.95.0 | R-47 |
| Follow-up | Choose the exact session length within 4–8 hours | 01 Q-15 |
| Follow-up | Decide who may read the master-key secret for break-glass, and write the procedure | TBD (Security / SOC, 2027-01-29) (R-45) |

## 6. Verification and review

- **Verified by:** V-3, T-010, T-012, T-047, T-076, T-077
- **Revisit when:** LiteLLM re-checks sessions with Entra or supports a session length per role; or the pinned version changes the cookie flags or the session key's rights; or remote access is added (01 NG-1).

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | Proposed | Proposed |
