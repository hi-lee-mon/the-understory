import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/39_research_nonverbal_guidance.md（本タスクの物差し——§2先行研究・§3正典制約G1〜G16・§4設計原則P-01〜P-12・§5組版テンプレ・§6レビュー基準・§7棚卸しN1〜N18は必須）
- docs/09_redesign_fusion.md §6（層構造・マイクラらしさの制約——ユーザー指針の出典）
- docs/20_art_ui_design_system.md（デザイン言語・パレット・シェーダー対応——本Issueの書き戻し先）
- docs/13_progression_map.md（進行・順不同・迷子防止——本Issueの書き戻し先）
- docs/50_opening_storyboard.md（OPビート——本Issueの書き戻し先）
- docs/26_narrative_vectors.md（語りベクター・「環境が先・文字が後」の棲み分け相手）
- docs/11_world_bible.md（世界法則・用語）
- docs/12_story_outline.md（章概要・感情マップ）
- docs/23_discard_grammar.md（ゴミ箱・異物・返礼——現実側導線の対象）
- docs/28_story_full_flow.md（全編ストーリー詳細）
- docs/32_system_specs.md（異物生成・羅針盤・往復・マルチ細目）
- docs/34_chapter_plots/ 全7本＋README.md（各章の環境ビート・ボス・結末・断片配置）
- docs/36_foreshadow_map.md（伏線配置表——非言語手がかりの配分対象）
- docs/15_mobs_bosses.md（ボスの予備動作・フェーズ・ノミ常時同行）
- docs/14_items_crafting.md（縁の羅針盤・拾得物・由来鑑定）
- docs/30_adr/（ADR-0003/0004/0005 等の確定決裁）
- AGENTS.md（作業規範）
"""

RULES = """成果物の組版（docs/39 §5 を厳守）：
- 担当ユニットのファイルの必須節を全て埋める。節構成を勝手に変えない
- 媒体×役割マトリクス・必須チャネル表など規定の表形式は必須列を全部入れる
- 全ルールに根拠（正典節／docs/39 の先行研究・原則番号）を付ける。感覚だけの提案は不可
- 各環境・導線設計は「バニラの器でどう実現するか」を明記（光源・パーティクル・音色・構造物・地形等、docs/39 §2.8 の語彙表を使う）
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（書き戻し先を明記し、本文で直接改変しない）
"""

CONSTRAINTS = """絶対条件（docs/39 §3 の正典制約 G1〜G16）：
- G1 層構造：表層＝読まなくても遊べる。平易さのために深さを削らない。目的は「楽しい」
- G2 環境が先・文字が後：進行必須情報を文字に置かない
- G3 UIはスキン的変更のみ・操作体系不変
- G4 第2〜4章は順不同：どの順でも導線が成立・他章攻略前提を置かない
- G5 審美「かすれた・欠けた・継がれた」＋基調パレット（灰青・月白・墨・古金／アクセント朱・琥珀）
- G6 シェーダー/影MOD共存（Iris＋主要シェーダーで崩れない）
- G7 救うと色が戻る（進行の可視化——確定済み）
- G8/G9 没腐コンパス・縁の羅針盤は二次装置。環境が一次導線
- G10 異物＝片道の発見型入口・周囲の没腐が濃い
- G11/G12 ボスは読み合い可能・撃破＝理解と救済
- G13 ノミ＝常時同行の語り装置。導線の主役は環境、ノミは補助
- G14 配信映え：視聴者が画面から読める強度
- G15 用語は正典どおり（拾い人/ノミ/拾得物/没腐/淀み/縁の地/読む者/原案の座等）
- G16 正典の変更は直接書き換えず「要ユーザー承認」
"""

UNITS = [
    {
        "id": "system_grammar",
        "title": "U1：導線の体系文法（01_system_grammar.md相当）",
        "scope": "非言語導線の文法体系——媒体×役割マトリクス（光・色彩・音・造形・粒子・動き・記号・ランドマーク・装置 × 方向指し・重要度・危険度・接近度・物語の痕跡・相互作用標識・領域区切り）。各媒体の強度ルール・距離による変化・複数導線競合時の優先順位・併用規則（必須ペア／相性／禁則）・禁止事項（押し付けすぎ・単一チャネル・文字依存）。「朧な光」（N1）・彩度勾配（N2）・拾える物の色と音（N3）の形式化。docs/39 §2.8 のバニラ語彙表を器として使い、シェーダー共存（G6）も規則に織り込む。",
    },
    {
        "id": "guidance_applications",
        "title": "U2：場面別の導線適用（02_guidance_applications.md相当）",
        "scope": "文法の場面別適用——漂着浜から第1章までの誘導全工程（docs/50 ビートに対応させる）・各環礁の共通構造（遠望点→遮蔽と開示→中心への勾配。順不同2〜4章で成立すること）・環礁内局面（探索・迷子時の自動誘導・ボス接近・結末地点・章クリア後の色の回帰 G7）・現実側（縁の地の発見 N16・異物の視認 N8・ゴミ箱への気づき・往来）・村の視認性・ボス戦と結末・幕間の演出（見得 N9・フェーズ転換・結末綴じ地点 N10）・補助環礁の見つけ方（本線より弱い気配）。迷子防止の二重構造（環境一次・装置二次 P-10）を全場面で具体化。",
    },
    {
        "id": "environmental_storytelling",
        "title": "U3：環境が語る層（03_environmental_storytelling.md相当）",
        "scope": "環境ストーリーテリングの語彙と章別適用——配置パターンの辞書（残骸・打痕・書きかけ・整頓/散乱・向き・反復・欠如・保存がそれぞれ語る意味）・因果の連鎖を見せる配置・密度勾配（中心へ向かうほど濃く）・docs/26 との棲み分け（環境が先に『何かがあった』、文字が後で『何だったか』）。各環礁で「ここで何があったか」を環境だけで示す設計（docs/34 各章の環境ビート N12 を言語化・拡張）。伏線の非言語手がかり配分（docs/36 と接続 N13）。解釈を開く作法（断定しない配置・複数の読み P-09）。",
    },
    {
        "id": "affordance_accessibility",
        "title": "U4：全年齢アフォーダンス・多重化・配慮（04_affordance_accessibility.md相当）",
        "scope": "中学生以上が説明なしに「次に何をすればいいか」分かる仕組み——行動・行き先・目的の見える化（何が拾えるか・どこが開いたか・何が終わったかの非言語表示）。多重化規則（重要度別の必須チャネル表：最重要＝3系統／主要＝2系統／補助＝1系統 P-07・N15）。色覚特性への配慮（色のみ依存の禁止・形と位置での代替）・聴覚配慮（音だけに依存しない・字幕・視覚的代替）・マルチ時の導線（環境手がかりの共有 N17）・Issue #34 へ手渡すコンフィグ項目の一覧。",
    },
]

META = {
    "name": "nonverbal-guidance-forge",
    "description": "非言語の導線・環境ストーリーテリング設計（Issue #31）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典から導線・環境手がかりの手渡し項目を棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・層整合・正典整合の横断監査", "count": 3},
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
        "inventory_md": {"type": "string", "description": "抽出した全手渡し項目・導線制約の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #31（非言語の導線・環境ストーリーテリング）へ手渡されている全ての項目・導線要求・未定義の物差し**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #31」「非言語」「導線」「環境ストーリーテリング」「迷子」「アフォーダンス」に言及されている箇所（grep で総当たり）
2. docs/39 §7 の棚卸し N1〜N18 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/34 各章プロットに既に書かれている環境ビート（配置・打痕・手紙の束・巡回・書きかけ・光・音による示唆）の全抽出
4. docs/36 伏線台帳のうち非言語・環境に置くべき手がかり
5. docs/50 のビートで非言語の演出が要求されている箇所
6. docs/09・20・26 で確定済みの層構造・審美・棲み分け規則のうち導線設計に効くもの
7. 「色・光・音・形・配置」で語るべきだがまだ仕様がない全項目

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（文法/場面/環境物語/アフォーダンス/a11y/制約）｜優先度（必須/任意）」。docs/39 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の導線設計者。{unit['title']} を、調査基準（docs/39）に基づき深い思考で執筆せよ。

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
- まず docs/39 §4 の設計原則 P-01〜P-12 に載せてから、場面の事情で具体化する
- 先行例（§2）を根拠に引く——「○○の系譜（Elden Ringの祝福）」等の参照明記
- 全ての導線はバニラの器に翻訳する（§2.8）。抽象論で終わらせない
- 環礁の導線は「遠望→遮蔽→勾配」の骨格を章ごとに言語化する
- 深読み層（docs/26）に踏み込まない——環境は「何かがあった」まで、『何だったか』は文字の層
- 「要承認」は推奨案つきで open_questions に集約（書き戻し先を明記）

## 出力形式（section_md）
docs/39 §5 の担当ユニットの必須節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の導線レビューア。以下の設計を、docs/39 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/39 の該当節を実際に開いて突き合わせること。記憶で判定しない��。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/39 §6 の3段分類を適用）
1. **正典制約適合**：G1〜G16 の各条項に反する設計がないか（特に G2 環境先・G3 操作体系不変・G4 順不同・G6 シェーダー共存・G13 ノミは補助）
2. **網羅性**：棚卸し項目（docs/39 §7 N1〜N18 と抽出結果）が全て回収されているか、§5 の必須節・必須列に欠落がないか
3. **根拠**：全ルールに参照（正典節／先行研究／原則番号）があるか
4. **実用レベル**：実装者がこの表だけで作業できる具体度か（バニラの器・強度・配置が書かれているか）
5. **層整合**：表層と深読み層の境界を守っているか、進行必須情報を文字に置いていないか
6. **状態管理**：要承認に書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の導線設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/39 §7・Issue #31 の設計対象（非言語導線・環境ストーリーテリング・全年齢アフォーダンス・視認性/聴覚配慮・バニラ語彙活用）が4ユニットのいずれかで扱われているか、必須節・必須表が揃っているか、要承認に書き戻し先があるか",
        "layers": "層・規則整合——ユニット間で導線ルールが食い違わないか（文法の強度規則と場面適用・多重化表と a11y・環境物語と docs/26 棲み分け）、表層/深読み層の境界が全体で一貫しているか、多重化（≥2チャネル）が全重要情報で守られているか",
        "canon": "正典整合——4ユニット全体が docs/09/11/13/20/23/26/28/32/34/36/50 の記述と矛盾しないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**導線設計の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/39 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 手渡し項目・導線制約の棚卸し（抽出） ===")
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

    cov_check, layer_check, canon_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "layers", inventory), phase="crosscheck", label="cc-layers", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("layers", layer_check), ("canon", canon_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "layers": layer_check, "canon": canon_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
