"""Japanese strings for md.py (jp). Keys are the exact English strings."""
import re

LIK = {"Low": "低", "Medium": "中", "High": "高"}


def RX(s, T):
    m = re.match(r"^(.*); must pass before first pilot user \(01 §1\.4\)$", s)
    if m:
        return f"{m.group(1)}。最初のパイロット利用者の受け入れ前に合格が必要（01 §1.4）"
    m = re.match(r"^Per month equivalent\. (.*)$", s)
    if m:
        return "月額換算。" + T(m.group(1))
    m = re.match(r"^Per month\. (.*)$", s)
    if m:
        return "月額。" + T(m.group(1))
    m = re.match(r"^02 §14 (R-\d+) \(likelihood (Low|Medium|High) = (\d+) %\)\. Expected value = impact × likelihood \(A7\)\. (.*)$", s)
    if m:
        return f"02 §14 {m.group(1)}（発生可能性：{LIK[m.group(2)]}＝{m.group(3)}%）。期待値＝影響額×発生確率（A7）。" + T(m.group(4))
    m = re.match(r"^Launch gate (V-\d+): (.*)$", s)
    if m and m.group(2) in JA:
        return f"ローンチゲート {m.group(1)}：{JA[m.group(2)]}"
    return None


JA = {
    # ---- Summary
    "Project name / 案件名": "案件名",
    "Internal LLM gateway on AWS (build and 24-month operation)": "社内LLMゲートウェイ（AWS）構築・24か月運用",
    "Estimate version / 版数": "版数",
    "Estimate date / 作成日": "作成日",
    "Prepared by / 作成者": "作成者",
    "Claude (AI assistant), for platform engineering": "Claude（AIアシスタント）、プラットフォームエンジニアリング向け",
    "Status / ステータス": "ステータス",
    "Draft / 作成中": "作成中",
    "PM cost (% of development cost) / PM費率": "PM費率（開発費に対する%）",
    "Template default kept; the design docs give no reason to change it.": "テンプレート既定値。設計文書に変更する根拠がないため維持。",
    "Contingency (% of cost) / 予備費率": "予備費率",
    "Template default kept. Identified risks from 02 §14 are added as line items (§2, Contingency).": "テンプレート既定値を維持。02 §14の特定済みリスクは明細として追加（§2 予備費）。",
    "Apply contingency to recurring cost? / 継続費用にも予備費を適用": "継続費用にも予備費を適用",
    "Template default.": "テンプレート既定値。",
    "Consumption tax rate / 消費税率": "消費税率",
    "Calculated once on each total and rounded down to JPY 1.": "各合計に対して1回計算し、1円未満切り捨て。",
    "Recurring months in grand total / 総額に含める継続月数": "総額に含める継続月数",
    "Operation period of 2 years (2027-08 to 2029-07). 12- and 36-month views are in the multi-year table below.": "運用期間2年（2027年8月〜2029年7月）。12か月・36か月の試算は下の複数年試算表を参照。",
    "Total initial cost (one-time) / 初期費用合計": "初期費用合計",
    "All one-time costs incl. PM and contingency": "PM費・予備費を含む全初期費用",
    "Total recurring cost – monthly / 継続費用（月額）": "継続費用（月額）",
    "Recurring rows per month (+ contingency)": "継続費用の行の月額（＋予備費）",
    "Total recurring cost – annual / 継続費用（年額）": "継続費用（年額）",
    "Monthly × 12": "月額×12",
    "Grand total (initial + 24 months recurring) / 総額": "総額（初期費用＋継続費用24か月分）",
    "Tax calculated on this total": "この合計に対して消費税を計算",
    "The same initial cost with 12, 24 (the grand total above) and 36 months of recurring cost. Model inference is excluded in every view.":
        "同じ初期費用に、継続費用12か月・24か月（上記の総額）・36か月分を加えた試算。いずれもモデル利用料は含まない。",
    "Initial + first year": "初期費用＋初年度",
    "Initial + operation period (grand total)": "初期費用＋運用期間（総額）",
    "Initial + 3 years": "初期費用＋3年間",
    "Line items not in any total (JPY) / 集計漏れ金額": "集計漏れ金額（円）",
    "Rows with quantity but no amount / 単価未設定の行数": "単価未設定の行数",
    "CHECK (deliberate): the LiteLLM Enterprise licence placeholder has no price yet (01 Q-17, owner: Product owner). All other rows are priced.":
        "CHECK（意図的）：LiteLLM Enterpriseライセンスの仮行に価格が未設定（01 Q-17、オーナー：プロダクトオーナー）。その他の行はすべて価格設定済み。",
    "Rows with unit 'one-time' marked Recurring / 一式×継続の行数": "一式×継続の行数",
    "PM line items while PM % > 0 / PM費の二重計上": "PM費の二重計上",
    "The workbook could not be recalculated with LibreOffice in this environment (not installed). The Summary values above were computed independently in Python with the workbook's formulas (unit cost lookup, ROUND for PM and contingency, ROUNDDOWN for tax); Excel recalculates the workbook when it is opened.":
        "この環境にはLibreOfficeがないため、ブックの再計算はできませんでした。上記のサマリー値は、ブックと同じ計算式（単価参照、PM費・予備費のROUND、消費税のROUNDDOWN）を用いてPythonで独立に計算したものです。ExcelではブックをÉ開いた時点で再計算されます。".replace("É", ""),
    "1. Phase-based costs / 工程別費用": "1. 工程別費用",
    "No rows: no data migration in 01/02 (A16)": "明細なし：01・02にデータ移行の定義なし（A16）",
    "Subtotal – phase-based / 小計（工程別）": "小計（工程別）",
    "One-time part = development cost": "初期費用部分＝開発費",
    "2. Cross-cutting costs / 横断費用": "2. 横断費用",
    "No bottom-up PM rows": "積上げのPM明細なし",
    "Project management: 10.0% of development cost / PM費（自動計算）": "PM費（自動計算：開発費の10.0%）",
    "PM % × development cost": "PM費率×開発費",
    "LiteLLM Enterprise licence not priced yet": "LiteLLM Enterpriseライセンスは価格未設定",
    "Identified risks at expected value (02 §14)": "特定済みリスクを期待値で計上（02 §14）",
    "Contingency buffer: 15.0% of initial and recurring cost / 予備費（自動計算）": "予備費（自動計算：初期費用・継続費用の15.0%）",
    "Contingency % × cost before contingency": "予備費率×予備費控除前の費用",
    "Subtotal – cross-cutting / 小計（横断）": "小計（横断）",
    "Total (excl. tax) / 合計（税抜）": "合計（税抜）",
    "Development cost (base for PM %) / 開発費": "開発費（PM費の算定基礎）",
    "One-time costs of all phase-based categories": "工程別費用のうち初期費用の合計",
    "Initial cost before contingency / 予備費控除前の初期費用": "予備費控除前の初期費用",
    "All one-time costs except the Contingency category (incl. calculated PM)": "予備費カテゴリを除く全初期費用（自動計算のPM費を含む）",
    "Recurring cost before contingency (monthly) / 予備費控除前の継続月額": "予備費控除前の継続月額",
    "Used because contingency applies to recurring": "継続費用にも予備費を適用するため使用",
    "Total one-time effort / 初期工数合計": "初期工数合計",
    "person-months": "人月",
    "Person-months + person-days ÷ 20 (One-time rows)": "人月＋人日÷20（初期費用の行）",
    "Testing share of development cost / テスト比率": "テスト比率（開発費に対する割合）",
    "Typical range 20–30%": "一般的な範囲は20〜30%",
    # ---- Estimate intro
    "Subtotal = Quantity × Unit cost. **Recurring rows show the cost per month.** Prices for monthly fees and one-time items are entered in column J (Unit cost override) in Excel; here they are shown directly as the unit cost. The bold subtotal rows are for reading convenience. In Excel each category also has a blank spare row with formulas. [PL] = AWS Price List API offer file for the region, checked 2026-11-17; USD amounts are converted at JPY 160/USD.":
        "小計＝数量×単価。**継続費用の行は月額です。** 月額料金・一式の価格はExcelではJ列（単価手入力）に入力しますが、ここでは単価として直接表示しています。太字の小計行は読みやすさのためのものです。Excelでは各カテゴリに数式入りの空行もあります。[PL]＝各リージョンのAWS Price List API価格ファイル（2026-11-17確認）。USD金額は1USD＝160円で換算。",
    "1. PHASE-BASED COSTS / 工程別費用": "1. 工程別費用",
    "2. CROSS-CUTTING COSTS / 横断費用": "2. 横断費用",
    "Subtotal": "小計",
    "per month": "月額",
    "*No line items: 01 and 02 define no data migration; what the gateway replaces is open (01 Q-2).*":
        "*明細なし：01・02にデータ移行の定義がなく、ゲートウェイが置き換える対象も未確定（01 Q-2）。*",
    "*No line items: PM is calculated on Summary (PM % x development cost).*":
        "*明細なし：PM費はSummaryで計算（PM費率×開発費）。*",
    # ---- labor rows
    "Close the 20 open questions in 01 §9 and confirm assumptions AS-1–AS-21 with their 8 owner teams; update 01 to v1.0":
        "01 §9の未決事項20件を解決し、前提AS-1〜AS-21を8つのオーナーチームと確認、01をv1.0に更新",
    "01 §9 (Q-1–Q-20, due 2026-12-18 / 2027-01-29), 01 §3. Sizing: ~0.75 pd per question incl. workshop and write-up":
        "01 §9（Q-1〜Q-20、期限2026-12-18／2027-01-29）、01 §3。算定：1件あたり約0.75人日（ワークショップと記述を含む）",
    "Requirements review and approval (security, legal/privacy, network, FinOps, platform lead)":
        "要件のレビューと承認（セキュリティ、法務／プライバシー、ネットワーク、FinOps、プラットフォームリード）",
    "01 header Approvers, 01 §11, REG-003. Sizing: 2 review rounds × 2 pd": "01ヘッダーの承認者、01 §11、REG-003。算定：レビュー2回×2人日",
    "Design v0.2: close uncovered requirements and High risks — Osaka egress and secrets copy (R-7), failover health check (R-8), AVL-001, spend-log store (R-1), profile granularity (R-12), data-tier choices (R-23), content logging if needed (PRV-002, R-6)":
        "設計v0.2：未対応の要件と高リスクの解消 — 大阪の出口経路とシークレット複製（R-7）、フェイルオーバーのヘルスチェック（R-8）、AVL-001、利用ログの格納先（R-1）、推論プロファイルの粒度（R-12）、データ層の選定（R-23）、必要ならコンテンツログ（PRV-002、R-6）",
    "02 §1.2, §14 (target 2027-01-29). Sizing: ~6 design topics × ~3 pd": "02 §1.2、§14（目標2027-01-29）。算定：設計テーマ約6件×約3人日",
    "Detailed design of remaining TBDs: accounts and environments (R-41), permission sets and break-glass (R-45), IaC tool (R-22), task sizing (R-42), routing values (R-49), request-size limit (R-17), key defaults (R-16), alert thresholds (R-39)":
        "残りのTBDの詳細設計：アカウントと環境（R-41）、権限セットと緊急用アクセス（R-45）、IaCツール（R-22）、タスクサイズ（R-42）、ルーティング設定値（R-49）、リクエストサイズ上限（R-17）、キーの既定値（R-16）、アラートしきい値（R-39）",
    "02 §1.3, §4.3, §9, §10, §14. Sizing: ~8 topics × ~2.5 pd": "02 §1.3、§4.3、§9、§10、§14。算定：約8テーマ×約2.5人日",
    "Guardrail classifier selection: evaluate Japanese-capable prompt-attack classifiers and Presidio Japanese recognizers against the Q-13 test set":
        "ガードレール分類器の選定：日本語対応のプロンプト攻撃分類器とPresidioの日本語認識器をQ-13のテストセットで評価",
    "02 §1.3, §8, D-9, R-10; 01 SEC-008, Q-13. Sizing: 3 candidates × 3 pd + report": "02 §1.3、§8、D-9、R-10。01 SEC-008、Q-13。算定：候補3件×3人日＋報告",
    "Early spikes on a sandbox: master-key UI login (R-2/V-3), Codex CLI Responses API (R-4), ARN pricing (R-5), SCIM key blocking (R-35)":
        "サンドボックスでの先行検証：マスターキーでのUIログイン（R-2／V-3）、Codex CLIのResponses API（R-4）、ARNの価格計算（R-5）、SCIMによるキー無効化（R-35）",
    "02 §14 mitigations 'run early'. Sizing: 4 spikes × 2.5 pd": "02 §14の対策「早期に実施」。算定：検証4件×2.5人日",
    "Design review and approval (security, network, platform lead, FinOps, SRE), incl. Security sign-off of R-48 parameters":
        "設計のレビューと承認（セキュリティ、ネットワーク、プラットフォームリード、FinOps、SRE）。R-48のパラメータに対するセキュリティの承認を含む",
    "02 header Approvers, R-48. Sizing: 2 rounds + 1 pd follow-up": "02ヘッダーの承認者、R-48。算定：レビュー2回＋フォローアップ1人日",
    "IaC for both regions: VPC/subnets/endpoints, ALB + WAF, ECS services, Aurora Global Database, ElastiCache, S3/KMS/Secrets, SCP and Config rules, Route 53 failover, TGW attachment":
        "両リージョンのIaC：VPC／サブネット／エンドポイント、ALB＋WAF、ECSサービス、Aurora Global Database、ElastiCache、S3／KMS／Secrets、SCPとConfigルール、Route 53フェイルオーバー、TGWアタッチメント",
    "02 §2.2, §6, §8, §9; OPS-002, D-8 (start from the AWS sample [CMP §3.1]). Sizing: ~20 components, one codebase for 4 environments":
        "02 §2.2、§6、§8、§9。OPS-002、D-8（AWSサンプルを起点［CMP §3.1］）。算定：構成要素約20、4環境を1つのコードで管理",
    "LiteLLM configuration and model catalog: config.yaml for 10 catalog models + aliases, Japan-only fallbacks, custom pricing per profile, application inference profiles, content-off settings, SSO/team-sync settings, key upper bounds":
        "LiteLLMの設定とモデルカタログ：カタログ10モデルと別名のconfig.yaml、国内限定のフォールバック、プロファイルごとの個別価格、アプリケーション推論プロファイル、コンテンツ非保存の設定、SSO／チーム同期の設定、キーの上限値",
    "Self-hosted in-VPC guardrail service: Presidio with Japanese recognizers, classifier service, LiteLLM pre-call integration, failure behaviour, metadata-only logging, container hardening":
        "VPC内のセルフホスト型ガードレールサービス：日本語認識器付きPresidio、分類器サービス、LiteLLMの呼び出し前連携、障害時の挙動、メタデータのみのログ、コンテナの堅牢化",
    "02 §2.2, §8 (D-9), R-10, R-11; 01 SEC-008, SEC-009. Sizing: new service with ML model, our own scaling and patching [CMP §7.1]":
        "02 §2.2、§8（D-9）、R-10、R-11。01 SEC-008、SEC-009。算定：MLモデルを含む新規サービスで、スケーリングとパッチ適用は自社対応［CMP §7.1］",
    "Entra SSO / SCIM integration: OIDC app per environment (3), app roles → LiteLLM roles, llm-team-* team sync, SCIM deprovisioning, offboarding job if SCIM does not block keys":
        "Entra SSO／SCIM連携：環境ごとのOIDCアプリ（3つ）、アプリロール→LiteLLMロール、llm-team-*のチーム同期、SCIMによるアカウント削除、SCIMでキーが無効化されない場合の退職者処理ジョブ",
    "Key-issuance pipeline: CI for teams, budgets, model access and service-account keys; upper bounds; secret-scanning pattern for the key format":
        "キー発行パイプライン：チーム、予算、モデルアクセス、サービスアカウントキーのCI、上限値、キー形式のシークレットスキャンパターン",
    "Client package: key helper (Windows Credential Manager / macOS Keychain), Claude Code managed settings, Codex CLI config.toml (deployed by Intune team)":
        "クライアントパッケージ：キーヘルパー（Windows資格情報マネージャー／macOSキーチェーン）、Claude Codeの管理設定、Codex CLIのconfig.toml（配布はIntuneチーム）",
    "02 §2.2 client package, §4.1, D-3; 01 FUN-009. Intune deployment itself excluded (B5)": "02 §2.2 クライアントパッケージ、§4.1、D-3。01 FUN-009。Intuneによる配布自体は対象外（B5）",
    "CUR reconciliation job: daily spend export to S3 Parquet with delete-after-export, CUR 2.0 export, Athena tables, Quick Sight chargeback with residual line, AWS Budgets backstop":
        "CUR突合ジョブ：利用額のS3 Parquetへの日次エクスポート（エクスポート後に削除）、CUR 2.0エクスポート、Athenaテーブル、差額行を含むQuick Sightの配賦レポート、AWS Budgetsによる歯止め",
    "Logging / SIEM pipeline: S3 metadata callback, log groups with KMS and retention, WAF credential redaction, cross-account subscription to SIEM and log-archive, audit-log export":
        "ログ／SIEMパイプライン：S3メタデータ出力、KMSと保持期間付きのロググループ、WAFでの認証情報マスキング、SIEMとログアーカイブへのクロスアカウント転送、監査ログのエクスポート",
    "02 §7.1, §7.4; 01 OBS-001, OBS-002, OBS-004, OBS-007, SEC-015. SIEM-side ingestion excluded (B6)": "02 §7.1、§7.4。01 OBS-001、OBS-002、OBS-004、OBS-007、SEC-015。SIEM側の取り込みは対象外（B6）",
    "Metrics, dashboards and alerts: AMP + ADOT, Grafana dashboards per team/key, dependency and missing-spend alarms, key-sharing alert, synthetic availability probe":
        "メトリクス、ダッシュボード、アラート：AMP＋ADOT、チーム／キー別のGrafanaダッシュボード、依存先障害と利用額記録漏れのアラーム、キー共有アラート、合成監視による可用性プローブ",
    "02 §2.2 metrics row, R-38, R-39; 01 OBS-003, OBS-005, OBS-006, AVL-M01": "02 §2.2 メトリクスの行、R-38、R-39。01 OBS-003、OBS-005、OBS-006、AVL-M01",
    "Unit tests for custom code (guardrail service, export job, offboarding job, key helper, CI pipeline)":
        "独自コードの単体テスト（ガードレールサービス、エクスポートジョブ、退職者処理ジョブ、キーヘルパー、CIパイプライン）",
    "Sizing: ≈15 % of custom-code build effort (≈5 pm)": "算定：独自コード構築工数（約5人月）の約15%",
    "Integration, security and inspection tests T-001–T-075 on staging: automate, run, retest":
        "ステージングでの結合・セキュリティ・点検テストT-001〜T-075：自動化、実施、再テスト",
    "02 §11.1 (75 tests). Sizing: avg 0.65 pd per test incl. automation + 1 retest cycle": "02 §11.1（75テスト）。算定：1テスト平均0.65人日（自動化と再テスト1回を含む）",
    "Load and long-stream tests (T-059, T-023, T-058, T-060) and task sizing": "負荷テストと長時間ストリームのテスト（T-059、T-023、T-058、T-060）、タスクのサイジング",
    "02 §11.1, R-42, R-49; 01 PRF-M02, PRF-M04, PRF-001 (sizing basis A-9)": "02 §11.1、R-42、R-49。01 PRF-M02、PRF-M04、PRF-001（サイジング根拠A-9）",
    "No prompt content outside approved stores: canary through every model and API style, guardrail-blocked and provider-rejected requests; search every store":
        "承認済みストア以外にプロンプト内容がないこと：全モデル・全API形式、ガードレールで遮断されたリクエスト、プロバイダーが拒否したリクエストでカナリアを送信し、全ストアを検索",
    "Key creation stays within limits, incl. the two-key check": "キー作成が上限内に収まること（2キーの確認を含む）",
    "Admin UI master-key login": "管理UIへのマスターキーでのログイン",
    "Spend correct per deployment (10 deployments, with and without prompt caching)": "デプロイメントごとの利用額が正しいこと（10デプロイメント、プロンプトキャッシュの有無）",
    "Cancelled requests are metered": "キャンセルされたリクエストが計測されること",
    "Clients cannot skip tracking": "クライアントが記録を回避できないこと",
    "Clients cannot choose who pays, incl. user in two teams": "クライアントが支払チームを選べないこと（2チームに所属する利用者を含む）",
    "Database outage behaviour": "データベース障害時の挙動",
    "Licence check unavailable": "ライセンス確認ができない場合",
    "Identity endpoints unavailable": "IDエンドポイントに到達できない場合",
    "Unmanaged devices cannot reach the gateway (with Network; CIDR list and owners)": "管理外の端末がゲートウェイに到達できないこと（ネットワークチームと実施、CIDR一覧と所有者）",
    "DR drill before launch: fail over to Osaka, measure RTO/RPO, call each model available in Osaka, fail back; AZ-loss test":
        "リリース前のDR訓練：大阪へのフェイルオーバー、RTO／RPOの計測、大阪で利用可能な各モデルの呼び出し、切り戻し、AZ障害テスト",
    "02 §11.1 T-055, T-056; 01 OPS-007, AVL-M02, AVL-M03, GA exit (01 §1.4)": "02 §11.1 T-055、T-056。01 OPS-007、AVL-M02、AVL-M03、GAの完了条件（01 §1.4）",
    "AWS accounts and landing-zone onboarding for dev, staging, prod: SCP, Identity Center permission sets, break-glass, TGW attachments, budgets":
        "開発・ステージング・本番のAWSアカウントとランディングゾーンへの組み込み：SCP、Identity Centerの権限セット、緊急用アクセス、TGWアタッチメント、予算",
    "CI/CD: image mirror to ECR by digest, scan gate, promotion dev → staging → prod, config deploy, IaC plan/apply with drift check":
        "CI/CD：ダイジェスト指定でのECRへのイメージ複製、スキャンゲート、開発→ステージング→本番への昇格、設定のデプロイ、ドリフト確認付きのIaC plan／apply",
    "Bedrock setup in both regions: model access, application inference profiles, quota requests in Tokyo and Osaka, GetInferenceProfile records, invocation logging off":
        "両リージョンのBedrock設定：モデルアクセス、アプリケーション推論プロファイル、東京・大阪のクォータ申請、GetInferenceProfileの記録、呼び出しログの無効化",
    "Production and DR deployment and release": "本番・DRのデプロイとリリース",
    "02 §10 (release unit, rolling deploy)": "02 §10（リリース単位、ローリングデプロイ）",
    "Technical docs 03, 04, 06, 07, 09 written to the design, incl. rewriting the R-21 conflicts": "技術文書03、04、06、07、09を設計に合わせて作成（R-21の矛盾箇所の書き直しを含む）",
    "README doc set, 02 R-21. Sizing: 5 docs × 4 pd": "README記載の文書セット、02 R-21。算定：5文書×4人日",
    "User-facing docs 05, 08, 10 and editing of the set to the 11 §D checklist": "利用者向け文書05、08、10と、11 §Dチェックリストに沿った文書セット全体の編集",
    "README doc set, 11 §D": "README記載の文書セット、11 §D",
    "User onboarding: guide and short video, 6 live sessions for pilot and GA cohorts, team-admin training (budgets, service-account keys)":
        "利用者オンボーディング：ガイドと短い動画、パイロット・GA向けのライブ説明会6回、チーム管理者研修（予算、サービスアカウントキー）",
    "01 §1.4, UC-3, UC-5; A-9 (≈5,000 employees). Sizing: 6 sessions × 1 pd + 4 pd material": "01 §1.4、UC-3、UC-5。A-9（従業員約5,000人）。算定：6回×1人日＋教材4人日",
    "Operations handover to on-call: 07 runbook walk-through and alert drills": "オンコールへの運用引き継ぎ：07ランブックの読み合わせとアラート訓練",
    "02 §10 on-call; 01 OPS-006": "02 §10 オンコール。01 OPS-006",
    "Pilot (1 month): onboard pilot teams, triage, fixes, findings into 08": "パイロット（1か月）：パイロットチームの受け入れ、問い合わせ対応、修正、知見の08への反映",
    "01 §1.4 (pilot teams Q-3)": "01 §1.4（パイロットチームはQ-3）",
    "GA readiness: re-run launch gates on the release that goes live": "GA準備：本番に出すリリースでローンチゲートを再実行",
    "01 §1.4 GA exit, OPS-001": "01 §1.4 GAの完了条件、OPS-001",
    "Hypercare 2 weeks after GA": "GA後2週間のハイパーケア",
    "Sizing: 1.5 engineers × 10 days": "算定：エンジニア1.5人×10日",
    "On-call and incident response in support hours (business hours assumed)": "サポート時間内のオンコールとインシデント対応（業務時間帯を前提）",
    "01 OPS-006 (hours open, Q-6); 00 §1.4": "01 OPS-006（時間帯は未確定、Q-6）。00 §1.4",
    "Monitoring, alert triage and CI changes for teams, budgets, models and service-account keys": "監視、アラートの一次切り分け、チーム・予算・モデル・サービスアカウントキーのCIによる変更",
    "First-line help desk: key renewal (90-day expiry), onboarding questions": "一次ヘルプデスク：キー更新（90日の有効期限）、利用開始時の問い合わせ",
    "Monthly chargeback run and residual investigation": "月次の配賦処理と差額の調査",
    "Periodic reviews: master-key readers, audit and operator activity": "定期レビュー：マスターキーの閲覧者、監査ログと運用者の操作",
    "01 SEC-010, OBS-007 (frequency Q-8)": "01 SEC-010、OBS-007（頻度はQ-8）",
    "Recurring DR drill (assumed every 6 months × 6 pd)": "定期DR訓練（6か月ごと×6人日を前提）",
    "01 OPS-007 (interval Q-6)": "01 OPS-007（間隔はQ-6）",
    "LiteLLM upgrades with every launch gate re-run on staging (assumed quarterly, 12 pd per upgrade)": "LiteLLMの更新とステージングでの全ローンチゲート再実行（四半期ごと、1回12人日を前提）",
    "01 OPS-001; 02 §10 upgrade gate, §7.5 (R-30) [CMP §2.10]": "01 OPS-001。02 §10 更新ゲート、§7.5（R-30）［CMP §2.10］",
    "Quarterly Japan model snapshot re-check of every catalog model and catalog updates (≈3 pd per quarter)": "全カタログモデルの国内処理状況の四半期ごとの再確認とカタログ更新（四半期あたり約3人日）",
    "Patching: base images, guardrail dependencies, Aurora/Valkey minor versions, advisories": "パッチ適用：ベースイメージ、ガードレールの依存ライブラリ、Aurora／Valkeyのマイナーバージョン、セキュリティ勧告",
    "Guardrail classifier and PII-recognizer upkeep": "ガードレール分類器と個人情報認識器の保守",
    "02 R-10 (accuracy, scaling and patching are ours)": "02 R-10（精度、スケーリング、パッチ適用は自社対応）",
    "Bug fixes and minor changes to custom components": "独自コンポーネントの不具合修正と軽微な変更",
    "Guardrail service, jobs, key helper, pipelines": "ガードレールサービス、ジョブ、キーヘルパー、パイプライン",
    "Independent review of IaC and security-critical configuration (§7.3 settings, SCP, endpoint policies, WAF rules) before launch":
        "リリース前のIaCとセキュリティ上重要な設定の独立レビュー（§7.3の設定、SCP、エンドポイントポリシー、WAFルール）",
    "Phase-gate reviews: design, build complete, launch readiness, GA": "フェーズゲートレビュー：設計、構築完了、リリース準備、GA",
    "01 §1.4 exit criteria. 4 gates × 1 pd": "01 §1.4 完了条件。4ゲート×1人日",
    "LiteLLM Enterprise licence (Admin UI SSO for all users, SCIM, audit logs) — PRICE NEEDED": "LiteLLM Enterpriseライセンス（全利用者の管理UI SSO、SCIM、監査ログ） — 価格未定",
    "[CMP A-6]; 01 AS-6, CON-2, Q-17; 02 R-36. No public price: J left blank on purpose so the check flags it. Ask the vendor for a monthly-equivalent price incl. the project months (dev/staging SSO)":
        "［CMP A-6］。01 AS-6、CON-2、Q-17。02 R-36。公開価格なし：チェックで検出されるよう意図的にJ列を空欄。プロジェクト期間（開発・ステージングのSSO）を含む月額換算価格をベンダーに確認",
    "Security design review: threat model and residual-risk acceptance, R-48 parameters, guardrail failure mode, SCP review":
        "セキュリティ設計レビュー：脅威モデルと残存リスクの受容、R-48のパラメータ、ガードレールの障害時モード、SCPのレビュー",
    "Third-party penetration test before launch": "リリース前の第三者ペネトレーションテスト",
    "02 §8.3 (R-48). Price = template sample value, placeholder until a vendor quote (Security)": "02 §8.3（R-48）。価格はテンプレートのサンプル値で、ベンダー見積までの仮置き（セキュリティ）",
    # ---- infrastructure rows
    "Dev environment during the project (Tokyo)": "プロジェクト期間中の開発環境（東京）",
    "Staging environment during the project (Tokyo, production topology at minimum scale)": "プロジェクト期間中のステージング環境（東京、本番と同構成・最小規模）",
    "Production Tokyo before GA (build and pilot)": "GA前の本番環境（東京）（構築とパイロット）",
    "DR Osaka before GA (build and DR drill)": "GA前のDR環境（大阪）（構築とDR訓練）",
    "Bedrock tokens used by the platform team during the project (development, tests, launch gates, DR drill)": "プロジェクト期間中に基盤チームが使うBedrockトークン（開発、テスト、ローンチゲート、DR訓練）",
    "Sizing: dev use ≈ USD 300/month × 6 + functional/gate tests ≈ USD 250 + load test on Haiku 5.5 (360k req × 1.2k tokens) ≈ USD 80 → ≈ USD 2,130. Prices: §usage table. Not charged back":
        "算定：開発での利用 約USD 300／月×6＋機能・ゲートテスト 約USD 250＋Haiku 5.5での負荷テスト（36万リクエスト×1.2kトークン）約USD 80 → 約USD 2,130。単価は§7の表。配賦対象外",
    "Dev environment after GA (Tokyo)": "GA後の開発環境（東京）",
    "Staging environment after GA (Tokyo)": "GA後のステージング環境（東京）",
    "Fargate: LiteLLM gateway tasks": "Fargate：LiteLLMゲートウェイのタスク",
    "02 §9 (min 3 tasks, 3 AZs; size open R-42); [CMP §4.9]; avg 4 = 3 off-peak, 6 at business-hour peak (A-9)": "02 §9（最小3タスク、3AZ、サイズは未確定R-42）、［CMP §4.9］。平均4＝閑散時3、業務時間帯のピーク時6（A-9）",
    "Fargate: in-VPC guardrail service (Presidio + classifier, CPU)": "Fargate：VPC内ガードレールサービス（Presidio＋分類器、CPU）",
    "02 §2.2, §8, D-9; classifier not chosen (R-10), CPU inference assumed; GPU is contingency row R-10": "02 §2.2、§8、D-9。分類器は未選定（R-10）でCPU推論を前提。GPUは予備費のR-10の行",
    "Aurora PostgreSQL (writer + reader, db.r7g.large, Multi-AZ)": "Aurora PostgreSQL（ライター＋リーダー、db.r7g.large、マルチAZ）",
    "02 §2.2, §7.1, §9 [CMP §4.7]; provisioned assumed (R-23); 90-day spend log ≈ 12 M rows ≈ 50 GB (R-1)": "02 §2.2、§7.1、§9［CMP §4.7］。プロビジョンド型を前提（R-23）。90日分の利用ログ 約1,200万行 約50GB（R-1）",
    "ElastiCache Valkey (2 × cache.m7g.large, Multi-AZ)": "ElastiCache Valkey（cache.m7g.large×2、マルチAZ）",
    "02 §2.2, §7.1 (counters only, no response cache); Valkey assumed (R-23)": "02 §2.2、§7.1（カウンターのみ、レスポンスキャッシュなし）。Valkeyを前提（R-23）",
    "Application Load Balancer (internet-facing)": "Application Load Balancer（インターネット向け）",
    "02 §2.2, §6 (Route B, 600 s idle); LCU from ~0.5 TB/month processed + long-lived streams": "02 §2.2、§6（Route B、アイドル600秒）。LCUは月約0.5TBの処理量と長時間ストリームから算定",
    "AWS WAF regional web ACL": "AWS WAF リージョナルWeb ACL",
    "02 §8 WAF row: IP set, rate rule, IP reputation, Known Bad Inputs, CRS, admin-path and route-block rules (~12)": "02 §8 WAFの行：IPセット、レートルール、IPレピュテーション、Known Bad Inputs、CRS、管理パスとルート遮断のルール（約12）",
    "Interface VPC endpoints (11 × 3 AZs)": "インターフェイスVPCエンドポイント（11×3AZ）",
    "02 §6 endpoint list (10) + aps-workspaces for AMP (finding F-1); 02 §12 'about 11 × 3 AZs'": "02 §6のエンドポイント一覧（10）＋AMP用のaps-workspaces（指摘F-1）。02 §12「約11×3AZ」",
    "Transit Gateway VPC attachment (egress path)": "Transit Gateway VPCアタッチメント（出口経路）",
    "02 §6 egress via TGW to network-prod (AS-18); attachment billed to gateway account": "02 §6 TGW経由でnetwork-prodへの出口（AS-18）。アタッチメントはゲートウェイのアカウントに課金",
    "Network Firewall (network-prod): incremental GB only": "Network Firewall（network-prod）：GB課金の増分のみ",
    "02 §6, D-12 [CMP §4.6]; Entra/licence traffic only": "02 §6、D-12［CMP §4.6］。Entra／ライセンス確認の通信のみ",
    "NAT gateway (network-prod): incremental GB only": "NATゲートウェイ（network-prod）：GB課金の増分のみ",
    "Data transfer out to office/DC clients (responses)": "オフィス／DCのクライアントへのデータ転送（レスポンス）",
    "Route B over internet (02 §6); 4 M responses × 20 KB SSE + 25 % overhead": "インターネット経由のRoute B（02 §6）。400万レスポンス×20KB（SSE）＋オーバーヘッド25%",
    "Secrets Manager": "Secrets Manager",
    "02 §7.1: master, salt, licence, DB, SSO client, CI admin key, Valkey AUTH, spare": "02 §7.1：マスター、ソルト、ライセンス、DB、SSOクライアント、CI管理キー、Valkey AUTH、予備",
    "KMS customer-managed keys": "KMSカスタマー管理キー",
    "S3 (metadata, spend export, CUR, ALB logs, archive)": "S3（メタデータ、利用額エクスポート、CUR、ALBログ、アーカイブ）",
    "02 §7.1; metadata ~6 GB/month, batched writes (A18); 1 year hot then archive": "02 §7.1。メタデータ月約6GB、バッチ書き込み（A18）。1年間は通常保存、その後アーカイブ",
    "CloudWatch Logs, alarms and metrics": "CloudWatch Logs、アラーム、メトリクス",
    "02 §7.1, §7.4: container INFO 6 GB, WAF 6 GB, VPC Flow 5 GB; 90 days hot; OBS-006 alarms": "02 §7.1、§7.4：コンテナINFOログ6GB、WAF 6GB、VPCフローログ5GB。90日間保持。OBS-006のアラーム",
    "Amazon Managed Service for Prometheus": "Amazon Managed Service for Prometheus",
    "02 §2.2 metrics row; LiteLLM labels by team/key/model (cardinality assumption)": "02 §2.2 メトリクスの行。LiteLLMのチーム／キー／モデル別ラベル（系列数は前提値）",
    "Amazon Managed Grafana": "Amazon Managed Grafana",
    "02 §2.2 (OBS-003); users: platform 5 editors; on-call, SOC, FinOps 15 viewers (assumption)": "02 §2.2（OBS-003）。利用者：基盤チームの編集者5人、オンコール・SOC・FinOpsの閲覧者15人（前提値）",
    "ECR image storage": "ECRイメージ保存",
    "02 §2.2, SEC-016: pinned LiteLLM and guardrail images, ~10 versions kept": "02 §2.2、SEC-016：固定したLiteLLMとガードレールのイメージ、約10バージョン保持",
    "Route 53 hosted zone and failover health check": "Route 53ホストゾーンとフェイルオーバー用ヘルスチェック",
    "02 §2.2 DNS row, §9 (R-8)": "02 §2.2 DNSの行、§9（R-8）",
    "Chargeback: CUR 2.0, Athena, Quick Sight, Budgets": "配賦：CUR 2.0、Athena、Quick Sight、Budgets",
    "02 §2.2 billing row, §5 [CMP §4.5]; readers = FinOps + department contacts (assumption); Quick Sight prices: aws.amazon.com/quicksight/pricing (checked 2026-11-17)":
        "02 §2.2 請求の行、§5［CMP §4.5］。閲覧者＝FinOps＋部門窓口（前提値）。Quick Sightの価格：aws.amazon.com/quicksight/pricing（2026-11-17確認）",
    "GuardDuty incl. ECS runtime monitoring": "GuardDuty（ECSランタイムモニタリングを含む）",
    "02 §2.2 threat detection, SEC-019": "02 §2.2 脅威検知、SEC-019",
    "Security Hub CSPM, AWS Config, Inspector (ECR)": "Security Hub CSPM、AWS Config、Inspector（ECR）",
    "02 §2.2, §8.3 (RES-003 Config rule, SEC-016 scanning); CloudTrail org trail first copy free": "02 §2.2、§8.3（RES-003のConfigルール、SEC-016のスキャン）。CloudTrail組織証跡の最初のコピーは無料",
    "Bedrock tokens for platform tests (gate re-runs, probe)": "基盤チームのテスト用Bedrockトークン（ゲート再実行、プローブ）",
    "OPS-001, AVL-M01; platform's own usage, not charged back": "OPS-001、AVL-M01。基盤チーム自身の利用で、配賦対象外",
    "Fargate warm standby (1 gateway + 1 guardrail task)": "Fargateウォームスタンバイ（ゲートウェイ1＋ガードレール1タスク）",
    "02 §9 D-15 warm standby; scaled out on failover; Valkey rebuilt cold, not running (finding F-4)": "02 §9 D-15 ウォームスタンバイ。フェイルオーバー時にスケールアウト。Valkeyはコールドで再構築し、平常時は稼働させない（指摘F-4）",
    "Aurora Global Database secondary (db.r7g.large) + snapshot copy": "Aurora Global Databaseのセカンダリ（db.r7g.large）＋スナップショットコピー",
    "02 §7.1, §9, AVL-M03 [CMP §4.9]": "02 §7.1、§9、AVL-M03［CMP §4.9］",
    "ALB (Osaka)": "ALB（大阪）",
    "02 §9 same allowlist on Osaka ALB": "02 §9 大阪のALBにも同じ許可リスト",
    "AWS WAF web ACL (Osaka)": "AWS WAF Web ACL（大阪）",
    "02 §9 same WAF rules": "02 §9 同じWAFルール",
    "Interface VPC endpoints (Osaka, 11 × 3 AZs)": "インターフェイスVPCエンドポイント（大阪、11×3AZ）",
    "02 §9 same IaC; could be 1 AZ in standby (saves ~USD 225)": "02 §9 同じIaC。スタンバイ中は1AZにできる（約USD 225削減）",
    "Secrets/KMS replicas and ECR replication (Osaka)": "Secrets／KMSのレプリカとECRレプリケーション（大阪）",
    "02 §2.2 (secrets copy R-7, ECR replicated to Osaka)": "02 §2.2（シークレットの複製R-7、ECRを大阪へ複製）",
    "CloudWatch, GuardDuty, Security Hub, Config (Osaka)": "CloudWatch、GuardDuty、Security Hub、Config（大阪）",
    "02 §2.2 threat detection in both regions": "02 §2.2 両リージョンでの脅威検知",
    # ---- risk rows
    "Risk R-3: mTLS becomes required (V-11 fails or A-16 unconfirmed) — ALB mutual auth, trust store, CRL job, local mTLS helper per tool":
        "リスクR-3：mTLSが必須になる（V-11不合格またはA-16未確認） — ALBの相互認証、トラストストア、CRLジョブ、ツールごとのローカルmTLSヘルパー",
    "Impact 1.5 pm. 01 SEC-003, D-4": "影響額1.5人月。01 SEC-003、D-4",
    "Risk R-3 (recurring part): AWS Private CA for workload certificates": "リスクR-3（継続部分）：ワークロード証明書用のAWS Private CA",
    "Impact USD 400/month general-purpose CA [PL ACM PCA Tokyo, 2026-11-17]": "影響額 汎用モードCA 月USD 400［PL ACM PCA 東京、2026-11-17］",
    "Risk R-7: Osaka egress path to Entra and licence endpoint, and secrets copy — design and build": "リスクR-7：大阪からEntraとライセンスエンドポイントへの出口経路、シークレットの複製 — 設計と構築",
    "Impact 0.5 pm. 01 AVL-001, 02 §9": "影響額0.5人月。01 AVL-001、02 §9",
    "Risk R-7 (recurring part): Osaka egress (1 Network Firewall endpoint + 1 NAT gateway + TGW attachment)": "リスクR-7（継続部分）：大阪の出口経路（Network Firewallエンドポイント1＋NATゲートウェイ1＋TGWアタッチメント）",
    "Impact (0.395 + 0.062 + 0.07)/h × 730 h = USD 384.71/month [PL 2026-11-17]": "影響額 (0.395 + 0.062 + 0.07)/時 × 730時間 = 月USD 384.71［PL 2026-11-17］",
    "Risk R-32: office firewall allows only fixed IPs — AWS Global Accelerator in front of the ALB": "リスクR-32：オフィスのファイアウォールが固定IPしか許可できない — ALBの前段にAWS Global Accelerator",
    "Impact 0.025/h × 730 h + 500 GB in × 0.01 DT-premium = USD 23.25/month [PL Global Accelerator 2026-11-17]; build effort in the % buffer":
        "影響額 0.025/時 × 730時間 ＋ 受信500GB × 0.01（DTプレミアム）= 月USD 23.25［PL Global Accelerator 2026-11-17］。構築工数は%予備費に含む",
    "Risk R-1: spend-log table slows key lookups — partitioning or separate store": "リスクR-1：利用ログテーブルがキー照会を遅くする — パーティション化または別ストア",
    "Impact 1.0 pm; Medium likelihood at expected volume (≈12 M rows / 90 days)": "影響額1.0人月。想定利用量（90日で約1,200万行）では発生可能性は中",
    "Risk R-10: Japanese classifier needs a GPU — SageMaker ml.g5.xlarge × 2 (2 AZs) in Tokyo": "リスクR-10：日本語分類器にGPUが必要 — 東京のSageMaker ml.g5.xlarge×2（2AZ）",
    "Impact 2 × 2.043/h × 730 h = USD 2,982.78/month [PL SageMaker Tokyo 2026-11-17]; CPU guardrail tasks would shrink (not netted)":
        "影響額 2 × 2.043/時 × 730時間 = 月USD 2,982.78［PL SageMaker 東京 2026-11-17］。CPUのガードレールタスクは減るが相殺していない",
    "Risk R-12: per-team or per-department inference profiles with team-specific model names": "リスクR-12：チーム別または部門別の推論プロファイルとチーム固有のモデル名",
    "Impact 10 pd (config, CI, V-4/V-7 re-run)": "影響額10人日（設定、CI、V-4／V-7の再実行）",
    "Risk R-6 / 01 Q-10: per-team content logging required this phase — separate store, Macie, V-1 re-run": "リスクR-6／01 Q-10：本フェーズでチーム別のコンテンツログが必要になる — 別ストア、Macie、V-1の再実行",
    "Impact 1.0 pm; whether it is needed is 01 Q-10, so Medium used instead of R-6's High": "影響額1.0人月。要否は01 Q-10のため、R-6の「高」ではなく「中」を使用",
    "Risk R-4: Codex CLI Responses API fails with non-OpenAI models — workaround": "リスクR-4：OpenAI以外のモデルでCodex CLIのResponses APIが動作しない — 回避策",
    "Impact 10 pd": "影響額10人日",
    "Risk AS-18: shared egress in network-prod not available — gateway's own Network Firewall + NAT (3 AZs)": "リスクAS-18：network-prodの共有出口経路が使えない — ゲートウェイ専用のNetwork Firewall＋NAT（3AZ）",
    "01 AS-18 (Low assumed = 25 %). Impact 3 × (0.395 + 0.062)/h × 730 h = USD 1,000.83/month [PL 2026-11-17]. Expected value = impact × likelihood (A7)":
        "01 AS-18（発生可能性：低＝25%と仮定）。影響額 3 × (0.395 + 0.062)/時 × 730時間 = 月USD 1,000.83［PL 2026-11-17］。期待値＝影響額×発生確率（A7）",
    # ---- Rates, lists, rules
    "Working days per month / 月間稼働日数: **20** (1 person-month = 20 person-days = 160 h)": "月間稼働日数：**20**（1人月＝20人日＝160時間）",
    "**OPEN ITEM (FinOps): there are no internal rates yet. These are the template's sample rates (indicative blended market rates, excl. tax), kept unchanged; replace them on the Rates sheet.**":
        "**【未決事項・FinOps】社内単価はまだありません。以下はテンプレートのサンプル単価（参考の平均相場、税抜）をそのまま使用したものです。Ratesシートで置き換えてください。**",
    "rows": "行",
    "No rate: prices in column J": "単価なし：価格はJ列",
    "Unchanged from the template: units person-months / person-days / monthly fee / one-time; types One-time / Recurring; the 10 phase-based and 6 cross-cutting categories in the breakdown above.":
        "テンプレートから変更なし：単位は人月／人日／月額／一式、種別は初期／継続、カテゴリは上記内訳の工程別10種と横断6種。",
    "Unit cost / 単価": "単価",
    "Override (column J) if entered, else role rate from Rates (monthly for person-months, daily for person-days)": "J列（単価手入力）があればその値、なければRatesの役割単価（人月は月単価、人日は日単価）",
    "Subtotal / 小計": "小計",
    "Quantity × Unit cost": "数量×単価",
    "Development cost / 開発費": "開発費",
    "Sum of one-time costs in phase-based categories": "工程別費用のうち初期費用の合計",
    "Project management / PM費": "PM費",
    "Contingency / 予備費": "予備費",
    "Contingency % × initial cost before contingency, + contingency % × monthly recurring cost; plus identified-risk line items": "予備費率×予備費控除前の初期費用＋予備費率×継続月額、および特定済みリスクの明細",
    "Total initial cost / 初期費用": "初期費用合計",
    "All one-time costs (phase-based + cross-cutting, incl. PM and contingency)": "全初期費用（工程別＋横断、PM費・予備費を含む）",
    "Recurring – monthly / 継続月額": "継続月額",
    "Sum of recurring rows (+ recurring contingency)": "継続費用の行の合計（＋継続費用の予備費）",
    "Grand total / 総額": "総額",
    "Initial cost + monthly recurring × 24 months": "初期費用＋継続月額×24か月",
    "Consumption tax / 消費税": "消費税",
    "Each total × tax rate, calculated once per total, rounded down to JPY 1": "各合計×税率。合計ごとに1回計算し、1円未満切り捨て",
    # ---- model usage
    "Model inference is a variable cost that LiteLLM charges back to the teams that use it (01 CST-007, 02 §5), so it is an exclusion (B1) and not part of the totals above. This table sizes it for budgeting by the teams and FinOps. Prices are the Bedrock on-demand prices for the `jp.` geographic cross-Region profiles (the non-global 'Standard' SKUs, about 10 % above Global) and the In-Region Tokyo prices, from [PL] AmazonBedrock and AmazonBedrockFoundationModels, ap-northeast-1, checked 2026-11-17.":
        "モデル利用料はLiteLLMが利用チームに配賦する変動費（01 CST-007、02 §5）のため対象外（B1）とし、上記の合計には含めません。本表は各チームとFinOpsが予算を立てるための試算です。単価は`jp.`地域クロスリージョン推論プロファイル（グローバル以外の「Standard」SKU、グローバルより約10%高い）と東京リージョン内のBedrockオンデマンド価格で、[PL] AmazonBedrockおよびAmazonBedrockFoundationModels（ap-northeast-1、2026-11-17確認）によります。",
    "Note: [PL] lists Claude Haiku 5.5 at USD 0.11 / 0.55 per million input / output tokens, below Claude Haiku 4.5 (USD 1.10 / 5.50). The estimate uses the listed price; re-check it before the budget is fixed. MDL-011 (Azure OpenAI) is not priced (B3).":
        "注：[PL]ではClaude Haiku 5.5が入力／出力100万トークンあたりUSD 0.11／0.55で、Claude Haiku 4.5（USD 1.10／5.50）より安く掲載されています。本見積は掲載価格を使用しますが、予算確定前に再確認してください。MDL-011（Azure OpenAI）は試算していません（B3）。",
    "Active coding-agent users per month": "月間のアクティブなコーディングエージェント利用者数",
    "CMP A-9: ~5,000 employees, ~300 concurrent at peak (low = peak concurrency, expected 20 %, high 40 % of employees)": "CMP A-9：従業員約5,000人、ピーク同時約300人（低＝ピーク同時数、想定＝従業員の20%、高＝40%）",
    "Active days per user per month": "利用者1人あたりの月間利用日数",
    "Claude Code cost docs (code.claude.com/docs/en/costs, checked 2026-11-17): enterprise average ≈ USD 13 per developer per active day and USD 150–250 per month → 12–19 active days":
        "Claude Codeのコストに関する文書（code.claude.com/docs/en/costs、2026-11-17確認）：企業平均は開発者1人の利用日あたり約USD 13、月USD 150〜250 → 月12〜19日",
    "Tokens per active user-day (M): input / cache write / cache read / output": "利用者1人1日あたりのトークン（100万）：入力／キャッシュ書込／キャッシュ読込／出力",
    "Calibrated so a full day on Claude Opus 5.5 at `jp.` prices costs ≈ USD 13 (": "`jp.`価格でClaude Opus 5.5を1日使うと約USD 13になるよう調整（",
    "Model mix for coding agents": "コーディングエージェントのモデル構成比",
    "Opus 5.5 60 %, Haiku 5.5 20 %, Sonnet 4.6 15 %, Opus 4.8 5 %": "Opus 5.5 60%、Haiku 5.5 20%、Sonnet 4.6 15%、Opus 4.8 5%",
    "Assumption; 01 §6.5 UC-1 models (Q-4 open)": "前提値。01 §6.5 UC-1のモデル（Q-4未確定）",
    "Workloads (UC-2), share of expected volume": "ワークロード（UC-2）、想定量に対する比率",
    "Expected per month: Haiku 4.5 1.0 B in / 0.2 B out; Nova 2 Lite 1.0 / 0.2; gpt-oss-120b 0.3 / 0.06; Mistral Large 3 0.2 / 0.04; Titan V2 and Cohere v4 embeddings 0.5 B each (assumption; 01 Q-4, Q-7)":
        "想定（月間）：Haiku 4.5 入力10億／出力2億、Nova 2 Lite 10億／2億、gpt-oss-120b 3億／6,000万、Mistral Large 3 2億／4,000万、Titan V2とCohere v4の埋め込み 各5億（前提値。01 Q-4、Q-7）",
    "Total": "合計",
    "Total per year (× 12)": "年間合計（×12）",
    "Total over the 24-month operation period": "運用期間24か月の合計",
    "Tokens include cache reads, which are most of the coding-agent volume. Excl. tax. At the expected scenario, model usage is about ": "トークン数はキャッシュ読込を含みます（コーディングエージェントの利用量の大半）。税抜。想定シナリオでは、モデル利用料はゲートウェイ自体の月額運用費の約",
    "× the gateway's own monthly running cost, which matches CMP §7.1 ('model usage dominates').": "倍で、CMP §7.1の「モデル利用料が支配的」と一致します。",
    # ---- options
    "Route A and the Azure OpenAI backend are optional in the design (01 NG-5, MDL-011; 02 D-6) and are exclusions B2 and B3. Indicative AWS-side costs, using the traffic basis of CMP §8.9 (about 1 TiB a month each way) and [PL] Tokyo rates:":
        "Route AとAzure OpenAIバックエンドは設計上オプション（01 NG-5、MDL-011。02 D-6）で、対象外B2・B3です。CMP §8.9の通信量（片方向で月約1TiB）と[PL]の東京の単価による、AWS側費用の参考値：",
    "Route A: Direct Connect ingress with internal ALB and split-horizon DNS": "Route A：内部ALBとスプリットホライズンDNSによるDirect Connect経由の入口",
    "DX data out 1,024 GB × 0.041": "DXデータ送信 1,024GB × 0.041",
    "TGW processing 2,048 GB × 0.02": "TGWデータ処理 2,048GB × 0.02",
    "Internal ALB 0.0243/h + 1 LCU": "内部ALB 0.0243/時 ＋ 1 LCU",
    "Route 53 Resolver inbound endpoint, 2 ENIs × 0.125/h": "Route 53 Resolverインバウンドエンドポイント、ENI 2個 × 0.125/時",
    "pd Infra/DevOps ≈ JPY": "人日（インフラ） 約",
    "DX ports and circuits (sunk, A-8), carrier and colocation fees, Network team time": "DXのポートと回線（既存、A-8）、通信事業者・コロケーション費用、ネットワークチームの工数",
    "Azure OpenAI Japan East over DX + ExpressRoute": "DX＋ExpressRoute経由のAzure OpenAI（東日本）",
    "DX data out for prompts 1,024 GB × 0.041": "プロンプトのDXデータ送信 1,024GB × 0.041",
    "TGW processing 1,024 GB × 0.02": "TGWデータ処理 1,024GB × 0.02",
    "pd Senior engineer ≈ JPY": "人日（シニアエンジニア） 約",
    "All Azure charges (tokens, private endpoint, ExpressRoute), colocation router [CMP §8.9], legal approval (REG-001)": "Azure側の全費用（トークン、プライベートエンドポイント、ExpressRoute）、コロケーションのルーター［CMP §8.9］、法務承認（REG-001）",
    "CMP §8.9 estimated Route A at about USD 120 a month with the US-East example TGW attachment; the gateway VPC is already attached to the TGW for egress (02 §6), so no extra attachment is counted here, and the Route 53 Resolver inbound endpoint (CMP §4.6) is added.":
        "CMP §8.9はUS-Eastの例のTGWアタッチメントを使いRoute Aを月約USD 120と試算しています。ゲートウェイのVPCは出口経路のため既にTGWに接続済み（02 §6）なので追加のアタッチメントは計上せず、Route 53 Resolverのインバウンドエンドポイント（CMP §4.6）を加えています。",
    # ---- sizing detail
    "Monthly AWS cost per environment in USD, before conversion. Production and DR are one row per component in §2; dev and staging are one row each in §2 with this breakdown.":
        "環境ごとのAWS月額（USD、円換算前）。本番とDRは§2で構成要素ごとに1行、開発とステージングは§2でそれぞれ1行とし、その内訳を示します。",
    "Production (Tokyo)": "本番（東京）",
    "DR (Osaka)": "DR（大阪）",
    "Dev (Tokyo)": "開発（東京）",
    "Staging (Tokyo)": "ステージング（東京）",
    "Fargate 1 gateway (1 vCPU/2 GB) + 1 guardrail (2 vCPU/4 GB)": "Fargate ゲートウェイ1（1vCPU/2GB）＋ガードレール1（2vCPU/4GB）",
    "Aurora db.t4g.medium single instance + 10 GB + I/O": "Aurora db.t4g.medium 単一インスタンス＋10GB＋I/O",
    "Valkey cache.t4g.small single node": "Valkey cache.t4g.small 単一ノード",
    "ALB + 1 LCU; WAF ACL + 12 rules": "ALB＋1 LCU、WAF ACL＋12ルール",
    "11 interface endpoints × 1 AZ": "インターフェイスエンドポイント11×1AZ",
    "TGW attachment (egress to Entra for SSO)": "TGWアタッチメント（SSOのためのEntraへの出口）",
    "CloudWatch, Secrets/KMS, S3, ECR, AMP share, Route 53 zone": "CloudWatch、Secrets／KMS、S3、ECR、AMPの按分、Route 53ゾーン",
    "GuardDuty, Security Hub, Config": "GuardDuty、Security Hub、Config",
    "Fargate 3 gateway (2 vCPU/4 GB) + 3 guardrail (4 vCPU/8 GB)": "Fargate ゲートウェイ3（2vCPU/4GB）＋ガードレール3（4vCPU/8GB）",
    "Aurora writer + reader db.r7g.large + storage/I/O": "Aurora ライター＋リーダー db.r7g.large＋ストレージ／I/O",
    "Valkey 2 × cache.m7g.large": "Valkey cache.m7g.large×2",
    "ALB + 2 LCU; WAF ACL + 12 rules": "ALB＋2 LCU、WAF ACL＋12ルール",
    "11 interface endpoints × 3 AZs": "インターフェイスエンドポイント11×3AZ",
    "TGW attachment": "TGWアタッチメント",
    "GuardDuty (18 vCPU), Security Hub, Config": "GuardDuty（18vCPU）、Security Hub、Config",
    "Comparison with 02 §12: the comparison's sample baseline of about USD 380 a month [CMP §7.1] covers one small environment before hardening. This design adds 3-AZ production, the guardrail service, 11 interface endpoints per AZ, the Osaka standby, observability and threat detection, and keeps staging at production topology; production alone is about USD 2,870 a month.":
        "02 §12との比較：比較資料のサンプルの基準値（月約USD 380）［CMP §7.1］は、堅牢化前の小規模な1環境分です。本設計は3AZの本番、ガードレールサービス、AZごとに11のインターフェイスエンドポイント、大阪のスタンバイ、監視と脅威検知を加え、ステージングも本番と同構成としているため、本番だけで月約USD 2,870になります。",
    # ---- open items
    "Product owner": "プロダクトオーナー",
    "LiteLLM Enterprise licence price, incl. project months (01 Q-17) — the deliberate check failure": "LiteLLM Enterpriseライセンス価格（プロジェクト期間を含む、01 Q-17） — 意図的なチェック不合格の要因",
    "Licences row (J blank)": "ライセンスの行（J列空欄）",
    "Pilot and GA dates (01 Q-3); they set the project-period environment months": "パイロットとGAの日程（01 Q-3）。プロジェクト期間中の環境の月数が決まる",
    "A2, Infrastructure one-time rows": "A2、インフラの初期費用の行",
    "Model list, usage forecast and growth (01 Q-4, Q-7) for the model-usage budget": "モデル利用料の予算のためのモデル一覧、利用量予測、伸び（01 Q-4、Q-7）",
    "AWS Support plan and LiteLLM support contract (01 Q-20)": "AWSサポートプランとLiteLLMサポート契約（01 Q-20）",
    "Exclusion B7": "対象外B7",
    "Support hours, DR drill interval (01 Q-6)": "サポート時間、DR訓練の間隔（01 Q-6）",
    "Operation rows (A17)": "運用の行（A17）",
    "FinOps": "FinOps",
    "Internal labor rates to replace the template sample rates": "テンプレートのサンプル単価に代わる社内単価",
    "Rates sheet, all labor rows (A4)": "Ratesシート、全工数行（A4）",
    "Budget exchange rate (JPY 160/USD assumed)": "予算レート（1USD＝160円を前提）",
    "A9, all AWS rows": "A9、全AWSの行",
    "Quick Sight reader and Grafana viewer counts; allocation of fixed platform cost (01 Q-12)": "Quick Sightの閲覧者数とGrafanaの閲覧者数、基盤固定費の配賦方法（01 Q-12）",
    "Chargeback and Grafana rows": "配賦とGrafanaの行",
    "Security / SOC": "セキュリティ／SOC",
    "Penetration-test vendor quote (template sample JPY 2,000,000 used)": "ペネトレーションテストのベンダー見積（テンプレートのサンプル2,000,000円を使用）",
    "Security row": "セキュリティの行",
    "Guardrail classifier choice and whether it needs a GPU (R-10, Q-13)": "ガードレール分類器の選定とGPUの要否（R-10、Q-13）",
    "Guardrail Fargate row, contingency R-10": "ガードレールのFargateの行、予備費R-10",
    "SIEM ingestion path and its cost (R-48)": "SIEMの取り込み経路とその費用（R-48）",
    "Exclusion B6": "対象外B6",
    "Network": "ネットワーク",
    "Osaka egress design (R-7) and whether a fixed-IP front end is needed (R-32, Q-14)": "大阪の出口経路の設計（R-7）と固定IPのフロントエンドの要否（R-32、Q-14）",
    "Contingency R-7, R-32": "予備費R-7、R-32",
    "Confirm the shared network-prod egress can serve the gateway (AS-18)": "共有のnetwork-prod出口経路をゲートウェイが使えることの確認（AS-18）",
    "A12, contingency AS-18": "A12、予備費AS-18",
    "Platform engineering": "プラットフォームエンジニアリング",
    "Task sizing (R-42), Aurora and Valkey choices (R-23), staging scale-down policy (R-41)": "タスクのサイジング（R-42）、AuroraとValkeyの選定（R-23）、ステージングの縮退方針（R-41）",
    "Infrastructure rows (A11)": "インフラの行（A11）",
    "LiteLLM S3 callback batching on the pinned version (A18)": "固定バージョンでのLiteLLM S3出力のバッチ書き込み（A18）",
    "S3 row": "S3の行",
    "Legal / privacy": "法務／プライバシー",
    "Whether per-team content logging is needed this phase (01 Q-10)": "本フェーズでチーム別のコンテンツログが必要か（01 Q-10）",
    "Contingency R-6": "予備費R-6",
    # ---- findings
    "docs/en/ was not changed. These are gaps or inconsistencies found while pricing the design; each should be resolved in 01/02 by its owner.":
        "docs/en/は変更していません。以下は設計の費用を試算する中で見つかった不足や不整合で、それぞれのオーナーが01／02で解消してください。",
    "02 §6 lists 10 interface endpoints and allows egress only to Entra and the licence endpoint, but 02 §2.2 sends LiteLLM metrics to Amazon Managed Service for Prometheus. Remote write from private subnets needs an `aps-workspaces` endpoint (or an egress rule). The estimate prices 11 endpoints (matching 02 §12 'about 11').":
        "02 §6はインターフェイスエンドポイントを10個とし、出口をEntraとライセンスエンドポイントに限定していますが、02 §2.2ではLiteLLMのメトリクスをAmazon Managed Service for Prometheusに送ります。プライベートサブネットからのリモート書き込みには`aps-workspaces`エンドポイント（または出口ルール）が必要です。本見積は11エンドポイントで試算しています（02 §12の「約11」と一致）。",
    "CMP A-9 / 01 PRF-M02 use 50–200 RPS as the sizing basis. Sustained 50 RPS is about 130 million requests a month; at the per-request token volume of a coding agent (≈ 66k tokens) that would be model spend of several million USD a month, far above the user-based forecast in §7 (≈ 4 million requests). PRF-M02 should be set from a usage forecast (01 Q-7). Fixed capacity here is sized to the peak; per-request charges use the forecast.":
        "CMP A-9／01 PRF-M02は50〜200 RPSをサイジングの根拠としています。50 RPSが継続すると月約1億3,000万リクエストで、コーディングエージェントの1リクエストあたりのトークン量（約6.6万）ではモデル利用料が月数百万USDとなり、§7の利用者数に基づく予測（約400万リクエスト）を大きく上回ります。PRF-M02は利用量予測から設定すべきです（01 Q-7）。本見積では固定容量はピークに合わせ、従量部分は予測を使っています。",
    "02 §12 says no price was re-checked and R-46 lists the unestimated items. This estimate prices them; R-46 can point to it once reviewed.":
        "02 §12は価格を再確認していないとし、R-46は未試算の項目を挙げています。本見積はそれらを試算しているため、レビュー後にR-46から本見積を参照できます。",
    "02 §2.2 and §9 say ElastiCache is 'rebuilt cold' in Osaka without saying whether the cluster is created at failover or kept running. It affects RTO (AVL-M02) and cost; the estimate assumes it is created at failover.":
        "02 §2.2と§9は大阪のElastiCacheを「コールドで再構築」としていますが、クラスターをフェイルオーバー時に作成するのか常時稼働させるのかが書かれていません。RTO（AVL-M02）と費用に影響します。本見積はフェイルオーバー時に作成する前提です。",
    "Osaka egress and the Osaka secrets copy (R-7) have no design, so they are priced only as a contingency row.":
        "大阪の出口経路とシークレットの複製（R-7）は設計がないため、予備費の行としてのみ試算しています。",
    "02 §10 requires staging to match production for valid launch gates. Kept at production topology, staging costs about USD 2,090 a month, close to production. The design should say whether staging may scale down between upgrade windows (R-41).":
        "02 §10はローンチゲートを有効にするためステージングを本番と一致させることを求めています。本番と同構成のままでは、ステージングは月約USD 2,090と本番に近い費用になります。更新作業の合間にステージングを縮退してよいかを設計で定めるべきです（R-41）。",
    "Dev and staging also need an egress path to Entra for SSO; 02 §6 designs it only for production. The estimate assumes the same network-prod path (TGW attachment per environment).":
        "開発とステージングもSSOのためにEntraへの出口経路が必要ですが、02 §6は本番についてのみ設計しています。本見積は同じnetwork-prod経路（環境ごとにTGWアタッチメント）を前提としています。",
    "02 §7.1 moves request metadata to Glacier after one year. If the LiteLLM S3 callback writes one object per request, per-object PUT and transition charges dominate the bucket cost; batching should be part of the design (A18).":
        "02 §7.1はリクエストのメタデータを1年後にGlacierへ移行します。LiteLLMのS3出力が1リクエスト1オブジェクトで書き込む場合、オブジェクト単位のPUTと移行の料金がバケット費用の大半を占めるため、バッチ書き込みを設計に含めるべきです（A18）。",
    "Grafana and Quick Sight user counts, and who the team-facing dashboards are for (Grafana or the LiteLLM UI), are not in the design; both are per-user licences.":
        "GrafanaとQuick Sightの利用者数、およびチーム向けダッシュボードをどちら（GrafanaかLiteLLM UIか）で提供するかが設計にありません。どちらもユーザー単位の課金です。",
}

JA.update({
    '02 §9 (min 3 tasks, 3 AZs; size open R-42) [CMP §4.9]; at 30 engineers no scale-out above the minimum is expected': '02 §9（最小3タスク、3AZ、サイズは未確定R-42）［CMP §4.9］。エンジニア30人では最小構成を超えるスケールアウトは見込まない',
    '02 §2.2, §8, D-9; one task per AZ; classifier not chosen (R-10), CPU inference assumed; GPU is contingency row R-10': '02 §2.2、§8、D-9。AZごとに1タスク。分類器は未選定（R-10）でCPU推論を前提。GPUは予備費のR-10の行',
    '02 §2.2, §7.1, §9 [CMP §4.7]; provisioned assumed (R-23); 90-day spend log ≈ 3.3 M rows; 50 GB allocated with headroom (R-1)': '02 §2.2、§7.1、§9［CMP §4.7］。プロビジョンド型を前提（R-23）。90日分の利用ログ 約330万行、余裕を見て50GB（R-1）',
    '02 §2.2, §6 (Route B, 600 s idle); LCU from ~0.15 TB/month processed + long-lived streams': '02 §2.2、§6（Route B、アイドル600秒）。LCUは月約0.15TBの処理量と長時間ストリームから算定',
    'Route B over internet (02 §6); 1.09 M responses × 20 KB SSE + 25 % overhead': 'インターネット経由のRoute B（02 §6）。109万レスポンス×20KB（SSE）＋オーバーヘッド25%',
    '02 §7.1; metadata ~2 GB/month, batched writes (A18); 1 year hot then archive': '02 §7.1。メタデータ月約2GB、バッチ書き込み（A18）。1年間は通常保存、その後アーカイブ',
    '02 §7.1, §7.4: container INFO and WAF 1.5 KB per request each, VPC Flow 5 GB; 90 days hot; OBS-006 alarms': '02 §7.1、§7.4：コンテナINFOログとWAFログは各1リクエスト1.5KB、VPCフローログ5GB。90日間保持。OBS-006のアラーム',
    '02 §2.2 metrics row; LiteLLM labels by team/key/model, ~3k series at 30 engineers (assumption)': '02 §2.2 メトリクスの行。LiteLLMのチーム／キー／モデル別ラベル、エンジニア30人で約3,000系列（前提値）',
    'User onboarding: guide and short video, 2 live sessions for pilot and GA cohorts, team-admin training (budgets, service-account keys)': '利用者オンボーディング：ガイドと短い動画、パイロット・GA向けのライブ説明会2回、チーム管理者研修（予算、サービスアカウントキー）',
    '01 §1.4, UC-3, UC-5; 30 engineers (A12). Sizing: 2 sessions × 1 pd + 4 pd material': '01 §1.4、UC-3、UC-5。エンジニア30人（A12）。算定：2回×1人日＋教材4人日',
    '01 TEN-006, Q-20. 30 engineers: ≈10 key renewals a month': '01 TEN-006、Q-20。エンジニア30人：キー更新は月約10件',
    'Impact 1.0 pm; Low at 30 engineers (≈3.3 M rows / 90 days), Medium in 02 §14 at A-9 scale': '影響額1.0人月。エンジニア30人では発生可能性は低（90日で約330万行）。02 §14ではA-9の規模で中',
    '30 engineers, set by the requester on 2026-11-17 (A12); scenarios vary active days and workload volume only': 'エンジニア30人（2026-11-17に依頼者が設定、A12）。シナリオ間で変えるのは利用日数とワークロード量のみ',
    'CMP A-9 / 01 PRF-M02 use 50–200 RPS as the sizing basis. Sustained 50 RPS is about 130 million requests a month; at the per-request token volume of a coding agent (≈ 66k tokens) that would be model spend of several million USD a month, far above the forecast in §7 (≈ 1.1 million requests with 30 engineers). PRF-M02 should be set from a usage forecast (01 Q-7). This estimate uses the design minimum for fixed capacity and the forecast for per-request charges.': 'CMP A-9／01 PRF-M02は50〜200 RPSをサイジングの根拠としています。50 RPSが継続すると月約1億3,000万リクエストで、コーディングエージェントの1リクエストあたりのトークン量（約6.6万）ではモデル利用料が月数百万USDとなり、§7の予測（エンジニア30人で約110万リクエスト）を大きく上回ります。PRF-M02は利用量予測から設定すべきです（01 Q-7）。本見積では固定容量に設計上の最小構成を、従量部分に予測を使っています。',
    "Comparison with 02 §12: the comparison's sample baseline of about USD 380 a month [CMP §7.1] covers one small environment before hardening. This design adds 3-AZ production, the guardrail service, 11 interface endpoints per AZ, the Osaka standby, observability and threat detection, and keeps staging at production topology; production alone is about": '02 §12との比較：比較資料のサンプルの基準値（月約USD 380）［CMP §7.1］は、堅牢化前の小規模な1環境分です。本設計は3AZの本番、ガードレールサービス、AZごとに11のインターフェイスエンドポイント、大阪のスタンバイ、監視と脅威検知を加え、ステージングも本番と同構成としているため、本番だけで月約',
    ' a month.': 'になります。',
})

CALC = [  # ordered word replacements for calculation strings (jp)
    ("(endpoint-hours are shared, AS-18)", "（エンドポイント時間は共有、AS-18）"),
    ("(gateway-hours are shared, AS-18)", "（ゲートウェイ時間は共有、AS-18）"),
    ("(first-10-TB tier)", "（最初の10TBの料金帯）"),
    ("(AWS-endpoint checks within free 50; alias queries free)", "（AWSエンドポイントのチェックは無料枠50以内、エイリアスへの問い合わせは無料）"),
    ("(CUR export and non-action Budgets free)", "（CURエクスポートとアクションなしのBudgetsは無料）"),
    ("≈ USD 200 per full gate run × 1 run/quarter + probe on Haiku 5.5 (< USD 1)", "ゲート全実行1回 約USD 200 × 四半期1回 ＋ Haiku 5.5でのプローブ（USD 1未満）"),
    ("at Tokyo-equal Osaka rates", "（大阪の単価は東京と同額）"),
    ("replicated write I/O", "レプリケーション書込I/O"), ("replica secrets", "レプリカシークレット"), ("replica keys", "レプリカキー"),
    ("CloudTrail events", "CloudTrailイベント"), ("API calls", "API呼び出し"), ("HTTPS option", "HTTPSオプション"),
    ("logs/alarms", "ログ／アラーム"), ("flow/DNS", "フロー／DNSログ"), ("GB/month", "GB／月"),
    ("avg ", "平均"), ("tasks", "タスク"), ("nodes", "ノード"), ("endpoints", "エンドポイント"), ("AZs", "AZ"),
    ("attachment", "アタッチメント"), ("rules", "ルール"), ("requests", "リクエスト"), ("secrets", "シークレット"),
    ("CMKs", "CMK"), ("backup", "バックアップ"), ("ingest", "取り込み"), ("stored", "保存"), ("alarms", "アラーム"),
    ("metrics", "メトリクス"), ("series", "系列"), ("scrape", "スクレイプ"), ("samples", "サンプル"), ("free", "無料分"),
    ("storage", "ストレージ"), ("editors", "編集者"), ("viewers", "閲覧者"), ("zone", "ゾーン"), ("authors", "作成者"),
    ("readers", "閲覧者"), ("checks", "チェック"), ("evals", "評価"), ("rescans", "再スキャン"), ("scans", "スキャン"),
    ("events", "イベント"), ("snapshot", "スナップショット"), ("Tokyo→Osaka", "東京→大阪"), ("/h", "/時"), (" h", "時間"),
]


def calc(s):
    for a, b in CALC:
        s = s.replace(a, b)
    return s
