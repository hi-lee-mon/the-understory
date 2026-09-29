import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/47_research_fusion_elements.md（本タスクの物差し——§2先行研究・§3正典制約G1〜G18・§4設計原則P-01〜P-08・§5組版テンプレ・§6レビュー基準・§7棚卸しF1〜F20は必須）
- docs/09_redesign_fusion.md（融合要素の出典——§2融合一覧・§3序破急・§4予告頁一般形・§6マイクラらしさの制約・§9エンドロール・§11器方針）
- docs/26_narrative_vectors.md（語りベクター・文体規範・環境文字上限§3.4・読み上げの間§8——語り形式と鑑賞層の棲み分け相手）
- docs/20_art_ui_design_system.md（デザイン言語・パレット・§8幻想文字フォント方針——演出UI・暗号字形の親）
- docs/34_chapter_plots/ 全7本＋README.md（各章の語り形式・ボス・見得・結末・環境ビート）
- docs/36_foreshadow_map.md（伏線台帳——F-ORIGIN-03幻想文字・T-PCポストクレジット・結末別演出・考察班対応）
- docs/38_numeric_tables/03_bosses.md（ボス数値・§4.3演出時間規格・拍子視覚合図・即死技予告多重化）
- docs/12_story_outline.md（章概要・感情マップ・序破急整合§43）
- docs/13_progression_map.md（進行表——序破急配分の書き戻し先）
- docs/15_mobs_bosses.md（ボス一覧・予備動作・ノミ同行）
- docs/17_streaming_design.md（配信構造・§7配信者素材・考察班§49）
- docs/28_story_full_flow.md（全編ストーリー——エンドロール後の一場面§145）
- docs/24_story_foundation.md（文書回収型の基本形§18）
- docs/45_nonverbal_guidance/（非言語導線の正典——演出と導線の棲み分け）
- docs/46_distribution_research.md（Patchouli・配布条件——鑑賞層の実装器候補 D-2 は承認待ち）
- docs/50_opening_storyboard.md（OPビート——コールドオープン参照）
- docs/32_system_specs.md（システム仕様——書き戻し先）
- docs/14_items_crafting.md（拾得物・図鑑節——書き戻し先）
- docs/30_adr/（ADR-0003/0004/0005 等の確定決裁）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/47 §5 を厳守）：
- 担当ユニットのファイルの必須節を全て埋める。節構成を勝手に変えない
- マトリクス・カタログ・対応表など規定の表形式は必須列を全部入れる
- 全ルール・仕様に根拠（正典節／docs/47 の先行研究・原則番号）を付ける。感覚だけの提案は不可
- 各演出・仕組みは「バニラの器でどう実現するか」を明記（書物UI・アイテム・暗転・パーティクル・音・挿絵・フォント等）
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（書き戻し先を明記し、本文で直接改変しない）
- docs/51・docs/18・docs/43 は未作成——それらを書き戻し先にする項目は「Issue #11/#3/#8 への手渡し」として記録する形に留める（G18）
- Patchouli は Issue #22 D-2 承認待ち——採用前提と不採用前提の**両形**で記述する（F19）
"""

CONSTRAINTS = """絶対条件（docs/47 §3 の正典制約 G1〜G18）：
- G1 層構造：表層＝読まなくても遊べる。平易さのために深さを削らない。目的は「楽しい」
- G2 環境が先・文字が後：進行必須情報を文字・暗号に置かない
- G3 UIはスキン的変更のみ・操作体系不変
- G4 第2〜4章は順不同：どの順でも成立・他章攻略前提を置かない
- G5 審美「かすれた・欠けた・継がれた」＋基調パレット
- G6 シェーダー/影MOD共存
- G7 救うと色が戻る
- G8 文字は補助層・主線の誘導は非言語で完結
- G9 ボスは読み合い可能・見得=予備動作の定型化
- G10 ノミ＝常時同行の語り装置・導線の主役は環境
- G11 予告頁＝ノミ語り＋挿絵（実シーン不採用・環境側二重化）
- G12 幕間暗転＝各約10秒・間＝応答窓±0.40秒・キュー3.0秒・拍子の視覚合図＝見得と同型
- G13 ポストクレジット＝結末別演出3種＋「まだ拾われていない物語」の示唆
- G14 幻想文字＝外側の世界の言葉・内容＝没になった世界設計の断片・必読情報を置かない・環境文字とは別系統
- G15 用語は正典どおり
- G16 正典の変更は直接書き換えず「要ユーザー承認」
- G17 配信映え・予告は配信の締めとして機能
- G18 未作成 docs（51/18/43）への書き戻しは「Issueへの手渡し」記録に留める
"""

UNITS = [
    {
        "id": "episode_production",
        "title": "U1：エピソード器（01_episode_production.md相当）",
        "scope": "エピソード構造を支える演出器——予告頁の内容構成（声・色・一場面の3要素の割り振り・章ごとの具体例・挿絵規格・動的選択の表示規則 F1/F2・考察材料の配分 F15）・幕間演出（章クリア〜結末綴じ〜次章への接続・幕の形式 F14）・エンドロール（名の流し方・残した者たち・協力者・操作可否・スキップ規則・時間）・ポストクレジット（結末別演出3種 G13 の詳細仕様・一場面の内容・長さ・リプレイ導線）。全てバニラの器（書物UI・暗転・音・挿絵・パーティクル）に翻訳する（P-03）。docs/34 各章・docs/36 T-PC・docs/28 §145・docs/50 との整合を取る。",
    },
    {
        "id": "narrative_forms",
        "title": "U2：語り形式・鑑賞層（02_narrative_forms.md相当）",
        "scope": "章別語り形式の実現仕様——6形式（絵本/書簡/戯曲/日誌/詩/設計書）×章×感情のマトリクス（docs/09 §46・docs/12 と整合）。形式別に「断片の形式（何として出るか）・UI表示（書物UIでの見せ方）・演出（読む際の音・間）・配分量」を定義（F3・F13）。鑑賞層の仕組み——拾い人の手記（読む物語）・拾得図鑑（集める図鑑）・形式の視覚差（読む・観る・聞くの3層 P-04）。Patchouli 採用/不採用の両形で設計（F19・Issue #22 D-2 連動）。読み返し規則（拾った断片がどこで・どう読み返せるか・未読表示）。docs/26 §3.4（環境文字上限）・§8（読み上げの間）との棲み分けを厳守。",
    },
    {
        "id": "theatrical_pacing",
        "title": "U3：演劇器・ペーシング（03_theatrical_pacing.md相当）",
        "scope": "幕/見得テレグラフと序破急ペーシングの実装仕様——見得カタログ（全ボスの予備動作を歌舞伎の見得型に体系化：攻撃種別×見得ポーズ×拍子合図の対応表。docs/34/01・02・docs/15・docs/38/03 から全ボスを抜き出して網羅 F4・F11・F17）・幕の仕様（フェーズ転換の暗転・間・柝の視覚合図 G12・ボス戦以外の幕を切る境界）・序破急配分（章ごとの序/破/急の時間配分・場面比率・章間の緩急差・docs/13 への反映形式 F6）・演劇器の相互作用ルール（見得・幕・序破急・拍子が重なる時の統合）。Issue #15（ボス数値詳細）への入力として使える粒度で。",
    },
    {
        "id": "cipher_ui_boundary",
        "title": "U4：暗号・演出UI線引き（04_cipher_ui_boundary.md相当）",
        "scope": "幻想文字の暗号体系——文字数・対応言語（日本語音節換字案。約50音＋記号）・字形の体系性（母音列/子音行で部品共有）・鍵の渡し方（ゲーム内のどこに対応表を埋め込むか——Tunic/Fez/原神の先例 §2.6）・内容ポリシー（G14 承認済み内容「没になった世界設計の断片」への文の落とし込み）・配置規則（どこに・どの密度・環境文字 G14/F12 との区別）・外部ARG接続（docs/09 §5 宣伝サイト構想 F20）。演出UI線引きの法典——可（スキン的変更：枠・書物UI装丁・頁めくり・幕間・結末綴じ・エンドロール・国UIスキン F16）／不可（操作体系・ホットバー・インベントリ・必須操作）を項目別に白黒明記＋語り形式別の「皮の変わり方」見本（装丁差・枠意匠差）。docs/20 §8 フォント方針と整合。",
    },
]

META = {
    "name": "fusion-elements-forge",
    "description": "異ジャンル融合要素の詳細化（Issue #28）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典から融合要素の手渡し項目を棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・形式整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットのファイル全文（Markdown）"},
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
        "inventory_md": {"type": "string", "description": "抽出した全手渡し項目・融合要素の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #28（異ジャンル融合要素の詳細化）へ手渡されている全ての項目・演出要求・未定義の物差し**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #28」「融合」「予告頁」「語り形式」「見得」「幕」「序破急」「エンドロール」「ポストクレジット」「幻想文字」「暗号」「鑑賞」「演出UI」に言及されている箇所（grep で総当たり）
2. docs/47 §7 の棚卸し F1〜F20 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/34 各章プロットに既に書かれている語り形式・見得・序破急・結末・予告・幕間の記述の全抽出
4. docs/36 伏線台帳のうち予告頁・幻想文字・ポストクレジット・語り形式に関わる項目（T-PC・F-ORIGIN-03・K9-K11・F-entries 等）
5. docs/09 で「詳細化が必要」とされている全要素
6. docs/20・26 で確定済みのフォント方針・文体規範・環境文字上限・読み上げの間——演出UI・暗号・鑑賞層が守るべき線
7. 「形式・演出・暗号・UIスキン」で語るべきだがまだ仕様がない全項目

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（演出器/語り形式/演劇器/暗号/UI線引き/制約）｜優先度（必須/任意）」。docs/47 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の演出設計者。{unit['title']} を、調査基準（docs/47）に基づき深い思考で執筆せよ。

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
- まず docs/47 §4 の設計原則 P-01〜P-08 に載せてから、要素の事情で具体化する
- 先行例（§2）を根拠に引く——「○○の系譜（TunicのTrunic）」「歌舞伎の見得」等の参照明記
- 全ての演出はバニラの器に翻訳する（P-03）。抽象論で終わらせない
- 語り形式は「どう読ませるか」まで掘る（断片の形式・UI表示・演出・配分量）
- 暗号は「必読情報を置かない・鍵はゲーム内・内容は承認済みポリシー」の3条件を満たす
- 「要承認」は推奨案つきで open_questions に集約（書き戻し先を明記）

## 出力形式（section_md）
docs/47 §5 の担当ユニットの必須節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の演出レビューア。以下の設計を、docs/47 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/47 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/47 §6 の3段分類を適用）
1. **正典制約適合**：G1〜G18 の各条項に反する設計がないか（特に G2 文字後置・G3 操作体系不変・G4 順不同・G11 予告頁方式・G12 幕間規格・G13 ポストクレジット3種・G14 暗号ポリシー）
2. **網羅性**：棚卸し項目（docs/47 §7 F1〜F20 と抽出結果）が全て回収されているか、§5 の必須節・必須列に欠落がないか
3. **根拠**：全仕様に参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：実装者がこの表だけで作業できる具体度か（バニラの器・形式・配分が書かれているか）
5. **層整合**：表層と深読み層の境界を守っているか、必読情報を文字・暗号に置いていないか
6. **状態管理**：要承認に書き戻し先があるか、未作成docs（51/18/43）への手渡しは Issue 記録になっているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の演出設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/47 §7・Issue #28 の対象要素（予告頁・語り形式・幕/見得・序破急・エンドロール・ポストクレジット・幻想文字暗号・鑑賞層・演出UI線引き）が4ユニットのいずれかで扱われているか、必須節・必須表が揃っているか、要承認に書き戻し先があるか",
        "forms": "形式・規則整合——ユニット間で演出ルールが食い違わないか（予告頁と幕間・語り形式と鑑賞層・見得と幕・暗号と環境文字の棲み分け・UI線引きと形式別スキン）、同じ要素（幕・書物UI・挿絵）がユニット間で矛盾なく使われているか、層構造（表層/深読み層）の境界が全体で一貫しているか",
        "canon": "正典整合——4ユニット全体が docs/09/12/13/15/17/20/26/28/32/34/36/38/45/46/50 の記述と矛盾しないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**融合要素詳細化の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/47 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 融合要素の手渡し項目棚卸し（抽出） ===")
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
