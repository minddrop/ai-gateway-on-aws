# Internal LLM gateway: Requirements

| Field | Value |
|---|---|
| Document ID | REQ-GW |
| Version | 0.1 |
| Status | Draft |
| Owner | TBD (Product owner, 2026-12-18): named in Q-1 |
| Approvers | Security, legal/privacy, network, FinOps, platform lead |
| Related design | 02 Architecture and design |
| Source analysis | llm-gateway-comparison commit `46699eb` (2026-11-17) |
| Last updated | 2026-11-17 |

## 1. Purpose and scope

### 1.1 Problem statement

Engineers want to use AI coding agents such as Claude Code and Codex CLI, and internal workloads and agents want to call large language models [CMP A-4]. Company rules require that prompts, responses and everything derived from them are processed and stored only in Japan [CMP A-5, A-11], and that no prompt content is stored by default [CMP A-10]. Without one controlled path, nobody can show where prompts were processed, who used which model, or what each team spent. A single gateway on AWS Tokyo gives that path, and enforces residency, identity, limits and chargeback on every call [CMP §7.2]. What engineers use today, and what the gateway replaces, is Q-2.

### 1.2 Goals

| ID | Goal (an outcome someone can check) | Measured by |
|---|---|---|
| G-1 | Every model call through the gateway is charged to one team. | Share of rows in the monthly spend export that carry a platform-assigned team: 100 % (CST-001). |
| G-2 | No prompt, response or derived data is processed or stored outside Japan. | Resource inventory and cloud policy inspection find nothing outside Tokyo and Osaka; every catalog backend is processed in Japan (RES-001, RES-002). |
| G-3 | No prompt or response content is stored by default. | Launch gate V-1 passes on the release that goes live (PRV-001). |
| G-4 | Engineers use the supported coding agents through the gateway with no setup beyond storing their key once. | Pilot demonstration on an Intune-managed laptop (FUN-009). |
| G-5 | Every control that rests on undocumented product behaviour or on our network is tested before launch and after every LiteLLM upgrade. | All launch gates V-1 to V-11 pass on the pinned version (OPS-001). |

### 1.3 Non-goals (out of scope for this phase)

| ID | Excluded | Why | Revisit when |
|---|---|---|---|
| NG-1 | Remote and home access | Users work from offices and the DC, and the IP allowlist depends on it [CMP A-13] | Remote access is requested. The allowlist must then be replaced by ZTNA or required mTLS [CMP A-13, §8.6]. |
| NG-2 | External model APIs that cannot prove in-Japan processing | Not allowed until legal and security confirm in-Japan processing in writing [CMP A-7] | A provider gives a written commitment to process and store in Japan (REG-001) |
| NG-3 | Response caching | A response cache would store full responses, keyed by request content [CMP §2.8] | A use case needs it and legal/privacy approves storing responses (PRV-001) |
| NG-4 | Model training and fine-tuning | The gateway governs how models are consumed, not how they are built [CMP §10.1, §10.9] | n/a: belongs to a separate ML platform [CMP §10.9] |
| NG-5 | Private-line ingress (Route A over Direct Connect) | It adds isolation, not identity or device protection, and adds carrier and DNS dependencies [CMP §2.6, §8.0] | A trigger in [CMP §8.0] applies, for example the office proxy cannot exempt the gateway from TLS inspection |
| NG-6 | mTLS with Intune device certificates | Not needed while unmanaged devices cannot use our egress IPs [CMP §2.3.2, A-16] | Gate V-11 fails, A-16 cannot be confirmed, or NG-1 is revisited (SEC-003) |
| NG-7 | Endpoint families other than those in FUN-001 to FUN-004: images, audio, batch, files, fine-tuning, vector stores, MCP gateway, A2A, pass-through routes | Each is a new data path that must pass the residency checklist first [CMP §10.8.7] | A team requests one and it passes [CMP §10.8.7]; MCP and embeddings are the likely first additions [CMP §10.9] (Q-5) |
| NG-8 | Keeping identity data (Entra ID, Okta, Intune) in Japan | The SaaS identity plane never processes prompts and is outside the residency scope [CMP A-11] | Legal requires identity data in Japan; that is a tenant-location question this system cannot solve [CMP A-11] |

### 1.4 Phasing

The pilot teams and the target dates are Q-3.

| Phase | Scope | Target date | Exit criteria |
|---|---|---|---|
| Pilot | Pilot teams TBD (Product owner, 2026-12-18) on the corporate network; Claude Code, Codex CLI, SDKs and IDE plugins; Bedrock models processed in Japan from the catalog (§6.5); Route B ingress | TBD (Product owner, 2026-12-18) | Every launch gate V-1 to V-11 passed before the first pilot user is admitted [CMP §2.10]; every Must requirement Verified |
| General availability | All engineers on the corporate network, and workloads in the on-premises DC and in the cloud [CMP A-4, A-13] | TBD (Product owner, 2026-12-18) | Pilot findings recorded in 08; a DR drill met AVL-M02 and AVL-M03; gates re-run on the release that goes live |

## 2. Stakeholders and users

Team names for each role are in 00 §1.3.

| Role | Description | Main needs | Represented by (team) |
|---|---|---|---|
| Engineer (interactive) | Uses Claude Code, Codex CLI, IDE plugins | Japan-processed frontier models in their usual tools; set up once, with no sign-in per request | Product owner |
| Workload / agent | On-prem DC or cloud service calling the API | A team-scoped service-account key with its own budget and model list; a dedicated egress IP or private path [CMP §2.3.5] | Product owner |
| Team admin | Manages a team's spend and its workload keys [CMP §2.3.5] | See team spend against budget; create team and service-account keys; budget alerts | Product owner |
| Platform operator | Builds, deploys and runs the gateway | IaC deploys, runbooks that match tested behaviour, alerts, SSO admin access with phishing-resistant MFA [CMP §2.9] | Platform engineering |
| FinOps | Charges usage back to teams | Per-team shares from the gateway applied to the AWS bill, with the residual on its own line [CMP §4.5] | FinOps |
| Security / SOC | Watches for misuse and incidents | Audit events and request metadata in the SIEM, guardrail results, no content in logs [CMP §2.8] | Security / SOC |
| Legal / privacy | Owns residency and content-logging approvals | Evidence that data stays in Japan; control over who sees per-user metadata [CMP A-11, §2.8] | Legal / privacy |
| Network | Owns egress IPs, the secure web gateway and guest networks | A stable allowlist, the TLS-inspection exemption, proof that unmanaged devices cannot use our egress IPs [CMP A-14, A-15, A-16] | Network |
| Identity | Owns Entra ID, Conditional Access and the Okta EAM link | One app registration per environment with the policy set CA-GW-01 to CA-GW-05 [CMP §2.1] | Identity |
| Endpoint / Intune | Owns device compliance and client configuration | Managed settings for Claude Code and Codex CLI, and the key helper, pushed by Intune [CMP §2.3.4] | Endpoint / Intune |

### 2.1 Use cases

| ID | Actor | Scenario | Supported by |
|---|---|---|---|
| UC-1 | Engineer | Runs Claude Code or Codex CLI from the office against a model processed in Japan; usage is charged to their team. | FUN-001, FUN-002, FUN-009, IAM-002, CST-001, RES-002, SEC-001 |
| UC-2 | Workload in the on-prem DC | Calls the chat completions API with its team's service-account key from a dedicated DC egress IP; spend is charged to the team. | FUN-003, IAM-002, TEN-002, TEN-003, SEC-002, CST-001 |
| UC-3 | Team admin | Checks team spend against the budget, and is notified as the budget is used up. | CST-002, CST-010, OBS-003 |
| UC-4 | Leaver | Access ends when the account is disabled in Entra: personal keys stop working. | IAM-006 |
| UC-5 | Engineer | Signs in to the Admin UI with Entra (MFA, compliant device) and creates or renews a personal key within the upper bounds. | FUN-008, IAM-001, TEN-001, TEN-005, TEN-006 |
| UC-6 | FinOps | Produces the monthly chargeback from the AWS bill and the gateway's per-team shares, with the residual on its own line. | CST-007, CST-008, CST-011 |
| UC-7 | Platform operator | Fails the gateway over to Osaka when Tokyo is lost. | AVL-001, AVL-M02, AVL-M03, OPS-007 |
| UC-8 | Team admin | Asks for a new model; it is added only after its processing locations are checked. | MDL-104, REG-001 |

## 3. Assumptions and dependencies

IDs AS-1 to AS-16 restate the comparison's assumptions A-1 to A-16 in one line each; the full text is in the source. Due dates are proposed and are confirmed in review.

| ID | Assumption / dependency | Source | Owner | Confirm by | Status | If false |
|---|---|---|---|---|---|---|
| AS-1 | Entra ID is the authoritative IdP, with synced UPNs and group membership for every user. | [CMP A-1] | Identity | 2026-12-18 | Open | Team sync and key ownership have no source of truth; the identity design in 02 §4 changes. |
| AS-2 | Okta is used only for MFA, attached to Entra as an External Authentication Method. | [CMP A-2, §2.1] | Identity | 2026-12-18 | Open | Use the federation pattern in [CMP §2.1.2]; 02 §4 changes. |
| AS-3 | Entra ID P1 or P2 licences are in place, and Intune enforces compliance on Windows and macOS. | [CMP A-3] | Identity | 2026-12-18 | Open | Conditional Access cannot require a compliant device; IAM-001 cannot be met. |
| AS-4 | Clients are a browser for the Admin UI, Claude Code, Codex CLI, IDE plugins, SDKs, internal apps and agents in the DC and in the cloud. | [CMP A-4] | Product owner | 2026-12-18 | Open | FUN requirements change. |
| AS-5 | Only Tokyo (primary) and Osaka (warm-standby DR) are used for anything in scope of residency. | [CMP A-5] | Legal / privacy | 2026-12-18 | Open | Constraint CON-4 and every RES requirement change. |
| AS-6 | A LiteLLM Enterprise licence is bought: Admin UI SSO for all users, SCIM and audit logs. | [CMP A-6] | Product owner | 2026-12-18 | Open | Users cannot create their own keys; keys come from a request workflow and CI [CMP §2.3.5]. FUN-008, TEN-001 and OBS-001 change. |
| AS-7 | External model APIs are not allowed unless legal and security confirm in-Japan processing in writing. | [CMP A-7] | Legal / privacy | 2026-12-18 | Open | REG-001 and the egress design change. |
| AS-8 | Existing Direct Connect circuits terminate in a hub already peered with landing-zone spokes. | [CMP A-8] | Network | 2027-01-29 | Open | Route A (NG-5) and the optional Azure OpenAI private path cost more to add. |
| AS-9 | Scale is about 5,000 employees, about 300 concurrent users at peak, and 50–200 RPS with streaming. | [CMP A-9] | Product owner | 2026-12-18 | Open | Sizing and the PRF targets change. |
| AS-10 | Prompt and response content is not stored by default; content logging is a per-team opt-in. | [CMP A-10] | Legal / privacy | 2026-12-18 | Open | PRV-001 and PRV-002 change. |
| AS-11 | Residency covers prompts, completions, embeddings and everything derived from them, not the identity SaaS or the cloud's own billing systems. | [CMP A-11] | Legal / privacy | 2026-12-18 | Open | NG-8 is revisited; identity data residency cannot be solved by this design [CMP A-11]. |
| AS-12 | Provider abuse monitoring is acceptable if its storage stays in Japan. | [CMP A-12] | Legal / privacy | 2026-12-18 | Open | The optional Azure OpenAI backend needs modified abuse monitoring approved first (REG-002). |
| AS-13 | Users are on the corporate network; remote access is out of scope. | [CMP A-13] | Product owner | 2026-12-18 | Open | NG-1 is revisited and SEC-003 makes mTLS required. |
| AS-14 | Office and DC breakouts use a small, stable set of public NAT egress IPs. | [CMP A-14] | Network | 2026-12-18 | Open | The allowlist cannot be maintained; access control needs mTLS or ZTNA instead [CMP A-13]. |
| AS-15 | The secure web gateway can exempt the gateway hostname from TLS inspection and allow it by FQDN. | [CMP A-15] | Network | 2026-12-18 | Open | Use a fixed-IP front end (Global Accelerator) or Route A [CMP §2.6, §8.0]. |
| AS-16 | Unmanaged devices cannot leave through the office or DC egress IPs. | [CMP A-16] | Network | 2027-01-29 | Open | mTLS becomes required before launch (SEC-003); tested by V-11. |
| AS-17 | The Bedrock models in §6.5 remain processed in Japan through `jp.` profiles or In-Region in Tokyo, as in the snapshot checked on 2026-10-30. | [CMP §2.5, §7.2] | Platform engineering | 2027-01-29 | Open | The catalog shrinks; a required model with no Japan option is a blocking question (§6.5). |
| AS-18 | A shared network account (`network-prod`) with a Transit Gateway and an inspection and egress VPC with Network Firewall exists in Tokyo and can serve the gateway. | [CMP §4.6] | Network | 2026-12-18 | Open | The gateway account needs its own egress design. |
| AS-19 | A SIEM is available whose storage is in Japan. | [CMP §4.7] | Security / SOC | 2026-12-18 | Open | OBS-001 and OBS-004 cannot be met without breaking RES-004. |
| AS-20 | Intune can deploy managed settings for Claude Code, a user-level `config.toml` for Codex CLI, and the key helper, to Windows and macOS. | [CMP §2.3.4] | Endpoint / Intune | 2026-12-18 | Open | FUN-009 is not met; users configure tools by hand. |
| AS-21 | Every user is enrolled in Okta Verify before first sign-in, because EAM does not support inline enrolment. | [CMP §2.1] | Identity | 2026-12-18 | Open | First sign-ins fail; an enrolment step is added to onboarding. |

## 4. Constraints

| ID | Constraint | Source / authority |
|---|---|---|
| CON-1 | The hosting cloud is AWS; primary Tokyo (`ap-northeast-1`), DR Osaka (`ap-northeast-3`). | [CMP §7.2] |
| CON-2 | The gateway software is LiteLLM Proxy, with an Enterprise licence. | [CMP §0, §7.2, A-6] |
| CON-3 | Entra ID is the only identity provider for the gateway; Okta Verify supplies MFA through Entra; Intune supplies device compliance. | [CMP A-1, A-2, A-3, §2.1] |
| CON-4 | Every gateway component, data store, backup, log, export and data pipeline is in Tokyo or Osaka. | [CMP A-5, §2.5] |
| CON-5 | Model deployments are allowed only where processing, not just the endpoint, is in Japan. | [CMP §2.5] |
| CON-6 | Public model provider APIs are blocked by default. | [CMP A-7] |

## 5. Requirement conventions

**ID format:** `<AREA>-<NNN>`, for example `RES-001`. IDs are never reused or renumbered. A deleted requirement keeps its row with status `Withdrawn`. Metric rows use `<AREA>-M<NN>`, for example `AVL-M01`. Model catalog rows use `MDL-0NN`, and requirements about model routing use `MDL-1NN`.

**Areas:**

| Code | Area |
|---|---|
| FUN | Functional: API surface, models, routing, clients |
| IAM | Identity, authentication, authorization, device trust |
| TEN | Tenancy: teams, users, keys |
| CST | Cost allocation, budgets, token/rate limits |
| RES | Data residency |
| PRV | Privacy: prompt/response content handling, retention |
| SEC | Security controls (network, WAF, secrets, guardrails) |
| AVL | Availability, DR, resilience |
| PRF | Performance and capacity |
| OBS | Observability, audit, logging |
| OPS | Operability: deploy, upgrade, runbooks, support |
| REG | Compliance and regulatory |
| MDL | Model catalog and routing behaviour |

**Wording:** each requirement is one testable sentence. Use "shall" for mandatory statements. Use a pattern:
- Always: `The gateway shall <response>.`
- Event: `When <trigger>, the gateway shall <response>.`
- State: `While <state>, the gateway shall <response>.`
- Unwanted behaviour: `If <condition>, then the gateway shall <response>.`

Avoid words that cannot be tested: *fast, secure, user-friendly, as appropriate, etc., support*. Replace them with a number or an observable behaviour.

**Priority (MoSCoW):** Must (launch blocks without it) / Should / Could / Won't (this phase).

**Verification method:** T = test, D = demonstration, I = inspection (config/code/document review), A = analysis. A requirement with no feasible verification method is not ready for approval.

**Status:** Proposed → Approved → Implemented → Verified. Also: Deferred, Withdrawn.

**Metrics:** each row in a metric table (§7.4, §7.5) is a requirement too, with the same priority, verification and status. A target states its window, where it is measured, and what is excluded.

## 6. Functional requirements

### 6.1 API and clients (FUN)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| FUN-001 | The gateway shall expose an Anthropic-compatible messages API, with streaming, for every Claude model in the catalog. | Claude Code calls this API natively [CMP §2.3.4, A-4] | Must | Claude Code completes a streamed multi-turn session with tool use against each catalog Claude model. | D | Proposed |
| FUN-002 | The gateway shall expose an OpenAI-compatible Responses API, with streaming, that Codex CLI can use against the catalog models approved for it. | Codex CLI uses the Responses API through a custom provider [CMP §2.3.4, §10.8.2] | Must | Codex CLI completes a streamed multi-turn session with tool use against each model approved for it. | D | Proposed |
| FUN-003 | The gateway shall expose an OpenAI-compatible chat completions API, with streaming, for every chat model in the catalog. | SDKs, IDE plugins and workloads use it [CMP A-4, §4.3] | Must | The OpenAI SDK completes a streamed and a non-streamed request against each catalog chat model. | T | Proposed |
| FUN-004 | The gateway shall expose an OpenAI-compatible embeddings API for every embedding model in the catalog. | Embeddings are processed in Tokyo In-Region [CMP §2.5]; likely next use [CMP §10.9] | Should | The OpenAI SDK gets embeddings of the expected dimension from each catalog embedding model. | T | Proposed |
| FUN-005 | When a caller lists models, the gateway shall return only the models that the caller's key and team may use. | Callers need to discover what they may call [CMP §2.4] | Should | For two teams with different model lists, each key sees exactly its team's list. | T | Proposed |
| FUN-006 | If a request targets an endpoint family that has not passed the residency checklist, then the gateway shall refuse it before any backend is called. | Each endpoint family is a new data path [CMP §10.8.7, §2.5] | Must | Requests to an image, audio, batch, file, fine-tuning, vector-store, MCP and pass-through endpoint are each refused, and no backend call appears in the backend's logs. | T | Proposed |
| FUN-007 | If a request contains an image by URL, then the gateway shall not fetch the URL. | Fetching would send traffic to arbitrary hosts; images must be sent inline [CMP §2.5] | Must | A request with an image URL fails; the egress firewall log shows no allowed connection to that host; the same image sent inline succeeds on a model that accepts images. | T | Proposed |
| FUN-008 | The gateway shall let a signed-in user create, renew, delete and list their own personal keys, and see their own usage, in a web UI. | Users issue their own keys after an Entra sign-in [CMP §2.3.5, §2.9 U1] | Must | A user with the user role creates, lists, renews and deletes a personal key, and sees their usage, in the Admin UI. | D | Proposed |
| FUN-009 | The supported coding agents shall reach the gateway on an Intune-managed device with no configuration by the user other than storing their personal key once, and shall read the key from the operating system's credential store. | Keeps keys out of dotfiles and history [CMP §2.3.4] | Must | On a freshly enrolled Windows and macOS device, after the user stores a key once, Claude Code and Codex CLI each complete a request; no key is found in any file under the user's home directory or in the environment. | D | Proposed |

### 6.2 Identity and access (IAM)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| IAM-001 | The gateway's web UI shall accept sign-in only through Entra ID, with MFA through Okta Verify and a compliant device required at sign-in. | Device and MFA are checked when keys are issued [CMP §2.1 CA-GW-01, §2.3.1] | Must | Sign-in succeeds from a compliant device with MFA; it is refused from a non-compliant device, and without completed MFA. | T | Proposed |
| IAM-002 | If an API request has no virtual key, or its key does not exist, has expired or is blocked, then the gateway shall refuse it with HTTP 401 before any model is called. | Every API client uses a virtual key [CMP §2.3, §2.3.1] | Must | Requests with no key, an unknown key, an expired key and a blocked key each get 401, and no model call is recorded. | T | Proposed |
| IAM-003 | Users with an admin role shall sign in with a compliant device and phishing-resistant MFA where available, and shall sign in again at least every 8 hours. | Admin sessions are the highest-value credential [CMP §2.1 CA-GW-02, §2.9] | Must | An admin sign-in with push-only MFA where a phishing-resistant method is available is refused; an admin session older than 8 hours requires a new sign-in. | T | Proposed |
| IAM-004 | The gateway shall take each user's role from their Entra app role assignment, and shall grant no admin permission to a user who has no admin app role. | Roles come from Entra app roles [CMP §2.3, §4.4] | Must | A user with only the user app role cannot reach any admin function; adding the admin app role grants it at next sign-in. | T | Proposed |
| IAM-005 | Device-code flow and legacy authentication shall be blocked for the gateway's Entra app and for the AWS operator app. | Device-code flow lets credentials land on another machine [CMP §2.1 CA-GW-04, CA-GW-05, §2.9] | Must | A device-code sign-in to each app is refused. | T | Proposed |
| IAM-006 | When a user's Entra account is disabled, the gateway shall block all of that user's keys within TBD (Security, 2026-12-18) (Q-8). | Keys outlive the Entra session [CMP §2.3.5, §2.3.6 row 6] | Must | After an account is disabled, a request with each of the user's keys gets 401 within the target time. | T | Proposed |
| IAM-007 | Operator sign-in to the AWS console and CLI shall require phishing-resistant MFA, a compliant device, and an office or DC egress IP. | Operator access has no gateway in front of it [CMP §2.1 CA-GW-05, §2.9 A2, A3] | Must | An operator sign-in from a non-compliant device, from a non-office IP, and with push-only MFA where a phishing-resistant method is available, are each refused. | T | Proposed |
| IAM-008 | Admin sessions in the AWS accounts shall last at most 1 hour, and AWS API calls made with operator credentials from outside the office and DC egress IPs shall be denied. | Cached CLI credentials can be copied [CMP §2.9, §4.4] | Must | An admin session expires after 1 hour; a CLI call with copied operator credentials from a non-office IP is denied. | T | Proposed |
| IAM-009 | Break-glass access to the AWS accounts shall exist, with credentials kept in a vault, and every use shall raise an alert to Security. | Operators need a path when SSO fails [CMP §4.4] | Should | A break-glass sign-in in a drill raises an alert in the SIEM. | D | Proposed |

### 6.3 Tenancy (TEN)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| TEN-001 | A user without an admin role shall be able to create keys only for themselves, only within the upper bounds for duration, budget and TPM/RPM, and never with admin permissions. | Self-service is safe only within limits [CMP §2.3.5, V-2] | Must | Launch gate V-2 passes. | T | Proposed |
| TEN-002 | Team keys and service-account keys shall be created only by the team's admins or the CI pipeline. | Workload keys must not be created by individuals [CMP §2.3.5] | Must | A user without the team admin role is refused when creating a team or service-account key through the UI and through the API. | T | Proposed |
| TEN-003 | Every key shall have an owner, an expiry, an explicit model list, a budget and TPM/RPM limits. | Every key must be attributable and bounded [CMP §2.3, §2.3.5] | Must | An inspection of all keys finds none without each field; creating a key without one of them is refused or filled from the upper bounds. | I, T | Proposed |
| TEN-004 | Each team shall correspond to one Entra security group, and a user's team membership shall follow that group at each sign-in. | Entra is the source of truth for teams [CMP §2.4, §4.4] | Must | Adding a user to a team group makes them a team member at next sign-in; removing them removes the membership. | T | Proposed |
| TEN-005 | User-level budget and TPM/RPM limits shall apply across all of a user's keys together. | Extra keys must not multiply the allowance [CMP §2.3.5] | Must | Launch gate V-2 passes, including its two-key check. | T | Proposed |
| TEN-006 | Personal and service-account keys shall expire no more than 90 days after they are created. | Bounded key lifetime [CMP §2.3, §2.3.5] | Must | Creating a key with a longer expiry is refused; an inspection finds no key with a longer lifetime. | T | Proposed |

### 6.4 Cost allocation and limits (CST)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| CST-001 | The gateway shall charge each request to the team that the platform assigns, whatever tags or `user` value the client sends. | Clients must not choose who pays [CMP §2.4, V-7] | Must | Launch gate V-7 passes, including the user in two teams; the rule for that case is Q-12. | T | Proposed |
| CST-002 | When a team's spend reaches its budget for the period, the gateway shall refuse further model requests charged to that team until the period resets or the budget is raised. | Budgets are enforced in real time [CMP §4.5] | Must | With a small test budget, requests succeed until it is used up and are then refused with a budget error; they succeed again after the reset. | T | Proposed |
| CST-003 | The gateway shall enforce user and key budgets and TPM/RPM limits across all gateway instances together. | Limits are shared through Redis [CMP §2.4] | Must | With load spread over every running instance, the number of requests allowed in one minute does not exceed the RPM limit. | T | Proposed |
| CST-004 | The gateway shall record a non-zero cost for every request to every catalog deployment, within a tolerance of the provider's price, including requests that use prompt caching. | A zero price makes budgets silent [CMP §2.4, V-4] | Must | Launch gate V-4 passes; the tolerance is Q-12. | T | Proposed |
| CST-005 | If a request asks not to be logged, then the gateway shall still record its spend. | Clients must not skip tracking [CMP §2.4, V-6] | Must | Launch gate V-6 passes. | T | Proposed |
| CST-006 | The cost of requests that end before the response completes shall be measured, and the gap between provider usage and recorded spend shall have a named owner in the chargeback model. | Cancelled streams may be unmetered [CMP §2.4, V-5] | Must | Launch gate V-5 passes. | T, A | Proposed |
| CST-007 | Each month, each team's charge shall equal the AWS bill total for the model service multiplied by the team's share of recorded cost, and the difference between the bill and total recorded cost shall be reported as its own line. | The bill is the cost truth, the gateway gives the shares [CMP §4.5, §7.2] | Must | A month's chargeback report reproduces from the bill and the spend export, and shows the residual line. | A | Proposed |
| CST-008 | When the monthly residual exceeds a threshold, it shall be investigated and the cause recorded. | The residual contains pricing errors and unmetered requests [CMP §4.5] | Should | A residual above the threshold (Q-12) has an investigation record in the following month. | I | Proposed |
| CST-009 | The budget policy signed off by finance shall state the maximum overshoot of a budget, derived from the concurrency and request-size limits. | Parallel requests started under budget can overshoot it [CMP §2.4] | Should | The signed policy states the bound and the calculation behind it. | A | Proposed |
| CST-010 | When a team's spend reaches 80 % and 100 % of its budget, the team's admins shall be notified, with no prompt content in the notification. | Same thresholds as the AWS Budgets backstop [CMP §4.5]; alerts carry no content [CMP §2.5] | Should | Crossing each threshold in a test sends one notification to the team admin, and its text contains no prompt content. | T | Proposed |
| CST-011 | Every team shall be mapped to one department or cost centre for chargeback. | Department chargeback [CMP §2.4, §4.5] | Must | An inspection finds no team without a department; the monthly report totals by department. | I | Proposed |

### 6.5 Model catalog and routing (MDL)

Availability is from the comparison's snapshot (checked 2026-10-30) and is re-checked before each model is onboarded (MDL-104). Which models are needed, by when and at what priority is Q-4. Models the snapshot lists as available from Tokyo only through global or multi-country routing (for example Claude Sonnet 5.5) are not in the catalog; a request for one goes to the residency owner, not to an exception [CMP §7.3].

| ID | Model family / capability | Use case | Needed by (phase) | Japan availability (how processed, date checked) | Available in DR region? | Priority | Status |
|---|---|---|---|---|---|---|---|
| MDL-001 | Frontier coding model (Claude Opus 5.5) | UC-1 | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` cross-Region inference profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile, with its own quota [CMP §4.5, §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-002 | Fast model (Claude Haiku 5.5) | UC-1, UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-003 | Previous frontier model (Claude Opus 4.8) | UC-1; fallback for MDL-001 [CMP §4.9] | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-004 | Mid-size model (Claude Sonnet 4.6) | UC-1, UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-005 | Previous fast model (Claude Haiku 4.5) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-006 | Low-cost general model (Amazon Nova 2 Lite) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, `jp.` profile (checked 2026-10-30) [CMP §2.5] | Osaka: yes, the same `jp.` profile [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-007 | Embeddings (Titan Text Embeddings V2) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, In-Region (checked 2026-10-30) [CMP §2.5] | TBD (Platform engineering, 2027-01-29): not checked; an embedding model cannot be swapped without re-indexing [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-008 | Embeddings (Cohere Embed v4) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, In-Region (checked 2026-10-30) [CMP §2.5] | TBD (Platform engineering, 2027-01-29): not checked [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-009 | Open-weight large model (Mistral Large 3) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, In-Region (checked 2026-10-30) [CMP §2.5] | TBD (Platform engineering, 2027-01-29): not checked [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-010 | Open-weight model (gpt-oss-120b) | UC-2 | TBD (Product owner, 2026-12-18) | Tokyo: yes, In-Region (checked 2026-10-30) [CMP §2.5] | TBD (Platform engineering, 2027-01-29): not checked [CMP §4.9] | TBD (Product owner, 2026-12-18) | Proposed |
| MDL-011 | OpenAI models, only if required (Azure OpenAI Standard deployments in Japan East, as a second backend) | TBD (Product owner, 2026-12-18) | TBD (Product owner, 2026-12-18) | Japan East: per model, not checked; geography-based deployments arrive last [CMP §2.5, §7.2] | TBD (Platform engineering, 2027-01-29): not checked per model [CMP §7.1] | TBD (Product owner, 2026-12-18): required only if OpenAI models are needed (Q-4) | Proposed |

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| MDL-101 | If a model is throttled or unavailable, the gateway shall fall back only to another deployment processed in Japan. | A fallback outside Japan silently breaks residency [CMP A-7, §2.5] | Must | Every fallback in the configuration points to a catalog deployment processed in Japan; with the primary forced to fail, requests go to the fallback, and the backend's audit log shows no call to a global or multi-country profile. | I, T | Proposed |
| MDL-102 | If a request names a model that is not in the catalog, then the gateway shall refuse it, and shall not route it to any default model. | Only catalog models are processed in Japan [CMP §2.5] | Must | A request for an unknown model name is refused, and no backend call is recorded. | T | Proposed |
| MDL-103 | If a request names a catalog model that the caller's key or team may not use, then the gateway shall refuse it. | Model access is granted per team [CMP §2.4] | Must | A key of a team without access to a model is refused for that model and accepted for its allowed models. | T | Proposed |
| MDL-104 | A model shall be added to the catalog only after its processing locations have been confirmed to be only Tokyo and Osaka and recorded with the date, and every catalog model shall be re-checked every quarter. | Availability changes faster than the analysis [CMP §4.8, §7.2] | Must | Each catalog row has a check record dated before its onboarding and within the last quarter. | I | Proposed |
| MDL-105 | The public model names that clients send shall stay stable, and any change of the model behind a name shall be announced in advance. | Clients pin model names [CMP §4.5] | Should | Each change of the backend behind a public name has a release note published before the change; the notice period is set in 10 §1. | I | Proposed |

## 7. Non-functional requirements

### 7.1 Data residency (RES)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| RES-001 | Prompts, completions, embeddings, and all data derived from them shall be processed and stored only in Japan. | [CMP A-5, A-11, §2.5] | Must | Every data store, backup, log, export and model backend in the inventory is in Tokyo or Osaka; an attempt to create a store outside them fails. | I, T | Proposed |
| RES-002 | The gateway shall call only model deployments that are processed in Japan, and a call to a global or multi-country deployment shall be refused by cloud policy even if it is added to the gateway configuration. | A Japanese endpoint is not enough; enforcement must not depend on configuration [CMP §2.5 rules 2 and 4] | Must | With a global and a multi-country profile added to a staging configuration, both calls are denied by cloud policy. | T | Proposed |
| RES-003 | Cloud policy shall deny creating resources outside Tokyo and Osaka in the gateway's accounts, except for global services. | Documentation and convention are not enough [CMP §2.5 rule 4] | Must | An attempt to create a bucket and a log group in a non-Japan region is denied. | T | Proposed |
| RES-004 | Spend exports, billing exports, SIEM copies, analytics and dashboards built from gateway data shall be stored and processed only in Japan. | Pipelines are in scope [CMP §2.5 rule 3, §4.7] | Must | Each pipeline in the inventory names a Japanese region for every store and compute step. | I | Proposed |
| RES-005 | The gateway shall send no data to any destination outside the approved list, and no observability or alerting service hosted outside Japan shall be on that list. | [CMP §2.5, §4.6] | Must | From a gateway task, connections to a public model API and to an unlisted SaaS host fail and are logged; the approved list contains only identity endpoints and the licence endpoint. | T | Proposed |
| RES-006 | For each supported client, what it sends to its vendor other than model calls shall be listed, turned off through managed settings where the client allows it, and the rest approved by legal/privacy. | Residency holds only if clients do not send data elsewhere [CMP §2.5 rule 5] | Must | A record per client lists its non-model traffic, the managed setting that turns each off, and legal's approval of what remains. | I | Proposed |
| RES-007 | Public model APIs and consumer AI services shall be blocked on the office secure web gateway. | Otherwise residency holds only for users who choose the gateway [CMP §2.5 rule 5] | Should | From an office device, connections to a sample of public model APIs and consumer AI sites are blocked. | T | Proposed |

### 7.2 Privacy (PRV)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| PRV-001 | The gateway shall not store prompt or response content anywhere unless the calling team is approved for content logging. | Content is not stored by default [CMP A-10, §2.8] | Must | Launch gate V-1 passes: a canary sent through every model and API style, including a guardrail-blocked and a provider-rejected request, is found in no store. | T | Proposed |
| PRV-002 | When a team is approved for content logging by legal/privacy, the gateway shall store that team's content only in the opt-in content store, separate from all other stores. | Per-team opt-in for compliance use [CMP A-10, §4.7]; mechanism not designed [CMP §2.8] | TBD (Legal / privacy, 2026-12-18) (Q-10) | V-1 run with the approved team's configuration finds that team's canary only in the opt-in store, and other teams' canaries nowhere. | T | Proposed |
| PRV-003 | Access to per-user usage reports, and how long they are kept, shall be agreed with the privacy office before any per-user report is shared. | Metadata is personal data too [CMP §2.8] | Must | A written agreement exists, and report access is limited to the roles it names. | I | Proposed |
| PRV-004 | Provider-side request logging that captures content shall be off for every model backend in the gateway's accounts. | It cannot be limited to one team in a shared account [CMP §2.8, §4.7] | Must | An inspection of every backend in both regions shows content logging off. | I | Proposed |

### 7.3 Security (SEC)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| SEC-001 | The gateway shall refuse connections from any source IP outside the office and DC egress IPs. | Users are on the corporate network [CMP A-13, A-14] | Must | A request from an IP outside the allowlist is refused before it reaches the gateway application; a request from each office and DC egress IP succeeds. | T | Proposed |
| SEC-002 | The allowlist shall contain only dedicated egress IPs of ours, each with a named owner, and no shared NAT or SASE ranges. | A shared NAT admits every workload behind it [CMP §2.3.5, V-11] | Must | Launch gate V-11 passes, including its list of every CIDR and owner. | I, T | Proposed |
| SEC-003 | If gate V-11 finds that an unmanaged device can reach the gateway, or AS-16 cannot be confirmed, or remote access is added, then the gateway shall require a client certificate issued through Intune on every connection before launch. | mTLS is the only per-request device check [CMP §2.3.2, §2.3.6] | Must | The V-11 record shows either a pass, or a design change to required mTLS that passed its own tests before launch. | I | Proposed |
| SEC-004 | All client connections shall use TLS 1.2 or later and shall terminate only in Japan, with no CDN or global edge in front of the gateway. | Residency and timeouts [CMP §2.6, §4.8] | Must | A TLS 1.1 handshake fails; the DNS name resolves only to a load balancer in Tokyo (or Osaka after failover). | T, I | Proposed |
| SEC-005 | The gateway hostname shall be exempt from TLS inspection on the corporate secure web gateway, and allowed by FQDN in the outbound firewall. | Inspection lets the proxy read prompts and keys [CMP A-15, §2.6] | Must | From an office device, the certificate presented for the gateway hostname is the gateway's own, not the proxy's. | T | Proposed |
| SEC-006 | The web application firewall shall pass legitimate API request bodies larger than 8 KB that contain source code, and shall apply stricter rules to the admin paths. | Default rule sets block coding-agent requests [CMP §2.7, §4.8] | Must | A request with a large body of source code succeeds on each API path; a known-bad input on an admin path is blocked. | T | Proposed |
| SEC-007 | If a request body is larger than the maximum request size, then the gateway shall refuse it. | The WAF cannot enforce total body size [CMP §2.7] | Must | A request just over the limit (TBD (Platform engineering, 2027-01-29), R-17) is refused; one just under succeeds. | T | Proposed |
| SEC-008 | The gateway shall check every request, before the model call and processed in Japan, for personal information to mask and for prompt attacks, in Japanese and in English. | Bedrock Guardrails cannot do this in Japan for Japanese [CMP §2.5, §4.8] | Must | For a test set in Japanese and English, every listed personal-information type is masked before the model call and the prompt-attack detection rate meets the target; the list and target are Q-13. | T | Proposed |
| SEC-009 | The behaviour of the gateway when the guardrail check fails (refuse or allow the request) shall be defined and approved by Security. | The comparison does not set it (R-11) | Should | The approved behaviour is recorded, and a test with the guardrail service stopped shows it. | I, T | Proposed |
| SEC-010 | The gateway's master key shall be held only in the secrets store, used by no person for routine work, rotated on a schedule and when an admin leaves, and everyone who can read it shall be reviewed as an admin. | It is a static admin credential [CMP §2.3.5] | Must | An inspection shows the secret's readers listed in the admin access review, and a rotation record within the schedule. | I | Proposed |
| SEC-011 | Password login with the master key on the web UI shall be turned off, or its residual risk accepted in writing. | It is accepted from every allowlisted IP [CMP §2.3.5, V-3] | Must | Launch gate V-3 passes. | T | Proposed |
| SEC-012 | Secrets shall not be stored in configuration files, images or the repository; the database credential shall rotate automatically; and the salt key shall never change without an approved re-encryption plan. | [CMP §4.8] | Must | Secret scanning of the repository and images finds none; the database secret shows automatic rotation. | I | Proposed |
| SEC-013 | The gateway's outbound traffic shall be limited to an allowlist of hostnames, with no model provider hostname on it, and all other traffic denied and logged. | [CMP §4.6, A-7] | Must | From a gateway task, a connection to an unlisted host is denied and appears in the firewall log. | T | Proposed |
| SEC-014 | The gateway shall reach model backends only over private endpoints or the private path inside Japan. | [CMP §4.3, §7.2] | Must | With the gateway's internet egress blocked for model hostnames, every catalog model still works. | T | Proposed |
| SEC-015 | Credentials in request headers shall be redacted in firewall and load balancer logs. | Keys must not land in logs [CMP §2.8] | Must | A request with a known test key leaves no copy of the key in any edge log. | T | Proposed |
| SEC-016 | Gateway container images shall be pinned by digest, scanned before use, and promoted through dev and staging to production. | Supply chain [CMP §4.8] | Must | The production deployment references a digest that has a scan result and ran in staging first. | I | Proposed |
| SEC-017 | No interactive shell access to running gateway containers shall be possible in production. | [CMP §4.4] | Should | An attempt to open a shell in a production container is refused. | T | Proposed |
| SEC-018 | Repositories shall be scanned for the virtual key format, with pushes that contain a key blocked. | Leaked keys are the commonest leak [CMP §2.3.6 row 1] | Should | A push containing a test key is rejected. | T | Proposed |
| SEC-019 | The gateway's AWS accounts shall run continuous threat detection and configuration compliance checks, with findings sent to the SIEM. | [CMP §4.8] | Should | A sample finding appears in the SIEM. | D | Proposed |

### 7.4 Availability and DR (AVL)

| ID | Metric | Target | Measurement (window, point, method) | Conditions and exclusions | Priority | Verif. | Status |
|---|---|---|---|---|---|---|---|
| AVL-M01 | Availability (monthly) | TBD (Product owner, 2026-12-18) (Q-6) | Calendar month; a synthetic probe calls a small model through the public endpoint from office networks; probe interval and the failure definition TBD (Platform engineering, 2026-12-18) | Whether upstream outages that affect every Japan deployment of a model are excluded: TBD (Product owner, 2026-12-18) | Must | A | Proposed |
| AVL-M02 | RTO (loss of the Tokyo region) | TBD (Product owner, 2026-12-18); the design estimate is 30–60 min [CMP §4.9] | DR drill: time from the failover decision until the probe in AVL-M01 succeeds from Osaka | Models with no Osaka deployment are excluded (§6.5) | Must | T | Proposed |
| AVL-M03 | RPO (spend and audit data) | TBD (Product owner, 2026-12-18); the design estimate is about 1 s for the database [CMP §4.9] | DR drill: latest spend row and audit event present in Osaka compared with the last ones written in Tokyo | Rate-limit counters, and spend held in Redis but not yet written to the database, are lost [CMP §4.9] | Must | T | Proposed |
| AVL-M04 | Maximum planned downtime per upgrade | TBD (Product owner, 2026-12-18) | Minutes in which the AVL-M01 probe fails during an upgrade | A database migration that cannot run online (02 §7.5) | Should | T | Proposed |

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| AVL-001 | When the Tokyo region is unavailable, the gateway shall serve requests from Osaka for every catalog model that is available there. | Warm-standby DR in Osaka [CMP A-5, §4.9] | Must | In a DR drill, requests for each model marked as available in Osaka succeed from Osaka within the RTO (AVL-M02). | T | Proposed |
| AVL-002 | The gateway's behaviour while its database is unavailable shall be measured, and the on-call runbook shall match it. | Key checks go through the database [CMP V-8] | Must | Launch gate V-8 passes. | T | Proposed |
| AVL-003 | While Entra ID cannot be reached, API requests with valid keys shall keep working, and web sign-in shall fail with a clear error and raise an alert. | Model traffic must not depend on the identity egress path [CMP §4.9, V-10] | Must | Launch gate V-10 passes. | T | Proposed |
| AVL-004 | While the licence endpoint cannot be reached, a restarted gateway instance shall still serve API requests and web sign-in, or the endpoint shall be monitored as a production dependency. | [CMP §2.5, V-9] | Must | Launch gate V-9 passes. | T | Proposed |
| AVL-005 | Loss of one availability zone in Tokyo shall not stop the service, apart from requests in flight on that zone. | [CMP §4.9] | Should | With the instances in one zone stopped, the AVL-M01 probe keeps succeeding. | T | Proposed |
| AVL-006 | When the shared counter store is unavailable, an alert shall be raised, and the effect on limits and budgets shall be documented in the runbook. | Limits degrade without Redis [CMP §2.4] | Should | With the counter store stopped in staging, the alert fires and the observed effect matches the runbook. | T | Proposed |

### 7.5 Performance and capacity (PRF)

| ID | Metric | Target | Measurement (window, point, method) | Conditions and exclusions | Priority | Verif. | Status |
|---|---|---|---|---|---|---|---|
| PRF-M01 | Added latency to first token (gateway overhead) | TBD (Product owner, 2026-12-18) (Q-7) | Gateway ingress to egress, excluding model time; p95 over a load test | At the throughput in PRF-M02 with a streaming mix | Should | T | Proposed |
| PRF-M02 | Sustained throughput | TBD (Product owner, 2026-12-18); sizing basis 50–200 RPS [CMP A-9] | Load test through the public endpoint for 1 hour with no errors caused by the gateway | Streaming mix; growth at 12 and 24 months TBD (Product owner, 2026-12-18) | Must | T | Proposed |
| PRF-M03 | Maximum request duration | 570 s [CMP §2.7, §4.9] | From the client's request to the last byte of the response | Long agent turns, including a long silence before the first token | Must | T | Proposed |
| PRF-M04 | Concurrent streams | TBD (Product owner, 2026-12-18); sizing basis about 300 concurrent users at peak [CMP A-9] | Open streams held during a load test | Streaming responses | Must | T | Proposed |

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| PRF-001 | The gateway shall complete a streamed request that lasts up to the maximum request duration (PRF-M03), including a long silence before the first token, without any layer cutting it, also while a deploy or scale-in is in progress. | Reasoning models can be silent for minutes before the first token [CMP §2.7] | Must | A streamed request with 300 s before its first token and 550 s in total completes; a deploy started during it does not cut it. | T | Proposed |

### 7.6 Observability and audit (OBS)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| OBS-001 | The gateway shall record every admin action that creates, changes or deletes a key, team, budget or model, with who did it and when, and deliver it to the SIEM. | Key issuance must be auditable [CMP §2.3.5, §4.7] | Must | Creating, changing and deleting a key and a team budget each produce an audit event in the SIEM naming the admin, within TBD (Security, 2026-12-18). | T | Proposed |
| OBS-002 | The gateway shall record, for every request, the user, team, key, model, tokens, cost, latency, status and guardrail result, with no content. | Metadata is the chargeback and audit record [CMP A-10, §4.3] | Must | Each request in a test produces one record with every field, and V-1 finds no content in it. | T | Proposed |
| OBS-003 | Spend, tokens, remaining budget, latency and failures shall be available per team and per key on dashboards. | [CMP §2.4] | Should | A dashboard shows each metric for a chosen team and key. | D | Proposed |
| OBS-004 | Load balancer, firewall, network flow and cloud audit logs shall be delivered to the SIEM, stored in Japan. | [CMP §4.7, §2.5] | Must | A sample event of each type is found in the SIEM. | I, T | Proposed |
| OBS-005 | When one key is used from several source IPs or user agents, an alert shall be raised. | Detects key sharing [CMP §2.3.3, §8.8] | Should | Using one test key from two user agents raises the alert. | T | Proposed |
| OBS-006 | An alert shall be raised when the database, the counter store, Entra ID, the licence endpoint or the guardrail service fails, and when requests complete without a spend record. | Each is a known failure mode [CMP §2.4, §2.10] | Must | Each failure, caused in staging, raises its alert. | T | Proposed |
| OBS-007 | Every operator and break-glass action in the gateway's AWS accounts shall be recorded in an audit trail delivered to the SIEM, and reviewed on a schedule. | Operator access is the most powerful path [CMP §2.9] | Must | A sample console action appears in the SIEM; the review schedule is recorded (TBD (Security, 2026-12-18)). | T, I | Proposed |

### 7.7 Operability (OPS)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| OPS-001 | A LiteLLM upgrade shall reach production only after every launch gate has passed on the upgraded version. | Launch gates are valid only for the version they ran on [CMP §2.10] | Must | The release record of each upgrade links a passing result for every launch gate, dated after the upgrade reached staging. | I | Proposed |
| OPS-002 | All gateway infrastructure in both regions shall be deployed from infrastructure as code. | Osaka is deployed from the same code [CMP §4.9] | Must | A plan against each environment shows no drift; no resource lacks an IaC owner. | I | Proposed |
| OPS-003 | Production changes to teams, budgets, models and service-account keys shall be made through the CI pipeline, not by hand in the web UI. | [CMP §2.3, §2.9] | Should | The audit log for a month shows no such change in production made outside the pipeline's identity. | I | Proposed |
| OPS-004 | Gate V-11 shall be re-run after every change to egress NAT, guest networks or the allowlist. | [CMP V-11] | Must | Each network change record links a V-11 result dated after the change. | I | Proposed |
| OPS-005 | When an office or DC egress IP changes, the allowlist shall be updated before the change takes effect. | Otherwise users are locked out [CMP A-14] | Must | Each egress change record shows the allowlist update deployed before the cutover. | I | Proposed |
| OPS-006 | Production incidents shall be handled within support hours of TBD (Product owner, 2026-12-18) (Q-6). | Service commitment (00 §1.4) | Must | The on-call rota covers the agreed hours. | I | Proposed |
| OPS-007 | Failover to Osaka shall be tested in a DR drill before launch, and then at least every TBD (Product owner, 2026-12-18). | DR must be proven, not assumed [CMP §4.9] | Must | A drill record exists before launch and within each later interval. | I | Proposed |
| OPS-008 | Changes to the shared egress path that the gateway depends on shall follow the gateway's change process. | It is owned by another team [CMP §4.9] | Should | Each change to those firewall rules and routes has a gateway change record. | I | Proposed |

### 7.8 Compliance (REG)

| ID | Requirement | Rationale / source | Priority | Acceptance criteria | Verif. | Status |
|---|---|---|---|---|---|---|
| REG-001 | The gateway shall send requests only to model providers that legal and security have approved in writing for in-Japan processing. | External providers are not allowed by default [CMP A-7] | Must | Every configured model backend has a written approval on file; an inspection of the model configuration finds none without one. | I | Proposed |
| REG-002 | Provider abuse monitoring for every backend shall store data only in Japan, and legal/privacy shall decide in writing whether human review from outside Japan is acceptable before a backend that allows it is used. | [CMP A-12, §2.5] | Should | A written decision exists for each backend. | I | Proposed |
| REG-003 | The retention periods in §8 shall be approved by legal/privacy and FinOps. | [CMP §4.7, §2.8] | Must | §8 has no TBD, and its approval is recorded in §11. | I | Proposed |
| REG-004 | Before first use, each user shall accept an acceptable-use policy that forbids sharing keys. | Each key's owner must be its only user [CMP §2.3.3] | Should | Key creation is possible only for users with a recorded acceptance. | I | Proposed |

## 8. Data classification and retention

The classification scheme and the open retention periods are Q-9.

| Data item | Contains prompt content? | Classification | Store (logical) | Retention | Who can read | Residency |
|---|---|---|---|---|---|---|
| Spend log metadata | No | TBD (Legal / privacy, 2026-12-18) | Gateway database, then a daily export | 90 days in the database [CMP §4.7]; the export's 7 years is an assumption in the comparison: TBD (FinOps, 2026-12-18) | TBD (Legal / privacy, 2026-12-18) (PRV-003) | Japan |
| Request metadata log | No | TBD (Legal / privacy, 2026-12-18) | Log bucket written by the gateway's logging callback | 1 year, then archive until 7 years [CMP §4.7]; to be confirmed by the privacy office: TBD (Legal / privacy, 2026-12-18) | TBD (Legal / privacy, 2026-12-18) | Japan |
| Opt-in content log | Yes | TBD (Legal / privacy, 2026-12-18) | Not designed [CMP §2.8] (Q-10) | Per team's legal requirement; 30 days if none is set [CMP §4.7] | TBD (Legal / privacy, 2026-12-18) | Japan |
| Audit log (admin actions, cloud audit trail) | No | TBD (Legal / privacy, 2026-12-18) | Immutable archive in a log-archive account, and the SIEM | 7 years [CMP §4.7] | Security / SOC | Japan |
| Infrastructure logs (load balancer, firewall, network flow) | No: credentials redacted (SEC-015); whether firewall logs can hold matched body text is TBD (Platform engineering, 2027-01-29) | TBD (Legal / privacy, 2026-12-18) | Log service, then archive | 90 days hot, then 1–7 years archived [CMP §4.7]; the archive period is TBD (Security, 2026-12-18) | Security / SOC, platform operators | Japan |
| Gateway configuration data (users, teams, key hashes, budgets) | No | TBD (Legal / privacy, 2026-12-18) | Gateway database | Life of the platform; point-in-time recovery 35 days [CMP §4.7] | Platform operators | Japan |
| Billing export (AWS cost and usage) | No | TBD (Legal / privacy, 2026-12-18) | Billing export bucket | TBD (FinOps, 2026-12-18) | FinOps | Japan |
| Rate-limit and budget counters | No | TBD (Legal / privacy, 2026-12-18) | Shared counter store | Ephemeral [CMP §4.7] | Gateway only | Japan |

## 9. Open questions

Due dates are proposed and are confirmed in review. Design-level open items are in 02 §14.

| ID | Question | Blocks | Owner | Due | Resolution |
|---|---|---|---|---|---|
| Q-1 | Who fills each role in 00 §1.3, under which team name, and with which contact details in 11 §C? Who owns and approves each document? | 00 Document control, 00 §1.3, 11 §C, this header | Product owner | 2026-12-18 | Open |
| Q-2 | What do engineers and workloads use today (direct provider accounts, personal API keys, nothing), and what will the gateway replace? | §1.1, 00 §1 | Product owner | 2026-12-18 | Open |
| Q-3 | Which teams are in the pilot, and what are the target dates for the pilot and general availability? | §1.4 | Product owner | 2026-12-18 | Open |
| Q-4 | Which catalog models (§6.5) are needed, by which phase and at which priority? Are OpenAI models required, which would add Azure OpenAI Japan East as a second backend [CMP §7.2]? | §6.5, MDL-011 | Product owner | 2026-12-18 | Open |
| Q-5 | Which optional capabilities are in the first phase: embeddings (FUN-004), the MCP gateway, self-hosted models? | NG-7, FUN-004 | Product owner | 2026-12-18 | Open |
| Q-6 | What are the service levels: the availability target and what counts as down, whether upstream outages are excluded, RTO and RPO targets, the maximum planned downtime per upgrade, support hours, and the DR drill interval? | AVL-M01 to AVL-M04, OPS-006, OPS-007, 00 §1.4 | Product owner | 2026-12-18 | Open |
| Q-7 | What are the performance targets: added latency, throughput, concurrent streams, and expected growth at 12 and 24 months? | PRF-M01, PRF-M02, PRF-M04 | Product owner | 2026-12-18 | Open |
| Q-8 | Security timings: how soon after an Entra account is disabled must the user's keys stop working; how soon must audit events reach the SIEM; how often are audit events and operator activity reviewed? | IAM-006, OBS-001, OBS-007, 02 §4.3, 02 §7.4 | Security / SOC | 2026-12-18 | Open |
| Q-9 | What is the classification of each data item in §8, the retention of the spend export, request metadata, infrastructure log archive and billing export, and who may read per-user metadata? | §8, PRV-003, REG-003 | Legal / privacy | 2026-12-18 | Open |
| Q-10 | Is per-team content logging needed in this phase? If so, how does a team opt in, who approves it, and what retention applies? The comparison leaves the mechanism open [CMP §2.8]. | PRV-002 | Legal / privacy | 2026-12-18 | Open |
| Q-11 | Does legal confirm the residency scope in A-11 and the abuse-monitoring position in A-12? | AS-11, AS-12, REG-002 | Legal / privacy | 2026-12-18 | Open |
| Q-12 | Chargeback rules: which team pays when a key's owner is in two teams; whether client-set `user` and tags are showback only; the V-4 price tolerance; the residual investigation threshold; how fixed platform costs are allocated; how teams map to departments; whether a rolling 30-day budget is acceptable against calendar-month chargeback; and the overshoot bound in the budget policy. | CST-001, CST-004, CST-008, CST-009, CST-011 | FinOps | 2026-12-18 | Open |
| Q-13 | Guardrails: which personal-information types are masked, what prompt-attack detection rate is required, and should a guardrail failure refuse or allow the request? | SEC-008, SEC-009 | Security / SOC | 2026-12-18 | Open |
| Q-14 | Network: which office and DC egress CIDRs go on the allowlist and who owns each (A-14); can A-16 be confirmed; can the gateway hostname be exempted from TLS inspection and allowed by FQDN (A-15); what is the production hostname (the comparison uses `llm.corp.example`); which dedicated egress IPs will cloud-hosted agents use? | SEC-001, SEC-002, SEC-005, AS-14 to AS-16, 00 Document control | Network | 2026-12-18 | Open |
| Q-15 | Identity: are AS-1 to AS-3 and AS-21 confirmed, is EAM generally available in our tenant, and what admin sign-in frequency within 4–8 hours is used [CMP §2.1]? | AS-1 to AS-3, AS-21, IAM-003 | Identity | 2026-12-18 | Open |
| Q-16 | Can Intune deploy the managed settings and the key helper for Claude Code and Codex CLI, and which client telemetry can be turned off? | AS-20, FUN-009, RES-006 | Endpoint / Intune | 2026-12-18 | Open |
| Q-17 | Is the LiteLLM Enterprise licence bought (A-6), and does the vendor offer offline licence verification? | AS-6, AVL-004 | Product owner | 2026-12-18 | Open |
| Q-18 | Does an internal AI use policy and an acceptable-use policy exist that forbid key sharing? Where are they published? | REG-004, 11 §B | Legal / privacy | 2026-12-18 | Open |
| Q-19 | Which compliance frameworks (for example ISO 27001, SOC 2) apply to the gateway? | 02 §8.2 | Security / SOC | 2026-12-18 | Open |
| Q-20 | Which AWS Support plan and LiteLLM Enterprise support contract cover the gateway, which help desk gives first-line support, and which issue tracker is used? | 11 §B, 11 §C | Product owner | 2027-01-29 | Open |

## 10. Traceability

The traceability matrix is kept in 02 §11.3, built from the Satisfies line and columns of each design section. Approval of 02 requires:
- every Must requirement maps to at least one design section and at least one test or launch gate;
- every launch gate in [CMP §2.10] maps to at least one requirement here.

## 11. Change control

- Changes after approval go through a pull request that updates the Version, the change log, and any affected design and test references in the same PR.
- A change to a Must requirement, a constraint, or an assumption that turns out false needs the approvers listed in the header.

| Version | Date | Author | Change | Approved by |
|---|---|---|---|---|
| 0.1 | 2026-11-17 | Claude (AI assistant), for platform engineering | Initial draft from the comparison at commit `46699eb` | — |

## 12. Glossary

Terms are defined in 11 §A. Add a new term there in the same pull request as the requirement that uses it. Changing the meaning of a term used here is a change to this document (§11).
