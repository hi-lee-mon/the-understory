import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/54_research_audio.md（本タスクの物差し——§2先行研究・§3正典制約G-AU-01〜18・§4設計原則P-AU-01〜10・§5組版テンプレ・§6レビュー基準・§7棚卸しH1〜H30は必須）
- docs/20_art_ui_design_system.md（§7 音の方向・§1 色の回帰規則・§2 色予約・§5 パレット）
- docs/18_ui_ux_detail.md（§1.5 UI音トークン・字幕名登録規則・§2.5 通知型統一表・§2.6 表示時間の権威・§8 手渡し一覧——本書が消費する音要件の発生源）
- docs/16_structures_dungeons.md（§2.6 聞き手規則の構造側担保・§5 05章構造物=鐘撞きの径・縦の音道・頂上鐘楼・§7.5 docs/19 への手渡し——響界音実装・16-U4-Q1 承認結果）
- docs/45_nonverbal_guidance/04_affordance_accessibility.md（§3.2 多重化算入制約 C6+C7・§5.2 聞き手規則 H-1/H-4・§6 #1 字幕登録範囲・§2.2 規則A-4 救出完了三点表示）
- docs/45_nonverbal_guidance/01_system_grammar.md・02_guidance_applications.md（音×光の複合併用・異物の音・導線上意味を持つSE）
- docs/48_fusion_elements/03_theatrical_pacing.md（幕三階層・柝/ツケ音・拍子キュー・U3-N2 拍子音色の章別割当）
- docs/48_fusion_elements/01_episode_production.md（幕切れ規格・綴じ音の間・エンドロール演出）
- docs/48_fusion_elements/02_narrative_forms.md（語り形式——詩・戯曲と音の関係・無音区間行）
- docs/38_numeric_tables/03_bosses.md（§4.3 幕・演出時間規格——音関連の確定値の権威）
- docs/38_numeric_tables/04_mobs_bosses.md（個人没腐度・淀み指標——音側表現の素材）
- docs/38_numeric_tables/02_gear_devices.md（縁の羅針盤・鳴る楽器・没の楽器の器仕様）
- docs/34_chapter_plots/（全7本＋README——特に 05_unsung_tower.md の聞き手規則+響界・無音区間・歌姫・03_unheld_square.md の拍子・祭囃子・04 の打鍵音・02 の港/灯台音景・00/06 の音）
- docs/14_items_crafting.md（§3 拾得トークン統一仕様 U1-Q3・縁の羅針盤の複合識別 U1-Q4・没の楽器→鳴る楽器）
- docs/32_system_specs.md（§4 羅針盤・異物の音・§6 マルチ共有/個別層）
- docs/11_world_bible.md（§4 異物——かすれた昔の音・欠損）
- docs/10_game_design_document.md（§87 音の基調——かすれた・欠けた・哀愁・章ごとの主題楽曲・異物の演出音）
- docs/17_streaming_design.md（§3 30秒基準・音のクリップ瞬間）
- docs/50_opening_storyboard.md（OP の音要件——説明なしの導入で音が担う分）
- docs/26_narrative_vectors.md（ノミの語り——05章の声→字退避との関係）
- docs/23_discard_grammar.md（ゴミ箱・捨てる文法——投入音の文脈）
- docs/13_progression_map.md（章横断の導線——音の導線位置づけ）
- docs/46_distribution_research.md（配布形態——素材の権利要件の前提）
- docs/30_adr/（ADR-0002 技術選定 NeoForge/1.21.1 等）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/54 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- SE 登録表は必須列（登録ID｜字幕名=〈主体〉：〈動作〉二項型｜カテゴリ｜stream｜定位mono/stereo｜トリガーイベント｜音色要件｜根拠）を全部入れる
- 章別音設計は全章で同じ列構成（環境音/章固有SE/章テーマ接続/救出後の変化）
- 全仕様に根拠（正典節／docs/54 の先行研究・原則番号）を付ける。感覚だけの提案は不可
- 数値は実装者が迷わない粒度まで（音量・減衰・長さ・ループ・発火条件——P-AU-05）
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝19-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- 承認済みの正典値（拍子窓±0.35〜0.40s・幕規格・字幕型・UI音パレット・聞き手規則・拾得音色統一）を再定義しない——引用のみ（P-AU-10）
- docs/51・52・43 は未作成——実文・ボード・リリース関連は手渡し記録に留める
"""

CONSTRAINTS = """絶対条件（docs/54 §3 の正典制約 G-AU-01〜18）：
- G-AU-01 音の質感「かすれた・古い」全編統一（現実側でも変えない）
- G-AU-02 字幕名＝〈主体〉：〈動作〉二項型・登録範囲＝導線上意味を持つSE限定
- G-AU-03 無音区間は字幕も出さない
- G-AU-04 聞き手規則＝05環礁ローカル法則（鳴らした者は聞き手に数えない・響界＝音の実在が許される円域・聞き手がいなければ消える・救出後存続=16-U4-Q1）
- G-AU-05 音は常に字幕名とペア（C6+C7）・音だけの必須情報は禁止
- G-AU-06 拾得トークンの音色は全章統一
- G-AU-07 羅針盤の対象種別＝音色＋字幕名の複合識別
- G-AU-08 幕・拍子の音規格は 38/03 §4.3・48/03 が権威——引用のみ
- G-AU-09 拍子音色の章別割当＝U3-N2 承認済み（03=柝系）
- G-AU-10 救出完了＝彩度・動き・音復帰の三点表示——音復帰規格は本書が定義
- G-AU-11 異物の音＝かすれた昔の音の残響
- G-AU-12 響界内では音が見える（音→光同期の音側要件のみ）
- G-AU-13 UI音パレット確定済み（拾得・かすれた鐘・綴じ・巻き戻る・静けさ/紙音）
- G-AU-14 05章ノミの語り＝声→字退避
- G-AU-15 ボス戦の音＝幕と同期（幕間=缶詰の拍手音のみ・ツケ柝→間）
- G-AU-16 音だけに依存する必須情報は禁止
- G-AU-17 音素材は権利クリアな自作/許諾素材のみ
- G-AU-18 NeoForge/MC1.21.1 sounds.json 規格内で設計
"""

UNITS = [
    {
        "id": "skeleton_impl",
        "title": "U1：音設計の骨格＋実装規格（§0〜§2）",
        "scope": "§0 位置づけ（docs/18 §1.5・docs/20 §7 との棲み分け——18 が確定した字幕名規則・UI音パレット・表示時間は引用のみ・本書が確定する値の範囲）＋§1 音設計の骨格（音の階層構造=世界音=環境/SE・器音=UI/インタラクト・楽曲の3層＋演出音・「かすれた・古い」質感の素材言語化=帯域・残響・ノイズの要件定義・多重化 C6+C7 での音の役割）＋§2 実装規格（sounds.json 規格=命名系 understory.* サブドメイン・サブタイトルキー・stream 判定基準=数秒超・mono/stereo 指針=定位必須音は mono・サウンドカテゴリ割当表・音量/減衰/定位の規範・環境音の発火方式=バイオーム ambient vs 独自発火の決定——外部アンビエンス MOD に依存しない自己完結方針）",
    },
    {
        "id": "se_registry",
        "title": "U2：器・UI・イベント SE 全登録表（§3）",
        "scope": "§3 SE 全登録表——Issue #3 §8 手渡しの本体。器・UI SE（拾得音=かすれた・古い全章統一・かすれた鐘・綴じ音=糸を締める・巻き戻る音・頁めくり音=0.30s/連続0.18s 同期・静けさ/紙音のみ・ゴミ箱投入音・名付けの台操作音・羅針盤の対象別音色=音色+字幕名複合識別・拾得図鑑/手記の器音・予告頁交付音）・イベント/演出 SE（幕三階層の柝+ツケ音・章の幕切れ=綴じ音の間+暗転10秒・通知型11種の音側=拾得/図鑑綴じ/頁追加/解放/交付・救出完了の音復帰・PC気配/再来・招待状/没配便・異物接近のかすれた昔の音）・モブ/ボス SE の器側要件（#15 境界——行動・数値は38が権威、音素材要件は本書）・定位必須 SE 一覧（方向が情報になる音=拍子・鐘・気配→mono）。全 SE に登録ID・字幕名二項型・カテゴリ・stream・定位・トリガー・音色要件・根拠を記す",
    },
    {
        "id": "chapters_kyokai",
        "title": "U3：章別音設計＋響界・聞き手規則（§4〜§5）",
        "scope": "§4 章別音設計（全章同じ列構成=環境音/章固有SE/章テーマ接続/救出後の変化）——00 序章・現実側（ゴミ箱・招待状・初接触の音）、01 月見翁の章（月・静けさの音景）、02 読み届けなかった港（灯台・嵐・手紙の音景）、03 開かなかった広場（拍子だけが律儀に鳴る・歌なし掛け声なし・祭囃子・幕間=缶詰の拍手音）、04 選ばれなかった鉱山（到着から鳴り続ける打鍵音=正体は炉心・坑道の音景）、05 歌えなかった塔（汀で全音消去・揺れて鳴らない鐘・響界・音無しの靄・間を喰う者・上るほど組み上がる塔の音楽・救出で音が爆発的に戻る）、06 終章（原案の座・余白の音）、異物・没腐系の音（異物のかすれた昔の音・没腐接近・淀みの段階の音的滲み=段階名を出さない環境演出のみ）＋§5 響界・聞き手規則の音実装（響界の音響定義=鳴る楽器が生む円域・半径・聞き手持続条件・音→光同期規則=波紋発生と音発火の対応・残響時間規格・聞き手規則の実装要件=聞き手判定系・ノミ/他PCの聞き手扱い・16-U4-Q1 救出後存続の反映・救出完了の音復帰規格=何がどの順で戻るか）",
    },
    {
        "id": "music_assets",
        "title": "U4：楽曲方針＋素材要件・権利＋集約（§6〜§9）",
        "scope": "§6 楽曲方針（次元環境楽曲=国ではバニラ楽曲を止め独自曲を常時化——TF 先例・章別テーマ曲=章ごとに主題・ボス曲/幕曲=戦闘フェーズ同期・OP/ED・エンドロール曲=残した者たちの頁の楽曲要件・発見型音楽報酬=music disc 相当物の所在・歌姫の歌=歌詞・旋律の発注要件）＋§7 素材要件・権利/ライセンス・制作体制（素材要件表=フォーマットogg・サンプルレート・長さ・ループ可否・レイヤード要件——発注/収録できる粒度・権利方針=自作/素材サイト/生成AI連携の境界・Issue #26 受け皿の定義・配信者向け注意書き・垂直スライスの最小音セット=#5 手渡し）＋§8 未決・要承認集約（19-U{n}-Q{m} ID・推奨案・書き戻し先）＋§9 手渡し一覧（#13 実装方式・#15 モブ音・#26 生成基盤・#34 a11y・#5 垂直スライス・#10 台詞音・#17 配信クリップ音）",
    },
]

META = {
    "name": "audio-direction-forge",
    "description": "オーディオ方向 docs/19（Issue #4）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からの音要件の棚卸し", "count": 1},
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
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝19-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した全音要件・未定義項目の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #4（オーディオ方向 docs/19）へ手渡されている全ての項目・音要件・未定義の値**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #4」「docs/19」「音」「SE」「サウンド」「楽曲」「BGM」「響界」「聞き手」「拍子」「柝」「鐘」「歌」「字幕」「静寂」「無音」「残響」に言及されている箇所（grep で総当たり）
2. docs/54 §7 の棚卸し H1〜H30 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/18 の音関連確定値の全抽出（§1.5 UI音パレット・字幕名規則・§2.5 通知型統一表の音列・§2.6 表示時間・§8 手渡し）
4. docs/16 §7.5 の docs/19 手渡し分（響界音実装・16-U4-Q1）と、§2.6 聞き手規則の構造側担保・05章構造物の音要件の全抽出
5. docs/34 各章プロットに書かれている音要件の全抽出（章別の環境音・固有SE・ボス音・救出音の記述——特に 03 拍子/祭囃子・04 打鍵音・05 無音/響界/鐘/歌姫の歌）
6. docs/48/03 の幕・拍子の音規格（柝/ツケ音・U3-N2 章別割当）と 48/01 の幕切れ音・エンドロールの音
7. docs/45/04 の音側義務（H-1・H-4・C6+C7 算入・聞き手規則・字幕登録範囲）
8. docs/10 §87・docs/11 §4・docs/20 §7・docs/14・docs/32 の音要件（基調・異物音・羅針盤・拾得音）
9. モブ/ボスの音（docs/38/03-04 の音関連記述——行動予告音・撃破音等）
10. 「音側で確定すべき値・素材」だがまだ仕様がない全項目（楽曲構成・素材要件・権利方針等）

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（SE/楽曲/環境音/規格/システム/手渡し）｜確定状況（確定済み/本書で確定/要承認）｜優先度（必須/任意）」。docs/54 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のサウンド設計者。{unit['title']} を、調査基準（docs/54）に基づき深い思考で執筆せよ。

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
- まず docs/54 §4 の設計原則 P-AU-01〜10 に載せてから、要素の事情で具体化する
- 先行例（§2）を根拠に引く——「TF の次元楽曲常時化」「Silent Hill の予告音」「Outer Wilds の場所と結びつく楽曲」等の参照明記
- 全ての音指定は実装粒度まで（登録ID・sounds.json 構成・カテゴリ・定位・トリガー条件・音量/減衰）——抽象論で終わらせない
- 「聞こえない音の演出」（無音区間・聞き手規則）も実装要件として書く——何が・いつ・どう消えるか
- docs/18・38・48 が確定した値は引用のみ。変更が必要なら要承認へ
- 「要承認」は 19-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/54 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」のオーディオレビューア。以下の設計を、docs/54 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/54 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/54 §6 の3段分類を適用）
1. **正典制約適合**：G-AU-01〜18 の各条項に反する設計がないか（特に G-AU-01 質感統一・G-AU-02 字幕二項型・G-AU-03 無音区間・G-AU-04 聞き手規則・G-AU-08 幕規格引用のみ・G-AU-16 音のみ必須情報禁止・G-AU-17 権利）
2. **網羅性**：棚卸し項目（docs/54 §7 H1〜H30 と抽出結果）が全て回収されているか、docs/54 §5 の必須節・必須列に欠落がないか（SE 登録表の8列・章別の4列構成）
3. **根拠**：全仕様に参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：実装者・作曲者がこの節だけで作業できる具体度か（登録ID・トリガー・音量・フォーマット要件が書かれているか）
5. **演出整合**：静寂の演出（05 無音・幕間の間・救出前）が「消える音の実装要件」まで降りているか——「無くす」だけの記述になっていないか
6. **権威侵害**：確定値（拍子窓・幕規格・字幕型・聞き手規則・UI音パレット）を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか、未作成 docs への手渡しは Issue 記録になっているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のサウンド設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/54 §7・Issue #4 の対象要素（骨格・実装規格・SE 全登録・章別・響界・楽曲・素材・権利・手渡し）が4ユニットのいずれかで扱われているか、必須節・必須列が揃っているか、要承認に ID・書き戻し先があるか",
        "forms": "形式・規則整合——ユニット間で音規則が食い違わないか（実装規格の命名系と各 SE の ID・字幕名規則と登録表・響界の定義と章別節・楽曲方針と章別テーマ・権利方針と素材要件）、同じ要素（拾得音・柝・鐘・気配音）がユニット間で矛盾なく使われているか",
        "canon": "正典整合——4ユニット全体が docs/10/11/14/16/17/18/20/32/34/38/45/48/50 の記述と矛盾しないか、承認済みの確定値（拍子窓・幕規格・字幕型・UI音パレット・聞き手規則・拾得音色）を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**オーディオ方向の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/54 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 音要件の棚卸し（抽出） ===")
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
