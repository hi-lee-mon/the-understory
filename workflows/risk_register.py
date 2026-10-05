import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/59_research_risk_register.md（本タスクの物差し——§1 先行調査・§2 正典制約 G-RR-01〜09・§3 原則 P-RR-01〜08・§4 棚卸し H-01〜17・§5 組版テンプレは必須）
- docs/00_development_plan.md（§5 主要リスクと対策——引き継ぎ元の5行。Phase 構造・ゲート規則）
- docs/40_vertical_slice_plan.md（§9 台帳「Issue #7」行——スライス固有リスク5件＋§7 台帳・40-Q2/Q6/Q7/Q20/Q23 の承認値）
- docs/41_playtest_plan.md（§8.4 リードタイム——L2 募集4週前・配信者交渉＝最長不確定要素・§5.5 失敗モード表・§7.5.2 致命傷認定線）
- docs/57_tech_verification_plan.md（Issue #13 PoC ゲート・H-01〜H-30・設計代替——技術リスクの緩和正本）
- docs/46_distribution_research.md（JEI/Patchouli 依存・modpack 収録条件5点・両プラットフォーム公開・ライセンス方針）
- docs/32_system_specs.md（§6 個別層モデル——最大の技術リスク源）
- docs/17_streaming_design.md（配信設計——配信リスクの文脈）
- docs/19_audio_direction.md（音素材120〜180・素材権利——H-08 の母本）
- docs/30_adr/（0002 技術スタック固定・0003/0004 個別化/状態モデル——依存リスクの前提）
- AGENTS.md（作業規範——Phase 0＝設計のみ・面白さの最終決定権＝ユーザー）
- Issue #35（Mojang 没案機能の調査——法務リスク行の入力）
"""

RULES = """成果物の組版（docs/59 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 台帳行の必須フィールド：{ID（R-XX 連番）・分類・リスク記述（if/then・なぜ負かを言明）・深刻度・発生確率・現在スコア・早期警戒指標（発火トリガー）・緩和設計・発生時対処・残存リスク・状態・接続先・出典}
- 承認済みの正典値（リードタイム4週・閾値・設計代替・失敗モード表）は**引用のみ**で再定義しない——docs/42 は行を持ち接続先を指す（G-RR-03/04/05）
- 全判断に根拠（正典節／docs/59 の先行調査節・原則番号・制約番号）を付ける。感覚だけの提案は不可
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝42-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- Phase 0/Phase 1 境界を明記：本書は運用設計であり、緩和策の実施判断はユーザー・該当 Issue 側
- リスク・前提・依存を並記（P-RR-04）：前提（成り立ち条件）と依存（外部）も監視対象の行にする
"""

CONSTRAINTS = """絶対条件（docs/59 §2 の正典制約 G-RR-01〜09）：
- G-RR-01 Phase 0＝設計のみ。緩和実施の判断はユーザー・該当 Issue 側
- G-RR-02 本書は全リスクの唯一の正本——docs/40 §9・docs/41 §8.4・docs/00 §5 の行を引き継ぎ、各書の台帳行は「docs/42 参照」に置き換える提案として扱う（直接改変は要承認）
- G-RR-03 主題装置の技術リスクは Issue #13 PoC が緩和正本——設計代替の内容を docs/57 に委譲し重複記述しない
- G-RR-04 リードタイム値は docs/41 §8.4 が正——値を変えず監視トリガーとして引用
- G-RR-05 定量閾値・合格ラインは引用のみ——台帳側で再定義しない
- G-RR-06 「追加しない」判断も記録する（スコープ抑制の緩和履歴）
- G-RR-07 収益化導入は EULA 上禁止——収益系検討の発生自体を赤信号行として設計
- G-RR-08 面白さの根幹はユーザー承認——深刻度上位・方向性に関わる行は推奨案つき要承認へ
- G-RR-09 日本語・要承認は 42-U{n}-Q{m} で §4 集約・推奨案と書き戻し先明記
"""

UNITS = [
    {
        "id": "framework",
        "title": "U1：§0 位置づけ・運用ルール＋§1 評価規則（docs/42 §0〜§1）",
        "scope": "§0 位置づけ（本書の役割＝全リスクの唯一の正本・対象範囲・RAID 並記の採用——リスク/前提/依存/課題の用語定義・Phase 0 制約・Issue #7 完了条件との対応）＋§1 評価規則（深刻度×発生確率のスコア規則を先に固定——各3〜5段の定義表［深刻度は工数被害＋主題装置/配信映え/体験品質への被害の2軸＝P-RR-07］・分類カテゴリ（技術/スコープ/工数・人手/法務・IP/外部依存/スケジュール/品質/コミュニティ）・状態ライフサイクル（identified→watching→mitigating→realized→closed）・レビュー周期（週次自己点検＋Issue 完了時＋Phase 境界——P-RR-08）・エスカレーション規則（深刻度上位・確率上昇中→ユーザー承認へ——G-RR-08）・退場規則（解消条件・退場記録の扱い——P-RR-06））",
    },
    {
        "id": "ledger_tech_scope",
        "title": "U2：§2 台帳本体 A——技術・スコープ・工数系（docs/42 §2 前半）",
        "scope": "§2 リスク台帳本体の技術・スコープ・工数系の行：H-01 スコープ過大・H-02 面白さ未検証・H-03 技術難度（Issue #13 PoC 接続——次元生成/異物チャンク/個別層同期/マルチ同期の各行・設計代替は docs/57 参照）・H-04 ローカライズ・演出工数・H-05 マルチ同期・H-07 Issue #13 遅延時の並走切替・H-09 タイムボックス逸脱（80-20 の罠）・H-10 マルチ設計変更の波及・H-15 属人化・H-16 Phase 1 移行棚卸し＋これらに加え自分で検出した同系統の追加行（技術負債・設計変更波及・品質）。各行は必須フィールド全部入り・if/then 記述・早期警戒指標を具体化（例：PoC 予定からの遅延週数・見積超過反復回数）",
    },
    {
        "id": "ledger_ops_legal",
        "title": "U3：§2 台帳本体 B——人手・配信・法務・依存系（docs/42 §2 後半）",
        "scope": "§2 リスク台帳本体の人手・配信・法務・依存系の行：H-06 外部テスト人手確保（L2 募集4週前・配信者交渉＝最長不確定・L2 並行開始——41 §8.4 引用）・H-08 音素材確保（120〜180・本線自作・CC0 調達難）・H-11 IP/法務（EULA 収益化禁止の赤信号行・Modrinth 収録条件・jarJar ライセンス適合・Mojang 没案距離＝Issue #35 結果待ち・OFL フォント・音素材ライセンス）・H-12 依存エコシステム（NeoForge 1.21.1/Java 21・JEI/Patchouli/GeckoLib API 変更・保守停止・MC バージョン追随方針の明文化）・H-13 配信リスク（ネタバレ拡散・権利枠組み 41-U3-Q2・配信モード係数不整合）・H-14 品質リスク（迷子頻発・説明なし完走不能——docs/41 §5.5/§7.5.2 へ引用接続）・H-17 リードタイム早期化設計の着地行＋自分で検出した追加行（コミュニティ・倫理・募集母数枯渇）。各行は必須フィールド全部入り・if/then 記述・トリガー具体化",
    },
    {
        "id": "ops_handoff",
        "title": "U4：§3 監視運用＋§4 要承認集約＋§5 手渡し（docs/42 §3〜§5）",
        "scope": "§3 監視運用（週次自己点検・Issue 完了時・Phase 境界のレビュー契機の運用手順・行の追加/再評価/状態遷移の手順・退場記録の扱い・「誰が・いつ・どこへ記録するか」まで具体化——P-RR-05 外在化）＋§4 未決・要承認集約（42-U{n}-Q{m}——唯一の台帳・推奨案・書き戻し先・統合元つき。§0〜§2 で検出した要承認を全て集約——U1〜U3 の起票も統合時に本節へ追記する設計として集約節の書式を定める）＋§5 手渡し（docs/40 §9 台帳行の参照置換提案・docs/41 §8.4 との相互参照・Issue #8 リリース計画・Issue #12 ADR・Issue #35 法務調査・Issue #13 への接続——受け渡し項目とその着地点を表に）",
    },
]

META = {
    "name": "risk-register",
    "description": "リスク台帳 docs/42（Issue #7）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からのリスク言及棚卸し", "count": 1},
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
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝42-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出したリスク言及・監視対象の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #7（リスク台帳→docs/42）が扱うべき全項目——リスク・前提・依存・課題として記述されているもの全て**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/00 §5 主要リスク表の全5行（原文のまま）
2. docs/40 §9 台帳「Issue #7（docs/42 リスク台帳）」行のスライス固有リスク5件（原文のまま）＋§7 台帳のうちリスク性を持つ行（「外す」判断・条件付き検討行）
3. docs/41 §8.4 のリードタイム設計（L2 募集4週前・配信者交渉の不確定性）・§5.5 失敗モード表・§7.5.2 致命傷認定線——監視対象となる兆候
4. docs/57 の Issue #13 PoC ゲート項目（H-01〜H-30 のうち「失敗したらスライス構造が変わる」もの＝ゲート級）と設計代替の一覧
5. docs/46 の収録条件5点・JEI/Patchouli 依存・両プラットフォーム公開・ライセンス方針
6. docs/32 §6 個別層モデル（技術リスク最大源）・ADR-0002/0003/0004 の依存前提
7. docs/19 §8 の音素材・権利関連の要承認（120〜180素材・CC0/自作方針）
8. docs/17 の配信設計が前提とする条件（配信者到達・切り抜き需要）
9. Issue #35（Mojang 没案機能の法律リスク調査——対象と現状）
10. docs/38 各書の数値前提（没腐度閾値等——前提が崩れたらリスクになる行）
11. 「台帳に入れるべきだがどこにも書かれていない」リスク候補（単独開発・コミュニティ・倫理・ツール依存）

## 出力
inventory_md に Markdown で：各行「項目｜内容｜出典（ファイル・節）｜種別（リスク/前提/依存/課題）｜分類候補（技術/スコープ/工数・人手/法務・IP/外部依存/スケジュール/品質/コミュニティ）｜確定状況」。docs/59 §4 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のリードリスクマネージャー。{unit['title']} を、調査基準（docs/59）に基づき深い思考で執筆せよ。

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
- まず docs/59 §3 の設計原則 P-RR-01〜08 に載せてから、項目の事情で具体化する
- docs/59 §1 の先行調査（if/then 記述・現在/目標リスク・RAID・早期信号・退場設計・MC MOD 法務）を根拠に引く
- 承認済みの正典値（リードタイム4週・閾値・設計代替・失敗モード・収録条件）は引用のみ——値を変えたり独自の新値を書かない。監視トリガーとしての引用は可
- 台帳行は「発火トリガー→誰が・何を・どこへ記録して実行するか」まで書く——「発生してから考える」行を作らない（P-RR-03）
- 選択肢がある運用判断（スコア規則の段数・レビュー周期・エスカレーション基準）は**複数案比較＋推奨案つき要承認**として構造化する
- 「要承認」は 42-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/59 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」のリスク台帳レビューア。以下の設計を、docs/59 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/59 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（3段分類）
1. **正典制約適合**：G-RR-01〜09 に反する記述がないか（特に G-RR-02/03/05 の引用のみ原則・値の再定義禁止・G-RR-07 EULA 赤信号）
2. **網羅性**：担当 H 項目が全て行化・運用化されているか、台帳行の必須フィールドに欠落がないか
3. **発火可能性**：早期警戒指標が「機械的に判定できる表現」か——「様子を見る」「注意する」で終わる行がないか
4. **行動接続**：緩和設計・発生時対処が「誰が・何を・どこへ記録するか」まで書かれているか
5. **運用実在性**：単独開発で実施可能か（週次点検の負荷・記録先の具体性）——机上の空論でないか
6. **権威侵害**：docs/40/41/57/46 の承認済み値を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のリードリスクマネージャー。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/59 §4 の H-01〜17 が4ユニットのいずれかで行化・運用化されているか、§0〜§5 の必須節が揃っているか、要承認に ID・書き戻し先があるか",
        "consistency": "整合——ユニット間で前提・運用定義が食い違わないか（例：§1 のスコア規則/状態定義と §2 台帳行の記入値、§3 のレビュー周期と §1 の規則、§2 の行と §5 手渡し表の対応）、行IDの重複・欠番がないか",
        "canon": "正典整合——4ユニット全体が docs/00/40/41/46/57 の記述と矛盾しないか、承認済みの確定値を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**リスク台帳の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/59 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: リスク言及の棚卸し（抽出） ===")
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
