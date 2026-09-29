import asyncio
import json
import os

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/49_research_structures_dungeons.md（本タスクの物差し——§1ユニット対応・§2先行研究・§3正典制約G1〜G20・§4設計原則P-01〜P-09・§5組版テンプレ・§6レビュー基準・§7棚卸しS1〜S20は必須）
- docs/34_chapter_plots/ 全7本＋README.md（各章 §3 場所系列＝クリティカルパスの名前つき場所、§5ボス、§6結末、§8断片・落書き配置、§11要承認）
- docs/23_discard_grammar.md（捨てる文法——§5 捨て場・転移箱・§8.3 L3ごみ処理場の構造文法・§8.4 灼熱の埋立て地・§8.5 他人を捨てる儀式）
- docs/11_world_bible.md（世界構造——棄てられたものしか存在しない・異物チャンク・自分の捨て場・デカいゴミ箱・ごみ処理場）
- docs/12_story_outline.md（章概要・縁の地・感情マップ）
- docs/13_progression_map.md（進行表——序破急配分・迷子規則・章間の幕間）
- docs/25_characters.md（住人・縁の民——村の構造物の利用者）
- docs/26_narrative_vectors.md（語りベクター——環境文字上限§3.4・拾い人の手記・拾得図鑑・村報）
- docs/27_experience_sample.md（体験サンプル——実際の探索ビート）
- docs/20_art_ui_design_system.md（審美「かすれた・欠けた・継がれた」・基調パレット・素材系統）
- docs/45_nonverbal_guidance/ 全4本＋README（非言語導線の正典——導線文法・場面別適用・環境物語・アフォーダンス。構造物の発見・内部誘導の規格元）
- docs/48_fusion_elements/ 全4本＋README（幕/見得・予告頁・語り形式・幻想文字——構造物内で出る演出の規格元）
- docs/50_opening_storyboard.md（OPビート——漂着浜の最初の見え方）
- docs/36_foreshadow_map.md（伏線台帳——構造物に配置される手がかり）
- docs/38_numeric_tables/03_bosses.md（ボス数値——戦場としてのアリーナ要件）・04_mobs_economy.md（経済）
- docs/15_mobs_bosses.md（ボス一覧・見得・領域）
- docs/32_system_specs.md（システム仕様——§5 処理口・帰還・§9 外部連携）
- docs/14_items_crafting.md（拾得物・図鑑部屋・拾い人の手記収納）
- docs/17_streaming_design.md（配信構造——固有名詞化する「場」の要件）
- docs/28_story_full_flow.md（全編ストーリー）
- docs/24_story_foundation.md（物語基盤）
- docs/05_production_docs_structure.md（docs/16 の想定構成）
- docs/30_adr/（ADR の確定決裁）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/49 §5 を厳守）：
- 担当ユニットの節構成を必須どおり埋める。節構成を勝手に変えない
- 構造物一覧表は必須列（名称｜所属章・領域｜型｜規模 S/M/L｜役割｜ボス・主関係者｜生成方式｜出典）を全部入れる
- 主要構造物の詳細カードは10節テンプレ（概要と役割→由来と没理由→外観と規模→内部構成→ギミックと仕掛け→導線→演出・状態遷移→収容物→生成方式→ボス・モブ結合）を厳守
- 全ルール・仕様に根拠（正典節／docs/49 の先行研究・原則番号）を付ける。感覚だけの提案は不可
- 生成方式は4型（①固定テンプレ.nbt ②jigsaw モジュラー——プール構成案と深度 ③地形依存埋没 ④手組み領域）から明記＋processor 劣化方針
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（書き戻し先を明記し、本文で直接改変しない）
- docs/51・docs/18・docs/43 は未作成——それらを書き戻し先にする項目は「Issue #11/#3/#8 への手渡し」として記録する形に留める（G18）
- 数値の詳細（耐久・サイズ絶対値・報酬テーブル数値）は Issue #15 の領域——構造物側は「何がどこにあるか」までに留め、数値は手渡しとして記す
"""

CONSTRAINTS = """絶対条件（docs/49 §3 の正典制約 G1〜G20）：
- G1 層構造：構造物探索は表層で楽しめる。内部の物語回収は任意の深い層
- G2 環境が先：構造物の発見・侵入・進行誘導は環境（遠望・光・音・構造そのもの）で担う
- G3 操作体系不変：新規操作・専用UIを要求するギミック不可
- G4 第2〜4章は順不同：構造物の前提関係を作らない
- G5 審美「かすれた・欠けた・継がれた」＋基調パレット（docs/20）
- G6 シェーダー共存：光演出は複合表現を仕込む
- G7 二状態：主要構造物は救済前/救済後（または結末後の殻）を設計に含める
- G8 主線誘導は非言語で完結
- G9 ボス戦構造物は見得の視認性・逃げ場・リスポーン近接を確保
- G10 ノミ同行：構造内にノミが収まる動線・語りポイント
- G11 構造物を「予告映像」的に先出ししない（環境側二重化）
- G12 幕間・転換規格は docs/48/03 に従う
- G13 「見届ける」では構造物は殻として残り再入可能——結末後状態を各主要構造物に定義
- G14 幻想文字は必読情報を置かず密度規則に従う
- G15 構造物名・場所名は正典の用語どおり
- G16 正典の変更は直接書き換えず「要ユーザー承認」
- G17 配信の「場」——固有名詞として呼ばれる規模・印象
- G18 未作成 docs への書き戻しは Issue 手渡し記録に留める
- G19 世界法則：国の構造物は「漂着した/没になった」由来。捨て場・縁の地・着弾点の規則（docs/23 §5）と整合
- G20 構造物の由来は「没になったもの」：単なる廃墟でなく「没になった理由」が構造の不完全さとして刻まれている
"""

UNITS = [
    {
        "id": "common_grammar",
        "title": "U1：共通規格＋序章・拠点・環礁共通構造物（docs/16 §2〜§3）",
        "scope": "構造物設計の総則を固める。§2 共通規格：型体系と使い分け（迷路/塔/広場/洞窟/集落/試行場/埋没/特殊——黄昏の森の型の使い分け §2.1-2.2 を本作の場に翻訳）・遠望→遮蔽→開示の劇場規格・二状態（救済前後・結末後の殻）規格・生成方式の選択基準（固定/jigsaw/地形依存/手組み）・命名文法（正典造語）・導線規格（迷子回帰・ノミ収まり・非言語一次導線）。§3 序章・拠点・環礁共通構造物：漂着浜（着弾点・転移箱の口の構造形・捨て場優先規則 S2）・拾い人の村の拠点構造物群（共同箱・図鑑部屋・村報発行所・聞き役の場・縁の民の住処・訪問客滞在場——P-06 規格見本として最初に固める）・自分の捨て場（生成規則・構造形・帰還点 S4）・縁の地（現実側の隠し導線構造 S5）・異物チャンク（「世界に捨てられた地形」の構造規格——Far Lands風崩れ・存在しないブロックの柱・文字化け看板・色の剥がれた村 S6）。docs/34/00・50・23 §5・11・45 の全関連節と整合。",
    },
    {
        "id": "ch1_ch2",
        "title": "U2：第1・2章の構造物（docs/16 §4）",
        "scope": "01 月の林：場所系列（手紙の径口・もうすぐ参道・熟すことを書かれなかった果樹園・月見の小屋・月読みの丘・摘み取りの丘——S7、docs/34/01 §3）の全地点を構造物・構造として設計。ボスアリーナ（摘み取りの丘・月欠狼戦の視認要件）。02 読まれなかった港：止まった灯台・返信棚・倉庫群・港施設（S8、docs/34/02 §3）。書簡形式の断片と構造の結びつき（届かなかった手紙が積まれる場）。両章とも場所系列の全地点を一覧表に載せ、主要構造物（各章2〜4件目安）に10節詳細カード。第2章は順不同耐性 G4——他章攻略前提を置かない。導線は docs/45、演出は docs/48、収容物は docs/14・36 と整合。",
    },
    {
        "id": "ch3_ch4",
        "title": "U3：第3・4章の構造物（docs/16 §5）",
        "scope": "03 踊らなかった広場：舞台機構・指揮台・観客席・祭具の残り（S9、docs/34/03 §3）。祭囃子没腐姿の造形——指揮台と舞台機構への一体化の度合い・救出時の復帰演出は Issue #2 の領域と指定済み（docs/34/03 §11）——構造側の要件を定義。戯曲形式との結びつき（演じ手にされる舞台構造）。04 選ばれなかった坑道：坑道系・（公の）作業場/検品小屋・隠し工房「作業場の床下の私室」・根幹坑道（S10、docs/34/04 §3）。隔離区画の熱・橙の漏れ光＝灼熱の埋立て地への一次導線造形（U2-F・docs/23 §8.4）。日誌篇と隠し工房の空間関係・発注書と幻想文字の一意配置（34/04 §8）を構造に載せる。両章とも場所系列の全地点を一覧表に載せ、主要構造物に10節詳細カード。順不同耐性 G4。",
    },
    {
        "id": "ch5_final_aux",
        "title": "U4：第5・終章・補助領域の構造物（docs/16 §6）",
        "scope": "05 歌えなかった塔：塔本体・内部構成・頂部（S11、docs/34/05 §3）——垂直劇場の設計。終章：原案の座・集積の間・書庫・座の境（S12、docs/34/06 §3・§6）——畳まれる/殻として残る二状態（G13）の構造定義、結末別の状態差。灼熱の埋立て地（S13）：焼却・処理物の届き先としての地形構造・独自素材領域・住人候補の場・隔離区画からの導線受け側（docs/23 §8.4）。L3 ごみ処理場（S14）：プレイヤーが組むマルチブロック構造——クレーン・マグマ槽・圧縮・選別の構成パーツ、組立てルール、視覚設計、他人を捨てる儀式の構造要件（docs/23 §8.3・§8.5——「構造物設計の詳細は Issue #2 の領域」の直接の受け皿）。全構造物に10節詳細カード。",
    },
]

META = {
    "name": "structures-dungeons-forge",
    "description": "構造物/ダンジョン設計書 docs/16（Issue #2）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典から構造物・場所の手渡し項目を棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・形式整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（書き戻し先の正典節つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した全構造物・場所の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #2（構造物/ダンジョン設計）へ手渡されている全ての構造物・場所・構造要求・未定義の物差し**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #2」「構造物」「ダンジョン」「場所」「アリーナ」「拠点」「捨て場」「処理場」「埋立て地」「異物チャンク」「灯台」「舞台」「坑道」「塔」「書庫」「座」に言及されている箇所（grep で総当たり）
2. docs/49 §7 の棚卸し S1〜S20 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/34 各章 §3 場所系列の全地点の抽出（名前つき場所・役割・クリティカルパス上の位）
4. docs/23 §5・§8 の捨て場・転移箱・ごみ処理場・灼熱の埋立て地の全要件（構造形・生成規則・行き方・帰還規則）
5. docs/11 の異物チャンク・自分を棄てる機構・村の構造記述
6. docs/45・48 で構造物に課された導線・演出規格（遠望・迷子回帰・ノミ収まり・幕・幻想文字配置）
7. docs/36 伏線台帳のうち構造物・場所に配置される手がかり
8. 構造として語るべきだがまだ仕様がない全項目（設計確定済みだが形が未定義の場所含む）

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（拠点/章構造/アリーナ/補助領域/導線構造/手組み領域/制約）｜優先度（必須/任意）」。docs/49 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の構造物・ダンジョン設計者。{unit['title']} を、調査基準（docs/49）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 正典からの手渡し棚卸し（抽出済み——これを網羅的に回収せよ）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/49 §4 の設計原則 P-01〜P-09 に載せてから、構造物の事情で具体化する
- 先行例（§2）を根拠に引く——「黄昏の森の塔型」「Trial Chambers の jigsaw 構成」等の参照明記
- 全構造物に生成方式（4型から選択）と器を明記（P-03）。抽象論で終わらせない
- 詳細カードは「実装者がこの表だけで作業できる具体度」へ：部屋割り・動線・ギミック・導線・二状態・生成構成案まで
- 構造物は「読む場所」（P-01）——没になった理由を構造の不完全さで示す（G20）
- 「要承認」は推奨案つきで open_questions に集約（書き戻し先を明記）

## 出力形式（section_md）
docs/49 §5 の担当ユニットの必須節構成（§2〜§6 の該当節）をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の構造物レビューア。以下の設計を、docs/49 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/49 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/49 §6 の3段分類を適用）
1. **正典制約適合**：G1〜G20 の各条項に反する設計がないか（特に G4 順不同・G7 二状態・G13 殻の定義・G19 世界法則・G20 由来）
2. **網羅性**：場所系列（docs/34 各章 §3）の全地点が一覧表に載っているか、棚卸し項目が全て回収されているか、必須列・必須節に欠落がないか
3. **根拠**：全仕様に参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：実装者がこの表だけで作業できる具体度か（部屋割り・動線・生成方式まで書かれているか）
5. **層整合**：表層と深読み層の境界を守っているか、必読情報を文字に置いていないか
6. **境界**：Issue #15（数値）・#13（生成技術検証）・#10（ロア本文）・#11（章ボード）との境界が明確か——数値・断片本文を内包しすぎていないか
7. **状態管理**：要承認に書き戻し先があるか、未作成docsへの手渡しは Issue 記録になっているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の構造物・ダンジョン設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/49 §7・Issue #2 の対象（全章の構造物一覧・主要構造物詳細・共通規格・拠点・捨て場・縁の地・異物チャンク・灼熱の埋立て地・L3ごみ処理場・結末後の殻）が4ユニットのいずれかで扱われているか、必須節・必須表が揃っているか、要承認に書き戻し先があるか",
        "forms": "形式・規格整合——ユニット間で構造規格が食い違わないか（型体系・遠望→遮蔽→開示・二状態・生成方式4型の用語と適用基準・命名文法・一覧表の必須列）、同じ構造物・場所（捨て場・村・環礁の構造）がユニット間で矛盾なく記述されているか、共通規格と章別設計の接続が正しいか",
        "canon": "正典整合——4ユニット全体が docs/11/12/13/14/15/20/23/24/25/26/32/34/36/38/45/48/50 の記述と矛盾しないか、正典を事実上書き換える提案が『要承認』になっているか、場所名・用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**構造物/ダンジョン設計の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/49 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 構造物・場所の手渡し項目棚卸し（抽出） ===")
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

    cov_check, form_check, canon_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "forms", inventory), phase="crosscheck", label="cc-forms", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("forms", form_check), ("canon", canon_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "forms": form_check, "canon": canon_check},
    }
    outdir = "/home/ubuntu/repos/the-understory/.devin-work/issue2"
    os.makedirs(outdir, exist_ok=True)
    with open(f"{outdir}/inventory.md", "w", encoding="utf-8") as f:
        f.write(inventory)
    for r in results:
        with open(f"{outdir}/{r['unit']}.json", "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
    with open(f"{outdir}/crosscheck.json", "w", encoding="utf-8") as f:
        json.dump(output["crosscheck"], f, ensure_ascii=False, indent=1)
    log(f"=== 完了 === {outdir} に {len(results)} ユニット＋横断監査を書き出し")


asyncio.run(main())
