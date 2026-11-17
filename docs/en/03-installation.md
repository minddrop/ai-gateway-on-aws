# Internal LLM gateway: Installation and setup

<!--
Answers: how a new engineer goes from nothing to (a) a local gateway they can test against and (b) a new AWS environment.
Reader: a new team member who has been given access but has no history with this system.
Owns: prerequisites, the environment list, one-time setup and teardown. Refers to: setting names and values (04), day-to-day deploys (07 §1), design (02).
Detail: every step is one action, then a Run: line with the exact command or console path, then an Expect: line with the result. Have someone new follow it word for word, and record the date in the status line.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Prerequisites

| Requirement | Version | Notes / how to get it |
|---|---|---|
| Docker / Docker Compose | [fill: x.y or later] | Local stack only |
| [fill: Terraform or CDK] | [fill: x.y] | Pinned in [fill: file] |
| AWS CLI v2 | [fill: x.y or later] | Sign in with IAM Identity Center (`aws sso login`), never long-lived keys |
| Python | [fill: x.y] | Launch-gate and smoke-test scripts |
| `litellm-token` helper | [fill: version] | Prints an Entra token for the gateway [CMP §2.3.4] |
| Access: repository | — | [fill: who grants it] |
| Access: AWS accounts | — | [fill: permission set names per environment; who approves] |
| Access: secrets | — | [fill: who can read which secret]. Reviewed as admin access [CMP §2.3.5]. |
| Access: Entra app registration | — | [fill: who can change redirect URIs and app roles] |

## 2. Environments

| Environment | URL | AWS account / region | Purpose | Deployed from | Models |
|---|---|---|---|---|---|
| Local | `http://localhost:4000` | None (Docker) | Development | Working copy | [fill: a stub, or a dev Bedrock profile with no real data] |
| Dev | [fill] | [fill] / ap-northeast-1 | Integration | `main` | [fill] |
| Staging | [fill] | [fill] / ap-northeast-1 | Pre-release, launch gates | [default: release tag] | Same as production |
| Production | `https://llm.corp.example` | [fill] / ap-northeast-1 | Live | [default: release tag] | The catalog in 01 §6.5 |
| DR | [fill] | [fill] / ap-northeast-3 | Warm standby | Same tag as production | [fill: those available in Osaka (02 §9)] |

## 3. Local setup

<!-- Local runs must not send real company data to a model. The Models column in §2 states what the local stack points at. -->

1. **Clone the repository.**
   - Run: `git clone [fill: repo URL]`
   - Expect: a `[fill: repo name]` directory with `docker-compose.yml` at the top.
2. **Create the local settings.**
   - Run: `cp .env.example .env`, then set the values listed under Local in 04 §2.1.
   - Expect: `grep -c '=$' .env` prints `0` (no empty values).
3. **Start PostgreSQL, Redis and LiteLLM.**
   - Run: `docker compose up -d`
   - Expect: `docker compose ps` shows the three services running.
4. **Wait for readiness.**
   - Run: `curl -fsS http://localhost:4000/health/readiness`
   - Expect: [default: HTTP 200, with `"db": "connected"` in the body].
5. **Create a local team and key.**
   - Run: `[fill: script, for example ./scripts/seed-local.sh]`
   - Expect: [fill: what the script prints, for example the team ID and key alias].
6. **Send a test request.**
   - Run: `[fill: curl command against /v1/chat/completions with the local key]`
   - Expect: HTTP 200, and a spend-log row for the local team ([fill: how to see it]).
7. **Stop the stack.**
   - Run: `docker compose down` (add `-v` to delete local data)
   - Expect: `docker compose ps` lists no services.

## 4. New AWS environment

<!-- One-time bootstrap. Day-to-day deploys are in 07 §1. -->

1. **Account guardrails.** Confirm that the region-deny SCP is attached [CMP §4.8] and that the account is in the right OU.
   - Run: `aws organizations list-policies-for-target --target-id [fill: account ID] --filter SERVICE_CONTROL_POLICY`, from the management account
   - Expect: [fill: SCP name] is listed.
2. **Bedrock model access.** Enable each model in the catalog (01 §6.5). Create the application inference profiles from `jp.` profiles, with cost tags [CMP §7.2].
   - Run: [fill: IaC module or command]
   - Expect: `aws bedrock get-inference-profile --inference-profile-identifier <profile ARN>` shows only `ap-northeast-1` and `ap-northeast-3` models for every profile [CMP §2.5], and each profile carries its cost tags.
3. **Quotas.** Request Bedrock TPM and RPM increases to the capacity plan (02 §9), in Tokyo and in Osaka: quotas for `jp.` profiles apply per source Region [CMP §4.5].
   - Run: the Service Quotas console, or `aws service-quotas request-service-quota-increase` for each quota
   - Expect: [fill: where the approved values are recorded]
4. **Network prerequisites.** Get the office and DC egress CIDRs from the network team [CMP A-14]. Confirm the TLS-inspection exemption for the gateway hostname [CMP A-15].
   - Run: [fill: how to request them from the network team]
   - Expect: the CIDRs are in [fill: IaC variable file], and the exemption request is closed as done.
5. **Certificates.** Issue an ACM certificate for the hostname. If mTLS is adopted, upload the trust store and CRL to S3 [CMP §2.3.2].
   - Run: [fill: IaC module, or `aws acm request-certificate` command]
   - Expect: `aws acm describe-certificate --certificate-arn <certificate ARN>` shows `"Status": "ISSUED"`.
6. **Secrets.** Create these in Secrets Manager before the first deploy: master key, salt key, licence key, DB credentials (04 §3). **The salt key can never change after first start without a re-encryption plan.**
   - Run: [fill: IaC module or command]
   - Expect: `aws secretsmanager list-secrets` shows the four secrets, with the names given in 04 §2.1.
7. **Entra.** Register the app, set app roles and group claims, and set the Conditional Access policies [CMP §2.1–2.3].
   - Run: [fill: script, or Entra admin center path]
   - Expect: a token from `litellm-token` carries the gateway audience and the group or role claims ([fill: how to decode and check it]).
8. **Infrastructure.**
   - Run: `[fill: IaC command]` with `[fill: environment variable file]`
   - Expect: the apply finishes without errors, and a second plan shows no changes.
9. **Post-install checks.**
   - Run: the smoke tests (`[fill: smoke test command]`), then the launch gates (02 §11.2).
   - Expect: `/health/readiness` returns healthy through the ALB; a request from outside the allowlist is refused; a JWT request and a virtual-key request both succeed and both write spend rows; every launch gate passes before any real user is admitted.
10. **Enable retention locks last.** Turn on S3 Object Lock only after launch gate V-1 has passed [CMP §2.10].
    - Run: [fill: IaC change or command]
    - Expect: `aws s3api get-object-lock-configuration --bucket <bucket>` shows `"ObjectLockEnabled": "Enabled"` for each log bucket.

## 5. Teardown

<!-- Teardown is where residency and retention obligations are easiest to break. -->

1. **Record retained data.** Data under retention (audit logs, spend exports under Object Lock) cannot be deleted early.
   - Run: [fill: where the record is kept]
   - Expect: the record names each bucket, the date its retention ends, and the team that owns it after teardown.
2. **Revoke client access.** Remove the Entra app registration and the Intune client configuration.
   - Run: [fill]
   - Expect: `litellm-token` fails for a test user.
3. **Delete credentials.** Delete the virtual keys and the master key. Schedule KMS key deletion only after the retained data no longer needs it.
   - Run: [fill]
   - Expect: [fill]
4. **Remove network entries.** Remove the egress IPs from the allowlist and delete the DNS records.
   - Run: [fill: request to the network team; DNS change]
   - Expect: the hostname no longer resolves.
5. **Confirm nothing is left.**
   - Run: [fill: Cost Explorer filter or CUR query on the environment's tags]
   - Expect: no charges for the environment after [fill: number of days].
