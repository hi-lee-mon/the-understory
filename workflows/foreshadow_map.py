import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/11_world_bible.md（世界法則）
- docs/12_story_outline.md（章概要）
- docs/22_research_emotion_design.md（感情設計）
- docs/23_discard_grammar.md（ゴミ箱文法）
- docs/24_story_foundation.md（真実の構造・伏線工学）
- docs/25_characters.md（登場人物）
- docs/26_narrative_vectors.md（語りベクター・文体規範）
- docs/28_story_full_flow.md（全編ストーリー詳細——正典）
- docs/32_system_specs.md（システム仕様）
- docs/35_research_foreshadowing.md（伏線設計の基準——本タスクの物差し）
- docs/34_chapter_plots/ 全7本（00_prologue, 01_moon_forest, 02_unread_harbor, 03_unheld_square, 04_unchosen_mine, 05_unsung_tower, 06_final_seat）——各章 §9 の伏線受け渡し表と §8 断片表が最重要の素材
- AGENTS.md（作業規範）
"""

LEDGER_SCHEMA_DESC = """伏線台帳の行形式（docs/35 §8）：
| ID | 伏線 | 表層の読み | 撒き（章・場所・ベクター） | 濃度勾配 | 回収（章・形態） | 距離 | 明答度 | 順不同耐性 | 再読の味 | 状態 |
距離 = 短距離（章内完結）/ 中距離（1〜2章跨ぎ）/ 長距離（全編——終盤で初めて問いが立つ種類のみ）
状態 = 設置済み（docs/34 または正典に実在）/ 要追記（配置先と追記内容を明記）
"""

CONSTRAINTS = """絶対条件：
- 明答しない構造：表層で答えを直接書かない。答えは断片の集積から組み立てる（20%ルール——注意深いプレイヤーの約2割が終章前に推測可能な程度）
- 順不同耐性：第2〜4章はどの攻略順でも伏線が破綻しない（他章の攻略を前提にしない）
- フェアプレイ：重大な真相は全て終章以前に断片として配置済み。終章は答え合わせであって新情報の開示ではない
- 副次的役目：各断片は伏線以外の物語機能を持つ（透ける伏線は作らない）
- 用語は正典どおり（拾い人/ノミ/拾得物/没腐/落慮王/原案の座/淀み/読む者 等）
- セリフの実文は書かない（配置と役割のみ）
- 正典を変更する提案は「要ユーザー承認」と明記し、直接変更しない
"""

UNITS = [
    {
        "id": "core_mysteries",
        "title": "U1：正体系・長距離伏線",
        "scope": "本作の核心の謎5系統の全ライフサイクル設計：①ノミの正体（原案の案内人——招待状の筆致・口癖・座の話題を逸らす・『来たか。待っていた』）②落慮王の正体と問い（世界の最初の原案・『選ばれなかったものに価値はなかったのか』）③前任の拾い人（落書きの主・磯の残骸・座で止まった者・白紙の頁）④国の起源（世界に捨てられた地形＝異物・原案の座・設計刻印・幻想文字）⑤『あんたも捨てる側だ』の転調（自分の捨て物が風景・二度棄て・集積の間の自分の区画）。各系統について：撒き（どこに何を・どのベクターで）→濃度勾配（中間でどう強化）→回収（終章での着地形態）→表層の読み（誤読を含む正しい中間解釈）→20%ルールの検証→順不同耐性。docs/34 各章 §9 の既存伏線を棚卸しして統合し、欠落した撒き・回収を補完設計する。",
    },
    {
        "id": "mechanism_foreshadowing",
        "title": "U2：機構系・中距離伏線",
        "scope": "ゲーム機構と絡む伏線の設計：①二度棄て→原案の座の文法（予告→着弾→着地証明）②ゴミ箱返信機構（読む者の存在の気配→灯台守救出→返信が来る→最後の手紙）③招待状の送り主（筆致の滲み→案内人の項）④拾得鍛錬の由来鑑定（名付き品の不在→各章で『誰かの宝物』として再会）⑤結末の欠片（結末綴じ画面の垣間見せ→終章の器）⑥月の共有空（第1章の結末が他環礁の空に見える）⑦淀みと滞留の規則（序章の窪地→届かなかった物の行き先→座の届きもの棚）⑧鍛冶師の没素材＝原案の一部⑨「一緒に歌う」分岐フラグ→歌姫の頁の差分⑩特大物→座行き。これらは短距離〜中距離が主体：各系統の撒き・中継・回収と、システム仕様（docs/23・32）との整合を設計する。",
    },
    {
        "id": "turning_points",
        "title": "U3：転調点の設計",
        "scope": "全編の「あっ」という転調点の一覧と品質設計：①中盤転調（落慮王の歪みがプレイヤーの捨て物に向く——『あんたも捨てる側だ』）②各章ミッドポイントの綱目（第1〜5章・終章で『知っているつもりが覆る』瞬間の構造比較——多様性があるか・型が反復して陳腐化しないか）③終章の二重転調（王の正体開示＋ノミの正体開示＋前任の着地）④「書き換える」の警告構造（前任の結末が書き換えの安易さを警告）⑤結末綴じ画面の反転（拾う＝第三の答えの出現条件）。各転調点に5問テスト（稼いだか/再読で太るか/意外だが必然か/再解釈するか/20%ルール）を適用し、事前布石と後の再解釈を明記する。",
    },
    {
        "id": "density_and_stealth",
        "title": "U4：考察班供給・再読性・隠蔽設計",
        "scope": "深読み層の密度設計：①考察班対応（幻想文字＝解読可能暗号の配置戦略、ARG・Wiki考察への投入物、確証なき推測が組める密度の基準）②再読性設計（2周目で意味が変わる断片の要件——初見で無害に読め、知ると意味が反転する文の作り方）③濃度勾配の全体配分（序章は最小限→第4章で前任の落書きが濃くなる→終章で収束、の曲線設計）④明答しないルールの運用基準（どの層までなら書いてよいか——表層/深読み層/考察班層の三段階）⑤ノイズ設計（本物の手がかりを埋もれさせる無害な情報の量と種類）。語りベクター（docs/26）との整合も担う。",
    },
]

META = {
    "name": "foreshadow-map-forge",
    "description": "全編を貫く伏線台帳・転調点の設計（Issue #30）——抽出→クラスタ別設計→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典・docs/34 から全伏線の棚卸し", "count": 1},
        {"title": "write", "detail": "4クラスタの設計執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・順不同耐性・明答度の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当クラスタの設計セクション全文（Markdown・台帳形式を含む）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項"},
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
        "inventory_md": {"type": "string", "description": "抽出した全伏線・転調の生棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の物語監査役。リポジトリ内の全設計書から、**現在実在する全ての伏線・転調・未回収の仕掛け**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/34 各章 §9「伏線の受け渡し」表の全行（撒く側と回収側の両方）
2. docs/34 各章 §8 ロア断片のうち「どこかで意味が回収される」断片
3. docs/24 §4 真実の構造の各要素（世界の起源・落慮王・没腐・ノミ・読む者・結末の意味）がどこに撒かれているか
4. docs/25 各人物の「秘密」の開示経路
5. docs/28 にある転調点（中盤転調・終章転調・章ごとの覆し）
6. 章間を跨ぐ全ての仕掛け（王宛の手紙・一緒に歌うフラグ・結末の欠片・前任の落書き・二度棄ての文法・月の共有・幻想文字等）

## 出力
inventory_md に Markdown で：各行「対象｜撒き（どこに・何が）｜回収（どこで・形態）｜出典（ファイル・節）｜分類（正体/機構/転調/考察班）」。回収先が設計上まだ無いものは「回収＝未配置」と明記。解釈せず実在する記述を忠実に集めること——判断は後続の設計エージェントが行う。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の伏線設計者。{unit['title']} の設計を、調査基準（docs/35）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 既存の伏線棚卸し（抽出済みの実在リスト——これに基づき統合・補完せよ）
```markdown
{inventory}
```

{LEDGER_SCHEMA_DESC}

{CONSTRAINTS}

## 出力形式（section_md）
1. **クラスタの目的**：この系統が全編に担う機能
2. **伏線台帳**（上記スキーマの表）：対象系統の全伏線。docs/34 に既にあるものは「設置済み」、不足・追加提案は「要追記」で配置先を明記
3. **開示ペースの設計**：どの章でどこまで見せるか（表層/深読み層/考察班層の段階）
4. **順不同耐性の検証**：第2〜4章をどの順でプレイしても成立する根拠
5. **20%ルールの検証**：注意深いプレイヤーが事前に推測可能か、何を見れば辿り着くか
6. **未決・要承認**（open_questions へも出力）"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の伏線レビューア。以下の設計を、docs/35 の検証基準に照らして厳しくレビューせよ（深い思考——正典の該当節を実際に開いて突き合わせること）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/35 §9 の物差しを適用）
1. **網羅性**：棚卸しにあった当該系統の伏線が全て台帳にあるか、各行に回収先があるか
2. **フェアプレイ**：終章以前に断片が置かれているか／表層に答えが書かれていないか
3. **順不同耐性**：第2〜4章依存の伏線がどの順でも成立するか
4. **距離の健全性**：長距離伏線が「終盤で初めて問いが立つ」種類か
5. **ミスディレクション**：各行に「表層の読み」があるか（副次的役目を持つか）
6. **正典整合**：docs/11/23/24/25/26/28/32 および docs/34 各章の記述と矛盾しないか
7. **実装可能性**：配置が場所・ベクター・個数まで具体化されているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings):
    return f"""あなたは Minecraft MOD「The Understory」の伏線設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{LEDGER_SCHEMA_DESC}

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
        "coverage": "網羅性——棚卸しの全伏線が4クラスタのいずれかで扱われているか、台帳の各行に回収先（または『回収しない』の明示的意図）があるか、終章で回収されるものが全て種を持つか（逆方向網羅性）",
        "ordering": "順不同耐性と距離の健全性——第2〜4章由来の伏線がどの攻略順でも破綻しないか、長距離伏線が『終盤で初めて問いが立つ』種類か（Lost効果の検査）、開示ペースのクラスタ間整合",
        "stealth": "明答度とベクター整合——表層に答えが直接書かれていないか、各断片のベクターが docs/26 の媒体配分と矛盾しないか、20%ルール（ノミ・王・前任の正体が注意深いプレイヤーに推測可能か）",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**伏線設計の4クラスタ全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：元の棚卸し
```markdown
{inventory}
```

## 全クラスタ設計
{all_sections_text}

出力：accepted、findings（クラスタ横断の問題のみ——単一クラスタ内の問題は各レビューの責任なので挙げない）。"""


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
    log("=== Phase 1: 伏線の棚卸し（抽出） ===")
    inv = await agent_retry(
        extract_prompt(),
        phase="extract", label="extract-inventory",
        schema=EXTRACT_SCHEMA, repos=[REPO], soft_time_limit_minutes=50,
    )
    inventory = inv["inventory_md"]
    log(f"棚卸し完了（{len(inventory)} 文字）")

    log("=== Phase 2: 4クラスタの設計・レビュー・改訂ループ ===")
    results = []
    for batch in (UNITS[:2], UNITS[2:]):
        results.extend(await pipeline(batch, lambda u: unit_flow(u, inventory)))
    log("=== 4クラスタ完了。横断監査へ ===")

    all_sections_text = "\n\n---\n\n".join(
        f"## {r['title']}\n\n{r['section_md']}" for r in results
    )
    log(f"全セクション合計 {len(all_sections_text)} 文字")

    cov_check, ord_check, stealth_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "ordering", inventory), phase="crosscheck", label="cc-ordering", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "stealth", inventory), phase="crosscheck", label="cc-stealth", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("ordering", ord_check), ("stealth", stealth_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "ordering": ord_check, "stealth": stealth_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
