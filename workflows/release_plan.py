import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/60_research_release_plan.md（本タスクの物差し——§1 先行調査・§2 正典制約 G-RL-01〜14・§3 原則 P-RL-01〜09・§4 棚卸し H-01〜17・§5 組版テンプレは必須）
- docs/46_distribution_research.md（D-1〜D-7 承認済み：JEI 必須・Patchouli・両公開・modpack 条件5点・公式パック・LICENSE・サーバーイベント主経路——§8 の Issue #8 入力）
- docs/41_playtest_plan.md（§10.2 手渡し＝アルファ可否判定の入力・§2.6 公開禁止期間・§5.1.1 限定公開配信・§8.4 リードタイム・41-U1-Q10/41-U3-Q2 承認値）
- docs/42_risk_register.md（§5.2 の Issue #8 行——R-36/R-38/R-22/R-29/R-33 の残存評価消費先・42-U3-Q2/Q4/Q5 承認値）
- docs/40_vertical_slice_plan.md（§7 台帳——アルファ収録範囲の境界・§9 手渡し）
- docs/17_streaming_design.md（§7 配信者向け提供素材——紹介文・章タイトル・サムネ・導入説明・シェーダー推奨設定）
- docs/00_development_plan.md（Phase 構造・Phase 4 ローカライズ・Phase 5 リリース・広報——42-U2-Q1 英語版範囲の注記）
- docs/30_adr/0002_tech_stack.md（Accepted 昇格済み＋Consequences の保守方針——移植評価は Issue #8）
- docs/19_audio_direction.md（§9 LICENSES-AUDIO の前倒し確定）
- docs/32_system_specs.md（§9 依存構成・解禁チャネル）
- AGENTS.md（作業規範——Phase 0＝設計のみ・面白さの最終決定権＝ユーザー）
"""

RULES = """成果物の組版（docs/60 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 承認済みの正典値（D-1〜D-7・41-U系・42-U系の承認値・リードタイム・判定基準）は**引用のみ**で再定義しない——値の正本は各ソース書（G-RL-11）
- 全判断に根拠（正典節／docs/60 の先行調査節・原則番号・制約番号）を付ける。感覚だけの提案は不可
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝43-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- Phase 0/Phase 5 境界を明記：本書は公開の計画設計であり、公開・交渉・宣伝の実施は Phase 5 以降・ユーザー判断
- リスクの状態管理は docs/42 §2 が正本——本書は台帳行の接続先・残存評価の消費先として記述（G-RL-14）
- 判定・ゲートは「誰が・何を見て・どこへ記録するか」まで書く（P-RL-04/06）
"""

CONSTRAINTS = """絶対条件（docs/60 §2 の正典制約 G-RL-01〜14）：
- G-RL-01 Phase 0＝設計のみ
- G-RL-02 両プラットフォーム公開必須（D-3）
- G-RL-03 modpack 収録条件5点は公開の前提条件（D-4）
- G-RL-04 公式軽量パック（D-5）
- G-RL-05 配信者到達＝サーバーイベント主経路（D-7）
- G-RL-06 解禁判定の正本＝本書（Modrinth 公開アルファ掲載を目安——41-U1-Q10/41-U3-Q2）
- G-RL-07 実配信・公開アルファの実施は本 Issue の範囲（G-PT-08）
- G-RL-08 MC 1.21.1 固定・移植評価は本書で実施（42-U3-Q2）
- G-RL-09 LICENSES-AUDIO は Phase 1 着手まで（42-U3-Q4）
- G-RL-10 EULA 収益化禁止＝赤信号
- G-RL-11 正典値は引用のみ
- G-RL-12 面白さ根幹・公開方針はユーザー承認
- G-RL-13 日本語・要承認 43-U{n}-Q{m} 集約
- G-RL-14 リスク行の重複起票禁止（docs/42 が正本）
"""

UNITS = [
    {
        "id": "stages_gates",
        "title": "U1：§0 位置づけ＋§1 公開段階設計＋§2 段間ゲート（docs/43 §0〜§2）",
        "scope": "§0 位置づけ（本書の役割＝公開工程の唯一の計画書・対象範囲＝限定招待以降の公開全般・Phase 0 制約・完了条件対応・参照マップ・用語定義）＋§1 公開段階設計（段構成の全体図——L2 限定招待→L3 限定公開配信→公開アルファ〔alpha チャネル〕→ベータ→正式リリース→章追加リリース。各段の目的・対象層・収録範囲〔スライス端到端＝OP〜序〜第1章〜村〜帰還を基準に〕・公開物・解禁範囲を表で設計——P-RL-01 章追加の刻み・P-RL-02 ネタバレ保全）＋§2 段間ゲート（各段→次段の移行判定を「誰が・何を見て・どこへ記録」まで——公開アルファ可否判定＝docs/41 §10.2 入力〔限定招待実績・クリップ実在確認・配信所要内訳〕の消費手順・解禁判定正本〔G-RL-06〕の運用・章追加公開の判定・正式リリース化の条件）",
    },
    {
        "id": "distribution_legal",
        "title": "U2：§3 配布運用＋§4 ライセンス・法務（docs/43 §3〜§4）",
        "scope": "§3 配布運用（Modrinth/CurseForge それぞれの公開手順〔プロジェクト作成・モデレーション・必須メタデータ——§1.1 の一次情報どおり〕・バージョンチャネル運用〔alpha/beta/release の使い分け〕・環境タイプ〔client_and_server〕・依存宣言〔JEI required・Patchouli optional/embedded 等〕・版数体系〔TF 型 major.minor.build 準拠の検討——MC バージョンごとの系統〕・変更履歴規則・公式軽量パック仕様〔.mrpack/CF 両形式・本体＋JEI＋Patchouli＋前提〕・D-4 収録条件5点の公開前確認手順）＋§4 ライセンス・法務（本体 LICENSE の選択肢比較〔§1.3 表：MIT/LGPL-3.0/ARR+許諾——modpack 同梱許可・再配布・SPDX 識別子〕→推奨案・EULA 適合確認〔無償公開・再配布不含有・非公式明記〕・権利台帳 LICENSES-AUDIO.md〔Phase 1 着手まで作成——42-U3-Q4〕との接続・jarJar 同梱適合〔57-H-28 併設〕・公開停止時の撤退規則）",
    },
    {
        "id": "reach_spoiler_port",
        "title": "U3：§5 配信者到達＋§6 ネタバレポリシー＋§7 移植評価（docs/43 §5〜§7）",
        "scope": "§5 配信者到達設計（サーバーイベント主経路の運用——企画形式の選択肢比較〔自前主催/既存イベント乗合——ぶいきゃす型実績を根拠に〕・配布単位〔公式パック+サーバーテンプレ〕・導入一発化〔CF→レンタルサーバーワンクリック——docs/46 §8〕・提供素材一覧〔docs/17 §7＋パック作者・運営向け素材〕・波及設計〔見た人が自分も捨てたくなる——P-RL-09〕・Issue #17 配信者網との接続）＋§6 ネタバレ・情報開示ポリシー（公開禁止期間の解除運用＝解禁判定正本〔G-RL-06〕・公開物の情報粒度表〔説明文/スクショ/トレーラー/告知文言ごとの開示範囲——核心ネタバレの定義と除外規則〕・重大流出時の対処→R-38 接続・英語版の公開範囲〔42-U2-Q1：範囲確定は Phase 4——アルファ時の言語対応線引は要承認〕）＋§7 移植・保守評価（MC バージョン追随の評価手順——42-U3-Q2 で「リリース後に実施」と確定：評価契機・評価項目〔依存 MOD 対応状況・移植工数・ユーザー分布〕・評価記録の場・R-25 依存監視との接続）",
    },
    {
        "id": "schedule_aggregate",
        "title": "U4：§8 スケジュール＋§9 要承認集約＋§10 手渡し（docs/43 §8〜§10）",
        "scope": "§8 公開工程スケジュール（段間の依存関係と前提条件の順序組立——LICENSES-AUDIO〔Phase 1〕→D-6 LICENSE 決定→アルファ可否判定〔docs/41 入力〕→公開アルファ→正式→章追加の依存鎖・リードタイムの見積〔モデレーション期間・素材制作〕を表で——日付ではなく依存順で設計）＋§9 未決・要承認集約（43-U{n}-Q{m}——唯一の台帳・推奨案・書き戻し先・統合元つき。U1〜U3 の起票を統合時に本節へ追記する設計として集約節の書式を定める）＋§10 手渡し（消費先一覧——docs/41 §2.6/§10.2 解禁判定連動・docs/42 リスク接続〔R-36/R-38/R-22/R-29/R-33〕・Issue #17・Issue #12 ADR・Issue #35・Issue #34・Issue #5・docs/46/17/00 への参照置換提案）",
    },
]

META = {
    "name": "release-plan",
    "description": "リリース計画 docs/43（Issue #8）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からの公開・配布関連項目の棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝43-U{n}-Q{m}・推奨案・書き戻し先つき）"},
    },
    "required": ["section_md"],
}

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "accepted": {"type": "boolean"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["blocker", "major", "minor"]},
                    "issue": {"type": "string"},
                    "suggestion": {"type": "string"},
                },
                "required": ["severity", "issue"],
            },
        },
    },
    "required": ["accepted", "findings"],
}

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "inventory_md": {"type": "string", "description": "抽出した公開・配布関連項目の棚卸し（Markdown）"},
    },
    "required": ["inventory_md"],
}


async def agent_retry(*args, _tries=8, _wait=120, **kwargs):
    for i in range(_tries):
        try:
            return await agent(*args, **kwargs)
        except WorkflowAgentError as e:
            msg = str(e)
            if i == _tries - 1:
                raise
            log(f"agent retry {i+1}/{_tries}: {msg[:160]}")
            await asyncio.sleep(_wait * (i + 1))


def extract_prompt():
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #8（リリース計画→docs/43）が扱うべき全項目——公開・配布・ライセンス・配信者到達・解禁・移植評価に関わる記述全て**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/46 §7 D-1〜D-7 の承認済み決定全件（原文のまま）＋§8 の Issue #8 入力
2. docs/41：§10.2 の Issue #8 手渡し行・§2.6 公開禁止期間・§5.1.1 限定公開配信・§8.4 リードタイム・41-U1-Q10/41-U3-Q2 の承認値
3. docs/42：§5.2 の Issue #8 手渡し行・R-36/R-38/R-22/R-29/R-33 の行タイトルと残存評価・42-U3-Q2/Q4/Q5 承認値
4. docs/40：§7 台帳のうち公開・収録に関わる行・§9 手渡しの Issue #8 関連
5. docs/17 §7 配信者向け提供素材の全項目＋配信者経路の記述
6. docs/00：Phase 4（ローカライズ——英語版範囲注記）・Phase 5（リリース・広報）の記述
7. ADR-0002：技術スタック＋保守方針（移植評価は Issue #8）
8. docs/32 §9 依存構成・解禁チャネルの記述
9. docs/19 §9 の LICENSES-AUDIO 前倒し注記
10. Issue #8 本文の要件（Modrinth/CurseForge・日英対応・トレーラー素材・段階リリース）と既存コメントの手渡し全件
11. 「リリース計画に入れるべきだがどこにも書かれていない」項目候補（告知・コミュニティ導線・サポート・バージョン命名・変更履歴・モデレーション対策）

## 出力
inventory_md に Markdown で：各行「項目｜内容｜出典（ファイル・節）｜種別（決定済み/前提/未決/手渡し）｜docs/60 §4 H 番号との対応」。docs/60 §4 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のリリース計画責任者。{unit['title']} を、調査基準（docs/60）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 正典からの棚卸し（抽出済み——これを網羅的に回収せよ）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/60 §3 の設計原則 P-RL-01〜09 に載せてから、項目の事情で具体化する
- docs/60 §1 の先行調査（Modrinth/CF 仕様・TF 版数慣行・段階リリース・ライセンス比較・サーバーイベント形式）を根拠に引く
- 承認済みの正典値（D-1〜D-7・41-U 系・42-U 系・リードタイム・収録条件）は引用のみ——値を変えたり独自の新値を書かない
- ゲート・運用は「発火条件→誰が・何を見て・どこへ記録して実行するか」まで書く——「公開時に考える」設計を作らない（P-RL-04/06）
- 選択肢がある運用判断（LICENSE 選択・公開アルファ範囲・言語対応・章追加刻み・トレーラー構成・イベント形式・移植契機）は**複数案比較＋推奨案つき要承認**として構造化する
- 「要承認」は 43-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/60 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」のリリース計画レビューア。以下の設計を、docs/60 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/60 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（3段分類）
1. **正典制約適合**：G-RL-01〜14 に反する記述がないか（特に G-RL-02 両公開・G-RL-06 解禁正本・G-RL-08 移植評価・G-RL-11 引用のみ・G-RL-14 台帳権威侵害）
2. **網羅性**：担当 H 項目が全て設計に回収されているか、組版テンプレの必須節に欠落がないか
3. **ゲート実在性**：段間移行・解禁判定が「誰が・何を見て・どこへ記録」まで機械的に実施できる表現か——「時期が来たら判断」で終わる設計がないか
4. **配布運用の具体性**：チャネル別の手順・版数体系・依存宣言・モデレーション対策が一次情報（docs/60 §1.1）と食い違わないか
5. **ネタバレ保全**：公開物の情報粒度が P-RL-02 を満たすか——核心要素の除外規則が機械判定できるか
6. **権威侵害**：docs/46/41/42 の承認済み値を独自に再定義していないか・docs/42 のリスク行を重複起票していないか
7. **運用実在性**：単独開発で回る規模か（P-RL-08）
8. **要承認管理**：ID・推奨案・書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のリリース計画責任者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行設計
```markdown
{section_md}
```

## レビュー指摘
```json
{json.dumps(findings, ensure_ascii=False)}
```

出力：改訂後の section_md 全文、open_questions。"""


def crosscheck_prompt(all_sections_text, focus, inventory):
    focus_desc = {
        "coverage": "網羅性——棚卸しと docs/60 §4 の H-01〜17 が4ユニットのいずれかで回収されているか、§0〜§10 の必須節が揃っているか、要承認に ID・書き戻し先があるか",
        "consistency": "整合——ユニット間で前提・運用定義が食い違わないか（例：§1 の段構成と §2 のゲート・§3 のチャネル運用、§5 の到達設計と §6 の情報粒度、§8 スケジュールと §1〜§7 の依存関係）、ID の重複・欠番がないか",
        "canon": "正典整合——4ユニット全体が docs/46/41/42/17/00/ADR-0002 の記述と矛盾しないか、承認済みの確定値を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**リリース計画の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/60 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：元の棚卸し
```markdown
{inventory}
```

## 全ユニット設計
{all_sections_text}

出力：accepted、findings（ユニット横断の問題のみ——単一ユニット内の問題は各レビューの責任なので挙げない）。"""


async def unit_flow(unit, inventory):
    draft = await agent_retry(
        author_prompt(unit, inventory),
        phase="write", label=f"write-{unit['id']}",
        schema=SECTION_SCHEMA, repos=[REPO], soft_time_limit_minutes=55,
    )
    section_md = draft["section_md"]
    open_qs = draft.get("open_questions", "")
    previous_findings = None
    for r in range(3):
        review = await agent_retry(
            review_prompt(unit, section_md),
            phase="review", label=f"review-{unit['id']}-r{r+1}",
            schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=40,
        )
        blocking = [f for f in review["findings"] if f.get("severity") in ("blocker", "major")]
        if review["accepted"] and not blocking:
            log(f"{unit['id']}: ラウンド{r+1}で受理（minor {len([f for f in review['findings'] if f.get('severity')=='minor'])}件）")
            return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs}
        findings_key = json.dumps(sorted(review["findings"], key=lambda f: f.get("issue", "")), ensure_ascii=False)
        if findings_key == previous_findings:
            log(f"{unit['id']}: 同一指摘の繰り返し——受理して人間レビューへ")
            return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs + "\n[レビュー未解決の指摘あり]"}
        previous_findings = findings_key
        log(f"{unit['id']}: ラウンド{r+1}で指摘{len(blocking)}件——改訂へ")
        draft2 = await agent_retry(
            revise_prompt(unit, section_md, review["findings"]),
            phase="revise", label=f"revise-{unit['id']}-r{r+1}",
            schema=SECTION_SCHEMA, repos=[REPO], soft_time_limit_minutes=45,
        )
        section_md = draft2["section_md"]
        open_qs = draft2.get("open_questions", open_qs)
    log(f"{unit['id']}: レビュー3ラウンド消化——最終版を採用")
    return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs + "\n[レビュー3ラウンド後も残存指摘あり]"}


async def main():
    await register_workflow(META)
    log("=== Phase 1: 公開・配布関連項目の棚卸し（抽出） ===")
    inv = await agent_retry(
        extract_prompt(),
        phase="extract", label="extract-inventory",
        schema=EXTRACT_SCHEMA, repos=[REPO], soft_time_limit_minutes=50,
    )
    inventory = inv["inventory_md"]
    log(f"棚卸し完了（{len(inventory)} 文字）")

    log("=== Phase 2: 4ユニットの設計・レビュー・改訂ループ ===")
    results = []
    for batch in (UNITS[:2], UNITS[2:]):
        results.extend(await pipeline(batch, lambda u: unit_flow(u, inventory)))
    log("=== 4ユニット完了。横断監査へ ===")

    all_sections_text = "\n\n---\n\n".join(
        f"## {r['title']}\n\n{r['section_md']}" for r in results
    )
    log(f"全セクション合計 {len(all_sections_text)} 文字")

    cov_check, cons_check, canon_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "consistency", inventory), phase="crosscheck", label="cc-consistency", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("consistency", cons_check), ("canon", canon_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "consistency": cons_check, "canon": canon_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
