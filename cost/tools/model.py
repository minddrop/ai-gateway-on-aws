"""Cost model for the Internal LLM gateway estimate (v0.1).

Single source of the numbers that go into the workbook and the markdown.
Prices: AWS Price List API offer files for ap-northeast-1 / ap-northeast-3
(publication 2026-11-17, checked 2026-11-17), cited as [PL].
"""
import math

CHECKED = "2026-11-17"
FX = 160            # JPY per USD, budget rate (assumption A9)
H = 730             # hours per month
PL = f"[PL {CHECKED}]"

# ---------------------------------------------------------------- template
CAT = {
    "req": "Requirements definition / 要件定義",
    "des": "Basic & detailed design / 基本・詳細設計",
    "imp": "Implementation / 実装",
    "tst": "Testing (unit, integration, system, UAT) / テスト",
    "mig": "Data migration / データ移行",
    "set": "Setup, build & deployment / 構築・リリース",
    "trn": "Training & documentation / 教育・ドキュメント",
    "cut": "Cutover & go-live support / 本番移行・稼働支援",
    "ops": "Operation / 運用",
    "mnt": "Maintenance / 保守",
    "pm":  "Project management / プロジェクト管理",
    "qa":  "Quality assurance & reviews / 品質保証",
    "inf": "Infrastructure / インフラ",
    "lic": "Software licenses & tools / ライセンス・ツール",
    "sec": "Security / セキュリティ",
    "con": "Contingency & risk buffer / 予備費",
}
CAT_ORDER = list(CAT)
PHASE = CAT_ORDER[:10]

R_PM, R_ARCH, R_BA, R_SR, R_ENG, R_UX, R_QA, R_INF, R_SEC, R_TW, R_OPS, R_HD, R_VEN = (
    "Project manager / PM", "Architect / tech lead / アーキテクト", "Business analyst / SE / 業務SE",
    "Senior engineer / シニアエンジニア", "Engineer / エンジニア", "UI/UX designer / デザイナー",
    "QA / test engineer / テスト担当", "Infra / DevOps engineer / インフラ",
    "Security specialist / セキュリティ", "Tech writer / trainer / ライター・講師",
    "Operations engineer / 運用担当", "Help desk / ヘルプデスク", "Vendor / non-labor / 外部・非人件費")
RATES = {R_PM: 1500000, R_ARCH: 1400000, R_BA: 1200000, R_SR: 1100000, R_ENG: 850000,
         R_UX: 1000000, R_QA: 800000, R_INF: 1100000, R_SEC: 1600000, R_TW: 700000,
         R_OPS: 750000, R_HD: 550000}
DAYS = 20
U_PM, U_PD, U_MF, U_OT = "person-months / 人月", "person-days / 人日", "monthly fee / 月額", "one-time / 一式"
T_OT, T_RC = "One-time / 初期", "Recurring / 継続"

# ---------------------------------------------------------------- schedule
PROJECT = "2027-01 to 2027-07 (7 months)"
MONTHS_DEV, MONTHS_STG, MONTHS_PRE_GA = 6, 4, 2
OPS_MONTHS = 24

# ---------------------------------------------------------------- prices [PL]
P = dict(
    fg_cpu=0.05056, fg_gb=0.00553,                     # Fargate x86 Linux, Tokyo = Osaka
    aur_r7gl_t=0.333, aur_r7gl_o=0.332, aur_t4gm=0.113,  # Aurora PostgreSQL instance-hour
    aur_gb=0.12, aur_io=0.24, aur_bkp=0.023, aur_repl_io=0.24,
    vk_m7gl_t=0.1616, vk_t4gs=0.0392,                  # ElastiCache Valkey node-hour
    alb_h=0.0243, alb_lcu=0.008,
    waf_acl=5.0, waf_rule=1.0, waf_req=0.60,           # per month / per rule / per million
    vpce_h=0.014, vpce_gb=0.01,
    tgw_h=0.07, tgw_gb=0.02,
    nfw_h=0.395, nfw_gb=0.065, nat_h=0.062, nat_gb=0.062,
    dto_gb=0.114, xreg_gb=0.09,
    sm_secret=0.40, sm_api=0.05,                       # per 10k calls
    kms_key=1.0, kms_req=0.03,                         # per 10k requests
    s3_gb=0.025, s3_put=0.0047,                        # per 1k PUT
    cw_ingest=0.76, cw_store=0.033, cw_alarm=0.10, cw_metric=0.30,
    amp_10m=0.90, graf_ed=9.0, graf_vw=5.0,
    ecr_gb=0.10, insp_init=0.11, insp_rescan=0.01,
    gd_vcpu=2.0, gd_ct_m=4.72, gd_log_gb=1.18,
    shub_check=0.001, cfg_ci=0.003, cfg_eval=0.001,
    r53_zone=0.50, r53_hc_opt=1.0,
    athena_tb=5.0, qs_author=24.0, qs_reader=3.0,
    pca=400.0, ga_h=0.025, ga_in_gb=0.01, sm_g5xl=2.043, resolver_eni=0.125, dx_out_gb=0.041,
)

def task_h(vcpu, gb):
    return vcpu * P["fg_cpu"] + gb * P["fg_gb"]

def usd(x):
    return f"USD {x:,.2f}"

# ---------------------------------------------------------------- sizing (A11)
ENGINEERS = 30     # engineers using coding agents (requester, 2026-11-17: "30 people for now")
WL_REQ_M = 1.0     # workload requests / month, million (2.5 B input tokens / ~2,500 per request)
REQ_M = round((ENGINEERS * 15 * 200) / 1e6 + WL_REQ_M, 2)   # million requests / month, expected scenario
REQ_KB, RESP_KB = 120, 20
GW_TASKS, GW_CPU, GW_GB = 3, 2, 4
GR_TASKS, GR_CPU, GR_GB = 3, 4, 8
N_VPCE = 11        # 10 listed in 02 §6 (without sagemaker.runtime) + aps-workspaces for AMP (finding F-1)


def comp(name, value, calc, basis):
    return dict(name=name, usd=round(value, 2), calc=calc, basis=basis)


def prod_tokyo():
    c = []
    v = GW_TASKS * task_h(GW_CPU, GW_GB) * H
    c.append(comp("Fargate: LiteLLM gateway tasks", v,
        f"avg {GW_TASKS} tasks × ({GW_CPU} vCPU × 0.05056 + {GW_GB} GB × 0.00553)/h × 730 h",
        "02 §9 (min 3 tasks, 3 AZs; size open R-42) [CMP §4.9]; at 30 engineers no scale-out above the minimum is expected"))
    v = GR_TASKS * task_h(GR_CPU, GR_GB) * H
    c.append(comp("Fargate: in-VPC guardrail service (Presidio + classifier, CPU)", v,
        f"avg {GR_TASKS} tasks × ({GR_CPU} vCPU × 0.05056 + {GR_GB} GB × 0.00553)/h × 730 h",
        "02 §2.2, §8, D-9; one task per AZ; classifier not chosen (R-10), CPU inference assumed; GPU is contingency row R-10"))
    inst = 2 * P["aur_r7gl_t"] * H
    v = inst + 50 * P["aur_gb"] + 30 * P["aur_io"] + 50 * P["aur_bkp"]
    c.append(comp("Aurora PostgreSQL (writer + reader, db.r7g.large, Multi-AZ)", v,
        "2 × 0.333/h × 730 h + 50 GB × 0.12 + 30 M I/O × 0.24/M + 50 GB backup × 0.023",
        "02 §2.2, §7.1, §9 [CMP §4.7]; provisioned assumed (R-23); 90-day spend log ≈ 3.3 M rows; 50 GB allocated with headroom (R-1)"))
    v = 2 * P["vk_m7gl_t"] * H
    c.append(comp("ElastiCache Valkey (2 × cache.m7g.large, Multi-AZ)", v,
        "2 nodes × 0.1616/h × 730 h", "02 §2.2, §7.1 (counters only, no response cache); Valkey assumed (R-23)"))
    v = P["alb_h"] * H + 2 * P["alb_lcu"] * H
    c.append(comp("Application Load Balancer (internet-facing)", v,
        "0.0243/h × 730 h + avg 2 LCU × 0.008/h × 730 h",
        "02 §2.2, §6 (Route B, 600 s idle); LCU from ~0.15 TB/month processed + long-lived streams"))
    v = P["waf_acl"] + 12 * P["waf_rule"] + REQ_M * P["waf_req"]
    c.append(comp("AWS WAF regional web ACL", v,
        f"1 ACL × 5 + 12 rules × 1 + {REQ_M} M requests × 0.60/M",
        "02 §8 WAF row: IP set, rate rule, IP reputation, Known Bad Inputs, CRS, admin-path and route-block rules (~12)"))
    gb = REQ_M * 1e6 * (REQ_KB + RESP_KB) / 1e6 * 1.1
    v = N_VPCE * 3 * P["vpce_h"] * H + gb * P["vpce_gb"]
    c.append(comp("Interface VPC endpoints (11 × 3 AZs)", v,
        f"11 endpoints × 3 AZs × 0.014/h × 730 h + {gb:,.0f} GB × 0.01",
        "02 §6 endpoint list (10) + aps-workspaces for AMP (finding F-1); 02 §12 'about 11 × 3 AZs'"))
    v = P["tgw_h"] * H + 5 * P["tgw_gb"]
    c.append(comp("Transit Gateway VPC attachment (egress path)", v,
        "1 attachment × 0.07/h × 730 h + 5 GB × 0.02", "02 §6 egress via TGW to network-prod (AS-18); attachment billed to gateway account"))
    v = 5 * P["nfw_gb"]
    c.append(comp("Network Firewall (network-prod): incremental GB only", v,
        "5 GB × 0.065 (endpoint-hours are shared, AS-18)", "02 §6, D-12 [CMP §4.6]; Entra/licence traffic only"))
    v = 5 * P["nat_gb"]
    c.append(comp("NAT gateway (network-prod): incremental GB only", v,
        "5 GB × 0.062 (gateway-hours are shared, AS-18)", "02 §6 [CMP §4.6]"))
    gb_out = REQ_M * 1e6 * RESP_KB / 1e6 * 1.25
    v = gb_out * P["dto_gb"]
    c.append(comp("Data transfer out to office/DC clients (responses)", v,
        f"{gb_out:,.0f} GB × 0.114 (first-10-TB tier)", f"Route B over internet (02 §6); {REQ_M} M responses × 20 KB SSE + 25 % overhead"))
    v = 8 * P["sm_secret"] + 0.1 * 1e6 / 1e4 * P["sm_api"]
    c.append(comp("Secrets Manager", v, "8 secrets × 0.40 + 100k API calls × 0.05/10k",
        "02 §7.1: master, salt, licence, DB, SSO client, CI admin key, Valkey AUTH, spare"))
    v = 6 * P["kms_key"] + 1.0 * 1e6 / 1e4 * P["kms_req"]
    c.append(comp("KMS customer-managed keys", v, "6 CMKs × 1 + 1 M requests × 0.03/10k",
        "02 §7.1: Aurora, ElastiCache, S3, CloudWatch Logs, Secrets Manager, ECR"))
    v = 60 * P["s3_gb"] + 100 * P["s3_put"] + 0.4
    c.append(comp("S3 (metadata, spend export, CUR, ALB logs, archive)", v,
        "avg 60 GB × 0.025 + 100k PUT × 0.0047/1k + GET 0.40",
        "02 §7.1; metadata ~2 GB/month, batched writes (A18); 1 year hot then archive"))
    ing = round(REQ_M * 1.5 + REQ_M * 1.5 + 5, 1)
    v = ing * P["cw_ingest"] + 50 * P["cw_store"] + 60 * P["cw_alarm"] + 50 * P["cw_metric"]
    c.append(comp("CloudWatch Logs, alarms and metrics", v,
        f"{ing} GB ingest × 0.76 + 50 GB stored × 0.033 + 60 alarms × 0.10 + 50 metrics × 0.30",
        "02 §7.1, §7.4: container INFO and WAF 1.5 KB per request each, VPC Flow 5 GB; 90 days hot; OBS-006 alarms"))
    samples = 3000 * 2 * 60 * H
    v = (samples - 40e6) / 1e7 * P["amp_10m"] + 1
    c.append(comp("Amazon Managed Service for Prometheus", v,
        f"3k series × 30 s scrape = {samples/1e6:,.0f} M samples; (− 40 M free) × 0.90/10M + 1 storage",
        "02 §2.2 metrics row; LiteLLM labels by team/key/model, ~3k series at 30 engineers (assumption)"))
    v = 5 * P["graf_ed"] + 15 * P["graf_vw"]
    c.append(comp("Amazon Managed Grafana", v, "5 editors × 9 + 15 viewers × 5",
        "02 §2.2 (OBS-003); users: platform 5 editors; on-call, SOC, FinOps 15 viewers (assumption)"))
    v = 40 * P["ecr_gb"]
    c.append(comp("ECR image storage", v, "40 GB × 0.10", "02 §2.2, SEC-016: pinned LiteLLM and guardrail images, ~10 versions kept"))
    v = P["r53_zone"] + P["r53_hc_opt"]
    c.append(comp("Route 53 hosted zone and failover health check", v,
        "1 zone × 0.50 + 1 HTTPS option × 1.00 (AWS-endpoint checks within free 50; alias queries free)",
        "02 §2.2 DNS row, §9 (R-8)"))
    v = 1 * P["athena_tb"] + 2 * P["qs_author"] + 30 * P["qs_reader"]
    c.append(comp("Chargeback: CUR 2.0, Athena, Quick Sight, Budgets", v,
        "Athena 1 TB × 5 + 2 authors × 24 + 30 readers × 3 (CUR export and non-action Budgets free)",
        "02 §2.2 billing row, §5 [CMP §4.5]; readers = FinOps + department contacts (assumption); Quick Sight prices: aws.amazon.com/quicksight/pricing (checked 2026-11-17)"))
    vcpu = GW_TASKS * GW_CPU + GR_TASKS * GR_CPU
    v = vcpu * P["gd_vcpu"] + 1 * P["gd_ct_m"] + 10 * P["gd_log_gb"]
    c.append(comp("GuardDuty incl. ECS runtime monitoring", v,
        f"{vcpu} vCPU × 2 + 1 M CloudTrail events × 4.72/M + 10 GB flow/DNS × 1.18",
        "02 §2.2 threat detection, SEC-019"))
    v = 10000 * P["shub_check"] + 3000 * P["cfg_ci"] + 6000 * P["cfg_eval"] + 10 * P["insp_init"] + 600 * P["insp_rescan"]
    c.append(comp("Security Hub CSPM, AWS Config, Inspector (ECR)", v,
        "10k checks × 0.001 + 3k CIs × 0.003 + 6k evals × 0.001 + 10 scans × 0.11 + 600 rescans × 0.01",
        "02 §2.2, §8.3 (RES-003 Config rule, SEC-016 scanning); CloudTrail org trail first copy free"))
    v = 75
    c.append(comp("Bedrock tokens for platform tests (gate re-runs, probe)", v,
        "≈ USD 200 per full gate run × 1 run/quarter + probe on Haiku 5.5 (< USD 1)",
        "OPS-001, AVL-M01; platform's own usage, not charged back"))
    return c


def dr_osaka():
    c = []
    v = (task_h(GW_CPU, GW_GB) + task_h(GR_CPU, GR_GB)) * H
    c.append(comp("Fargate warm standby (1 gateway + 1 guardrail task)", v,
        "(1 × 2 vCPU/4 GB + 1 × 4 vCPU/8 GB) at Tokyo-equal Osaka rates × 730 h",
        "02 §9 D-15 warm standby; scaled out on failover; Valkey rebuilt cold, not running (finding F-4)"))
    v = P["aur_r7gl_o"] * H + 50 * P["aur_gb"] + 50 * P["aur_repl_io"] + 30 * P["xreg_gb"] + 50 * P["aur_bkp"]
    c.append(comp("Aurora Global Database secondary (db.r7g.large) + snapshot copy", v,
        "0.332/h × 730 h + 50 GB × 0.12 + 50 M replicated write I/O × 0.24/M + 30 GB Tokyo→Osaka × 0.09 + 50 GB snapshot × 0.023",
        "02 §7.1, §9, AVL-M03 [CMP §4.9]"))
    v = P["alb_h"] * H + 1 * P["alb_lcu"] * H
    c.append(comp("ALB (Osaka)", v, "0.0243/h × 730 h + 1 LCU × 0.008/h × 730 h", "02 §9 same allowlist on Osaka ALB"))
    v = P["waf_acl"] + 12 * P["waf_rule"]
    c.append(comp("AWS WAF web ACL (Osaka)", v, "1 ACL × 5 + 12 rules × 1", "02 §9 same WAF rules"))
    v = N_VPCE * 3 * P["vpce_h"] * H
    c.append(comp("Interface VPC endpoints (Osaka, 11 × 3 AZs)", v, "11 × 3 AZs × 0.014/h × 730 h",
        "02 §9 same IaC; could be 1 AZ in standby (saves ~USD 225)"))
    v = 8 * P["sm_secret"] + 6 * P["kms_key"] + 40 * P["ecr_gb"] + 10 * P["xreg_gb"]
    c.append(comp("Secrets/KMS replicas and ECR replication (Osaka)", v,
        "8 replica secrets × 0.40 + 6 replica keys × 1 + 40 GB × 0.10 + 10 GB/month × 0.09",
        "02 §2.2 (secrets copy R-7, ECR replicated to Osaka)"))
    v = 5 + (GW_CPU + GR_CPU) * P["gd_vcpu"] + 2 + 10
    c.append(comp("CloudWatch, GuardDuty, Security Hub, Config (Osaka)", v,
        "logs/alarms 5 + 6 vCPU × 2 + events 2 + CSPM/Config 10", "02 §2.2 threat detection in both regions"))
    return c


def dev_env():
    c = [
        comp("Fargate 1 gateway (1 vCPU/2 GB) + 1 guardrail (2 vCPU/4 GB)", (task_h(1, 2) + task_h(2, 4)) * H, "", ""),
        comp("Aurora db.t4g.medium single instance + 10 GB + I/O", P["aur_t4gm"] * H + 10 * P["aur_gb"] + 5, "", ""),
        comp("Valkey cache.t4g.small single node", P["vk_t4gs"] * H, "", ""),
        comp("ALB + 1 LCU; WAF ACL + 12 rules", P["alb_h"] * H + P["alb_lcu"] * H + 17, "", ""),
        comp("11 interface endpoints × 1 AZ", N_VPCE * P["vpce_h"] * H, "", ""),
        comp("TGW attachment (egress to Entra for SSO)", P["tgw_h"] * H, "", ""),
        comp("CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone", 10 + 10 + 2 + 2 + 5 + 0.5, "", ""),
        comp("GuardDuty, Security Hub, Config", 3 * P["gd_vcpu"] + 10, "", ""),
    ]
    return c


def stg_env():
    c = [
        comp("Fargate 3 gateway (2 vCPU/4 GB) + 3 guardrail (4 vCPU/8 GB)", (3 * task_h(2, 4) + 3 * task_h(4, 8)) * H, "", ""),
        comp("Aurora writer + reader db.r7g.large + storage/I/O", 2 * P["aur_r7gl_t"] * H + 10, "", ""),
        comp("Valkey 2 × cache.m7g.large", 2 * P["vk_m7gl_t"] * H, "", ""),
        comp("ALB + 2 LCU; WAF ACL + 12 rules", P["alb_h"] * H + 2 * P["alb_lcu"] * H + 17, "", ""),
        comp("11 interface endpoints × 3 AZs", N_VPCE * 3 * P["vpce_h"] * H, "", ""),
        comp("TGW attachment", P["tgw_h"] * H, "", ""),
        comp("CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone", 15 + 12 + 3 + 0 + 20 + 0.5, "", ""),
        comp("GuardDuty (18 vCPU), Security Hub, Config", 18 * P["gd_vcpu"] + 24, "", ""),
    ]
    return c


def tot(cs):
    return round(sum(x["usd"] for x in cs), 2)


def jpy(u):
    return int(round(u * FX))


# ---------------------------------------------------------------- line items
def row(cat, desc, role, unit, qty, typ, notes, j=None):
    return dict(cat=CAT[cat], key=cat, desc=desc, role=role, unit=unit, qty=qty, type=typ, notes=notes, j=j)


def labor_rows():
    r = []
    a = r.append
    # 1-1 requirements (only what is left for 01)
    a(row("req", "Close the 20 open questions in 01 §9 and confirm assumptions AS-1–AS-21 with their 8 owner teams; update 01 to v1.0",
          R_BA, U_PD, 15, T_OT, "01 §9 (Q-1–Q-20, due 2026-12-18 / 2027-01-29), 01 §3. Sizing: ~0.75 pd per question incl. workshop and write-up"))
    a(row("req", "Requirements review and approval (security, legal/privacy, network, FinOps, platform lead)",
          R_ARCH, U_PD, 4, T_OT, "01 header Approvers, 01 §11, REG-003. Sizing: 2 review rounds × 2 pd"))
    # 1-2 design
    a(row("des", "Design v0.2: close uncovered requirements and High risks — Osaka egress and secrets copy (R-7), failover health check (R-8), AVL-001, spend-log store (R-1), profile granularity (R-12), data-tier choices (R-23), content logging if needed (PRV-002, R-6)",
          R_ARCH, U_PM, 1.0, T_OT, "02 §1.2, §14 (target 2027-01-29). Sizing: ~6 design topics × ~3 pd"))
    a(row("des", "Detailed design of remaining TBDs: accounts and environments (R-41), permission sets and break-glass (R-45), IaC tool (R-22), task sizing (R-42), routing values (R-49), request-size limit (R-17), key defaults (R-16), alert thresholds (R-39)",
          R_INF, U_PM, 1.0, T_OT, "02 §1.3, §4.3, §9, §10, §14. Sizing: ~8 topics × ~2.5 pd"))
    a(row("des", "Guardrail classifier selection: evaluate Japanese-capable prompt-attack classifiers and Presidio Japanese recognizers against the Q-13 test set",
          R_SR, U_PD, 10, T_OT, "02 §1.3, §8, D-9, R-10; 01 SEC-008, Q-13. Sizing: 3 candidates × 3 pd + report"))
    a(row("des", "Early spikes on a sandbox: master-key UI login (R-2/V-3), Codex CLI Responses API (R-4), ARN pricing (R-5), SCIM key blocking (R-35)",
          R_ENG, U_PD, 10, T_OT, "02 §14 mitigations 'run early'. Sizing: 4 spikes × 2.5 pd"))
    a(row("des", "Design review and approval (security, network, platform lead, FinOps, SRE), incl. Security sign-off of R-48 parameters",
          R_ARCH, U_PD, 5, T_OT, "02 header Approvers, R-48. Sizing: 2 rounds + 1 pd follow-up"))
    # 1-3 implementation
    a(row("imp", "IaC for both regions: VPC/subnets/endpoints, ALB + WAF, ECS services, Aurora Global Database, ElastiCache, S3/KMS/Secrets, SCP and Config rules, Route 53 failover, TGW attachment",
          R_INF, U_PM, 3.0, T_OT, "02 §2.2, §6, §8, §9; OPS-002, D-8 (start from the AWS sample [CMP §3.1]). Sizing: ~20 components, one codebase for 4 environments"))
    a(row("imp", "LiteLLM configuration and model catalog: config.yaml for 10 catalog models + aliases, Japan-only fallbacks, custom pricing per profile, application inference profiles, content-off settings, SSO/team-sync settings, key upper bounds",
          R_SR, U_PM, 1.0, T_OT, "02 §5, §5.1, §7.3; D-19, D-20, D-21, D-22; 01 §6.5 MDL-001–010"))
    a(row("imp", "Self-hosted in-VPC guardrail service: Presidio with Japanese recognizers, classifier service, LiteLLM pre-call integration, failure behaviour, metadata-only logging, container hardening",
          R_SR, U_PM, 2.0, T_OT, "02 §2.2, §8 (D-9), R-10, R-11; 01 SEC-008, SEC-009. Sizing: new service with ML model, our own scaling and patching [CMP §7.1]"))
    a(row("imp", "Entra SSO / SCIM integration: OIDC app per environment (3), app roles → LiteLLM roles, llm-team-* team sync, SCIM deprovisioning, offboarding job if SCIM does not block keys",
          R_ENG, U_PM, 1.0, T_OT, "02 §4.1, §4.2, §4.5 (R-35, R-24); 01 IAM-001, IAM-004, IAM-006, TEN-004"))
    a(row("imp", "Key-issuance pipeline: CI for teams, budgets, model access and service-account keys; upper bounds; secret-scanning pattern for the key format",
          R_ENG, U_PM, 1.0, T_OT, "02 §4.5, §5, §10; D-19, OPS-003, TEN-001–TEN-006, SEC-018"))
    a(row("imp", "Client package: key helper (Windows Credential Manager / macOS Keychain), Claude Code managed settings, Codex CLI config.toml (deployed by Intune team)",
          R_ENG, U_PD, 10, T_OT, "02 §2.2 client package, §4.1, D-3; 01 FUN-009. Intune deployment itself excluded (B5)"))
    a(row("imp", "CUR reconciliation job: daily spend export to S3 Parquet with delete-after-export, CUR 2.0 export, Athena tables, Quick Sight chargeback with residual line, AWS Budgets backstop",
          R_ENG, U_PM, 1.0, T_OT, "02 §5, §7.1, D-14, D-23; 01 CST-007, CST-008, CST-011 [CMP §4.5]"))
    a(row("imp", "Logging / SIEM pipeline: S3 metadata callback, log groups with KMS and retention, WAF credential redaction, cross-account subscription to SIEM and log-archive, audit-log export",
          R_INF, U_PM, 1.0, T_OT, "02 §7.1, §7.4; 01 OBS-001, OBS-002, OBS-004, OBS-007, SEC-015. SIEM-side ingestion excluded (B6)"))
    a(row("imp", "Metrics, dashboards and alerts: AMP + ADOT, Grafana dashboards per team/key, dependency and missing-spend alarms, key-sharing alert, synthetic availability probe",
          R_ENG, U_PD, 15, T_OT, "02 §2.2 metrics row, R-38, R-39; 01 OBS-003, OBS-005, OBS-006, AVL-M01"))
    # 1-4 testing
    a(row("tst", "Unit tests for custom code (guardrail service, export job, offboarding job, key helper, CI pipeline)",
          R_ENG, U_PD, 15, T_OT, "Sizing: ≈15 % of custom-code build effort (≈5 pm)"))
    a(row("tst", "Integration, security and inspection tests T-001–T-075 on staging: automate, run, retest",
          R_QA, U_PM, 2.5, T_OT, "02 §11.1 (75 tests). Sizing: avg 0.65 pd per test incl. automation + 1 retest cycle"))
    a(row("tst", "Load and long-stream tests (T-059, T-023, T-058, T-060) and task sizing", R_INF, U_PD, 8, T_OT,
          "02 §11.1, R-42, R-49; 01 PRF-M02, PRF-M04, PRF-001 (sizing basis A-9)"))
    gates = [
        ("V-1", "No prompt content outside approved stores: canary through every model and API style, guardrail-blocked and provider-rejected requests; search every store", R_SR, 5, "PRV-001, OBS-002"),
        ("V-2", "Key creation stays within limits, incl. the two-key check", R_QA, 3, "TEN-001, TEN-005, TEN-006"),
        ("V-3", "Admin UI master-key login", R_SR, 1, "SEC-011, R-2"),
        ("V-4", "Spend correct per deployment (10 deployments, with and without prompt caching)", R_ENG, 4, "CST-004, R-5, D-21"),
        ("V-5", "Cancelled requests are metered", R_ENG, 3, "CST-006"),
        ("V-6", "Clients cannot skip tracking", R_QA, 1, "CST-005"),
        ("V-7", "Clients cannot choose who pays, incl. user in two teams", R_QA, 2, "CST-001, R-26"),
        ("V-8", "Database outage behaviour", R_INF, 3, "AVL-002, D-25"),
        ("V-9", "Licence check unavailable", R_INF, 2, "AVL-004, R-19"),
        ("V-10", "Identity endpoints unavailable", R_INF, 2, "AVL-003"),
        ("V-11", "Unmanaged devices cannot reach the gateway (with Network; CIDR list and owners)", R_SEC, 3, "SEC-001–SEC-003, OPS-004"),
    ]
    for g, d, role, q, req in gates:
        a(row("tst", f"Launch gate {g}: {d}", role, U_PD, q, T_OT, f"02 §11.2 [CMP {g}, §2.10]; 01 {req}; must pass before first pilot user (01 §1.4)"))
    a(row("tst", "DR drill before launch: fail over to Osaka, measure RTO/RPO, call each model available in Osaka, fail back; AZ-loss test",
          R_INF, U_PD, 6, T_OT, "02 §11.1 T-055, T-056; 01 OPS-007, AVL-M02, AVL-M03, GA exit (01 §1.4)"))
    # 1-5 data migration: none
    # 1-6 setup
    a(row("set", "AWS accounts and landing-zone onboarding for dev, staging, prod: SCP, Identity Center permission sets, break-glass, TGW attachments, budgets",
          R_INF, U_PD, 10, T_OT, "02 §4.3, §10 (R-41, R-45); 01 IAM-007–IAM-009, RES-003"))
    a(row("set", "CI/CD: image mirror to ECR by digest, scan gate, promotion dev → staging → prod, config deploy, IaC plan/apply with drift check",
          R_INF, U_PD, 15, T_OT, "02 §8, §10; 01 SEC-016, OPS-002 (T-051, T-068)"))
    a(row("set", "Bedrock setup in both regions: model access, application inference profiles, quota requests in Tokyo and Osaka, GetInferenceProfile records, invocation logging off",
          R_ENG, U_PD, 4, T_OT, "02 §5.1, §9 (R-27), D-10, D-13; 01 MDL-104, PRV-004"))
    a(row("set", "Production and DR deployment and release", R_INF, U_PD, 5, T_OT, "02 §10 (release unit, rolling deploy)"))
    # 1-7 training & docs
    a(row("trn", "Technical docs 03, 04, 06, 07, 09 written to the design, incl. rewriting the R-21 conflicts", R_SR, U_PM, 1.0, T_OT,
          "README doc set, 02 R-21. Sizing: 5 docs × 4 pd"))
    a(row("trn", "User-facing docs 05, 08, 10 and editing of the set to the 11 §D checklist", R_TW, U_PD, 12, T_OT, "README doc set, 11 §D"))
    a(row("trn", "User onboarding: guide and short video, 2 live sessions for pilot and GA cohorts, team-admin training (budgets, service-account keys)",
          R_TW, U_PD, 6, T_OT, "01 §1.4, UC-3, UC-5; 30 engineers (A12). Sizing: 2 sessions × 1 pd + 4 pd material"))
    a(row("trn", "Operations handover to on-call: 07 runbook walk-through and alert drills", R_SR, U_PD, 3, T_OT, "02 §10 on-call; 01 OPS-006"))
    # 1-8 cutover
    a(row("cut", "Pilot (1 month): onboard pilot teams, triage, fixes, findings into 08", R_ENG, U_PM, 1.0, T_OT, "01 §1.4 (pilot teams Q-3)"))
    a(row("cut", "GA readiness: re-run launch gates on the release that goes live", R_QA, U_PD, 5, T_OT, "01 §1.4 GA exit, OPS-001"))
    a(row("cut", "Hypercare 2 weeks after GA", R_ENG, U_PD, 15, T_OT, "Sizing: 1.5 engineers × 10 days"))
    # 1-9 operation (per month)
    a(row("ops", "On-call and incident response in support hours (business hours assumed)", R_OPS, U_PM, 0.5, T_RC, "Per month. 01 OPS-006 (hours open, Q-6); 00 §1.4"))
    a(row("ops", "Monitoring, alert triage and CI changes for teams, budgets, models and service-account keys", R_OPS, U_PM, 0.25, T_RC, "Per month. 01 OPS-003, OBS-006; 02 §10"))
    a(row("ops", "First-line help desk: key renewal (90-day expiry), onboarding questions", R_HD, U_PD, 2, T_RC, "Per month. 01 TEN-006, Q-20. 30 engineers: ≈10 key renewals a month"))
    a(row("ops", "Monthly chargeback run and residual investigation", R_ENG, U_PD, 2, T_RC, "Per month. 01 CST-007, CST-008; 02 §5"))
    a(row("ops", "Periodic reviews: master-key readers, audit and operator activity", R_SEC, U_PD, 1, T_RC, "Per month. 01 SEC-010, OBS-007 (frequency Q-8)"))
    a(row("ops", "Recurring DR drill (assumed every 6 months × 6 pd)", R_INF, U_PD, 1, T_RC, "Per month equivalent. 01 OPS-007 (interval Q-6)"))
    # 1-10 maintenance (per month)
    a(row("mnt", "LiteLLM upgrades with every launch gate re-run on staging (assumed quarterly, 12 pd per upgrade)", R_SR, U_PD, 4, T_RC,
          "Per month. 01 OPS-001; 02 §10 upgrade gate, §7.5 (R-30) [CMP §2.10]"))
    a(row("mnt", "Quarterly Japan model snapshot re-check of every catalog model and catalog updates (≈3 pd per quarter)", R_ENG, U_PD, 1, T_RC,
          "Per month. 01 MDL-104, AS-17; 02 §5.1 (R-28)"))
    a(row("mnt", "Patching: base images, guardrail dependencies, Aurora/Valkey minor versions, advisories", R_INF, U_PD, 2, T_RC, "Per month. 02 §8.3"))
    a(row("mnt", "Guardrail classifier and PII-recognizer upkeep", R_SR, U_PD, 1, T_RC, "Per month. 02 R-10 (accuracy, scaling and patching are ours)"))
    a(row("mnt", "Bug fixes and minor changes to custom components", R_ENG, U_PD, 2, T_RC, "Per month. Guardrail service, jobs, key helper, pipelines"))
    # 2-2 QA
    a(row("qa", "Independent review of IaC and security-critical configuration (§7.3 settings, SCP, endpoint policies, WAF rules) before launch",
          R_ARCH, U_PD, 5, T_OT, "02 §7.3, §8, D-11, D-13"))
    a(row("qa", "Phase-gate reviews: design, build complete, launch readiness, GA", R_QA, U_PD, 4, T_OT, "01 §1.4 exit criteria. 4 gates × 1 pd"))
    # 2-4 licence placeholder
    a(row("lic", "LiteLLM Enterprise licence (Admin UI SSO for all users, SCIM, audit logs) — PRICE NEEDED", R_VEN, U_MF, 1, T_RC,
          "[CMP A-6]; 01 AS-6, CON-2, Q-17; 02 R-36. No public price: J left blank on purpose so the check flags it. Ask the vendor for a monthly-equivalent price incl. the project months (dev/staging SSO)"))
    # 2-5 security
    a(row("sec", "Security design review: threat model and residual-risk acceptance, R-48 parameters, guardrail failure mode, SCP review",
          R_SEC, U_PD, 10, T_OT, "02 §8, §8.1, R-11, R-48"))
    a(row("sec", "Third-party penetration test before launch", R_VEN, U_OT, 1, T_OT,
          "02 §8.3 (R-48). Price = template sample value, placeholder until a vendor quote (Security)", j=2000000))
    return r


def infra_rows(pt, dr, dev, stg):
    r = []
    a = r.append
    pt_t, dr_t, dev_t, stg_t = tot(pt), tot(dr), tot(dev), tot(stg)
    dev_list = "; ".join(f"{c['name']} {usd(c['usd'])}" for c in dev)
    stg_list = "; ".join(f"{c['name']} {usd(c['usd'])}" for c in stg)
    a(row("inf", "Dev environment during the project (Tokyo)", R_VEN, U_MF, MONTHS_DEV, T_OT,
          f"Quantity = {MONTHS_DEV} months (2027-02 to 2027-07). {usd(dev_t)}/month × {FX} = J. {dev_list}. 02 §10, 03 §2 (R-41). {PL}", j=jpy(dev_t)))
    a(row("inf", "Staging environment during the project (Tokyo, production topology at minimum scale)", R_VEN, U_MF, MONTHS_STG, T_OT,
          f"Quantity = {MONTHS_STG} months (2027-04 to 2027-07). {usd(stg_t)}/month. {stg_list}. 02 §10 (matches production for launch gates). {PL}", j=jpy(stg_t)))
    a(row("inf", "Production Tokyo before GA (build and pilot)", R_VEN, U_MF, MONTHS_PRE_GA, T_OT,
          f"Quantity = {MONTHS_PRE_GA} months (2027-06 to 2027-07). Same components as the recurring production rows below: {usd(pt_t)}/month. {PL}", j=jpy(pt_t)))
    a(row("inf", "DR Osaka before GA (build and DR drill)", R_VEN, U_MF, MONTHS_PRE_GA, T_OT,
          f"Quantity = {MONTHS_PRE_GA} months. Same components as the recurring DR rows below: {usd(dr_t)}/month. {PL}", j=jpy(dr_t)))
    a(row("inf", "Bedrock tokens used by the platform team during the project (development, tests, launch gates, DR drill)", R_VEN, U_OT, 1, T_OT,
          "Sizing: dev use ≈ USD 300/month × 6 + functional/gate tests ≈ USD 250 + load test on Haiku 5.5 (360k req × 1.2k tokens) ≈ USD 80 → ≈ USD 2,130. Prices: §usage table. Not charged back", j=jpy(2130)))
    for c in pt:
        a(row("inf", f"Production Tokyo: {c['name']}", R_VEN, U_MF, 1, T_RC,
              f"Per month from GA. {c['calc']} = {usd(c['usd'])}. {c['basis']}. {PL}", j=jpy(c["usd"])))
        r[-1].update(env="pt", comp=c)
    for c in dr:
        a(row("inf", f"DR Osaka: {c['name']}", R_VEN, U_MF, 1, T_RC,
              f"Per month from GA. {c['calc']} = {usd(c['usd'])}. {c['basis']}. {PL} (ap-northeast-3)", j=jpy(c["usd"])))
        r[-1].update(env="dr", comp=c)
    a(row("inf", "Dev environment after GA (Tokyo)", R_VEN, U_MF, 1, T_RC,
          f"Per month. Same sizing as the project-period row: {usd(dev_t)}. Kept for maintenance (02 §10). {PL}", j=jpy(dev_t)))
    a(row("inf", "Staging environment after GA (Tokyo)", R_VEN, U_MF, 1, T_RC,
          f"Per month. Same sizing as the project-period row: {usd(stg_t)}. Needed for gate re-runs on every upgrade (OPS-001); scale-down between upgrades not assumed (finding F-6). {PL}", j=jpy(stg_t)))
    return r


LIK = {"Low": 0.25, "Medium": 0.5, "High": 0.75}


def risk_rows():
    r = []
    a = r.append
    def note(rid, lik, txt):
        return f"02 §14 {rid} (likelihood {lik} = {int(LIK[lik]*100)} %). Expected value = impact × likelihood (A7). {txt}"
    a(row("con", "Risk R-3: mTLS becomes required (V-11 fails or A-16 unconfirmed) — ALB mutual auth, trust store, CRL job, local mTLS helper per tool",
          R_SR, U_PM, 0.5 * 1.5, T_OT, note("R-3", "Medium", "Impact 1.5 pm. 01 SEC-003, D-4")))
    pca = P["pca"]
    a(row("con", "Risk R-3 (recurring part): AWS Private CA for workload certificates", R_VEN, U_MF, 0.5, T_RC,
          note("R-3", "Medium", f"Impact USD {pca:.0f}/month general-purpose CA [PL ACM PCA Tokyo, {CHECKED}]"), j=jpy(pca)))
    a(row("con", "Risk R-7: Osaka egress path to Entra and licence endpoint, and secrets copy — design and build",
          R_INF, U_PM, 0.75 * 0.5, T_OT, note("R-7", "High", "Impact 0.5 pm. 01 AVL-001, 02 §9")))
    eg = P["nfw_h"] * H + P["nat_h"] * H + P["tgw_h"] * H
    a(row("con", "Risk R-7 (recurring part): Osaka egress (1 Network Firewall endpoint + 1 NAT gateway + TGW attachment)", R_VEN, U_MF, 0.75, T_RC,
          note("R-7", "High", f"Impact (0.395 + 0.062 + 0.07)/h × 730 h = {usd(eg)}/month {PL}"), j=jpy(eg)))
    ga = P["ga_h"] * H + 500 * P["ga_in_gb"]
    a(row("con", "Risk R-32: office firewall allows only fixed IPs — AWS Global Accelerator in front of the ALB", R_VEN, U_MF, 0.5, T_RC,
          note("R-32", "Medium", f"Impact 0.025/h × 730 h + 500 GB in × 0.01 DT-premium = {usd(ga)}/month [PL Global Accelerator {CHECKED}]; build effort in the % buffer"), j=jpy(ga)))
    a(row("con", "Risk R-1: spend-log table slows key lookups — partitioning or separate store", R_SR, U_PM, 0.25 * 1.0, T_OT,
          note("R-1", "Low", "Impact 1.0 pm; Low at 30 engineers (≈3.3 M rows / 90 days), Medium in 02 §14 at A-9 scale")))
    gpu = 2 * P["sm_g5xl"] * H
    a(row("con", "Risk R-10: Japanese classifier needs a GPU — SageMaker ml.g5.xlarge × 2 (2 AZs) in Tokyo", R_VEN, U_MF, 0.5, T_RC,
          note("R-10", "Medium", f"Impact 2 × 2.043/h × 730 h = {usd(gpu)}/month [PL SageMaker Tokyo {CHECKED}]; CPU guardrail tasks would shrink (not netted)"), j=jpy(gpu)))
    a(row("con", "Risk R-12: per-team or per-department inference profiles with team-specific model names", R_ENG, U_PD, 0.75 * 10, T_OT,
          note("R-12", "High", "Impact 10 pd (config, CI, V-4/V-7 re-run)")))
    a(row("con", "Risk R-6 / 01 Q-10: per-team content logging required this phase — separate store, Macie, V-1 re-run", R_SR, U_PM, 0.5 * 1.0, T_OT,
          note("R-6", "Medium", "Impact 1.0 pm; whether it is needed is 01 Q-10, so Medium used instead of R-6's High")))
    a(row("con", "Risk R-4: Codex CLI Responses API fails with non-OpenAI models — workaround", R_ENG, U_PD, 0.5 * 10, T_OT,
          note("R-4", "Medium", "Impact 10 pd")))
    own = 3 * (P["nfw_h"] + P["nat_h"]) * H
    a(row("con", "Risk AS-18: shared egress in network-prod not available — gateway's own Network Firewall + NAT (3 AZs)", R_VEN, U_MF, 0.25, T_RC,
          f"01 AS-18 (Low assumed = 25 %). Impact 3 × (0.395 + 0.062)/h × 730 h = {usd(own)}/month {PL}. Expected value = impact × likelihood (A7)", j=jpy(own)))
    return r


# ---------------------------------------------------------------- assumptions & exclusions
ASSUMPTIONS = [
    ("Scope / 範囲",
     "Build and 24-month operation of the Internal LLM gateway as designed in 01 and 02 v0.1 (Draft, 2026-11-17): LiteLLM Proxy on ECS Fargate in Tokyo with a warm standby in Osaka, the Bedrock catalog in 01 §6.5, Route B ingress only.",
     "01・02 v0.1（作成中、2026-11-17）で設計された社内LLMゲートウェイの構築と24か月の運用を対象とする。東京のECS Fargate上のLiteLLM Proxy、大阪のウォームスタンバイ、01 §6.5のBedrockモデル、Route B経路のみ。"),
    ("Schedule / スケジュール",
     "Project 2027-01 to 2027-07 (7 months): M1 remaining requirements, design and approval; M2–M5 build; M4–M6 tests and launch gates; M6 production and DR build, penetration test; M7 pilot and DR drill. GA 2027-08. Recurring costs start at GA; operation period 24 months (2027-08 to 2029-07). Dates are open (01 Q-3).",
     "プロジェクト期間 2027年1月〜7月（7か月）：1か月目 残りの要件・設計・承認、2〜5か月目 構築、4〜6か月目 テスト・ローンチゲート、6か月目 本番・DR構築とペネトレーションテスト、7か月目 パイロットとDR訓練。2027年8月GA。継続費用はGAから発生し、運用期間は24か月（2027年8月〜2029年7月）。日程は未確定（01 Q-3）。"),
    ("Effort unit / 工数単位",
     "1 person-month = 20 person-days = 160 hours (Rates sheet). Rates are blended and exclude tax.",
     "1人月＝20人日＝160時間（Ratesシート）。単価は平均単価・税抜。"),
    ("Rates / 単価",
     "OPEN ITEM (FinOps): no internal rates exist yet. The template's sample rates (indicative FY2026 market rates) are kept unchanged and are not quotes. Replace them on the Rates sheet; every labor row updates.",
     "【未決事項・FinOps】社内単価が未設定のため、テンプレートのサンプル単価（2026年度の参考相場）をそのまま使用しており、見積回答ではない。Ratesシートで置き換えると全工数行が更新される。"),
    ("Recurring costs / 継続費用",
     "Recurring lines are monthly amounts; annual = monthly x 12. The grand total includes 24 recurring months (the operation period). The markdown output also gives 12- and 36-month views.",
     "継続費用は月額で計上し、年額＝月額×12。総額には運用期間の24か月分の継続費用を含む。Markdown出力には12か月・36か月の試算も記載。"),
    ("Project management / PM費",
     "Project management = PM % (10 %, template default) x development cost (one-time phase-based costs). PM effort is not included in phase rows.",
     "PM費＝PM費率（10%、テンプレート既定値）×開発費（工程別の初期費用）。工程別の行にはPM工数を含めない。"),
    ("Contingency / 予備費",
     "Contingency = 15 % (template default) of initial cost excluding contingency, plus 15 % of monthly recurring cost. Identified risks from 02 §14 are line items at expected value = impact x likelihood (Low 25 %, Medium 50 %, High 75 %). Tax is never included in the base.",
     "予備費＝予備費を除く初期費用×15%（既定値）＋継続月額×15%。02 §14の特定済みリスクは期待値（影響額×発生確率：低25%、中50%、高75%）で明細計上。消費税は算定基礎に含めない。"),
    ("Tax / 消費税",
     "Consumption tax is calculated once on each total at the rate on Summary; amounts below JPY 1 are rounded down.",
     "消費税はSummaryの税率で各合計に対して1回計算し、1円未満は切り捨て。"),
    ("Cloud / クラウド",
     "AWS On-Demand list prices from the AWS Price List API offer files for ap-northeast-1 and ap-northeast-3 (publication 2026-11-17, checked 2026-11-17), cited as [PL]; 730 h per month; no Savings Plans, reserved or EDP discounts. Budget exchange rate JPY 160 / USD (market about 158–160 in mid-November 2026). OPEN ITEM (FinOps): confirm the budget rate.",
     "AWSの価格はAWS Price List API（ap-northeast-1／ap-northeast-3、2026-11-17公開版、2026-11-17確認）のオンデマンド定価（[PL]と表記）。1か月730時間、Savings Plans・リザーブド・EDP割引は考慮しない。予算レートは1USD＝160円（2026年11月中旬の市場水準は約158〜160円）。【未決事項・FinOps】予算レートの確認。"),
    ("Environments / 環境",
     "Four environments (02 §10, 03 §2): dev (minimal, Tokyo), staging (production topology at minimum scale, Tokyo), production (Tokyo, 3 AZs) and DR (Osaka, warm standby). Dev and staging remain after GA; staging is needed to re-run launch gates on every LiteLLM upgrade (OPS-001). Accounts are open (R-41).",
     "開発（最小構成・東京）、ステージング（本番と同構成・最小規模・東京）、本番（東京・3AZ）、DR（大阪・ウォームスタンバイ）の4環境（02 §10、03 §2）。開発・ステージングはGA後も維持し、ステージングはLiteLLM更新ごとのローンチゲート再実行に使う（OPS-001）。アカウント構成は未定（R-41）。"),
    ("Sizing / サイジング",
     "Fixed capacity is the design minimum (02 §9): gateway 3 Fargate tasks of 2 vCPU / 4 GB and guardrail 3 tasks of 4 vCPU / 8 GB on CPU, one per AZ; Aurora db.r7g.large writer + reader; Valkey cache.m7g.large x 2. Per-request charges use the expected usage scenario: about 1.1 million requests per month (30 engineers plus workloads), 120 KB request and 20 KB response on average. Sizing is open (R-42, R-23, R-10).",
     "固定容量は設計上の最小構成（02 §9）：ゲートウェイはFargate 3タスク（2vCPU/4GB）、ガードレールは3タスク（4vCPU/8GB、CPU推論）でAZごとに1つ、Aurora db.r7g.large（ライター＋リーダー）、Valkey cache.m7g.large×2。従量部分は想定利用シナリオ（エンジニア30人とワークロードで月約110万リクエスト、平均リクエスト120KB・レスポンス20KB）による。サイジングは未確定（R-42、R-23、R-10）。"),
    ("Users / 利用者",
     "30 engineers use the gateway with coding agents (set by the requester on 2026-11-17, for now). CMP A-9 (about 5,000 employees, about 300 concurrent users) is not used for sizing. Workload volume (UC-2) is as in the markdown usage table.",
     "コーディングエージェントでゲートウェイを利用するエンジニアは30人（2026-11-17に依頼者が当面の値として設定）。CMP A-9（従業員約5,000人、同時約300人）はサイジングに使わない。ワークロード（UC-2）の利用量はMarkdownの利用試算表のとおり。"),
    ("Shared network / 共有ネットワーク",
     "AS-18 holds: the shared network-prod account provides Transit Gateway, Network Firewall and NAT. Their endpoint-hours are not charged to this project; the gateway pays its TGW attachments and per-GB charges. Dev and staging use the same path. If AS-18 is false, see the contingency row.",
     "AS-18が成立し、共有アカウントnetwork-prodのTransit Gateway・Network Firewall・NATを利用する前提。それらの時間課金は本案件に計上せず、TGWアタッチメントとGB課金のみ計上。開発・ステージングも同経路。不成立の場合は予備費の行を参照。"),
    ("Model usage / モデル利用料",
     "Bedrock token charges for teams are not in the totals: LiteLLM charges them back to teams (01 CST-007). The markdown output gives a separate low / expected / high usage table. Bedrock tokens used by the platform team itself (development, tests, gates, probe) are included.",
     "チームのBedrockトークン料金は合計に含めない（LiteLLMでチームに配賦、01 CST-007）。Markdown出力に低・想定・高の利用試算を別表で記載。基盤チーム自身の利用（開発・テスト・ゲート・監視プローブ）は計上する。"),
    ("Licences / ライセンス",
     "OPEN ITEM (Product owner): the LiteLLM Enterprise licence price is unknown (01 Q-17). It is a placeholder row with no price, so the check 'Rows with quantity but no amount' shows 1 on purpose. Presidio and the guardrail classifier are assumed to be open source with no licence fee.",
     "【未決事項・プロダクトオーナー】LiteLLM Enterpriseライセンス価格は未確定（01 Q-17）。単価未入力の仮行としており、チェック「単価未設定の行数」が意図的に1となる。Presidioとガードレール分類器はオープンソース（ライセンス費なし）を前提とする。"),
    ("Delivery team / 実施体制",
     "Platform engineering does all build and run work estimated here, using the template roles. Penetration test is by a third party; its price is the template sample value until a vendor quote (OPEN ITEM, Security).",
     "本見積の構築・運用作業はプラットフォームエンジニアリングがテンプレートの役割で実施する。ペネトレーションテストは外部委託で、ベンダー見積までテンプレートのサンプル価格を使用（【未決事項・セキュリティ】）。"),
    ("Data migration / データ移行",
     "No data migration: 01 and 02 define none, and what the gateway replaces is still open (01 Q-2).",
     "データ移行なし：01・02に定義がなく、置き換え対象も未確定（01 Q-2）。"),
    ("Support hours / サポート時間",
     "On-call covers business hours (01 OPS-006, Q-6 open). 24x7 on-call would increase the Operation rows.",
     "オンコールは業務時間帯を前提（01 OPS-006、Q-6未確定）。24時間365日対応の場合、運用の行が増える。"),
    ("Logging volume / ログ量",
     "The LiteLLM S3 metadata callback writes in batches (about 100 records per object). If it writes one object per request, PUT and archive-transition charges rise by roughly USD 250 per month from month 13 (to be checked on the pinned version).",
     "LiteLLMのS3メタデータ出力はバッチ書き込み（1オブジェクト約100件）を前提。1リクエスト1オブジェクトの場合、PUTとアーカイブ移行の料金が13か月目以降に月約250USD増える（固定バージョンで要確認）。"),
]

EXCLUSIONS = [
    ("Model inference / モデル利用料",
     "Bedrock token charges for teams' usage (charged back through LiteLLM, 01 CST-007). See the separate usage table in the markdown output.",
     "各チームの利用によるBedrockトークン料金（LiteLLMで配賦、01 CST-007）。Markdown出力の別表を参照。"),
    ("Route A / 専用線経路",
     "Private-line ingress over Direct Connect (01 NG-5, 02 D-6). Optional; priced separately in the markdown output.",
     "Direct Connect経由の専用線経路（01 NG-5、02 D-6）。オプション扱いで、Markdown出力に別途試算を記載。"),
    ("Azure OpenAI / Azure OpenAI",
     "Azure OpenAI Japan East as a second backend, with its cross-cloud private path and Azure charges (01 MDL-011, Q-4). Optional; priced separately in the markdown output.",
     "第2バックエンドとしてのAzure OpenAI（東日本）、クラウド間の閉域経路およびAzure側料金（01 MDL-011、Q-4）。オプション扱いで、Markdown出力に別途試算を記載。"),
    ("Remote access, mTLS client side / リモート・mTLS端末側",
     "Remote and home access (01 NG-1) and Intune certificate profiles for mTLS; only the gateway-side mTLS risk is in contingency.",
     "リモート・在宅アクセス（01 NG-1）およびmTLS用のIntune証明書配布。ゲートウェイ側のmTLS対応のみ予備費に計上。"),
    ("Internal staff / 社内要員",
     "Time of other internal teams for their own deliverables: Network (allowlist, egress, V-11 data), Identity (Conditional Access, app registrations), Endpoint/Intune (client deployment), Legal/privacy and FinOps approvals, users attending training.",
     "他部門の要員工数：ネットワーク（許可リスト・出口経路・V-11の情報）、ID管理（条件付きアクセス・アプリ登録）、端末/Intune（クライアント配布）、法務・FinOpsの承認、研修受講者。"),
    ("Shared platforms / 共有基盤",
     "Costs of shared platforms already paid elsewhere: network-prod firewall and NAT endpoint-hours, Direct Connect circuits, SIEM licence and ingestion (02 R-48), log-archive account, corporate Git/CI, Entra ID P1/P2, Okta and Intune licences.",
     "他で負担済みの共有基盤費用：network-prodのファイアウォール・NATの時間課金、Direct Connect回線、SIEMのライセンスと取り込み（02 R-48）、ログアーカイブアカウント、社内Git/CI、Entra ID P1/P2・Okta・Intuneのライセンス。"),
    ("Support contracts / サポート契約",
     "AWS Support plan and any LiteLLM support beyond the licence (01 Q-20).",
     "AWSサポートプランおよびライセンス外のLiteLLMサポート（01 Q-20）。"),
    ("Enhancements / 機能追加",
     "New endpoint families (01 NG-7, e.g. MCP gateway), self-hosted models on SageMaker, response caching (NG-3), and features beyond the maintenance allowance.",
     "新しいエンドポイント種別（01 NG-7、MCPゲートウェイ等）、SageMakerでのセルフホストモデル、レスポンスキャッシュ（NG-3）、保守範囲を超える機能追加。"),
    ("Expenses / 経費",
     "Travel, accommodation and on-site expenses.",
     "出張・宿泊・現地作業に伴う経費。"),
    ("Unlisted purchases / 記載外の購入",
     "Hardware or software not listed on the Estimate sheet; end-user devices and office network changes.",
     "Estimateシートに記載のないハードウェア・ソフトウェア、利用者端末および社内ネットワークの変更。"),
    ("Price changes / 価格変動",
     "Exchange-rate movements beyond JPY 160 / USD and AWS or vendor price changes after 2026-11-17.",
     "1USD＝160円を超える為替変動、および2026-11-17以降のAWS・ベンダーの価格改定。"),
    ("Legal & audit / 法務・監査",
     "Legal, regulatory or external audit fees, incl. any ISO 27001 / SOC 2 work (01 Q-19).",
     "法務・規制対応・外部監査の費用（ISO 27001／SOC 2対応を含む、01 Q-19）。"),
    ("Decommissioning / 旧システム廃止",
     "Decommissioning of anything the gateway replaces (01 Q-2 open).",
     "ゲートウェイが置き換えるものの廃止作業（01 Q-2未確定）。"),
]

# ---------------------------------------------------------------- Bedrock usage (not in totals)
# jp. (geographic CRIS, 'Standard' non-global) and In-Region prices, USD per 1M tokens, [PL Tokyo]
BR = {
    "Claude Opus 5.5":   dict(inp=4.40, cw=5.50, cr=0.22, out=22.00),
    "Claude Haiku 5.5":  dict(inp=0.11, cw=0.1375, cr=0.011, out=0.55),
    "Claude Opus 4.8":   dict(inp=5.50, cw=6.875, cr=0.55, out=27.50),
    "Claude Sonnet 4.6": dict(inp=3.30, cw=4.125, cr=0.33, out=16.50),
    "Claude Haiku 4.5":  dict(inp=1.10, cw=1.375, cr=0.11, out=5.50),
    "Amazon Nova 2 Lite": dict(inp=0.396, cw=0.0, cr=0.099, out=3.311),
    "Titan Text Embeddings V2": dict(inp=0.029, cw=0, cr=0, out=0),
    "Cohere Embed v4":   dict(inp=0.12, cw=0, cr=0, out=0),
    "Mistral Large 3":   dict(inp=0.61, cw=0, cr=0, out=1.82),
    "gpt-oss-120b":      dict(inp=0.18, cw=0, cr=0, out=0.73),
}
MDL = {"Claude Opus 5.5": "MDL-001", "Claude Haiku 5.5": "MDL-002", "Claude Opus 4.8": "MDL-003",
       "Claude Sonnet 4.6": "MDL-004", "Claude Haiku 4.5": "MDL-005", "Amazon Nova 2 Lite": "MDL-006",
       "Titan Text Embeddings V2": "MDL-007", "Cohere Embed v4": "MDL-008", "Mistral Large 3": "MDL-009",
       "gpt-oss-120b": "MDL-010"}
# interactive coding-agent profile per active user-day (M tokens), calibrated: Opus 5.5 day ≈ USD 13
DAY = dict(inp=0.6, cw=0.4, cr=12.0, out=0.25)
MIX = {"Claude Opus 5.5": 0.60, "Claude Sonnet 4.6": 0.15, "Claude Opus 4.8": 0.05, "Claude Haiku 5.5": 0.20}
SCEN = {"Low": dict(users=ENGINEERS, days=12, wl=0.25), "Expected": dict(users=ENGINEERS, days=15, wl=1.0),
        "High": dict(users=ENGINEERS, days=19, wl=3.0)}
# workloads (UC-2), expected scenario, billions of tokens per month
WL = {"Claude Haiku 4.5": dict(inp=1.0, out=0.2), "Amazon Nova 2 Lite": dict(inp=1.0, out=0.2),
      "gpt-oss-120b": dict(inp=0.3, out=0.06), "Mistral Large 3": dict(inp=0.2, out=0.04),
      "Titan Text Embeddings V2": dict(inp=0.5, out=0), "Cohere Embed v4": dict(inp=0.5, out=0)}


def usage():
    res = {}
    for s, p in SCEN.items():
        rows = {}
        for m in BR:
            t = dict(inp=0.0, cw=0.0, cr=0.0, out=0.0)
            if m in MIX:
                k = p["users"] * p["days"] * MIX[m]
                for f in t:
                    t[f] += DAY[f] * k  # M tokens
            if m in WL:
                t["inp"] += WL[m]["inp"] * 1000 * p["wl"]
                t["out"] += WL[m]["out"] * 1000 * p["wl"]
            cost = sum(t[f] * BR[m][f] for f in t)
            rows[m] = dict(tokens_m=t, total_b=sum(t.values()) / 1000, usd=cost)
        res[s] = rows
    return res


def day_cost(m):
    return sum(DAY[f] * BR[m][f] for f in DAY)


# ---------------------------------------------------------------- optional items priced separately
def options():
    # Route A: CMP §8.9 worked example re-priced with Tokyo PL rates
    dx = 1024 * P["dx_out_gb"]
    tgw = 2048 * P["tgw_gb"]
    alb = P["alb_h"] * H + 1 * P["alb_lcu"] * H
    res = 2 * P["resolver_eni"] * H
    route_a = dict(monthly_usd=dx + tgw + alb + res, parts=[
        ("DX data out 1,024 GB × 0.041", dx), ("TGW processing 2,048 GB × 0.02", tgw),
        ("Internal ALB 0.0243/h + 1 LCU", alb), ("Route 53 Resolver inbound endpoint, 2 ENIs × 0.125/h", res)],
        build_pd=15)
    az = dict(monthly_usd=1024 * P["dx_out_gb"] + 1024 * P["tgw_gb"], parts=[
        ("DX data out for prompts 1,024 GB × 0.041", 1024 * P["dx_out_gb"]),
        ("TGW processing 1,024 GB × 0.02", 1024 * P["tgw_gb"])], build_pd=20)
    return route_a, az
