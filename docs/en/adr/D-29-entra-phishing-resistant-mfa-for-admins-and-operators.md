# D-29: Require an Entra phishing-resistant method for gateway admins and operators

| Field | Value |
|---|---|
| Decision ID | D-29 |
| Status | Proposed |
| Date | 2026-11-20 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Identity |
| Decided by | Identity and Security / SOC (pending approval of 02) |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.2 |
| Supersedes | — |

## 1. Context

IAM-003 and IAM-007 require phishing-resistant MFA for gateway admins and for operators of the AWS accounts. [CMP §2.1] puts this in CA-GW-02 ("phishing-resistant MFA where available (Okta FastPass, or Windows Hello for Business as an Entra method)") and CA-GW-05, while Okta Verify reaches Entra as an External Authentication Method (01 AS-2). Entra requires phishing-resistant MFA only through an authentication strength, and External MFA cannot satisfy any authentication strength, including the built-in Phishing-resistant MFA strength ([External MFA](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-external-method-provider)). So CA-GW-02 and CA-GW-05 cannot be built as written. Conditional Access also cannot target the holders of an app role, only users, groups, directory roles and workload identities ([CA assignments](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-users-groups)).

## 2. Decision drivers

| Driver | Source |
|---|---|
| Admins sign in with a compliant device and phishing-resistant MFA, and again at least every 8 hours | IAM-003 |
| Operators sign in to the AWS console and CLI with phishing-resistant MFA, a compliant device and an office or DC IP | IAM-007 |
| Entra ID is the only IdP, and one policy engine evaluates MFA, device compliance and location | CON-3; [CMP §2.1] |
| Okta is used only for MFA, attached to Entra as an External Authentication Method | 01 AS-2; [CMP A-2] |
| The control must be enforced and testable in Entra: a push-only sign-in by an admin or operator is refused | T-012, T-016 |
| Admins and operators can register an Entra-native phishing-resistant method | 01 AS-22 |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| Entra-native phishing-resistant method (passkey / FIDO2, Windows Hello for Business, or certificate-based authentication), required by the built-in Phishing-resistant MFA authentication strength in CA-GW-02 and CA-GW-05; Okta Verify through External MFA stays the MFA for everyone else (CA-GW-01) | — | Admins and operators register a second method; Identity sets the authentication-method policy and the two policies | Synced passkeys count as phishing-resistant ([authentication strengths](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths)); whether admins may use them is open | Chosen |
| Okta FastPass, required only by Okta's own policy for admins and operators, with Entra requiring "Require MFA" | IAM-003, IAM-007: Entra sees only External MFA and cannot check which Okta method was used, so the control cannot be enforced or tested in Entra | No new method in Entra | If Okta's policy accepts a push for an admin, Entra accepts it too | Rejected |
| Federate the domain to Okta and accept its MFA claim (`federatedIdpMfaBehavior`) [CMP §2.1.2] | CON-3, 01 AS-2: Okta becomes the federated IdP | Domain federation is a larger blast radius to change [CMP §2.1] | Policy split across two engines; Intune compliance still evaluated only by Entra [CMP §2.1] | Rejected |
| "Require MFA" through External MFA only, for admins and operators as for users | IAM-003, IAM-007: no phishing resistance | None | A colleague can complete someone else's sign-in by having them approve a push [CMP §2.3.3] | Rejected |

## 4. Decision

Members of the gateway's admin and viewer groups (CA-GW-02) and operators signing in to IAM Identity Center (CA-GW-05) must satisfy the built-in Phishing-resistant MFA authentication strength with an Entra-native method: a passkey or FIDO2 security key, Windows Hello for Business, or certificate-based authentication. CA-GW-02 targets those groups, because Conditional Access cannot target app-role holders. Okta Verify through External MFA stays the MFA for all other users (CA-GW-01). This deviates from [CMP §2.1], which names Okta FastPass. It is the only option that Entra itself can enforce and that T-012 and T-016 can test.

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §3 AS-22; §4 CON-3; §9 Q-15 | New assumption that admins and operators can register an Entra-native method; CON-3 names the exception; Q-15 asks Identity to confirm |
| 02 Architecture and design | §4.2, §4.4 | CA-GW-02 targets the admin and viewer groups with the Phishing-resistant MFA strength; CA-GW-05 uses the same strength |
| 02 Architecture and design | §11.1 T-012, T-016; §13; §14 R-56 | Tests sign in with External MFA only and with an Entra-native method; decision row; risk on the comparison's policy set |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | Entra enforces and logs the method for every admin and operator sign-in, so IAM-003 and IAM-007 can be tested | T-012, T-016 |
| Cost | Admins and operators hold two MFA methods: Okta Verify for other apps, and an Entra-native method for the gateway and AWS | 01 AS-22 |
| Cost | CA-GW-02 and CA-GW-05 differ from [CMP §2.1]; the comparison's policy set cannot be met as written | R-56 |
| Follow-up | Whether synced passkeys are allowed for admins and operators | TBD (Identity, 2026-12-18) (01 Q-15) |
| Follow-up | Global Administrators can sign in to the app even with "Assignment required" ([application properties](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/application-properties)); whether CA-GW-02 also targets the Global Administrator directory role | TBD (Identity, 2026-12-18) (01 Q-15) |
| Follow-up | If admins or operators cannot register an Entra-native method, IAM-003 and IAM-007 cannot be met | 01 AS-22, R-56 |

## 6. Verification and review

- **Verified by:** T-012, T-016
- **Revisit when:** Entra lets External MFA satisfy authentication strengths; Okta stops being attached through External MFA (01 AS-2); 01 AS-22 turns out false

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | Proposed after the authentication and authorization review of 2026-11-20 found that External MFA cannot satisfy authentication strengths | Proposed |
