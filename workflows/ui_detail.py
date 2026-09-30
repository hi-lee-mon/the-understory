import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/53_research_ui_ux.md（本タスクの物差し——§2先行研究・§3正典制約G-UI-01〜23・§4設計原則P-UI-01〜12・§5組版テンプレ・§6レビュー基準・§7棚卸しH1〜H26は必須）
- docs/20_art_ui_design_system.md（デザインシステム——§2デザインシステム・§3フォント方針・§4シェーダー・§5パレット・§6 UI画面一覧・§7 UI音・§8残件）
- docs/48_fusion_elements/04_cipher_ui_boundary.md（演出UI線引きの法典——§4.1 判定規則・§4.2 可/不可表——本書の絶対境界）
- docs/48_fusion_elements/02_narrative_forms.md（語り形式・鑑賞層——§3〜§5 形式別装丁・手記/図鑑の器割当・読み返し規則）
- docs/48_fusion_elements/01_episode_production.md（予告頁・幕切れ・エンドロール/PC規格）
- docs/48_fusion_elements/03_theatrical_pacing.md（幕三階層・幕切れ規格）
- docs/45_nonverbal_guidance/01_system_grammar.md・02_guidance_applications.md・04_affordance_accessibility.md（非言語導線・a11y規則——M-2・P-1・P-2・C-1・B-1・A-2・H-1 等）
- docs/26_narrative_vectors.md（語りベクター——§8 読み上げの間の委譲・§3.4 環境文字・§6 分量）
- docs/32_system_specs.md（システム仕様——§2.3 個人没腐度・§4 羅針盤・§6 マルチ/綴じ規則 K3/K7・§9 外部連携）
- docs/14_items_crafting.md（拾得図鑑の入手・JEI連携・由来鑑定）
- docs/16_structures_dungeons.md（§2.3 器・§7.5 手渡し——名付けの台・綴じ画面素材・祭囃子没腐姿メモ）
- docs/34_chapter_plots/（全7本＋README——結末綴じ画面の章別使用・名付けの台・坐る/観客化・祭囃子没腐姿）
- docs/17_streaming_design.md（配信構造——§3 30秒基準・§8 配信モード）
- docs/46_distribution_research.md（Patchouli D-2・JEI D-1）
- docs/38_numeric_tables/03_bosses.md（§4.3 演出時間規格・拍子窓の確定値）
- docs/38_numeric_tables/04_mobs_economy.md（個人没腐度・淀み指標・名札代替経路）
- docs/09_redesign_fusion.md（§6 マイクラらしさの制約——UI線引きの原点）
- docs/13_progression_map.md（迷子規則・章横断の導線）
- docs/50_opening_storyboard.md（OP ビート——説明テキストなしの証明責任）
- docs/30_adr/（ADR-0003/0004 等の確定決裁）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/53 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 各画面・各表示は規格表の必須列（名称｜実装形｜起動条件｜構成要素｜入力操作｜表示内容｜状態遷移・閉じ方｜多重化｜共有/個別層｜a11y・コンフィグ｜根拠）を全部入れる
- 全仕様に根拠（正典節／docs/53 の先行研究・原則番号）を付ける。感覚だけの提案は不可
- 全 UI は「実装形」を必ず明記する（Patchouli 標準頁／自前 Screen／バニラ器＝HUD層・字幕・ツールチップ・Title/Toast 等）
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝18-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- docs/52・docs/51・docs/43 は未作成——実文・ボード・リリース関連は「Issue #10/#11/#8 への手渡し」記録に留める
- 既に承認済みの正典決定（G-UI 表の項目・H 棚卸しの承認済み値）を再検討しない——本書はその UI 側の実現形を定める
- 祭囃子没腐姿の造形メモ（Issue #2 手渡し）は「デザイン側造形の概略」として §6 または open_questions に記録に留める（UI 詳細の本題ではないが拾う）
"""

CONSTRAINTS = """絶対条件（docs/53 §3 の正典制約 G-UI-01〜23）：
- G-UI-01 見た目のみ変更可・操作体系不変
- G-UI-02 国スキンは国にいる間だけ（現実側はバニラのまま）
- G-UI-03 新規 UI 画面は docs/20 §6 一覧限定——一覧外の新設は要承認
- G-UI-04 必読情報を UI テキストのみで運ばない（環境一次）
- G-UI-05 環境一次・装置/UI 二次——UI だけで成立する導線の新設は禁止
- G-UI-06 色のみ依存禁止
- G-UI-07 多重化義務（45/04 §3.2 必須チャネル表）
- G-UI-08 層構造（表層で遊べる・深読み層は読むほど重厚）
- G-UI-09 第2〜4章は順不同——順序依存の UI 提示を置かない
- G-UI-10 審美「かすれた・欠けた・継がれた」＋琥珀/朱の予約（docs/20 §5）
- G-UI-11 シェーダー/影MOD共存
- G-UI-12 フォント3系統＝font プロバイダ＋架空書体1系統新設
- G-UI-13 器割当確定（図鑑＝Patchouli soft dep・手記＝自前書物器）
- G-UI-14 綴じ画面の型（閉じて再開可・かすれた項存在表示・選択は頁所持者・綴じは先着）
- G-UI-15 字幕表示名＝「〈主体〉：〈動作〉」二項型
- G-UI-16 個別層＝由来札のみ・環境形は全員同一
- G-UI-17 用語正典どおり・正典変更は要承認
- G-UI-18 幕/間/演出時間の規格は 38/03 §4.3 が権威・場面別定量は 45/02 §3 が権威——本書は引用のみ
- G-UI-19 配信モード＝専用画面なし・コンフィグで対応
- G-UI-20 「◯◯の物」由来表示＝既定ホバー/接近時・常時はコンフィグのみ
- G-UI-21 個人没腐度の段階名・数値の常時表示は不可（環境演出のみ）
- G-UI-22 拍子 UI＝二次補助のみ（一次＝見得同型・間隔3.0秒・窓±0.35〜±0.40秒は確定値引用）
- G-UI-23 操作ヒント＝照準時のみの最小表示（環境誘導一次・二次フォールバック）
"""

UNITS = [
    {
        "id": "tokens_common",
        "title": "U1：トークン・共通規格（§0〜§2）",
        "scope": "§0 位置づけ（docs/20 との棲み分け・docs/48/04 法典を境界の権威として引用・本書が確定する値の範囲）＋§1 デザイントークン完全定義（色トークン=docs/20 §5 パレットの UI 用途別割当＋琥珀/朱の予約適用・形トークン=書物/頁/綴じ目/折れ目/枠意匠/アイコン体系=統一線幅と欠け表現・動きトークン=かすれて現れる/欠片が綴じられる/頁めくり/幕遷移のモーション言語と実数値・フォントトークン=3系統の役割と font プロバイダ実装方式・架空書体1系統・UI音トークン=紙/木/かすれた鐘＋字幕名登録規則）＋§2 共通規格（画面階層表=HUD層/Screen/コンテナ画面/Title・Toast/字幕・国スキン適用境界=国にいる間だけの判定規則・遷移言語=開く/閉じる/戻るの統一挙動と閉じて再開可能原則・入力規則=七つの身体動詞＋既存入力のみ・通知言語=Toast/Title/書物音の使い分け・テキスト表示規則=**読み上げの間の確定値**=基本時間＋1文字あたり時間の式と上限・頁めくり速度——26 §8・48/02 U2-R-5 の委譲着地。全年齢で読み切れる値を推奨案として要承認へ）",
    },
    {
        "id": "book_forms",
        "title": "U2：書物器 UI 群（§3）",
        "scope": "§3 書物器 UI 群——拾得図鑑（Patchouli：book.json 構成・頁型の割当・綴じ片=項の目録・住人授与主軸・失われた物語欄・JEI 連携の画面側）・拾い人の手記（自前書物器：見開き・頁単位増殖・ノミ綴じ演出・序章から記録・村で冊子実体・形式別ファクシミリ頁）・欠頁/未読表示（綴じ目の空き=枚数のみ可視・折れ目・綴じ糸色・表紙の新頁気配——U2-N2）・予告頁（交付→図鑑挿入→語り再生→頁提示・挿絵頁=書物スキンの画像頁・閉じて再開可・語りは方角のみ——U1-#1/#2）・結末の記録（各章選択と世界変化の記録形式）・村報（発行・掲示板=書物 UI を開く器・発展/住人/解放要素）・語り形式別装丁見本（6形式=絵本/書簡/戯曲/日誌/詩/設計書の頁面構成表——48/02 §4.1 観る層の UI 着地）。各器ごとに規格表の必須列を埋める",
    },
    {
        "id": "ceremony_screens",
        "title": "U3：演出画面群（§4）",
        "scope": "§4 演出画面群——結末綴じ画面（最大の演出面の全仕様：見開き器の構成・欠片が見開きを形作る素材＝16 §6.2 U2-Q1・三択の提示形・かすれた項の存在常時表示＝全員/本文と選択は頁所持者のみ・綴じ動作の操作=読み選びの範囲・閉じて再開可・マルチ表示=共有層の綴じ表示＋個別層の項・先着規則の画面表現・配信の山場としての視認性）・名付けの台 UI（バニラ命名器=看板/アンビル型の国スキン器・入力操作不変・白紙の名札の投入）・幕間の画面遷移（大幕=開幕/幕切れ・中幕=ボス戦フェーズ転換・小幕=転移の画面側仕様——規格は 38/03 §4.3 引用のみ・画面側の見え方を書く）・エンドロール/ポストクレジット画面（残した者たちの頁＝三節構成・60〜90秒・史記調傍注・スキップ規則・結末別演出3種の画面形・再演導線——U1-#3/#6）",
    },
    {
        "id": "hud_config",
        "title": "U4：HUD/環境内 UI＋コンフィグ/a11y（§5〜§8）",
        "scope": "§5 HUD・フィードバック・環境内 UI——没腐コンパス（ノミ連動・未攻略主線環礁の淀みのみ・表示形=コンパス UI のスキン）・拍子キュー（二次補助の形と位置・窓表示の有無・38/03 §4.3 確定値引用）・照準時アクション表示（「坐る」等——表示条件/形/消滅条件・環境一次の前提）・由来札「◯◯の物」（ホバー/接近時・常時はコンフィグ）・かすれた項の存在表示（結末画面内の第三項——K3）・字幕表示名（二項型の登録規則・方向語・内容言明禁止）・個人没腐度の提示（常時表示不可——段階名を出さず環境演出のみで伝える形・コンフィグでの任意表示可否）・拾得/進行通知の統一型・ツールチップと JEI 連携（由来鑑定の表示位置・レシピ表示・隠すレシピ制御）＋§6 コンフィグ/a11y/配信/シェーダー（コンフィグ項目表=項目名・既定値・範囲・影響先——演出強度・演出スキップ・由来表示常時・拍子 UI・字幕・没腐度表示等・Issue #34 への手渡し項目明記／a11y 仕様=45/04 の UI 側義務の履行表／配信対応=視認強度・専用画面なし／シェーダー共存の UI 要件）＋§7 未決・要承認集約（18-U*-Q* ID・推奨案・書き戻し先）＋§8 手渡し一覧（#10 実文・#11 ボード・#15 数値・#19 音・#34 コンフィグ・#13 実装方式）＋祭囃子没腐姿の造形メモ（Issue #2 手渡し——デザイン側造形の概略を記録）",
    },
]

META = {
    "name": "ui-detail-forge",
    "description": "UI詳細仕様 docs/18（Issue #3）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からの UI 手渡し項目の棚卸し", "count": 1},
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
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝18-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した全 UI 手渡し項目・未定義項目の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #3（UI詳細仕様 docs/18）へ手渡されている全ての項目・UI 要求・未定義の値**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #3」「docs/18」「UI」「画面」「表示」「綴じ」「図鑑」「ヒント」「フォント」「コンフィグ」「字幕」「読み上げ」に言及されている箇所（grep で総当たり）
2. docs/53 §7 の棚卸し H1〜H26 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/48/04 §4.2 の可/不可表・§4.3 の条件つき可表の全項目（UI 側で実現形を定めるべき全項目）
4. docs/34 各章プロットに既に書かれている UI タッチポイントの全抽出（綴じ画面の章別使用・名付け・坐る・祭囃子没腐姿・村報・掲示板等）
5. docs/20 §6 UI画面一覧・§8 残件の全項目
6. docs/45/04 の UI 側義務（M-2・P-1・P-2・C-1・B-1・A-2・H-1・X-4 等——UI が満たすべき規則）
7. docs/32 §6・docs/38 の UI 関連確定値（綴じ・マルチ・没腐度・拍子窓等）
8. 実装形（Patchouli/自前 Screen/HUD 層/字幕/ツールチップ/Toast/Title）の指定がある全項目
9. 「UI 側で確定すべき値・形」だがまだ仕様がない全項目

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（画面/器/HUD/トークン/時間値/コンフィグ/実装形/手渡し）｜確定状況（確定済み/本書で確定/要承認）｜優先度（必須/任意）」。docs/53 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の UI 設計者。{unit['title']} を、調査基準（docs/53）に基づき深い思考で執筆せよ。

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
- まず docs/53 §4 の設計原則 P-UI-01〜12 に載せてから、要素の事情で具体化する
- 先行例（§2）を根拠に引く——「Patchouli の頁型」「Tunic の説明書」「Cadence of Hyrule の拍バー」等の参照明記
- 全ての UI は実装形を明記する（Patchouli 標準頁／自前 Screen／HUD 層／字幕／ツールチップ／Title・Toast）。抽象論で終わらせない
- 画面は「起動条件→構成要素→入力→表示→状態遷移・閉じ方」まで掘る——実装者がこの節だけで作れる粒度
- docs/48/04 §4 法典の可/不可に反する設計は絶対にしない。境界のグレーがあれば「要承認」に回す
- 時間値（読み上げの間・頁めくり・通知保持等）は本書で確定値を出す——ただし新設の数値は推奨案として open_questions にも記す（P-UI-10）
- 「要承認」は 18-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/53 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の UI レビューア。以下の設計を、docs/53 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/53 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/53 §6 の3段分類を適用）
1. **正典制約適合**：G-UI-01〜23 の各条項に反する設計がないか（特に G-UI-01 操作体系不変・G-UI-03 新規画面限定・G-UI-04 必読情報・G-UI-05 環境一次・G-UI-06 色のみ禁止・G-UI-14 綴じ画面の型・G-UI-19〜23）
2. **網羅性**：棚卸し項目（docs/53 §7 H1〜H26 と抽出結果）が全て回収されているか、docs/53 §5 の必須節・必須列に欠落がないか
3. **根拠**：全仕様に参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：実装者がこの節だけで作業できる具体度か（実装形・起動条件・構成要素・状態遷移が書かれているか）
5. **層整合**：表層と深読み層の境界を守っているか——「あるが読めない」の文法（かすれた項・白紙の頁）を壊していないか
6. **値の確定**：本書が持つべき確定値（読み上げの間等）が空白のまま残っていないか。権威のある値（38/03 §4.3 等）を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか、未作成 docs への手渡しは Issue 記録になっているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の UI 設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/53 §7・Issue #3 の対象要素（トークン・共通規格・書物器・演出画面・HUD・環境内 UI・コンフィグ・a11y・配信・シェーダー・手渡し）が4ユニットのいずれかで扱われているか、必須節・必須列が揃っているか、要承認に ID・書き戻し先があるか",
        "forms": "形式・規則整合——ユニット間で UI 規則が食い違わないか（トークン定義と画面仕様・書物器と装丁見本・綴じ画面とかすれた項・通知言語と各画面・コンフィグ項目と各表示の対応）、同じ要素（綴じ目・フォント・読み上げの間・由来札）がユニット間で矛盾なく使われているか、法典の境界（可/不可・一次/二次・共有/個別）が全体で一貫しているか",
        "canon": "正典整合——4ユニット全体が docs/09/14/17/20/26/32/34/38/45/46/48/50 の記述と矛盾しないか、承認済みの確定値（器割当・拍子窓・字幕型・綴じ画面の型等）を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**UI詳細仕様の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/53 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: UI 手渡し項目の棚卸し（抽出） ===")
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
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
