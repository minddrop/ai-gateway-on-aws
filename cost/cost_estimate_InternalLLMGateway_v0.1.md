# Cost Estimate — Internal LLM gateway on AWS, v0.1

> **Generated, read-only snapshot of the estimate model.** The master is the Excel workbook built from the cost estimate template (`CostEstimate_InternalLLMGateway_v0.1.xlsx`, kept locally and not committed in this change); it holds the formulas, dropdowns, rate lookups and checks. Numbers here do not recalculate — change the workbook instead. A Japanese version is in `cost_estimate_InternalLLMGateway_v0.1_jp.md`.

> Purpose: internal budget approval in the design phase — **a budget estimate, not a quote** · Currency: JPY (line items excl. tax) · Prices: AWS list prices checked 2026-11-17, JPY 160/USD · Parameters: PM 10%, contingency 15% (applied to recurring: Yes), tax 10%, **24 recurring months in grand total** (24-month operation period). Model inference (Bedrock tokens charged back to teams) is **not** in the totals; see §7.

Sections 1–6 mirror the workbook sheets (Summary · Estimate · Rates · Assumptions · Lists · Calculation rules). Sections 7–11 are additions for this estimate: model usage, separately priced options, infrastructure sizing detail, open pricing items by owner, and findings for the design documents.

## 1. Summary / サマリー

### Project information / 案件情報

| Item | Value |
|---|---|
| Project name / 案件名 | Internal LLM gateway on AWS (build and 24-month operation) |
| Estimate version / 版数 | v0.1 |
| Estimate date / 作成日 | 2026-11-17 |
| Prepared by / 作成者 | Claude (AI assistant), for platform engineering |
| Status / ステータス | Draft / 作成中 |

### Parameters / パラメータ

| Parameter | Value | Notes |
|---|---:|---|
| PM cost (% of development cost) / PM費率 | 10.0% | Template default kept; the design docs give no reason to change it. |
| Contingency (% of cost) / 予備費率 | 15.0% | Template default kept. Identified risks from 02 §14 are added as line items (§2, Contingency). |
| Apply contingency to recurring cost? / 継続費用にも予備費を適用 | Yes | Template default. |
| Consumption tax rate / 消費税率 | 10.0% | Calculated once on each total and rounded down to JPY 1. |
| Recurring months in grand total / 総額に含める継続月数 | 24 | Operation period of 2 years (2027-08 to 2029-07). 12- and 36-month views are in the multi-year table below. |

### Totals / 合計

| Item | Excl. tax (JPY) / 税抜 | Consumption tax (JPY) / 消費税 | Incl. tax (JPY) / 税込 | Notes |
|---|---:|---:|---:|---|
| Total initial cost (one-time) / 初期費用合計 | 43,820,838 | 4,382,083 | 48,202,921 | All one-time costs incl. PM and contingency |
| Total recurring cost – monthly / 継続費用（月額） | 3,019,657 | 301,965 | 3,321,622 | Recurring rows per month (+ contingency) |
| Total recurring cost – annual / 継続費用（年額） | 36,235,887 | 3,623,588 | 39,859,475 | Monthly × 12 |
| **Grand total (initial + 24 months recurring) / 総額** | **116,292,612** | **11,629,261** | **127,921,873** | Tax calculated on this total |

### Multi-year views / 複数年試算

The same initial cost with 12, 24 (the grand total above) and 36 months of recurring cost. Model inference is excluded in every view.

| View | Recurring months | Excl. tax (JPY) | Consumption tax (JPY) | Incl. tax (JPY) |
|---|---:|---:|---:|---:|
| Initial + first year | 12 | 80,056,725 | 8,005,672 | 88,062,397 |
| Initial + operation period (grand total) | 24 | 116,292,612 | 11,629,261 | 127,921,873 |
| Initial + 3 years | 36 | 152,528,499 | 15,252,849 | 167,781,348 |

### Checks / チェック

| Check | Value | Result |
|---|---:|---|
| Line items not in any total (JPY) / 集計漏れ金額 | 0 | OK |
| Rows with quantity but no amount / 単価未設定の行数 | 1 | CHECK (deliberate): the LiteLLM Enterprise licence placeholder has no price yet (01 Q-17, owner: Product owner). All other rows are priced. |
| Rows with unit 'one-time' marked Recurring / 一式×継続の行数 | 0 | OK |
| PM line items while PM % > 0 / PM費の二重計上 | 0 | OK |

The workbook could not be recalculated with LibreOffice in this environment (not installed). The Summary values above were computed independently in Python with the workbook's formulas (unit cost lookup, ROUND for PM and contingency, ROUNDDOWN for tax); Excel recalculates the workbook when it is opened.

### Cost breakdown by category / 費目別内訳

| Category / 費目 | One-time (JPY) / 初期 | Recurring monthly (JPY) / 月額 | Recurring annual (JPY) / 年額 | Notes / 備考 | Share of dev. cost |
|---|---:|---:|---:|---|---:|
| ***1. Phase-based costs / 工程別費用*** |  |  |  |  |  |
| Requirements definition / 要件定義 | 1,180,000 | - | - |  | 4.4% |
| Basic & detailed design / 基本・詳細設計 | 3,825,000 | - | - |  | 14.4% |
| Implementation / 実装 | 11,312,500 | - | - |  | 42.5% |
| Testing (unit, integration, system, UAT) / テスト | 4,900,000 | - | - |  | 18.4% |
| Data migration / データ移行 | - | - | - | No rows: no data migration in 01/02 (A16) | - |
| Setup, build & deployment / 構築・リリース | 1,820,000 | - | - |  | 6.8% |
| Training & documentation / 教育・ドキュメント | 1,895,000 | - | - |  | 7.1% |
| Cutover & go-live support / 本番移行・稼働支援 | 1,687,500 | - | - |  | 6.3% |
| Operation / 運用 | - | 837,500 | 10,050,000 |  | - |
| Maintenance / 保守 | - | 512,500 | 6,150,000 |  | - |
| **Subtotal – phase-based / 小計（工程別）** | **26,620,000** | **1,350,000** | **16,200,000** | One-time part = development cost | **100.0%** |
| ***2. Cross-cutting costs / 横断費用*** |  |  |  |  |  |
| Project management / プロジェクト管理 | - | - | - | No bottom-up PM rows |  |
| Project management: 10.0% of development cost / PM費（自動計算） | 2,662,000 |  |  | PM % × development cost |  |
| Quality assurance & reviews / 品質保証 | 510,000 | - | - |  |  |
| Infrastructure / インフラ | 3,257,642 | 963,892 | 11,566,704 |  |  |
| Software licenses & tools / ライセンス・ツール | - | - | - | LiteLLM Enterprise licence not priced yet |  |
| Security / セキュリティ | 2,800,000 | - | - |  |  |
| Contingency & risk buffer / 予備費 | 2,593,750 | 358,681 | 4,304,175 | Identified risks at expected value (02 §14) |  |
| Contingency buffer: 15.0% of initial and recurring cost / 予備費（自動計算） | 5,377,446 | 347,084 | 4,165,008 | Contingency % × cost before contingency |  |
| **Subtotal – cross-cutting / 小計（横断）** | **17,200,838** | **1,669,657** | **20,035,887** |  |  |
| **Total (excl. tax) / 合計（税抜）** | **43,820,838** | **3,019,657** | **36,235,887** |  |  |

### Calculation bases and indicators / 計算基礎・指標

| Item | Value | Definition |
|---|---:|---|
| Development cost (base for PM %) / 開発費 | 26,620,000 | One-time costs of all phase-based categories |
| Initial cost before contingency / 予備費控除前の初期費用 | 35,849,642 | All one-time costs except the Contingency category (incl. calculated PM) |
| Recurring cost before contingency (monthly) / 予備費控除前の継続月額 | 2,313,892 | Used because contingency applies to recurring |
| Total one-time effort / 初期工数合計 | 30.1 person-months | Person-months + person-days ÷ 20 (One-time rows) |
| Testing share of development cost / テスト比率 | 18.4% | Typical range 20–30% |

## 2. Estimate details / 見積明細

Subtotal = Quantity × Unit cost. **Recurring rows show the cost per month.** Prices for monthly fees and one-time items are entered in column J (Unit cost override) in Excel; here they are shown directly as the unit cost. The bold subtotal rows are for reading convenience. In Excel each category also has a blank spare row with formulas. [PL] = AWS Price List API offer file for the region, checked 2026-11-17; USD amounts are converted at JPY 160/USD.

### 1. PHASE-BASED COSTS / 工程別費用

| Category / phase | Task or item description | Role | Unit | Quantity | Unit cost (JPY) | Subtotal (JPY) | One-time / Recurring | Notes / assumptions |
|---|---|---|---:|---:|---:|---:|---|---|
| Requirements definition / 要件定義 | Close the 20 open questions in 01 §9 and confirm assumptions AS-1–AS-21 with their 8 owner teams; update 01 to v1.0 | Business analyst / SE / 業務SE | person-days / 人日 | 15.0 | 60,000 | 900,000 | One-time / 初期 | 01 §9 (Q-1–Q-20, due 2026-12-18 / 2027-01-29), 01 §3. Sizing: ~0.75 pd per question incl. workshop and write-up |
| Requirements definition / 要件定義 | Requirements review and approval (security, legal/privacy, network, FinOps, platform lead) | Architect / tech lead / アーキテクト | person-days / 人日 | 4.0 | 70,000 | 280,000 | One-time / 初期 | 01 header Approvers, 01 §11, REG-003. Sizing: 2 review rounds × 2 pd |
| **Subtotal 1-1** | **Requirements definition / 要件定義** |  |  |  |  | **1,180,000** | One-time / 初期 |  |
| Basic & detailed design / 基本・詳細設計 | Design v0.2: close uncovered requirements and High risks — Osaka egress and secrets copy (R-7), failover health check (R-8), AVL-001, spend-log store (R-1), profile granularity (R-12), data-tier choices (R-23), content logging if needed (PRV-002, R-6) | Architect / tech lead / アーキテクト | person-months / 人月 | 1.0 | 1,400,000 | 1,400,000 | One-time / 初期 | 02 §1.2, §14 (target 2027-01-29). Sizing: ~6 design topics × ~3 pd |
| Basic & detailed design / 基本・詳細設計 | Detailed design of remaining TBDs: accounts and environments (R-41), permission sets and break-glass (R-45), IaC tool (R-22), task sizing (R-42), routing values (R-49), request-size limit (R-17), key defaults (R-16), alert thresholds (R-39) | Infra / DevOps engineer / インフラ | person-months / 人月 | 1.0 | 1,100,000 | 1,100,000 | One-time / 初期 | 02 §1.3, §4.3, §9, §10, §14. Sizing: ~8 topics × ~2.5 pd |
| Basic & detailed design / 基本・詳細設計 | Guardrail classifier selection: evaluate Japanese-capable prompt-attack classifiers and Presidio Japanese recognizers against the Q-13 test set | Senior engineer / シニアエンジニア | person-days / 人日 | 10.0 | 55,000 | 550,000 | One-time / 初期 | 02 §1.3, §8, D-9, R-10; 01 SEC-008, Q-13. Sizing: 3 candidates × 3 pd + report |
| Basic & detailed design / 基本・詳細設計 | Early spikes on a sandbox: master-key UI login (R-2/V-3), Codex CLI Responses API (R-4), ARN pricing (R-5), SCIM key blocking (R-35) | Engineer / エンジニア | person-days / 人日 | 10.0 | 42,500 | 425,000 | One-time / 初期 | 02 §14 mitigations 'run early'. Sizing: 4 spikes × 2.5 pd |
| Basic & detailed design / 基本・詳細設計 | Design review and approval (security, network, platform lead, FinOps, SRE), incl. Security sign-off of R-48 parameters | Architect / tech lead / アーキテクト | person-days / 人日 | 5.0 | 70,000 | 350,000 | One-time / 初期 | 02 header Approvers, R-48. Sizing: 2 rounds + 1 pd follow-up |
| **Subtotal 1-2** | **Basic & detailed design / 基本・詳細設計** |  |  |  |  | **3,825,000** | One-time / 初期 |  |
| Implementation / 実装 | IaC for both regions: VPC/subnets/endpoints, ALB + WAF, ECS services, Aurora Global Database, ElastiCache, S3/KMS/Secrets, SCP and Config rules, Route 53 failover, TGW attachment | Infra / DevOps engineer / インフラ | person-months / 人月 | 3.0 | 1,100,000 | 3,300,000 | One-time / 初期 | 02 §2.2, §6, §8, §9; OPS-002, D-8 (start from the AWS sample [CMP §3.1]). Sizing: ~20 components, one codebase for 4 environments |
| Implementation / 実装 | LiteLLM configuration and model catalog: config.yaml for 10 catalog models + aliases, Japan-only fallbacks, custom pricing per profile, application inference profiles, content-off settings, SSO/team-sync settings, key upper bounds | Senior engineer / シニアエンジニア | person-months / 人月 | 1.0 | 1,100,000 | 1,100,000 | One-time / 初期 | 02 §5, §5.1, §7.3; D-19, D-20, D-21, D-22; 01 §6.5 MDL-001–010 |
| Implementation / 実装 | Self-hosted in-VPC guardrail service: Presidio with Japanese recognizers, classifier service, LiteLLM pre-call integration, failure behaviour, metadata-only logging, container hardening | Senior engineer / シニアエンジニア | person-months / 人月 | 2.0 | 1,100,000 | 2,200,000 | One-time / 初期 | 02 §2.2, §8 (D-9), R-10, R-11; 01 SEC-008, SEC-009. Sizing: new service with ML model, our own scaling and patching [CMP §7.1] |
| Implementation / 実装 | Entra SSO / SCIM integration: OIDC app per environment (3), app roles → LiteLLM roles, llm-team-* team sync, SCIM deprovisioning, offboarding job if SCIM does not block keys | Engineer / エンジニア | person-months / 人月 | 1.0 | 850,000 | 850,000 | One-time / 初期 | 02 §4.1, §4.2, §4.5 (R-35, R-24); 01 IAM-001, IAM-004, IAM-006, TEN-004 |
| Implementation / 実装 | Key-issuance pipeline: CI for teams, budgets, model access and service-account keys; upper bounds; secret-scanning pattern for the key format | Engineer / エンジニア | person-months / 人月 | 1.0 | 850,000 | 850,000 | One-time / 初期 | 02 §4.5, §5, §10; D-19, OPS-003, TEN-001–TEN-006, SEC-018 |
| Implementation / 実装 | Client package: key helper (Windows Credential Manager / macOS Keychain), Claude Code managed settings, Codex CLI config.toml (deployed by Intune team) | Engineer / エンジニア | person-days / 人日 | 10.0 | 42,500 | 425,000 | One-time / 初期 | 02 §2.2 client package, §4.1, D-3; 01 FUN-009. Intune deployment itself excluded (B5) |
| Implementation / 実装 | CUR reconciliation job: daily spend export to S3 Parquet with delete-after-export, CUR 2.0 export, Athena tables, Quick Sight chargeback with residual line, AWS Budgets backstop | Engineer / エンジニア | person-months / 人月 | 1.0 | 850,000 | 850,000 | One-time / 初期 | 02 §5, §7.1, D-14, D-23; 01 CST-007, CST-008, CST-011 [CMP §4.5] |
| Implementation / 実装 | Logging / SIEM pipeline: S3 metadata callback, log groups with KMS and retention, WAF credential redaction, cross-account subscription to SIEM and log-archive, audit-log export | Infra / DevOps engineer / インフラ | person-months / 人月 | 1.0 | 1,100,000 | 1,100,000 | One-time / 初期 | 02 §7.1, §7.4; 01 OBS-001, OBS-002, OBS-004, OBS-007, SEC-015. SIEM-side ingestion excluded (B6) |
| Implementation / 実装 | Metrics, dashboards and alerts: AMP + ADOT, Grafana dashboards per team/key, dependency and missing-spend alarms, key-sharing alert, synthetic availability probe | Engineer / エンジニア | person-days / 人日 | 15.0 | 42,500 | 637,500 | One-time / 初期 | 02 §2.2 metrics row, R-38, R-39; 01 OBS-003, OBS-005, OBS-006, AVL-M01 |
| **Subtotal 1-3** | **Implementation / 実装** |  |  |  |  | **11,312,500** | One-time / 初期 |  |
| Testing (unit, integration, system, UAT) / テスト | Unit tests for custom code (guardrail service, export job, offboarding job, key helper, CI pipeline) | Engineer / エンジニア | person-days / 人日 | 15.0 | 42,500 | 637,500 | One-time / 初期 | Sizing: ≈15 % of custom-code build effort (≈5 pm) |
| Testing (unit, integration, system, UAT) / テスト | Integration, security and inspection tests T-001–T-075 on staging: automate, run, retest | QA / test engineer / テスト担当 | person-months / 人月 | 2.5 | 800,000 | 2,000,000 | One-time / 初期 | 02 §11.1 (75 tests). Sizing: avg 0.65 pd per test incl. automation + 1 retest cycle |
| Testing (unit, integration, system, UAT) / テスト | Load and long-stream tests (T-059, T-023, T-058, T-060) and task sizing | Infra / DevOps engineer / インフラ | person-days / 人日 | 8.0 | 55,000 | 440,000 | One-time / 初期 | 02 §11.1, R-42, R-49; 01 PRF-M02, PRF-M04, PRF-001 (sizing basis A-9) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-1: No prompt content outside approved stores: canary through every model and API style, guardrail-blocked and provider-rejected requests; search every store | Senior engineer / シニアエンジニア | person-days / 人日 | 5.0 | 55,000 | 275,000 | One-time / 初期 | 02 §11.2 [CMP V-1, §2.10]; 01 PRV-001, OBS-002; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-2: Key creation stays within limits, incl. the two-key check | QA / test engineer / テスト担当 | person-days / 人日 | 3.0 | 40,000 | 120,000 | One-time / 初期 | 02 §11.2 [CMP V-2, §2.10]; 01 TEN-001, TEN-005, TEN-006; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-3: Admin UI master-key login | Senior engineer / シニアエンジニア | person-days / 人日 | 1.0 | 55,000 | 55,000 | One-time / 初期 | 02 §11.2 [CMP V-3, §2.10]; 01 SEC-011, R-2; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-4: Spend correct per deployment (10 deployments, with and without prompt caching) | Engineer / エンジニア | person-days / 人日 | 4.0 | 42,500 | 170,000 | One-time / 初期 | 02 §11.2 [CMP V-4, §2.10]; 01 CST-004, R-5, D-21; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-5: Cancelled requests are metered | Engineer / エンジニア | person-days / 人日 | 3.0 | 42,500 | 127,500 | One-time / 初期 | 02 §11.2 [CMP V-5, §2.10]; 01 CST-006; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-6: Clients cannot skip tracking | QA / test engineer / テスト担当 | person-days / 人日 | 1.0 | 40,000 | 40,000 | One-time / 初期 | 02 §11.2 [CMP V-6, §2.10]; 01 CST-005; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-7: Clients cannot choose who pays, incl. user in two teams | QA / test engineer / テスト担当 | person-days / 人日 | 2.0 | 40,000 | 80,000 | One-time / 初期 | 02 §11.2 [CMP V-7, §2.10]; 01 CST-001, R-26; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-8: Database outage behaviour | Infra / DevOps engineer / インフラ | person-days / 人日 | 3.0 | 55,000 | 165,000 | One-time / 初期 | 02 §11.2 [CMP V-8, §2.10]; 01 AVL-002, D-25; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-9: Licence check unavailable | Infra / DevOps engineer / インフラ | person-days / 人日 | 2.0 | 55,000 | 110,000 | One-time / 初期 | 02 §11.2 [CMP V-9, §2.10]; 01 AVL-004, R-19; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-10: Identity endpoints unavailable | Infra / DevOps engineer / インフラ | person-days / 人日 | 2.0 | 55,000 | 110,000 | One-time / 初期 | 02 §11.2 [CMP V-10, §2.10]; 01 AVL-003; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | Launch gate V-11: Unmanaged devices cannot reach the gateway (with Network; CIDR list and owners) | Security specialist / セキュリティ | person-days / 人日 | 3.0 | 80,000 | 240,000 | One-time / 初期 | 02 §11.2 [CMP V-11, §2.10]; 01 SEC-001–SEC-003, OPS-004; must pass before first pilot user (01 §1.4) |
| Testing (unit, integration, system, UAT) / テスト | DR drill before launch: fail over to Osaka, measure RTO/RPO, call each model available in Osaka, fail back; AZ-loss test | Infra / DevOps engineer / インフラ | person-days / 人日 | 6.0 | 55,000 | 330,000 | One-time / 初期 | 02 §11.1 T-055, T-056; 01 OPS-007, AVL-M02, AVL-M03, GA exit (01 §1.4) |
| **Subtotal 1-4** | **Testing (unit, integration, system, UAT) / テスト** |  |  |  |  | **4,900,000** | One-time / 初期 |  |
| Data migration / データ移行 | *No line items: 01 and 02 define no data migration; what the gateway replaces is open (01 Q-2).* |  |  |  |  |  |  |  |
| Setup, build & deployment / 構築・リリース | AWS accounts and landing-zone onboarding for dev, staging, prod: SCP, Identity Center permission sets, break-glass, TGW attachments, budgets | Infra / DevOps engineer / インフラ | person-days / 人日 | 10.0 | 55,000 | 550,000 | One-time / 初期 | 02 §4.3, §10 (R-41, R-45); 01 IAM-007–IAM-009, RES-003 |
| Setup, build & deployment / 構築・リリース | CI/CD: image mirror to ECR by digest, scan gate, promotion dev → staging → prod, config deploy, IaC plan/apply with drift check | Infra / DevOps engineer / インフラ | person-days / 人日 | 15.0 | 55,000 | 825,000 | One-time / 初期 | 02 §8, §10; 01 SEC-016, OPS-002 (T-051, T-068) |
| Setup, build & deployment / 構築・リリース | Bedrock setup in both regions: model access, application inference profiles, quota requests in Tokyo and Osaka, GetInferenceProfile records, invocation logging off | Engineer / エンジニア | person-days / 人日 | 4.0 | 42,500 | 170,000 | One-time / 初期 | 02 §5.1, §9 (R-27), D-10, D-13; 01 MDL-104, PRV-004 |
| Setup, build & deployment / 構築・リリース | Production and DR deployment and release | Infra / DevOps engineer / インフラ | person-days / 人日 | 5.0 | 55,000 | 275,000 | One-time / 初期 | 02 §10 (release unit, rolling deploy) |
| **Subtotal 1-6** | **Setup, build & deployment / 構築・リリース** |  |  |  |  | **1,820,000** | One-time / 初期 |  |
| Training & documentation / 教育・ドキュメント | Technical docs 03, 04, 06, 07, 09 written to the design, incl. rewriting the R-21 conflicts | Senior engineer / シニアエンジニア | person-months / 人月 | 1.0 | 1,100,000 | 1,100,000 | One-time / 初期 | README doc set, 02 R-21. Sizing: 5 docs × 4 pd |
| Training & documentation / 教育・ドキュメント | User-facing docs 05, 08, 10 and editing of the set to the 11 §D checklist | Tech writer / trainer / ライター・講師 | person-days / 人日 | 12.0 | 35,000 | 420,000 | One-time / 初期 | README doc set, 11 §D |
| Training & documentation / 教育・ドキュメント | User onboarding: guide and short video, 2 live sessions for pilot and GA cohorts, team-admin training (budgets, service-account keys) | Tech writer / trainer / ライター・講師 | person-days / 人日 | 6.0 | 35,000 | 210,000 | One-time / 初期 | 01 §1.4, UC-3, UC-5; 30 engineers (A12). Sizing: 2 sessions × 1 pd + 4 pd material |
| Training & documentation / 教育・ドキュメント | Operations handover to on-call: 07 runbook walk-through and alert drills | Senior engineer / シニアエンジニア | person-days / 人日 | 3.0 | 55,000 | 165,000 | One-time / 初期 | 02 §10 on-call; 01 OPS-006 |
| **Subtotal 1-7** | **Training & documentation / 教育・ドキュメント** |  |  |  |  | **1,895,000** | One-time / 初期 |  |
| Cutover & go-live support / 本番移行・稼働支援 | Pilot (1 month): onboard pilot teams, triage, fixes, findings into 08 | Engineer / エンジニア | person-months / 人月 | 1.0 | 850,000 | 850,000 | One-time / 初期 | 01 §1.4 (pilot teams Q-3) |
| Cutover & go-live support / 本番移行・稼働支援 | GA readiness: re-run launch gates on the release that goes live | QA / test engineer / テスト担当 | person-days / 人日 | 5.0 | 40,000 | 200,000 | One-time / 初期 | 01 §1.4 GA exit, OPS-001 |
| Cutover & go-live support / 本番移行・稼働支援 | Hypercare 2 weeks after GA | Engineer / エンジニア | person-days / 人日 | 15.0 | 42,500 | 637,500 | One-time / 初期 | Sizing: 1.5 engineers × 10 days |
| **Subtotal 1-8** | **Cutover & go-live support / 本番移行・稼働支援** |  |  |  |  | **1,687,500** | One-time / 初期 |  |
| Operation / 運用 | On-call and incident response in support hours (business hours assumed) | Operations engineer / 運用担当 | person-months / 人月 | 0.5 | 750,000 | 375,000 | Recurring / 継続 | Per month. 01 OPS-006 (hours open, Q-6); 00 §1.4 |
| Operation / 運用 | Monitoring, alert triage and CI changes for teams, budgets, models and service-account keys | Operations engineer / 運用担当 | person-months / 人月 | 0.25 | 750,000 | 187,500 | Recurring / 継続 | Per month. 01 OPS-003, OBS-006; 02 §10 |
| Operation / 運用 | First-line help desk: key renewal (90-day expiry), onboarding questions | Help desk / ヘルプデスク | person-days / 人日 | 2.0 | 27,500 | 55,000 | Recurring / 継続 | Per month. 01 TEN-006, Q-20. 30 engineers: ≈10 key renewals a month |
| Operation / 運用 | Monthly chargeback run and residual investigation | Engineer / エンジニア | person-days / 人日 | 2.0 | 42,500 | 85,000 | Recurring / 継続 | Per month. 01 CST-007, CST-008; 02 §5 |
| Operation / 運用 | Periodic reviews: master-key readers, audit and operator activity | Security specialist / セキュリティ | person-days / 人日 | 1.0 | 80,000 | 80,000 | Recurring / 継続 | Per month. 01 SEC-010, OBS-007 (frequency Q-8) |
| Operation / 運用 | Recurring DR drill (assumed every 6 months × 6 pd) | Infra / DevOps engineer / インフラ | person-days / 人日 | 1.0 | 55,000 | 55,000 | Recurring / 継続 | Per month equivalent. 01 OPS-007 (interval Q-6) |
| **Subtotal 1-9** | **Operation / 運用** |  |  |  |  | **837,500** | Recurring / 継続 | per month |
| Maintenance / 保守 | LiteLLM upgrades with every launch gate re-run on staging (assumed quarterly, 12 pd per upgrade) | Senior engineer / シニアエンジニア | person-days / 人日 | 4.0 | 55,000 | 220,000 | Recurring / 継続 | Per month. 01 OPS-001; 02 §10 upgrade gate, §7.5 (R-30) [CMP §2.10] |
| Maintenance / 保守 | Quarterly Japan model snapshot re-check of every catalog model and catalog updates (≈3 pd per quarter) | Engineer / エンジニア | person-days / 人日 | 1.0 | 42,500 | 42,500 | Recurring / 継続 | Per month. 01 MDL-104, AS-17; 02 §5.1 (R-28) |
| Maintenance / 保守 | Patching: base images, guardrail dependencies, Aurora/Valkey minor versions, advisories | Infra / DevOps engineer / インフラ | person-days / 人日 | 2.0 | 55,000 | 110,000 | Recurring / 継続 | Per month. 02 §8.3 |
| Maintenance / 保守 | Guardrail classifier and PII-recognizer upkeep | Senior engineer / シニアエンジニア | person-days / 人日 | 1.0 | 55,000 | 55,000 | Recurring / 継続 | Per month. 02 R-10 (accuracy, scaling and patching are ours) |
| Maintenance / 保守 | Bug fixes and minor changes to custom components | Engineer / エンジニア | person-days / 人日 | 2.0 | 42,500 | 85,000 | Recurring / 継続 | Per month. Guardrail service, jobs, key helper, pipelines |
| **Subtotal 1-10** | **Maintenance / 保守** |  |  |  |  | **512,500** | Recurring / 継続 | per month |

### 2. CROSS-CUTTING COSTS / 横断費用

| Category / phase | Task or item description | Role | Unit | Quantity | Unit cost (JPY) | Subtotal (JPY) | One-time / Recurring | Notes / assumptions |
|---|---|---|---:|---:|---:|---:|---|---|
| Project management / プロジェクト管理 | *No line items: PM is calculated on Summary (PM % x development cost).* |  |  |  |  |  |  |  |
| Quality assurance & reviews / 品質保証 | Independent review of IaC and security-critical configuration (§7.3 settings, SCP, endpoint policies, WAF rules) before launch | Architect / tech lead / アーキテクト | person-days / 人日 | 5.0 | 70,000 | 350,000 | One-time / 初期 | 02 §7.3, §8, D-11, D-13 |
| Quality assurance & reviews / 品質保証 | Phase-gate reviews: design, build complete, launch readiness, GA | QA / test engineer / テスト担当 | person-days / 人日 | 4.0 | 40,000 | 160,000 | One-time / 初期 | 01 §1.4 exit criteria. 4 gates × 1 pd |
| **Subtotal 2-2** | **Quality assurance & reviews / 品質保証** |  |  |  |  | **510,000** | One-time / 初期 |  |
| Infrastructure / インフラ | Dev environment during the project (Tokyo) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 6.0 | 80,298 | 481,788 | One-time / 初期 | Quantity = 6 months (2027-02 to 2027-07). USD 501.86/month × 160 = J. Fargate 1 gateway (1 vCPU/2 GB) + 1 guardrail (2 vCPU/4 GB) USD 134.95; Aurora db.t4g.medium single instance + 10 GB + I/O USD 88.69; Valkey cache.t4g.small single node USD 28.62; ALB + 1 LCU; WAF ACL + 12 rules USD 40.58; 11 interface endpoints × 1 AZ USD 112.42; TGW attachment (egress to Entra for SSO) USD 51.10; CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone USD 29.50; GuardDuty, Security Hub, Config USD 16.00. 02 §10, 03 §2 (R-41). [PL 2026-11-17] |
| Infrastructure / インフラ | Staging environment during the project (Tokyo, production topology at minimum scale) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 4.0 | 333,934 | 1,335,736 | One-time / 初期 | Quantity = 4 months (2027-04 to 2027-07). USD 2,087.09/month. Fargate 3 gateway (2 vCPU/4 GB) + 3 guardrail (4 vCPU/8 GB) USD 809.69; Aurora writer + reader db.r7g.large + storage/I/O USD 496.18; Valkey 2 × cache.m7g.large USD 235.94; ALB + 2 LCU; WAF ACL + 12 rules USD 46.42; 11 interface endpoints × 3 AZs USD 337.26; TGW attachment USD 51.10; CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone USD 50.50; GuardDuty (18 vCPU), Security Hub, Config USD 60.00. 02 §10 (matches production for launch gates). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo before GA (build and pilot) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 2.0 | 396,851 | 793,702 | One-time / 初期 | Quantity = 2 months (2027-06 to 2027-07). Same components as the recurring production rows below: USD 2,480.32/month. [PL 2026-11-17] |
| Infrastructure / インフラ | DR Osaka before GA (build and DR drill) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 2.0 | 152,808 | 305,616 | One-time / 初期 | Quantity = 2 months. Same components as the recurring DR rows below: USD 955.05/month. [PL 2026-11-17] |
| Infrastructure / インフラ | Bedrock tokens used by the platform team during the project (development, tests, launch gates, DR drill) | Vendor / non-labor / 外部・非人件費 | one-time / 一式 | 1.0 | 340,800 | 340,800 | One-time / 初期 | Sizing: dev use ≈ USD 300/month × 6 + functional/gate tests ≈ USD 250 + load test on Haiku 5.5 (360k req × 1.2k tokens) ≈ USD 80 → ≈ USD 2,130. Prices: §usage table. Not charged back |
| Infrastructure / インフラ | Production Tokyo: Fargate: LiteLLM gateway tasks | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 43,184 | 43,184 | Recurring / 継続 | Per month from GA. avg 3 tasks × (2 vCPU × 0.05056 + 4 GB × 0.00553)/h × 730 h = USD 269.90. 02 §9 (min 3 tasks, 3 AZs; size open R-42) [CMP §4.9]; at 30 engineers no scale-out above the minimum is expected. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Fargate: in-VPC guardrail service (Presidio + classifier, CPU) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 86,366 | 86,366 | Recurring / 継続 | Per month from GA. avg 3 tasks × (4 vCPU × 0.05056 + 8 GB × 0.00553)/h × 730 h = USD 539.79. 02 §2.2, §8, D-9; one task per AZ; classifier not chosen (R-10), CPU inference assumed; GPU is contingency row R-10. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Aurora PostgreSQL (writer + reader, db.r7g.large, Multi-AZ) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 80,085 | 80,085 | Recurring / 継続 | Per month from GA. 2 × 0.333/h × 730 h + 50 GB × 0.12 + 30 M I/O × 0.24/M + 50 GB backup × 0.023 = USD 500.53. 02 §2.2, §7.1, §9 [CMP §4.7]; provisioned assumed (R-23); 90-day spend log ≈ 3.3 M rows; 50 GB allocated with headroom (R-1). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: ElastiCache Valkey (2 × cache.m7g.large, Multi-AZ) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 37,750 | 37,750 | Recurring / 継続 | Per month from GA. 2 nodes × 0.1616/h × 730 h = USD 235.94. 02 §2.2, §7.1 (counters only, no response cache); Valkey assumed (R-23). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Application Load Balancer (internet-facing) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 4,707 | 4,707 | Recurring / 継続 | Per month from GA. 0.0243/h × 730 h + avg 2 LCU × 0.008/h × 730 h = USD 29.42. 02 §2.2, §6 (Route B, 600 s idle); LCU from ~0.15 TB/month processed + long-lived streams. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: AWS WAF regional web ACL | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 2,824 | 2,824 | Recurring / 継続 | Per month from GA. 1 ACL × 5 + 12 rules × 1 + 1.09 M requests × 0.60/M = USD 17.65. 02 §8 WAF row: IP set, rate rule, IP reputation, Known Bad Inputs, CRS, admin-path and route-block rules (~12). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Interface VPC endpoints (11 × 3 AZs) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 54,230 | 54,230 | Recurring / 継続 | Per month from GA. 11 endpoints × 3 AZs × 0.014/h × 730 h + 168 GB × 0.01 = USD 338.94. 02 §6 endpoint list (10) + aps-workspaces for AMP (finding F-1); 02 §12 'about 11 × 3 AZs'. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Transit Gateway VPC attachment (egress path) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 8,192 | 8,192 | Recurring / 継続 | Per month from GA. 1 attachment × 0.07/h × 730 h + 5 GB × 0.02 = USD 51.20. 02 §6 egress via TGW to network-prod (AS-18); attachment billed to gateway account. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Network Firewall (network-prod): incremental GB only | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 53 | 53 | Recurring / 継続 | Per month from GA. 5 GB × 0.065 (endpoint-hours are shared, AS-18) = USD 0.33. 02 §6, D-12 [CMP §4.6]; Entra/licence traffic only. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: NAT gateway (network-prod): incremental GB only | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 50 | 50 | Recurring / 継続 | Per month from GA. 5 GB × 0.062 (gateway-hours are shared, AS-18) = USD 0.31. 02 §6 [CMP §4.6]. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Data transfer out to office/DC clients (responses) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 498 | 498 | Recurring / 継続 | Per month from GA. 27 GB × 0.114 (first-10-TB tier) = USD 3.11. Route B over internet (02 §6); 1.09 M responses × 20 KB SSE + 25 % overhead. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Secrets Manager | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 592 | 592 | Recurring / 継続 | Per month from GA. 8 secrets × 0.40 + 100k API calls × 0.05/10k = USD 3.70. 02 §7.1: master, salt, licence, DB, SSO client, CI admin key, Valkey AUTH, spare. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: KMS customer-managed keys | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 1,440 | 1,440 | Recurring / 継続 | Per month from GA. 6 CMKs × 1 + 1 M requests × 0.03/10k = USD 9.00. 02 §7.1: Aurora, ElastiCache, S3, CloudWatch Logs, Secrets Manager, ECR. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: S3 (metadata, spend export, CUR, ALB logs, archive) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 379 | 379 | Recurring / 継続 | Per month from GA. avg 60 GB × 0.025 + 100k PUT × 0.0047/1k + GET 0.40 = USD 2.37. 02 §7.1; metadata ~2 GB/month, batched writes (A18); 1 year hot then archive. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: CloudWatch Logs, alarms and metrics | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 4,634 | 4,634 | Recurring / 継続 | Per month from GA. 8.3 GB ingest × 0.76 + 50 GB stored × 0.033 + 60 alarms × 0.10 + 50 metrics × 0.30 = USD 28.96. 02 §7.1, §7.4: container INFO and WAF 1.5 KB per request each, VPC Flow 5 GB; 90 days hot; OBS-006 alarms. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Amazon Managed Service for Prometheus | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 3,368 | 3,368 | Recurring / 継続 | Per month from GA. 3k series × 30 s scrape = 263 M samples; (− 40 M free) × 0.90/10M + 1 storage = USD 21.05. 02 §2.2 metrics row; LiteLLM labels by team/key/model, ~3k series at 30 engineers (assumption). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Amazon Managed Grafana | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 19,200 | 19,200 | Recurring / 継続 | Per month from GA. 5 editors × 9 + 15 viewers × 5 = USD 120.00. 02 §2.2 (OBS-003); users: platform 5 editors; on-call, SOC, FinOps 15 viewers (assumption). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: ECR image storage | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 640 | 640 | Recurring / 継続 | Per month from GA. 40 GB × 0.10 = USD 4.00. 02 §2.2, SEC-016: pinned LiteLLM and guardrail images, ~10 versions kept. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Route 53 hosted zone and failover health check | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 240 | 240 | Recurring / 継続 | Per month from GA. 1 zone × 0.50 + 1 HTTPS option × 1.00 (AWS-endpoint checks within free 50; alias queries free) = USD 1.50. 02 §2.2 DNS row, §9 (R-8). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Chargeback: CUR 2.0, Athena, Quick Sight, Budgets | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 22,880 | 22,880 | Recurring / 継続 | Per month from GA. Athena 1 TB × 5 + 2 authors × 24 + 30 readers × 3 (CUR export and non-action Budgets free) = USD 143.00. 02 §2.2 billing row, §5 [CMP §4.5]; readers = FinOps + department contacts (assumption); Quick Sight prices: aws.amazon.com/quicksight/pricing (checked 2026-11-17). [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: GuardDuty incl. ECS runtime monitoring | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 8,403 | 8,403 | Recurring / 継続 | Per month from GA. 18 vCPU × 2 + 1 M CloudTrail events × 4.72/M + 10 GB flow/DNS × 1.18 = USD 52.52. 02 §2.2 threat detection, SEC-019. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Security Hub CSPM, AWS Config, Inspector (ECR) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 5,136 | 5,136 | Recurring / 継続 | Per month from GA. 10k checks × 0.001 + 3k CIs × 0.003 + 6k evals × 0.001 + 10 scans × 0.11 + 600 rescans × 0.01 = USD 32.10. 02 §2.2, §8.3 (RES-003 Config rule, SEC-016 scanning); CloudTrail org trail first copy free. [PL 2026-11-17] |
| Infrastructure / インフラ | Production Tokyo: Bedrock tokens for platform tests (gate re-runs, probe) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 12,000 | 12,000 | Recurring / 継続 | Per month from GA. ≈ USD 200 per full gate run × 1 run/quarter + probe on Haiku 5.5 (< USD 1) = USD 75.00. OPS-001, AVL-M01; platform's own usage, not charged back. [PL 2026-11-17] |
| Infrastructure / インフラ | DR Osaka: Fargate warm standby (1 gateway + 1 guardrail task) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 43,184 | 43,184 | Recurring / 継続 | Per month from GA. (1 × 2 vCPU/4 GB + 1 × 4 vCPU/8 GB) at Tokyo-equal Osaka rates × 730 h = USD 269.90. 02 §9 D-15 warm standby; scaled out on failover; Valkey rebuilt cold, not running (finding F-4). [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: Aurora Global Database secondary (db.r7g.large) + snapshot copy | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 42,274 | 42,274 | Recurring / 継続 | Per month from GA. 0.332/h × 730 h + 50 GB × 0.12 + 50 M replicated write I/O × 0.24/M + 30 GB Tokyo→Osaka × 0.09 + 50 GB snapshot × 0.023 = USD 264.21. 02 §7.1, §9, AVL-M03 [CMP §4.9]. [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: ALB (Osaka) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 3,773 | 3,773 | Recurring / 継続 | Per month from GA. 0.0243/h × 730 h + 1 LCU × 0.008/h × 730 h = USD 23.58. 02 §9 same allowlist on Osaka ALB. [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: AWS WAF web ACL (Osaka) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 2,720 | 2,720 | Recurring / 継続 | Per month from GA. 1 ACL × 5 + 12 rules × 1 = USD 17.00. 02 §9 same WAF rules. [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: Interface VPC endpoints (Osaka, 11 × 3 AZs) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 53,962 | 53,962 | Recurring / 継続 | Per month from GA. 11 × 3 AZs × 0.014/h × 730 h = USD 337.26. 02 §9 same IaC; could be 1 AZ in standby (saves ~USD 225). [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: Secrets/KMS replicas and ECR replication (Osaka) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 2,256 | 2,256 | Recurring / 継続 | Per month from GA. 8 replica secrets × 0.40 + 6 replica keys × 1 + 40 GB × 0.10 + 10 GB/month × 0.09 = USD 14.10. 02 §2.2 (secrets copy R-7, ECR replicated to Osaka). [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | DR Osaka: CloudWatch, GuardDuty, Security Hub, Config (Osaka) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 4,640 | 4,640 | Recurring / 継続 | Per month from GA. logs/alarms 5 + 6 vCPU × 2 + events 2 + CSPM/Config 10 = USD 29.00. 02 §2.2 threat detection in both regions. [PL 2026-11-17] (ap-northeast-3) |
| Infrastructure / インフラ | Dev environment after GA (Tokyo) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 80,298 | 80,298 | Recurring / 継続 | Per month. Same sizing as the project-period row: USD 501.86. Kept for maintenance (02 §10). [PL 2026-11-17] |
| Infrastructure / インフラ | Staging environment after GA (Tokyo) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 | 333,934 | 333,934 | Recurring / 継続 | Per month. Same sizing as the project-period row: USD 2,087.09. Needed for gate re-runs on every upgrade (OPS-001); scale-down between upgrades not assumed (finding F-6). [PL 2026-11-17] |
| **Subtotal 2-3** | **Infrastructure / インフラ** |  |  |  |  | **3,257,642** | One-time / 初期 |  |
| **Subtotal 2-3** | **Infrastructure / インフラ** |  |  |  |  | **963,892** | Recurring / 継続 | per month |
| Software licenses & tools / ライセンス・ツール | LiteLLM Enterprise licence (Admin UI SSO for all users, SCIM, audit logs) — PRICE NEEDED | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 1.0 |  | 0 | Recurring / 継続 | [CMP A-6]; 01 AS-6, CON-2, Q-17; 02 R-36. No public price: J left blank on purpose so the check flags it. Ask the vendor for a monthly-equivalent price incl. the project months (dev/staging SSO) |
| **Subtotal 2-4** | **Software licenses & tools / ライセンス・ツール** |  |  |  |  | **0** | Recurring / 継続 | per month |
| Security / セキュリティ | Security design review: threat model and residual-risk acceptance, R-48 parameters, guardrail failure mode, SCP review | Security specialist / セキュリティ | person-days / 人日 | 10.0 | 80,000 | 800,000 | One-time / 初期 | 02 §8, §8.1, R-11, R-48 |
| Security / セキュリティ | Third-party penetration test before launch | Vendor / non-labor / 外部・非人件費 | one-time / 一式 | 1.0 | 2,000,000 | 2,000,000 | One-time / 初期 | 02 §8.3 (R-48). Price = template sample value, placeholder until a vendor quote (Security) |
| **Subtotal 2-5** | **Security / セキュリティ** |  |  |  |  | **2,800,000** | One-time / 初期 |  |
| Contingency & risk buffer / 予備費 | Risk R-3: mTLS becomes required (V-11 fails or A-16 unconfirmed) — ALB mutual auth, trust store, CRL job, local mTLS helper per tool | Senior engineer / シニアエンジニア | person-months / 人月 | 0.75 | 1,100,000 | 825,000 | One-time / 初期 | 02 §14 R-3 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact 1.5 pm. 01 SEC-003, D-4 |
| Contingency & risk buffer / 予備費 | Risk R-3 (recurring part): AWS Private CA for workload certificates | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 0.5 | 64,000 | 32,000 | Recurring / 継続 | 02 §14 R-3 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact USD 400/month general-purpose CA [PL ACM PCA Tokyo, 2026-11-17] |
| Contingency & risk buffer / 予備費 | Risk R-7: Osaka egress path to Entra and licence endpoint, and secrets copy — design and build | Infra / DevOps engineer / インフラ | person-months / 人月 | 0.38 | 1,100,000 | 412,500 | One-time / 初期 | 02 §14 R-7 (likelihood High = 75 %). Expected value = impact × likelihood (A7). Impact 0.5 pm. 01 AVL-001, 02 §9 |
| Contingency & risk buffer / 予備費 | Risk R-7 (recurring part): Osaka egress (1 Network Firewall endpoint + 1 NAT gateway + TGW attachment) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 0.75 | 61,554 | 46,166 | Recurring / 継続 | 02 §14 R-7 (likelihood High = 75 %). Expected value = impact × likelihood (A7). Impact (0.395 + 0.062 + 0.07)/h × 730 h = USD 384.71/month [PL 2026-11-17] |
| Contingency & risk buffer / 予備費 | Risk R-32: office firewall allows only fixed IPs — AWS Global Accelerator in front of the ALB | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 0.5 | 3,720 | 1,860 | Recurring / 継続 | 02 §14 R-32 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact 0.025/h × 730 h + 500 GB in × 0.01 DT-premium = USD 23.25/month [PL Global Accelerator 2026-11-17]; build effort in the % buffer |
| Contingency & risk buffer / 予備費 | Risk R-1: spend-log table slows key lookups — partitioning or separate store | Senior engineer / シニアエンジニア | person-months / 人月 | 0.25 | 1,100,000 | 275,000 | One-time / 初期 | 02 §14 R-1 (likelihood Low = 25 %). Expected value = impact × likelihood (A7). Impact 1.0 pm; Low at 30 engineers (≈3.3 M rows / 90 days), Medium in 02 §14 at A-9 scale |
| Contingency & risk buffer / 予備費 | Risk R-10: Japanese classifier needs a GPU — SageMaker ml.g5.xlarge × 2 (2 AZs) in Tokyo | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 0.5 | 477,245 | 238,622 | Recurring / 継続 | 02 §14 R-10 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact 2 × 2.043/h × 730 h = USD 2,982.78/month [PL SageMaker Tokyo 2026-11-17]; CPU guardrail tasks would shrink (not netted) |
| Contingency & risk buffer / 予備費 | Risk R-12: per-team or per-department inference profiles with team-specific model names | Engineer / エンジニア | person-days / 人日 | 7.5 | 42,500 | 318,750 | One-time / 初期 | 02 §14 R-12 (likelihood High = 75 %). Expected value = impact × likelihood (A7). Impact 10 pd (config, CI, V-4/V-7 re-run) |
| Contingency & risk buffer / 予備費 | Risk R-6 / 01 Q-10: per-team content logging required this phase — separate store, Macie, V-1 re-run | Senior engineer / シニアエンジニア | person-months / 人月 | 0.5 | 1,100,000 | 550,000 | One-time / 初期 | 02 §14 R-6 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact 1.0 pm; whether it is needed is 01 Q-10, so Medium used instead of R-6's High |
| Contingency & risk buffer / 予備費 | Risk R-4: Codex CLI Responses API fails with non-OpenAI models — workaround | Engineer / エンジニア | person-days / 人日 | 5.0 | 42,500 | 212,500 | One-time / 初期 | 02 §14 R-4 (likelihood Medium = 50 %). Expected value = impact × likelihood (A7). Impact 10 pd |
| Contingency & risk buffer / 予備費 | Risk AS-18: shared egress in network-prod not available — gateway's own Network Firewall + NAT (3 AZs) | Vendor / non-labor / 外部・非人件費 | monthly fee / 月額 | 0.25 | 160,133 | 40,033 | Recurring / 継続 | 01 AS-18 (Low assumed = 25 %). Impact 3 × (0.395 + 0.062)/h × 730 h = USD 1,000.83/month [PL 2026-11-17]. Expected value = impact × likelihood (A7) |
| **Subtotal 2-6** | **Contingency & risk buffer / 予備費** |  |  |  |  | **2,593,750** | One-time / 初期 |  |
| **Subtotal 2-6** | **Contingency & risk buffer / 予備費** |  |  |  |  | **358,681** | Recurring / 継続 | per month |

## 3. Rates / 単価表

Working days per month / 月間稼働日数: **20** (1 person-month = 20 person-days = 160 h)

**OPEN ITEM (FinOps): there are no internal rates yet. These are the template's sample rates (indicative blended market rates, excl. tax), kept unchanged; replace them on the Rates sheet.**

| Role / 役割 | Monthly rate (JPY / person-month) | Daily rate (JPY / person-day) | Used in this estimate |
|---|---:|---:|---|
| Project manager / PM | 1,500,000 | 75,000 | - |
| Architect / tech lead / アーキテクト | 1,400,000 | 70,000 | 4 rows |
| Business analyst / SE / 業務SE | 1,200,000 | 60,000 | 1 rows |
| Senior engineer / シニアエンジニア | 1,100,000 | 55,000 | 12 rows |
| Engineer / エンジニア | 850,000 | 42,500 | 17 rows |
| UI/UX designer / デザイナー | 1,000,000 | 50,000 | - |
| QA / test engineer / テスト担当 | 800,000 | 40,000 | 6 rows |
| Infra / DevOps engineer / インフラ | 1,100,000 | 55,000 | 14 rows |
| Security specialist / セキュリティ | 1,600,000 | 80,000 | 3 rows |
| Tech writer / trainer / ライター・講師 | 700,000 | 35,000 | 2 rows |
| Operations engineer / 運用担当 | 750,000 | 37,500 | 2 rows |
| Help desk / ヘルプデスク | 550,000 | 27,500 | 1 rows |
| Vendor / non-labor / 外部・非人件費 |  |  | No rate: prices in column J |

## 4. Assumptions and exclusions / 前提条件・対象外事項

### A. Assumptions / 前提条件

| No. | Area / 区分 | Description (English) | 内容（日本語） |
|---|---|---|---|
| A1 | Scope / 範囲 | Build and 24-month operation of the Internal LLM gateway as designed in 01 and 02 v0.1 (Draft, 2026-11-17): LiteLLM Proxy on ECS Fargate in Tokyo with a warm standby in Osaka, the Bedrock catalog in 01 §6.5, Route B ingress only. | 01・02 v0.1（作成中、2026-11-17）で設計された社内LLMゲートウェイの構築と24か月の運用を対象とする。東京のECS Fargate上のLiteLLM Proxy、大阪のウォームスタンバイ、01 §6.5のBedrockモデル、Route B経路のみ。 |
| A2 | Schedule / スケジュール | Project 2027-01 to 2027-07 (7 months): M1 remaining requirements, design and approval; M2–M5 build; M4–M6 tests and launch gates; M6 production and DR build, penetration test; M7 pilot and DR drill. GA 2027-08. Recurring costs start at GA; operation period 24 months (2027-08 to 2029-07). Dates are open (01 Q-3). | プロジェクト期間 2027年1月〜7月（7か月）：1か月目 残りの要件・設計・承認、2〜5か月目 構築、4〜6か月目 テスト・ローンチゲート、6か月目 本番・DR構築とペネトレーションテスト、7か月目 パイロットとDR訓練。2027年8月GA。継続費用はGAから発生し、運用期間は24か月（2027年8月〜2029年7月）。日程は未確定（01 Q-3）。 |
| A3 | Effort unit / 工数単位 | 1 person-month = 20 person-days = 160 hours (Rates sheet). Rates are blended and exclude tax. | 1人月＝20人日＝160時間（Ratesシート）。単価は平均単価・税抜。 |
| A4 | Rates / 単価 | OPEN ITEM (FinOps): no internal rates exist yet. The template's sample rates (indicative FY2026 market rates) are kept unchanged and are not quotes. Replace them on the Rates sheet; every labor row updates. | 【未決事項・FinOps】社内単価が未設定のため、テンプレートのサンプル単価（2026年度の参考相場）をそのまま使用しており、見積回答ではない。Ratesシートで置き換えると全工数行が更新される。 |
| A5 | Recurring costs / 継続費用 | Recurring lines are monthly amounts; annual = monthly x 12. The grand total includes 24 recurring months (the operation period). The markdown output also gives 12- and 36-month views. | 継続費用は月額で計上し、年額＝月額×12。総額には運用期間の24か月分の継続費用を含む。Markdown出力には12か月・36か月の試算も記載。 |
| A6 | Project management / PM費 | Project management = PM % (10 %, template default) x development cost (one-time phase-based costs). PM effort is not included in phase rows. | PM費＝PM費率（10%、テンプレート既定値）×開発費（工程別の初期費用）。工程別の行にはPM工数を含めない。 |
| A7 | Contingency / 予備費 | Contingency = 15 % (template default) of initial cost excluding contingency, plus 15 % of monthly recurring cost. Identified risks from 02 §14 are line items at expected value = impact x likelihood (Low 25 %, Medium 50 %, High 75 %). Tax is never included in the base. | 予備費＝予備費を除く初期費用×15%（既定値）＋継続月額×15%。02 §14の特定済みリスクは期待値（影響額×発生確率：低25%、中50%、高75%）で明細計上。消費税は算定基礎に含めない。 |
| A8 | Tax / 消費税 | Consumption tax is calculated once on each total at the rate on Summary; amounts below JPY 1 are rounded down. | 消費税はSummaryの税率で各合計に対して1回計算し、1円未満は切り捨て。 |
| A9 | Cloud / クラウド | AWS On-Demand list prices from the AWS Price List API offer files for ap-northeast-1 and ap-northeast-3 (publication 2026-11-17, checked 2026-11-17), cited as [PL]; 730 h per month; no Savings Plans, reserved or EDP discounts. Budget exchange rate JPY 160 / USD (market about 158–160 in mid-November 2026). OPEN ITEM (FinOps): confirm the budget rate. | AWSの価格はAWS Price List API（ap-northeast-1／ap-northeast-3、2026-11-17公開版、2026-11-17確認）のオンデマンド定価（[PL]と表記）。1か月730時間、Savings Plans・リザーブド・EDP割引は考慮しない。予算レートは1USD＝160円（2026年11月中旬の市場水準は約158〜160円）。【未決事項・FinOps】予算レートの確認。 |
| A10 | Environments / 環境 | Four environments (02 §10, 03 §2): dev (minimal, Tokyo), staging (production topology at minimum scale, Tokyo), production (Tokyo, 3 AZs) and DR (Osaka, warm standby). Dev and staging remain after GA; staging is needed to re-run launch gates on every LiteLLM upgrade (OPS-001). Accounts are open (R-41). | 開発（最小構成・東京）、ステージング（本番と同構成・最小規模・東京）、本番（東京・3AZ）、DR（大阪・ウォームスタンバイ）の4環境（02 §10、03 §2）。開発・ステージングはGA後も維持し、ステージングはLiteLLM更新ごとのローンチゲート再実行に使う（OPS-001）。アカウント構成は未定（R-41）。 |
| A11 | Sizing / サイジング | Fixed capacity is the design minimum (02 §9): gateway 3 Fargate tasks of 2 vCPU / 4 GB and guardrail 3 tasks of 4 vCPU / 8 GB on CPU, one per AZ; Aurora db.r7g.large writer + reader; Valkey cache.m7g.large x 2. Per-request charges use the expected usage scenario: about 1.1 million requests per month (30 engineers plus workloads), 120 KB request and 20 KB response on average. Sizing is open (R-42, R-23, R-10). | 固定容量は設計上の最小構成（02 §9）：ゲートウェイはFargate 3タスク（2vCPU/4GB）、ガードレールは3タスク（4vCPU/8GB、CPU推論）でAZごとに1つ、Aurora db.r7g.large（ライター＋リーダー）、Valkey cache.m7g.large×2。従量部分は想定利用シナリオ（エンジニア30人とワークロードで月約110万リクエスト、平均リクエスト120KB・レスポンス20KB）による。サイジングは未確定（R-42、R-23、R-10）。 |
| A12 | Users / 利用者 | 30 engineers use the gateway with coding agents (set by the requester on 2026-11-17, for now). CMP A-9 (about 5,000 employees, about 300 concurrent users) is not used for sizing. Workload volume (UC-2) is as in the markdown usage table. | コーディングエージェントでゲートウェイを利用するエンジニアは30人（2026-11-17に依頼者が当面の値として設定）。CMP A-9（従業員約5,000人、同時約300人）はサイジングに使わない。ワークロード（UC-2）の利用量はMarkdownの利用試算表のとおり。 |
| A13 | Shared network / 共有ネットワーク | AS-18 holds: the shared network-prod account provides Transit Gateway, Network Firewall and NAT. Their endpoint-hours are not charged to this project; the gateway pays its TGW attachments and per-GB charges. Dev and staging use the same path. If AS-18 is false, see the contingency row. | AS-18が成立し、共有アカウントnetwork-prodのTransit Gateway・Network Firewall・NATを利用する前提。それらの時間課金は本案件に計上せず、TGWアタッチメントとGB課金のみ計上。開発・ステージングも同経路。不成立の場合は予備費の行を参照。 |
| A14 | Model usage / モデル利用料 | Bedrock token charges for teams are not in the totals: LiteLLM charges them back to teams (01 CST-007). The markdown output gives a separate low / expected / high usage table. Bedrock tokens used by the platform team itself (development, tests, gates, probe) are included. | チームのBedrockトークン料金は合計に含めない（LiteLLMでチームに配賦、01 CST-007）。Markdown出力に低・想定・高の利用試算を別表で記載。基盤チーム自身の利用（開発・テスト・ゲート・監視プローブ）は計上する。 |
| A15 | Licences / ライセンス | OPEN ITEM (Product owner): the LiteLLM Enterprise licence price is unknown (01 Q-17). It is a placeholder row with no price, so the check 'Rows with quantity but no amount' shows 1 on purpose. Presidio and the guardrail classifier are assumed to be open source with no licence fee. | 【未決事項・プロダクトオーナー】LiteLLM Enterpriseライセンス価格は未確定（01 Q-17）。単価未入力の仮行としており、チェック「単価未設定の行数」が意図的に1となる。Presidioとガードレール分類器はオープンソース（ライセンス費なし）を前提とする。 |
| A16 | Delivery team / 実施体制 | Platform engineering does all build and run work estimated here, using the template roles. Penetration test is by a third party; its price is the template sample value until a vendor quote (OPEN ITEM, Security). | 本見積の構築・運用作業はプラットフォームエンジニアリングがテンプレートの役割で実施する。ペネトレーションテストは外部委託で、ベンダー見積までテンプレートのサンプル価格を使用（【未決事項・セキュリティ】）。 |
| A17 | Data migration / データ移行 | No data migration: 01 and 02 define none, and what the gateway replaces is still open (01 Q-2). | データ移行なし：01・02に定義がなく、置き換え対象も未確定（01 Q-2）。 |
| A18 | Support hours / サポート時間 | On-call covers business hours (01 OPS-006, Q-6 open). 24x7 on-call would increase the Operation rows. | オンコールは業務時間帯を前提（01 OPS-006、Q-6未確定）。24時間365日対応の場合、運用の行が増える。 |
| A19 | Logging volume / ログ量 | The LiteLLM S3 metadata callback writes in batches (about 100 records per object). If it writes one object per request, PUT and archive-transition charges rise by roughly USD 250 per month from month 13 (to be checked on the pinned version). | LiteLLMのS3メタデータ出力はバッチ書き込み（1オブジェクト約100件）を前提。1リクエスト1オブジェクトの場合、PUTとアーカイブ移行の料金が13か月目以降に月約250USD増える（固定バージョンで要確認）。 |

### B. Exclusions (not covered by this estimate) / 対象外事項

| No. | Area / 区分 | Description (English) | 内容（日本語） |
|---|---|---|---|
| B1 | Model inference / モデル利用料 | Bedrock token charges for teams' usage (charged back through LiteLLM, 01 CST-007). See the separate usage table in the markdown output. | 各チームの利用によるBedrockトークン料金（LiteLLMで配賦、01 CST-007）。Markdown出力の別表を参照。 |
| B2 | Route A / 専用線経路 | Private-line ingress over Direct Connect (01 NG-5, 02 D-6). Optional; priced separately in the markdown output. | Direct Connect経由の専用線経路（01 NG-5、02 D-6）。オプション扱いで、Markdown出力に別途試算を記載。 |
| B3 | Azure OpenAI / Azure OpenAI | Azure OpenAI Japan East as a second backend, with its cross-cloud private path and Azure charges (01 MDL-011, Q-4). Optional; priced separately in the markdown output. | 第2バックエンドとしてのAzure OpenAI（東日本）、クラウド間の閉域経路およびAzure側料金（01 MDL-011、Q-4）。オプション扱いで、Markdown出力に別途試算を記載。 |
| B4 | Remote access, mTLS client side / リモート・mTLS端末側 | Remote and home access (01 NG-1) and Intune certificate profiles for mTLS; only the gateway-side mTLS risk is in contingency. | リモート・在宅アクセス（01 NG-1）およびmTLS用のIntune証明書配布。ゲートウェイ側のmTLS対応のみ予備費に計上。 |
| B5 | Internal staff / 社内要員 | Time of other internal teams for their own deliverables: Network (allowlist, egress, V-11 data), Identity (Conditional Access, app registrations), Endpoint/Intune (client deployment), Legal/privacy and FinOps approvals, users attending training. | 他部門の要員工数：ネットワーク（許可リスト・出口経路・V-11の情報）、ID管理（条件付きアクセス・アプリ登録）、端末/Intune（クライアント配布）、法務・FinOpsの承認、研修受講者。 |
| B6 | Shared platforms / 共有基盤 | Costs of shared platforms already paid elsewhere: network-prod firewall and NAT endpoint-hours, Direct Connect circuits, SIEM licence and ingestion (02 R-48), log-archive account, corporate Git/CI, Entra ID P1/P2, Okta and Intune licences. | 他で負担済みの共有基盤費用：network-prodのファイアウォール・NATの時間課金、Direct Connect回線、SIEMのライセンスと取り込み（02 R-48）、ログアーカイブアカウント、社内Git/CI、Entra ID P1/P2・Okta・Intuneのライセンス。 |
| B7 | Support contracts / サポート契約 | AWS Support plan and any LiteLLM support beyond the licence (01 Q-20). | AWSサポートプランおよびライセンス外のLiteLLMサポート（01 Q-20）。 |
| B8 | Enhancements / 機能追加 | New endpoint families (01 NG-7, e.g. MCP gateway), self-hosted models on SageMaker, response caching (NG-3), and features beyond the maintenance allowance. | 新しいエンドポイント種別（01 NG-7、MCPゲートウェイ等）、SageMakerでのセルフホストモデル、レスポンスキャッシュ（NG-3）、保守範囲を超える機能追加。 |
| B9 | Expenses / 経費 | Travel, accommodation and on-site expenses. | 出張・宿泊・現地作業に伴う経費。 |
| B10 | Unlisted purchases / 記載外の購入 | Hardware or software not listed on the Estimate sheet; end-user devices and office network changes. | Estimateシートに記載のないハードウェア・ソフトウェア、利用者端末および社内ネットワークの変更。 |
| B11 | Price changes / 価格変動 | Exchange-rate movements beyond JPY 160 / USD and AWS or vendor price changes after 2026-11-17. | 1USD＝160円を超える為替変動、および2026-11-17以降のAWS・ベンダーの価格改定。 |
| B12 | Legal & audit / 法務・監査 | Legal, regulatory or external audit fees, incl. any ISO 27001 / SOC 2 work (01 Q-19). | 法務・規制対応・外部監査の費用（ISO 27001／SOC 2対応を含む、01 Q-19）。 |
| B13 | Decommissioning / 旧システム廃止 | Decommissioning of anything the gateway replaces (01 Q-2 open). | ゲートウェイが置き換えるものの廃止作業（01 Q-2未確定）。 |

## 5. Lists / プルダウン用リスト

Unchanged from the template: units person-months / person-days / monthly fee / one-time; types One-time / Recurring; the 10 phase-based and 6 cross-cutting categories in the breakdown above.

## 6. Calculation rules / 計算ルール

| Item | Rule |
|---|---|
| Unit cost / 単価 | Override (column J) if entered, else role rate from Rates (monthly for person-months, daily for person-days) |
| Subtotal / 小計 | Quantity × Unit cost |
| Development cost / 開発費 | Sum of one-time costs in phase-based categories |
| Project management / PM費 | PM % × development cost |
| Contingency / 予備費 | Contingency % × initial cost before contingency, + contingency % × monthly recurring cost; plus identified-risk line items |
| Total initial cost / 初期費用 | All one-time costs (phase-based + cross-cutting, incl. PM and contingency) |
| Recurring – monthly / 継続月額 | Sum of recurring rows (+ recurring contingency) |
| Grand total / 総額 | Initial cost + monthly recurring × 24 months |
| Consumption tax / 消費税 | Each total × tax rate, calculated once per total, rounded down to JPY 1 |

## 7. Model usage (Bedrock tokens) — not in the totals

Model inference is a variable cost that LiteLLM charges back to the teams that use it (01 CST-007, 02 §5), so it is an exclusion (B1) and not part of the totals above. This table sizes it for budgeting by the teams and FinOps. Prices are the Bedrock on-demand prices for the `jp.` geographic cross-Region profiles (the non-global 'Standard' SKUs, about 10 % above Global) and the In-Region Tokyo prices, from [PL] AmazonBedrock and AmazonBedrockFoundationModels, ap-northeast-1, checked 2026-11-17.

### 7.1 Prices used (USD per 1 million tokens)

| Catalog ID | Model | How processed in Japan (01 §6.5) | Input | Cache write | Cache read | Output |
|---|---|---|---:|---:|---:|---:|
| MDL-001 | Claude Opus 5.5 | `jp.` profile | 4.4 | 5.5 | 0.22 | 22 |
| MDL-002 | Claude Haiku 5.5 | `jp.` profile | 0.11 | 0.1375 | 0.011 | 0.55 |
| MDL-003 | Claude Opus 4.8 | `jp.` profile | 5.5 | 6.875 | 0.55 | 27.5 |
| MDL-004 | Claude Sonnet 4.6 | `jp.` profile | 3.3 | 4.125 | 0.33 | 16.5 |
| MDL-005 | Claude Haiku 4.5 | `jp.` profile | 1.1 | 1.375 | 0.11 | 5.5 |
| MDL-006 | Amazon Nova 2 Lite | `jp.` profile | 0.396 | - | 0.099 | 3.311 |
| MDL-007 | Titan Text Embeddings V2 | In-Region Tokyo | 0.029 | - | - | - |
| MDL-008 | Cohere Embed v4 | In-Region Tokyo | 0.12 | - | - | - |
| MDL-009 | Mistral Large 3 | In-Region Tokyo | 0.61 | - | - | 1.82 |
| MDL-010 | gpt-oss-120b | In-Region Tokyo | 0.18 | - | - | 0.73 |

Note: [PL] lists Claude Haiku 5.5 at USD 0.11 / 0.55 per million input / output tokens, below Claude Haiku 4.5 (USD 1.10 / 5.50). The estimate uses the listed price; re-check it before the budget is fixed. MDL-011 (Azure OpenAI) is not priced (B3).

### 7.2 Scenario assumptions

| Driver | Low | Expected | High | Basis |
|---|---:|---:|---:|---|
| Active coding-agent users per month | 30 | 30 | 30 | 30 engineers, set by the requester on 2026-11-17 (A12); scenarios vary active days and workload volume only |
| Active days per user per month | 12 | 15 | 19 | Claude Code cost docs (code.claude.com/docs/en/costs, checked 2026-11-17): enterprise average ≈ USD 13 per developer per active day and USD 150–250 per month → 12–19 active days |
| Tokens per active user-day (M): input / cache write / cache read / output | 0.6 / 0.4 / 12 / 0.25 | 0.6 / 0.4 / 12 / 0.25 | 0.6 / 0.4 / 12 / 0.25 | Calibrated so a full day on Claude Opus 5.5 at `jp.` prices costs ≈ USD 13 (USD 12.98) |
| Model mix for coding agents |  | Opus 5.5 60 %, Haiku 5.5 20 %, Sonnet 4.6 15 %, Opus 4.8 5 % |  | Assumption; 01 §6.5 UC-1 models (Q-4 open) |
| Workloads (UC-2), share of expected volume | 25 % | 100 % | 300 % | Expected per month: Haiku 4.5 1.0 B in / 0.2 B out; Nova 2 Lite 1.0 / 0.2; gpt-oss-120b 0.3 / 0.06; Mistral Large 3 0.2 / 0.04; Titan V2 and Cohere v4 embeddings 0.5 B each (assumption; 01 Q-4, Q-7) |

### 7.3 Monthly usage and cost by model

| Catalog ID | Model | Tokens/month Low (B) | Expected (B) | High (B) | JPY/month Low | Expected | High |
|---|---|---:|---:|---:|---:|---:|---:|
| MDL-001 | Claude Opus 5.5 | 2.9 | 3.6 | 4.5 | 448,589 | 560,736 | 710,266 |
| MDL-002 | Claude Haiku 5.5 | 1.0 | 1.2 | 1.5 | 4,499 | 5,623 | 7,123 |
| MDL-003 | Claude Opus 4.8 | 0.2 | 0.3 | 0.4 | 56,232 | 70,290 | 89,034 |
| MDL-004 | Claude Sonnet 4.6 | 0.7 | 0.9 | 1.1 | 101,218 | 126,522 | 160,261 |
| MDL-005 | Claude Haiku 4.5 | 0.3 | 1.2 | 3.6 | 88,000 | 352,000 | 1,056,000 |
| MDL-006 | Amazon Nova 2 Lite | 0.3 | 1.2 | 3.6 | 42,328 | 169,312 | 507,936 |
| MDL-007 | Titan Text Embeddings V2 | 0.1 | 0.5 | 1.5 | 580 | 2,320 | 6,960 |
| MDL-008 | Cohere Embed v4 | 0.1 | 0.5 | 1.5 | 2,400 | 9,600 | 28,800 |
| MDL-009 | Mistral Large 3 | 0.1 | 0.2 | 0.7 | 7,792 | 31,168 | 93,504 |
| MDL-010 | gpt-oss-120b | 0.1 | 0.4 | 1.1 | 3,912 | 15,648 | 46,944 |
|  | **Total** | **5.8** | **10.0** | **19.6** | **755,549** | **1,343,219** | **2,706,828** |
|  | Total per year (× 12) |  |  |  | 9,066,588 | 16,118,630 | 32,481,930 |
|  | Total over the 24-month operation period |  |  |  | 18,133,175 | 32,237,261 | 64,963,860 |

Tokens include cache reads, which are most of the coding-agent volume. Excl. tax. At the expected scenario, model usage is about 0× the gateway's own monthly running cost, which matches CMP §7.1 ('model usage dominates').

## 8. Optional items priced separately (not in the totals)

Route A and the Azure OpenAI backend are optional in the design (01 NG-5, MDL-011; 02 D-6) and are exclusions B2 and B3. Indicative AWS-side costs, using the traffic basis of CMP §8.9 (about 1 TiB a month each way) and [PL] Tokyo rates:

| Option | Monthly AWS cost (USD) | Monthly (JPY) | One-time build | Not included |
|---|---:|---:|---|---|
| Route A: Direct Connect ingress with internal ALB and split-horizon DNS | DX data out 1,024 GB × 0.041 42.0; TGW processing 2,048 GB × 0.02 41.0; Internal ALB 0.0243/h + 1 LCU 23.6; Route 53 Resolver inbound endpoint, 2 ENIs × 0.125/h 182.5 = **289** | 46,244 | 15 pd Infra/DevOps ≈ JPY 825,000 | DX ports and circuits (sunk, A-8), carrier and colocation fees, Network team time |
| Azure OpenAI Japan East over DX + ExpressRoute | DX data out for prompts 1,024 GB × 0.041 42.0; TGW processing 1,024 GB × 0.02 20.5 = **62** | 9,994 | 20 pd Senior engineer ≈ JPY 1,100,000 | All Azure charges (tokens, private endpoint, ExpressRoute), colocation router [CMP §8.9], legal approval (REG-001) |

CMP §8.9 estimated Route A at about USD 120 a month with the US-East example TGW attachment; the gateway VPC is already attached to the TGW for egress (02 §6), so no extra attachment is counted here, and the Route 53 Resolver inbound endpoint (CMP §4.6) is added.

## 9. Infrastructure sizing detail

Monthly AWS cost per environment in USD, before conversion. Production and DR are one row per component in §2; dev and staging are one row each in §2 with this breakdown.

| Environment | Component | USD / month |
|---|---|---:|
| Production (Tokyo) | Fargate: LiteLLM gateway tasks | 269.90 |
| Production (Tokyo) | Fargate: in-VPC guardrail service (Presidio + classifier, CPU) | 539.79 |
| Production (Tokyo) | Aurora PostgreSQL (writer + reader, db.r7g.large, Multi-AZ) | 500.53 |
| Production (Tokyo) | ElastiCache Valkey (2 × cache.m7g.large, Multi-AZ) | 235.94 |
| Production (Tokyo) | Application Load Balancer (internet-facing) | 29.42 |
| Production (Tokyo) | AWS WAF regional web ACL | 17.65 |
| Production (Tokyo) | Interface VPC endpoints (11 × 3 AZs) | 338.94 |
| Production (Tokyo) | Transit Gateway VPC attachment (egress path) | 51.20 |
| Production (Tokyo) | Network Firewall (network-prod): incremental GB only | 0.33 |
| Production (Tokyo) | NAT gateway (network-prod): incremental GB only | 0.31 |
| Production (Tokyo) | Data transfer out to office/DC clients (responses) | 3.11 |
| Production (Tokyo) | Secrets Manager | 3.70 |
| Production (Tokyo) | KMS customer-managed keys | 9.00 |
| Production (Tokyo) | S3 (metadata, spend export, CUR, ALB logs, archive) | 2.37 |
| Production (Tokyo) | CloudWatch Logs, alarms and metrics | 28.96 |
| Production (Tokyo) | Amazon Managed Service for Prometheus | 21.05 |
| Production (Tokyo) | Amazon Managed Grafana | 120.00 |
| Production (Tokyo) | ECR image storage | 4.00 |
| Production (Tokyo) | Route 53 hosted zone and failover health check | 1.50 |
| Production (Tokyo) | Chargeback: CUR 2.0, Athena, Quick Sight, Budgets | 143.00 |
| Production (Tokyo) | GuardDuty incl. ECS runtime monitoring | 52.52 |
| Production (Tokyo) | Security Hub CSPM, AWS Config, Inspector (ECR) | 32.10 |
| Production (Tokyo) | Bedrock tokens for platform tests (gate re-runs, probe) | 75.00 |
| **Production (Tokyo)** | **Total** | **2,480.32** |
| DR (Osaka) | Fargate warm standby (1 gateway + 1 guardrail task) | 269.90 |
| DR (Osaka) | Aurora Global Database secondary (db.r7g.large) + snapshot copy | 264.21 |
| DR (Osaka) | ALB (Osaka) | 23.58 |
| DR (Osaka) | AWS WAF web ACL (Osaka) | 17.00 |
| DR (Osaka) | Interface VPC endpoints (Osaka, 11 × 3 AZs) | 337.26 |
| DR (Osaka) | Secrets/KMS replicas and ECR replication (Osaka) | 14.10 |
| DR (Osaka) | CloudWatch, GuardDuty, Security Hub, Config (Osaka) | 29.00 |
| **DR (Osaka)** | **Total** | **955.05** |
| Dev (Tokyo) | Fargate 1 gateway (1 vCPU/2 GB) + 1 guardrail (2 vCPU/4 GB) | 134.95 |
| Dev (Tokyo) | Aurora db.t4g.medium single instance + 10 GB + I/O | 88.69 |
| Dev (Tokyo) | Valkey cache.t4g.small single node | 28.62 |
| Dev (Tokyo) | ALB + 1 LCU; WAF ACL + 12 rules | 40.58 |
| Dev (Tokyo) | 11 interface endpoints × 1 AZ | 112.42 |
| Dev (Tokyo) | TGW attachment (egress to Entra for SSO) | 51.10 |
| Dev (Tokyo) | CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone | 29.50 |
| Dev (Tokyo) | GuardDuty, Security Hub, Config | 16.00 |
| **Dev (Tokyo)** | **Total** | **501.86** |
| Staging (Tokyo) | Fargate 3 gateway (2 vCPU/4 GB) + 3 guardrail (4 vCPU/8 GB) | 809.69 |
| Staging (Tokyo) | Aurora writer + reader db.r7g.large + storage/I/O | 496.18 |
| Staging (Tokyo) | Valkey 2 × cache.m7g.large | 235.94 |
| Staging (Tokyo) | ALB + 2 LCU; WAF ACL + 12 rules | 46.42 |
| Staging (Tokyo) | 11 interface endpoints × 3 AZs | 337.26 |
| Staging (Tokyo) | TGW attachment | 51.10 |
| Staging (Tokyo) | CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone | 50.50 |
| Staging (Tokyo) | GuardDuty (18 vCPU), Security Hub, Config | 60.00 |
| **Staging (Tokyo)** | **Total** | **2,087.09** |

Comparison with 02 §12: the comparison's sample baseline of about USD 380 a month [CMP §7.1] covers one small environment before hardening. This design adds 3-AZ production, the guardrail service, 11 interface endpoints per AZ, the Osaka standby, observability and threat detection, and keeps staging at production topology; production alone is about USD 2,480 a month.

## 10. Open items that need a price or a decision, by owner

| Owner | Item | Where it is in the estimate | Due (from 01/02) |
|---|---|---|---|
| Product owner | LiteLLM Enterprise licence price, incl. project months (01 Q-17) — the deliberate check failure | Licences row (J blank) | 2026-12-18 |
| Product owner | Pilot and GA dates (01 Q-3); they set the project-period environment months | A2, Infrastructure one-time rows | 2026-12-18 |
| Product owner | Model list, usage forecast and growth (01 Q-4, Q-7) for the model-usage budget | §7 | 2026-12-18 |
| Product owner | AWS Support plan and LiteLLM support contract (01 Q-20) | Exclusion B7 | 2027-01-29 |
| Product owner | Support hours, DR drill interval (01 Q-6) | Operation rows (A17) | 2026-12-18 |
| FinOps | Internal labor rates to replace the template sample rates | Rates sheet, all labor rows (A4) | — |
| FinOps | Budget exchange rate (JPY 160/USD assumed) | A9, all AWS rows | — |
| FinOps | Quick Sight reader and Grafana viewer counts; allocation of fixed platform cost (01 Q-12) | Chargeback and Grafana rows | 2026-12-18 |
| Security / SOC | Penetration-test vendor quote (template sample JPY 2,000,000 used) | Security row | 2027-01-29 |
| Security / SOC | Guardrail classifier choice and whether it needs a GPU (R-10, Q-13) | Guardrail Fargate row, contingency R-10 | 2026-12-18 |
| Security / SOC | SIEM ingestion path and its cost (R-48) | Exclusion B6 | 2027-01-29 |
| Network | Osaka egress design (R-7) and whether a fixed-IP front end is needed (R-32, Q-14) | Contingency R-7, R-32 | 2027-01-29 |
| Network | Confirm the shared network-prod egress can serve the gateway (AS-18) | A12, contingency AS-18 | 2026-12-18 |
| Platform engineering | Task sizing (R-42), Aurora and Valkey choices (R-23), staging scale-down policy (R-41) | Infrastructure rows (A11) | 2027-01-29 |
| Platform engineering | LiteLLM S3 callback batching on the pinned version (A18) | S3 row | 2027-01-29 |
| Legal / privacy | Whether per-team content logging is needed this phase (01 Q-10) | Contingency R-6 | 2026-12-18 |

## 11. Findings for the design documents (not edited)

docs/en/ was not changed. These are gaps or inconsistencies found while pricing the design; each should be resolved in 01/02 by its owner.

| ID | Finding | Owner |
|---|---|---|
| F-1 | 02 §6 lists 10 interface endpoints and allows egress only to Entra and the licence endpoint, but 02 §2.2 sends LiteLLM metrics to Amazon Managed Service for Prometheus. Remote write from private subnets needs an `aps-workspaces` endpoint (or an egress rule). The estimate prices 11 endpoints (matching 02 §12 'about 11'). | Platform engineering |
| F-2 | CMP A-9 / 01 PRF-M02 use 50–200 RPS as the sizing basis. Sustained 50 RPS is about 130 million requests a month; at the per-request token volume of a coding agent (≈ 66k tokens) that would be model spend of several million USD a month, far above the forecast in §7 (≈ 1.1 million requests with 30 engineers). PRF-M02 should be set from a usage forecast (01 Q-7). This estimate uses the design minimum for fixed capacity and the forecast for per-request charges. | Product owner |
| F-3 | 02 §12 says no price was re-checked and R-46 lists the unestimated items. This estimate prices them; R-46 can point to it once reviewed. | Platform engineering |
| F-4 | 02 §2.2 and §9 say ElastiCache is 'rebuilt cold' in Osaka without saying whether the cluster is created at failover or kept running. It affects RTO (AVL-M02) and cost; the estimate assumes it is created at failover. | Platform engineering |
| F-5 | Osaka egress and the Osaka secrets copy (R-7) have no design, so they are priced only as a contingency row. | Network |
| F-6 | 02 §10 requires staging to match production for valid launch gates. Kept at production topology, staging costs about USD 2,090 a month, close to production. The design should say whether staging may scale down between upgrade windows (R-41). | Platform engineering |
| F-7 | Dev and staging also need an egress path to Entra for SSO; 02 §6 designs it only for production. The estimate assumes the same network-prod path (TGW attachment per environment). | Network |
| F-8 | 02 §7.1 moves request metadata to Glacier after one year. If the LiteLLM S3 callback writes one object per request, per-object PUT and transition charges dominate the bucket cost; batching should be part of the design (A18). | Platform engineering |
| F-9 | Grafana and Quick Sight user counts, and who the team-facing dashboards are for (Grafana or the LiteLLM UI), are not in the design; both are per-user licences. | FinOps |
