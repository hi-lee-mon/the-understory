import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/55_research_vertical_slice.md（本タスクの物差し——§1先行研究・§2正典制約G-VS-01〜08・§3棚卸しH1〜22・§4原則P-VS-01〜08・§5組版テンプレは必須）
- docs/00_development_plan.md（Phase 2 定義・技術選定の制約・リスク表——本書の完了条件の出典）
- docs/13_progression_map.md（章構成・序＋第1章＝1〜2時間・配信1回＝第1章クリア）
- docs/34_chapter_plots/00_prologue.md・01_moon_forest.md（序章・第1章の全内容——範囲表の母本）
- docs/34_chapter_plots/README.md（章プロット体系）
- docs/16_structures_dungeons.md（§1 総覧表・§2 共通規格・§3 序章/拠点/共通・§4 第1・2章の構造物行）
- docs/38_numeric_tables/（README・01_items・02_gear_devices・03_bosses・04_mobs_economy——第1章・序章の数値一式：N-BOS-00/01・N-MOB-001〜003・段位 T0/T1・拾得物・没腐係数）
- docs/18_ui_ux_detail.md（UI 器一式——HUD・字幕・拾得図鑑・書物器・綴じ画面・通知型・表示時間の権威）
- docs/19_audio_direction.md（第1章の音要件——§3.3-01・§4.0-4.1・幕/柝規格・環境床・拾得音）
- docs/45_nonverbal_guidance/（01 文法・02 場面適用・03 環境物語・04 a11y——第1章の導線規格）
- docs/48_fusion_elements/（01 予告頁・02 語り形式・03 幕/見得/序破急・04 演出UI線引き——幕転換・交付演出の規格）
- docs/50_opening_storyboard.md（OP Beat1-3——スライスへの序章・OP の扱いの判断材料）
- docs/14_items_crafting.md（第1章で使う器・アイテム——拾得の携行品・縁の羅針盤・名札・クラフト）
- docs/23_discard_grammar.md（ゴミ箱機構・招待状ゲート・捨てる文法——スライス基盤機構）
- docs/32_system_specs.md（死亡・没腐・転移・リスポーン・マルチ共有/個別層）
- docs/15_mobs_bosses.md・docs/25_characters.md（翁・ノミ・救出対象の仕様）
- docs/26_narrative_vectors.md（語りベクター——第1章の語り形式・VO不採用）
- docs/11_world_bible.md（世界設定——異物・縁・漂着浜）
- docs/09_redesign_fusion.md（再設計方針——次元MOD×連続ドラマの骨格）
- docs/46_distribution_research.md（依存MOD：JEI必須・Patchouli図鑑・配布形態）
- docs/17_streaming_design.md（配信適性——クリップ瞬間・30秒基準）
- docs/10_game_design_document.md（原GDD——第1章の元設計・音の基調§87）
- docs/30_adr/（ADR-0002 技術選定・0003 ゴミ箱主機構・0004 状態モデル・0005 異物）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/55 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 範囲表は必須列（項目｜含む/含まない｜品質/範囲の境界｜根拠｜受け渡し先）を全部入れる
- 仕上げ基準は「完成品質」の項目化——領域別に検証可能な合格基準まで書く（P-VS-05）
- 全判断に根拠（正典節／docs/55 の先行研究・原則番号・制約番号）を付ける。感覚だけの提案は不可
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝40-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- 承認済みの正典値（章構成・数値・幕規格・ID・依存MOD・公開方針）を再定義しない——引用のみ
- docs/40 は Phase 0 の計画書——実装コード・詳細手順ではなく「何を・どの品質で・どう検証するか」の確定（G-VS-06）
"""

CONSTRAINTS = """絶対条件（docs/55 §2 の正典制約 G-VS-01〜08）：
- G-VS-01 Phase 2＝第1章を完成品質で作り切る（地形・構造物・モブ・ボス・ロア・クラフト・演出・サウンド）・実プレイ検証が通過条件
- G-VS-02 NeoForge/MC1.21.1/Java21 前提
- G-VS-03 依存MOD：JEI必須・Patchouli（図鑑のみsoft）・自前書物器・GeckoLib+Blockbench定石
- G-VS-04 配信者ターゲット——見せる瞬間にクリップ可能な場面を含める
- G-VS-05 a11y 多系統規則を実装対象に含める（色のみ依存禁止・字幕名台帳）
- G-VS-06 本書は計画の確定までが範囲——実装指示書にしない
- G-VS-07 主題装置（没の掴み・拾得・語り・綴じ・選択の記憶）は機構として必ず残す——切るのはコンテンツ量
- G-VS-08 マルチをスライス検証対象に含めるかは要承認項目（本文で勝手に確定しない）
"""

UNITS = [
    {
        "id": "scope_def",
        "title": "U1：スライスの体験定義＋範囲表（§0〜§2）",
        "scope": "§0 位置づけと完了条件（docs/00 Phase 2 との関係・本書の役割・合格基準の概要）＋§1 スライスの体験定義（ゲームプレイループ記述＝OP/序章→漂着→第1章→救出→綴じ→村への帰還の一連・クリエイティブ支柱＝没の掴み/拾得/待つ/救出/記憶の5〜6本・モーメント一覧＝各モーメント→支柱紐付け＋クリップ可能性の注記）＋§2 範囲表（含む/含まない2欄・全資産種別＝環境・構造物・モブ・ボス・アイテム/クラフト・UI器・音・演出・物語/語り・システム・技術——各項目に品質/範囲の境界・根拠・受け渡し先。序章/OP・マルチ・再戦等の境界項目は扱いを明確化）",
    },
    {
        "id": "finish_criteria",
        "title": "U2：第1章コンテンツ仕上げ基準（§3）",
        "scope": "§3 第1章コンテンツ仕上げ基準——docs/00 Phase 2 の列挙（地形・構造物・モブ・ボス・ロア・クラフト・演出・サウンド）の8領域それぞれに「完成品質」の項目化：各領域で「何が・どの粒度で・どこまで」あれば合格かのチェック可能な基準（例：地形=環礁レイアウト・定点・月明かり演出の完成度、ボス=窓ゲート全段・予告・幕同期、a11y=多系統導線・字幕登録済みSE一式）。「good enough」の定義を各領域に明文化し、研磨のタイムボックス方針を書く（P-VS-05）。参照：docs/34/01 の全要素・38 の第1章数値・16 §4 の構造物・19 §4.1 の音・18 の UI・45 の導線・48 の幕規格",
    },
    {
        "id": "tech_verify",
        "title": "U3：基盤・技術要件＋検証計画＋工程（§4〜§6）",
        "scope": "§4 基盤・技術要件（依存MOD構成・次元生成方式・構造物生成・ボス状態遷移・カスタムフォント・環礁生成パフォーマンス・データ構造=拡張前提の形・Issue #13 技術検証との住み分け＝何を先に検証し何をスライス内で試すか）＋§5 検証計画（検証者3層=自分たち/テストプレイヤー/配信実環境・検証項目=体験/技術/a11y/配信の4系統・合格基準=各項目の測定方法と合否ライン・失敗時の巻き戻し方針=docs/00「面白くなければ仕様を巻き戻す」の具体化）＋§6 工程・工数測定（スライス内の作業順序・段階的マイルストーン・量産への外挿方法=スライス工数から章量産見通しを立てる手順——P-VS-08）",
    },
    {
        "id": "ledger_aggregate",
        "title": "U4：スライス外台帳＋要承認集約＋手渡し（§7〜§9）",
        "scope": "§7 スライス外台帳（範囲表で「含まない」となった全項目の一覧——いつ/なぜ/どこへ受け渡すか・再検討条件。第2〜5章・終章・響界・没腐全段階・レコード残り・補助環礁・再戦ハード・ポストゲーム等）＋§8 未決・要承認集約（40-U{n}-Q{m} ID・推奨案・書き戻し先——序章/OPの扱い・マルチ検証・完成品質の定量ライン・外部テスト方法・技術検証との順序等、docs/55 §6 の想定枠を全件処理）＋§9 手渡し一覧（Issue #6 プレイテスト計画・#13 技術検証・docs/00 Phase 2 への書き戻し・#8 リリース計画・#34 a11y・#17 配信）",
    },
]

META = {
    "name": "vertical-slice-plan",
    "description": "垂直スライス計画 docs/40（Issue #5）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からのスライス対象要素の棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・範囲整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝40-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出したスライス対象候補・未定義項目の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #5（垂直スライス計画 docs/40）が扱うべき全要素——第1章（月の森）のコンテンツ・スライスに必要な基盤・検証すべき事項・現時点で未定義の値**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/34/00・01 の全要素（序章・第1章の場所・イベント・NPC・ギミック・救出・結末——スライス範囲表の母本）
2. docs/16 §3・§4 の序章/第1章構造物行（名称・型・規模・生成方式）
3. docs/38 の序章/第1章数値（N-BOS-00/01・N-MOB-001〜003・T0/T1 段位・拾得物・没腐係数の該当行）
4. docs/19 の序章/第1章音要件（§3.3-00/01・§4.0・§4.1——SE・環境床・楽曲の該当行と素材ID）
5. docs/18 の序章/第1章で使う UI 器（HUD・字幕・拾得図鑑・書物器・綴じ画面・通知型——初回体験で必須のもの）
6. docs/45・48 の第1章導線・演出規格（定点・月光の筋・幕転換・交付演出）
7. docs/50 の OP Beat 全要素（序章/OP をスライスに含めるかの判断材料）
8. docs/14・23・32 のスライス基盤機構（拾得の携行品・羅針盤・ゴミ箱・招待状・死亡/没腐・転移・リスポーン・マルチ）
9. docs/46 の依存 MOD・docs/00 の技術制約（次元生成・構造物・ボス・フォント・環礁負荷）
10. 「スライスで検証すべきだが仕様がない」全項目（検証者層・合格基準・外部テスト方法・工数測定）
11. 第1章以降の要素でスライス外候補となるもの（第2〜5章・終章・響界・没腐全段階・レコード・補助環礁・再戦・ポストゲーム——§7 台帳の母本）

## 出力
inventory_md に Markdown で：各行「項目｜内容｜出典（ファイル・節）｜種別（環境/構造物/モブ/ボス/アイテム/UI/音/演出/物語/システム/技術/検証）｜スライス内/外の示唆｜確定状況」。docs/55 §3 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のリードプランナー。{unit['title']} を、調査基準（docs/55）に基づき深い思考で執筆せよ。

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
- まず docs/55 §4 の設計原則 P-VS-01〜08 に載せてから、要素の事情で具体化する
- 先行例（§1）を根拠に引く——「スコーピング≠見積もり」「モーメント逆引き」「good enough の定義」「速度の錯覚」等の参照明記
- 判断は「その要素を抜くとコア体験の証明が壊れるか」の軸で行う——含まない判断は全て §7 台帳行を意識する
- 数値・判定ラインは検証者が迷わない粒度まで（合格基準＝測定方法つき）
- docs/00・38・16・18・19 等が確定した値は引用のみ。変更が必要なら要承認へ
- 「要承認」は 40-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/55 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の制作現実性レビューア。以下の設計を、docs/55 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/55 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/55 §1 の失敗パターンも踏まえ3段分類）
1. **正典制約適合**：G-VS-01〜08 に反する設計がないか（特に G-VS-01 Phase 2 定義・G-VS-03 依存MOD・G-VS-05 a11y・G-VS-07 主題装置・G-VS-08 マルチ未確定の扱い）
2. **網羅性**：棚卸し項目（docs/55 §3 H1〜H22 と抽出結果）が全て回収されているか、docs/55 §5 の必須節・必須列に欠落がないか
3. **根拠**：全判断に参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：この計画だけで「何を作るか・何が合格か・何を測るか」が分かるか——曖昧な「ちゃんと作る」記述がないか
5. **スコーピング健全性**：範囲表の境界が明確か（含む/含まないの線がぼやけた項目がないか）・速度の錯覚（スライス工数→全体工数の安易な外挿）に陥っていないか
6. **権威侵害**：確定値（章構成・数値・幕規格・依存MOD・公開方針）を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか、後続 Issue への手渡しが記録されているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のリードプランナー。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/55 §3・Issue #5 の対象要素（体験定義・範囲表・仕上げ基準・技術要件・検証計画・工程・台帳・要承認・手渡し）が4ユニットのいずれかで扱われているか、必須節・必須列が揃っているか、要承認に ID・書き戻し先があるか",
        "scope_consistency": "範囲整合——ユニット間で範囲の境界が食い違わないか（範囲表の「含む/含まない」と仕上げ基準・台帳の対応、同じ要素が一方で含む・他方で含まない等の矛盾）、モーメント→支柱紐付けと範囲表の整合、技術要件と検証計画の齟齬",
        "canon": "正典整合——4ユニット全体が docs/00/13/14/16/18/19/23/32/34/38/45/46/48/50 の記述と矛盾しないか、承認済みの確定値を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**垂直スライス計画の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/55 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: スライス対象要素の棚卸し（抽出） ===")
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

    cov_check, scope_check, canon_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "scope_consistency", inventory), phase="crosscheck", label="cc-scope", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("scope_consistency", scope_check), ("canon", canon_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "scope_consistency": scope_check, "canon": canon_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
