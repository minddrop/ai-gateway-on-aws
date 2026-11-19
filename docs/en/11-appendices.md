# Internal LLM gateway: Appendices

> Owner: Documentation owner (00 Document control) · Last reviewed: 2026-11-17, design phase, before the first release · Status: Draft

## A. Glossary

| Term | Meaning |
|---|---|
| Admin UI | LiteLLM's web interface, where users sign in with Entra ID to create their own keys, and platform viewers inspect the gateway read-only (02 D-26, D-27) |
| Allowlist | The list of office and DC egress IP ranges that the ALB security group and the WAF admit; everything else is refused |
| Application inference profile | A Bedrock profile we create from a `jp.` profile so that usage can be tagged and charged |
| Authentication strength | The Conditional Access grant that names which sign-in methods count; admins and operators must meet the built-in Phishing-resistant MFA strength (02 D-29) |
| CA-GW-01 to CA-GW-05 | The Conditional Access policies for the gateway app and the AWS operator app [CMP §2.1] |
| Chargeback / showback | Charging a team's budget for usage / only reporting it |
| Conditional Access | The Entra ID policy engine that requires MFA and a compliant device at sign-in |
| CUR | AWS Cost and Usage Report: the billing source of truth |
| EAM | External Authentication Method: how Okta Verify supplies MFA to Entra ID [CMP §2.1] |
| External MFA | Microsoft's current name for EAM. It cannot satisfy a Conditional Access authentication strength (02 D-29). |
| Guardrail | A check that LiteLLM runs on a request before the model call, here PII masking and prompt-attack detection in the VPC |
| In-Region model | A Bedrock model processed only in the Region that is called, here Tokyo |
| `jp.` profile | A Bedrock geographic cross-Region inference profile that routes only between Tokyo and Osaka [CMP §2.5] |
| JWT | An Entra access token. This gateway does not accept JWTs for API traffic; they appear only in the Admin UI sign-in [CMP §2.3] |
| Key helper | The command, deployed by Intune, that prints the user's personal key from the OS credential store for Claude Code and Codex CLI [CMP §2.3.4] |
| Launch gate | A test that must pass before launch and after every LiteLLM upgrade [CMP §2.10] |
| LiteLLM break-glass | Emergency admin access to LiteLLM: the master key used as a Bearer token on the API from an allowlisted IP; every read of the secret alerts Security (02 D-28) |
| LiteLLM Proxy | The open-source gateway software the system runs |
| LLM-API key | A virtual key with `key_type: llm_api`, which LiteLLM refuses on every management route; every key a user creates is one (02 D-26) |
| Master key | LiteLLM's static admin credential |
| Model access group | A named set of models granted to teams |
| Organization | LiteLLM's level above teams; a candidate for mapping departments (02 R-14) |
| Personal virtual key | A virtual key that one user creates for their own tools in the Admin UI: owned by the user, charged to one of their teams, and valid only on the model routes (02 D-26) |
| Residual | The AWS bill total for the model service minus the total cost LiteLLM recorded, reported as its own line each month [CMP §4.5] |
| Route A / Route B | Private-line / internet ingress [CMP §2.6]. Only Route B is built in this phase. |
| RTO / RPO | Recovery time / point objective |
| Salt key | LiteLLM key that encrypts stored credentials; must not change |
| SCIM | The protocol Entra ID uses to provision operators in IAM Identity Center. LiteLLM's SCIM endpoint is not used; the sync job keeps LiteLLM in step with Entra (02 D-30). |
| SCP | AWS Organizations service control policy; here it denies anything outside Tokyo and Osaka |
| Service-account key | A virtual key owned by a team for one workload, created only by CI and kept in that workload's secret store (02 D-27) |
| Spend log | LiteLLM's per-request record of user, team, key, model, tokens and cost, with no content |
| Sync job | The scheduled task in the gateway VPC that reads Entra through Microsoft Graph, blocks the keys of disabled users, removes users from teams whose group they left, and resets roles Entra no longer grants (02 D-30) |
| Team | A cost centre in LiteLLM, mapped from an Entra group |
| Team lead | The lead of a team: sees the team's spend and budget alerts, and requests workload keys and changes to budgets, members and models through CI. LiteLLM's team admin role is not used (02 D-27). |
| Upper bounds | The maximum duration, budget and TPM/RPM a user may set on a key they create |
| Virtual key | A LiteLLM-issued key that every API client sends; personal for people, service-account for workloads |
| Warm standby | The Osaka copy of the gateway, deployed and ready to take traffic after a DNS failover |

## B. Related documents and links

- Comparison and design analysis: [../../../llm-gateway-comparison/README.md](../../../llm-gateway-comparison/README.md). The sections this set cites most: [assumptions A-1 to A-16](../../../llm-gateway-comparison/docs/en/00-overview.md), [common design §2 and launch gates §2.10](../../../llm-gateway-comparison/docs/en/01-common-design.md), [AWS design §4](../../../llm-gateway-comparison/docs/en/03-aws.md), [recommendation §7.2](../../../llm-gateway-comparison/docs/en/06-comparison.md), [private connectivity §8](../../../llm-gateway-comparison/docs/en/07-private-connectivity.md), [reference links §9](../../../llm-gateway-comparison/docs/en/08-references.md)
- Documentation template: [../../../llm-gateway-docs-template/README.md](../../../llm-gateway-docs-template/README.md)
- Baseline AWS sample: [sample-litellm-bedrock-gateway-on-eks](https://github.com/aws-samples/sample-litellm-bedrock-gateway-on-eks) [CMP §3.1]
- Source code and IaC: TBD (Platform engineering, 2027-01-29): none exists yet (02 R-22)
- Dashboards: TBD (Platform engineering, 2027-01-29): built with the system (02 R-39)
- Issue tracker: TBD (Product owner, 2027-01-29) (01 Q-20)
- Internal AI use policy: TBD (Legal / privacy, 2026-12-18) (01 Q-18)
- LiteLLM docs for the pinned version: TBD (Platform engineering, 2027-01-29): the version is not pinned yet (02 §1.3, 02 R-47). Current docs: [LiteLLM proxy docs](https://docs.litellm.ai/docs/simple_proxy)

## C. Contacts

Every contact is open until the roles are staffed (01 Q-1; support contracts are 01 Q-20).

| Role | Contact person | Channel | Use for |
|---|---|---|---|
| Product owner | TBD (Product owner, 2026-12-18) | TBD (Product owner, 2026-12-18) | Product questions, the model catalog |
| Platform engineering | TBD (Platform engineering, 2026-12-18) | TBD (Platform engineering, 2026-12-18) | Integration help, platform changes |
| On-call | TBD (Platform engineering, 2027-01-29) | TBD (Platform engineering, 2027-01-29) | Production incidents |
| Security / SOC | TBD (Security / SOC, 2026-12-18) | TBD (Security / SOC, 2026-12-18) | Security concerns, guardrail false positives, incidents involving prompts |
| Legal / privacy | TBD (Legal / privacy, 2026-12-18) | TBD (Legal / privacy, 2026-12-18) | Residency and content-logging approvals |
| FinOps | TBD (FinOps, 2026-12-18) | TBD (FinOps, 2026-12-18) | Chargeback questions |
| Network | TBD (Network, 2026-12-18) | TBD (Network, 2026-12-18) | Egress IPs, secure web gateway, TLS inspection |
| Identity | TBD (Identity, 2026-12-18) | TBD (Identity, 2026-12-18) | Entra ID, Okta, Conditional Access |
| Endpoint / Intune | TBD (Endpoint / Intune, 2026-12-18) | TBD (Endpoint / Intune, 2026-12-18) | Client configuration, certificates |
| Help desk | TBD (Product owner, 2027-01-29) | TBD (Product owner, 2027-01-29) | First-line user support |
| AWS Support | TBD (Product owner, 2027-01-29) | TBD (Product owner, 2027-01-29) | AWS service problems |
| LiteLLM Enterprise support | TBD (Product owner, 2027-01-29) | TBD (Product owner, 2027-01-29) | LiteLLM defects and advisories |

## D. Documentation checklist (tick before marking the set Approved)

- [ ] The check in the README's "Checking a document", run over `docs/`, prints nothing: no markers, examples, instruction comments or blank cells
- [ ] Every remaining TBD is also tracked in 01 §9 or 02 §14
- [ ] Text that came pre-filled (no marker) checked against the system as built and the pinned versions
- [ ] Setup (03) tested by someone new, date recorded
- [ ] Every alert in 07 §3 has an incident entry in 07 §6, with every field filled
- [ ] Every security-critical setting in 04 §4.2 has a passing launch gate
- [ ] Every Must requirement appears in the traceability matrix (02 §11.3)
- [ ] Every section from 02 §2 to §10 has a Satisfies line
- [ ] Every decision in 02 §13 that needs an ADR links one in `docs/en/adr/`, and the status in the row matches the status in the ADR
- [ ] Each fact appears only in its home, as listed in the README's "Where each fact lives"
- [ ] Links checked
- [ ] Owner and next review date set in 00 Document control; owner and last-reviewed date set in the status line of 03–11
- [ ] Japanese translation updated, if kept
