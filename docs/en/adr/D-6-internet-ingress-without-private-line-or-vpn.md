# D-6: Reach the gateway over the internet with an IP allowlist, without a private line or VPN

| Field | Value |
|---|---|
| Decision ID | D-6 |
| Status | Accepted |
| Date | 2026-11-17 |
| Owner | TBD (Product owner, 2026-12-18) (01 Q-1); Network |
| Decided by | The comparison ([CMP §2.6, §8.0]); confirmed when 02 is approved |
| Requirements baseline | REQ-GW 0.2 |
| Design version | SPEC-GW 0.1 |
| Supersedes | — |

## 1. Context

Engineers and workloads in our offices and DC must reach a gateway in AWS Tokyo. The path can be the internet, with a load balancer that admits only our egress IPs (Route B), or the existing Direct Connect circuits to an internal load balancer (Route A) [CMP §2.6]. A site-to-site VPN, or a remote-access VPN for people outside the office, are further ways to build a private path. The path decides which network dependencies the gateway has and what the IP allowlist can prove. It does not decide who the caller is: user, device and key checks are the same on every path [CMP §8.5].

## 2. Decision drivers

| Driver | Source |
|---|---|
| Requests from outside the office and DC egress IPs are refused | SEC-001; [CMP A-13, A-14] |
| The allowlist holds only dedicated egress IPs of ours, with no shared NAT or SASE ranges | SEC-002; [CMP V-11] |
| TLS terminates only in Japan, with no CDN or global edge | SEC-004; D-7 |
| The gateway hostname is exempt from TLS inspection on the corporate proxy | SEC-005; 01 AS-15 |
| Users work from offices and the DC; remote access is out of scope | 01 AS-13, NG-1 |
| Office and DC breakouts use a small, stable set of egress IPs, and unmanaged devices cannot use them | 01 AS-14, AS-16 |
| A private line is excluded unless a trigger applies | 01 NG-5; [CMP §8.0] |
| Identity, device and authorization checks do not depend on the network path | [CMP §8.5] |

## 3. Options considered

| Option | Drivers not met | Cost and effort | Risks | Outcome |
|---|---|---|---|---|
| Route B only: internet breakout, regional WAF and internet-facing ALB that admit only office and DC egress IPs | — | No new circuits or routing; WAF IP set and security group kept in step with the egress list (OPS-005) | Depends on 01 AS-14 to AS-16, all Open; one wrong security-group or WAF change exposes the endpoint to the internet | Chosen |
| Route A only: Direct Connect to an internal ALB | — | Carrier contract and bandwidth, DC routing, DNS forwarding to the VPC [CMP §2.6]; about USD 120 a month incremental [CMP §8.9] (02 §12) | A path, not an identity: every compromised host on the corporate network or a routed VPC can reach the gateway [CMP §8.5]; sign-in still needs the internet breakout [CMP §8.5] | Rejected unless a trigger in [CMP §8.0] applies |
| Both routes: a second, internal ALB in front of the same LiteLLM service | — | Everything in Route A, plus split-horizon DNS to choose the load balancer [CMP §2.6] | As Route A, and two front doors to keep identical | Rejected for this phase; Route A is added only on a trigger [CMP §8.0] |
| Site-to-site IPsec VPN from the offices and DC to the gateway VPC | — | VPN tunnels to run, plus the Route A changes: internal load balancer, DC routing and DNS forwarding [CMP §2.6, §8.1]; not costed | A path, not an identity, as Route A [CMP §8.5]; the tunnels use the same internet breakout as Route B | Rejected: it changes the path but not who can call the gateway |
| Remote-access VPN or ZTNA (Entra Private Access) for people outside the office | 01 NG-1, AS-13: remote access is out of scope | Per [CMP §8.6]: ZTNA connectors in the VPC, or VPN capacity and a hairpin through the DC | Removes the office IP allowlist, so mTLS or ZTNA becomes the per-request device check [CMP A-13, §8.6] | Out of scope this phase; revisited if remote access is requested |

## 4. Decision

Build Route B only: office and DC clients reach an internet-facing ALB in Tokyo through a regional WAF and a security group that admit only our egress IPs, with the virtual key on every request (D-1). Route A, a site-to-site VPN and remote-access options are not built. A private path adds isolation, but no identity, device or encryption protection, and every identity control is the same on both routes [CMP §8.5]. Route B therefore gives the same protection without the carrier, DC routing and DNS forwarding dependencies of Route A [CMP §2.6].

What it changes in the set:

| Document | Section | Change |
|---|---|---|
| 01 Requirements | §1.3 NG-1, NG-5; §7.3 SEC-001, SEC-002 | Remote access and private ingress (private line or site-to-site VPN) out of scope; allowlist requirements |
| 02 Architecture and design | §2.2 Ingress, §6, §9, §12 | Internet-facing ALB with allowlist; drift detection on its security group; Route 53 health check (R-8); Route A not costed |
| 07 Operations runbook | §5 | Allowlist review and update before any egress change (OPS-005) |

## 5. Consequences

| Kind | Consequence | Tracked in |
|---|---|---|
| Benefit | No carrier, circuit bandwidth, DC routing or DNS forwarding dependency, and no split-horizon DNS [CMP §2.6] | — |
| Cost | The decision rests on 01 AS-13 to AS-16, which are all Open; AS-13 may already be false if people work from home | R-50, V-11 |
| Cost | The endpoint is internet-facing, so a wrong security-group or WAF change exposes it; drift detection uses AWS Config [`vpc-sg-port-restriction-check`](https://docs.aws.amazon.com/config/latest/developerguide/vpc-sg-port-restriction-check.html) on port 443 and a probe from a non-allowlisted IP | 02 §6, T-040 |
| Cost | Route 53 health checkers cannot reach an ALB that admits only office IPs [CMP §4.9] | R-8 |
| Cost | Entra's provisioning service connects from the `AzureActiveDirectory` ranges ([SCIM provisioning](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups)), which the allowlist refuses, so LiteLLM SCIM is replaced by a sync job | D-30 |
| Cost | If the office firewall can allow only fixed destination IPs, the ALB needs AWS Global Accelerator, or Route A [CMP §2.6] | R-32 |
| Cost | Without the TLS-inspection exemption the corporate proxy can read prompts and keys; that is a trigger for Route A [CMP §8.0] | SEC-005, 01 Q-14 |
| Follow-up | A request for remote access reopens this decision and D-4: ZTNA or required mTLS replaces the allowlist [CMP §8.6] | 01 NG-1, D-4 |

## 6. Verification and review

- **Verified by:** T-040, T-041, T-042, T-070, V-11
- **Revisit when:** a trigger in [CMP §8.0] applies; remote access is requested (01 NG-1); office or DC egress moves to shared SASE or cloud NAT ranges, so SEC-002 fails; V-11 fails

## 7. Change log

| Date | Author | Change | Status after |
|---|---|---|---|
| 2026-11-20 | Claude (AI assistant), for platform engineering | ADR written for the decision accepted in [CMP §2.6, §8.0] on 2026-11-17, including the authentication and authorization review of 2026-11-20, which added the site-to-site and remote-access VPN options | Accepted |
