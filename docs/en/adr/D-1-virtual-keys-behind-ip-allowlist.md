# D-1: Authenticate every API client with a virtual key behind the IP allowlist

| Field | Value |
|---|---|
| Decision ID | D-1 |
| Status | Accepted |
| Date | 2026-11-17 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Platform engineering |
| Decided by | The comparison ([CMP §2.3]); confirmed when 02 is approved |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.1 |
| Supersedes | — |

## 1. Context

Every API caller needs a credential the gateway can check on every request: Claude Code, Codex CLI, IDE plugins, SDKs and workloads. Entra checks the user, MFA and device only at sign-in, so whatever credential the sign-in produces is a bearer credential afterwards [CMP §2.9]. The documentation template assumed Entra access tokens (JWT) fetched by a token helper; the comparison chose LiteLLM virtual keys behind the office/DC IP allowlist instead [CMP §2.3]. Without a decision, the client package (02 §2.2), the key issuance flow (02 §4.5) and the threat model (02 §8.1) have no basis.

## 2. Decision drivers

| Driver | Source |
|---|---|
| Requests without a valid credential are refused before any model call | IAM-002 |
| API requests keep working while Entra cannot be reached | AVL-003; [CMP V-10] |
| Coding agents work with no setup beyond storing a key once, and read it from the OS credential store | FUN-009; [CMP §2.3.4] |
| Requests from outside the office and DC egress IPs are refused | SEC-001; [CMP A-13, A-14] |
| Each option is judged by the threats it blocks that the network and key controls do not already block | [CMP §2.3.6] |
| Unmanaged devices cannot use our egress IPs, so the allowlist stands in for a device check | 01 AS-16; [CMP A-16] |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| LiteLLM virtual key on every request, behind the office/DC IP allowlist; Entra checks the user and device when the key is created | — | Key issuance through the Admin UI (D-2, now D-26); a key helper for Claude Code and Codex CLI (D-3) | A copied key works from any allowlisted IP until it expires or is blocked: [CMP §2.3.6] rows 4–8 need fixes outside client authentication | Chosen |
| Entra access token from a token command, behind the same allowlist | AVL-003: every client needs a working Entra sign-in about once an hour [CMP §2.3.1] | LiteLLM's Enterprise JWT feature [CMP A-6]; a token command on every client [CMP §2.3.1] | Adds protection only in [CMP §2.3.6] rows 4, 6 and 7, which have fixes outside client authentication | Rejected |
| Virtual key plus mTLS with Intune device certificates on every connection | — while built; it is not built by default (D-4) | Intune certificate profile with non-exportable keys, a CRL job, a local mTLS helper per CLI, the TLS-inspection exemption [CMP §2.3.2, §2.3.4] | Claude Code reads certificates only as files and Codex CLI has no certificate option (02 R-3); adds protection only in rows 4 and 8 [CMP §2.3.6] | Rejected as the default; required if V-11 fails or remote access is added (D-4, SEC-003) |

## 4. Decision

Every API client authenticates with a LiteLLM virtual key, and reaches the gateway only from an allowlisted office or DC egress IP. Entra tokens are not used for API traffic. Entra authenticates the user, with MFA and a compliant device, when they sign in to the Admin UI to create the key [CMP §2.3, §2.3.1]. Behind the allowlist, with 01 AS-16 holding, keys block the same threats as Entra tokens or mTLS, with no dependency on Entra or certificates on each request [CMP §2.3.6].

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §6.2 IAM-002; §7.3 SEC-001, SEC-003 | A virtual key on every request; the allowlist; mTLS only on a trigger |
| 02 Architecture and design | §2.3.1, §2.3.2, §3.1, §4.1, §8.1 | Request flows, client authentication table and threat model use virtual keys |
| 04 Configuration reference | §4.2 | No JWT authentication settings; key settings instead (02 R-21) |
| 06 API reference | §2 | Callers send a virtual key in `x-api-key` or `Authorization: Bearer` |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | API traffic does not depend on Entra, the Okta link or a token service; only Admin UI sign-in does | V-10 |
| Benefit | No client certificates to issue, renew or revoke while 01 AS-16 holds | D-4 |
| Cost | Malware or a prompt-injected agent on the managed laptop can use the key ([CMP §2.3.6] row 5); keys that users create are limited to the model routes, so a stolen key cannot create more keys | D-26, R-51 |
| Cost | An unmanaged device behind our egress IPs could use a copied key ([CMP §2.3.6] row 4); V-11 tests this, and mTLS becomes required if it fails | V-11, R-3 |
| Cost | A leaver's key works until it is blocked ([CMP §2.3.6] row 6); the sync job blocks it | D-30 |
| Cost | A key shared with a colleague works from their managed laptop ([CMP §2.3.6] row 7); the alert on one key used from several IPs or user agents detects it | OBS-005 |
| Cost | A workload behind an allowlisted shared NAT could use a stolen key ([CMP §2.3.6] row 8); only dedicated egress IPs are allowlisted | D-24 |
| Follow-up | Keys outlive the device check: a device that falls out of compliance keeps working keys until they expire [CMP §8.8] | 02 §8.1, R-16 |

## 6. Verification and review

- **Verified by:** T-001, T-002, T-011, V-2, V-10, V-11, V-12
- **Revisit when:** remote access is added (01 NG-1, [CMP A-13]); V-11 fails or 01 AS-16 cannot be confirmed (SEC-003); key sharing becomes common, or a team with sensitive data needs per-request proof of the user [CMP §2.3.3]

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | ADR written for the decision accepted in [CMP §2.3] on 2026-11-17, including the authentication and authorization review of 2026-11-20 | Accepted |
