import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/61_research_glossary.md（本タスクの物差し——§1 先行調査・§2 絶対制約 G-GL-01〜12・§3 原則 P-GL-01〜10・§4 棚卸し H-01〜10・§5 組版テンプレは必須）
- docs/05_production_docs_structure.md（文書体系——用語集の参照関係の前提）
- docs/00_development_plan.md（Phase 構造——工程語の由来）
- docs/11_world_bible.md（世界観語の最大源泉）
- docs/10_game_design_document.md（GDD——世界観語・システム語）
- AGENTS.md（作業規範——Phase 0＝設計のみ・日本語・面白さの最終決定権＝ユーザー）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/61 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 用語集＝**名前の台帳**。定義・数値・仕様は再掲せず「定義の正本＝docs/NN §x.y」の参照で示す（G-GL-01）
- 承認済みの正典の名・ID・キーを本書側で改変しない（G-GL-02）。英語名は既存のもののみ収録——新造しない（G-GL-03）
- 層別：世界観語＝§1、システム語＝§2、工程語＝§3、識別子＝§4、英語名＝§5（G-GL-04/05）
- エントリ欄：｜用語｜読み（非自明のみ）｜英語名/識別子｜定義の正本（docs/NN §x.y）｜状態（確定/暫定/未命名/異表記あり）｜異表記・備考｜
- 異表記・同名異物・定義ずれ・未命名の語は「衝突」として検出し open_questions に起票（P-GL-09・G-GL-10——ID＝44-U{n}-Q{m}・推奨案・書き戻し先つき）
- 「要承認」は open_questions に集約し、本文側では参照IDを括弧書きで示す
- Phase 0 制約：lang ファイル等の実装成果物は作らない
"""

CONSTRAINTS = """絶対条件（docs/61 §2 の G-GL-01〜12）：
- G-GL-01：定義は引用のみ——数値・仕様の再掲禁止
- G-GL-02：命名の権威は正典側——改名・統一は要承認のみ
- G-GL-03：英語名を新造しない——未定は「未命名」と記す
- G-GL-04/05：層別・識別子は索引化のみ（個別IDの全列挙はしない）
- G-GL-06：収録は正典で命名・定義済みの語に限る
- G-GL-09：非自明な読みは全件に読み仮名
- G-GL-10：要承認は 44-U{n}-Q{m}・推奨案・書き戻し先つき
- G-GL-12：登録運用（新語登録・改名・廃止の手順）を本書に含める
"""

UNITS = [
    {
        "id": "world_terms",
        "title": "U1：§1 世界観語（docs/44 §1）＋§5 英語名台帳（同 §5）",
        "scope": "§1 世界観語（ゲーム内・物語上の固有名称の全表——棄てられたものの国・没腐・拾得鍛錬・落慮王・ノミ・拾い人・拾い人の村・縁の地・月中継点・異物・デカいゴミ箱/ゴミ箱・返礼・没の由来品・残影・写し・由来札・拾得物・拾得・響界・白紙の名札・見得・幕・柝・拍子・物語の終わり・静まり・章名5章＋終章・祭事・月・沖の小島・結晶・記憶の欠片 等——読み仮名・英語名・正本節・状態・異表記の各欄）＋§5 英語名台帳（正典で既に使われている英語名の一覧〔The Understory・anomaly 等〕＋未命名の主要語リスト——Phase 4 対訳の種表。未命名は全件可視化し、新造しない）",
        "docs": "担当正典：docs/10・11・12・13・23・24・25・26・27・28・34_chapter_plots/（README＋7章＋終章）・36・36a・48_fusion_elements/・50・09",
    },
    {
        "id": "system_terms",
        "title": "U2：§2 システム語（docs/44 §2）",
        "scope": "§2 システム語（機構・数値・UI/音響の仕様名の全表——器スロット・段位・拾得鍛錬台・個人没腐度・没腐遺留物・拾い直し制・環礁・疑似ループ・発火抑制・イベント台帳・解禁チャネル・没腐度・リスポーン優先順位・同士討ち・変換表・迷子・導線・照準層・通知型・読み上げ・字幕名・配信モード・没腐コンパス・羅針盤・名札器・葬送・パフォーマンス 等——読み仮名・英語名/識別子・正本節・状態・異表記の各欄）",
        "docs": "担当正典：docs/14・15・16・17・18・19・20・32・38_numeric_tables/（README＋01〜04）・45_nonverbal_guidance/（README＋01〜04）・33・35・37・39",
    },
    {
        "id": "process_terms",
        "title": "U3：§3 工程語（docs/44 §3）＋§4 識別子・命名規則の索引（同 §4）",
        "scope": "§3 工程語（開発内部語の全表——垂直スライス・スライス外台帳・完成品質・検証3層・good enough・量産可否・先行ゲート・段間ゲート・解禁判定・巻き戻し・要承認・決裁・レビュー契機・発火トリガー・段 A〜F・工程 8-A〜N・PoC・熱リハ・スパイク・スコアリング・閾値・台帳・監視票・早期警戒指標・残存リスク・状態 watching/realized/closed・Phase 0〜5・テスト3層・L1/L2/L3・母集団・分母・イベント台帳・切り抜き瞬間・見どころ 等——読み・英語名は原則なし・正本節・状態・異表記）＋§4 識別子・命名規則の索引（N-ITEM/N-DEV/N-GEAR/N-ECO 接頭辞体系・`understory.<領域>.<主体>.<動作>` 音名・`subtitles.*`・advancement・config キー・セーブキー・lang キー規則——**個別IDは列挙せず採番規則の正本節を索引化**。命名の新規採番ルール〔命名が要る時の手続き：正本書で採番→用語集へ登録〕）",
        "docs": "担当正典：docs/00・05・40・41・42・43・46・57・58・59・60・30_adr/（README＋ADR全件）・STATE.md・todo.md・AGENTS.md・.devin-work は対象外",
    },
    {
        "id": "scaffold_conflicts",
        "title": "U4：§0 位置づけ＋§7 登録運用＋§9 手渡し＋衝突棚卸し（docs/44 §0・§7・§9）",
        "scope": "§0 位置づけ（本書の役割＝名前の唯一台帳・定義の正本は各正典・引用のみ・収録基準・状態欄の読み方・使い方4局面〔設計書執筆/実装命名/翻訳/配信素材〕）＋§7 登録運用（新語の登録手順〔Issue 手渡し→用語集登録→正本節指定〕・改名/廃止の手順〔要承認必須〕・衝突検出時の流れ〔検出→要承認起票→承認後に主語と異表記を編集〕・定期的な語彙の衛生〔Issue 完了時・Phase 境界の点検項目化〕）＋§9 手渡し（消費先一覧——docs/05 文書体系・Issue #10/#11 執筆時の語彙参照・Issue #34 a11y・Phase 4 英語版・docs/43 §5 配信素材・実装命名規則）＋**衝突棚卸し**：全正典を読み、一概念複数名（用字ゆれ・略称・旧称）・同名異物・定義ずれ・正典で参照されるが名のない概念を検出して一覧化（各候補に正典出典2箇所以上の引用を付す——全件要承認候補として open_questions へ）",
        "docs": "担当正典：全書を横断して読む（特に用語の出現が多い docs/10〜13・23〜28・32・38・40〜43・45・48・50 系）",
    },
]

META = {
    "name": "glossary",
    "description": "用語集 docs/44（Issue #9）——用語棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からの用語候補の棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown——エントリ表）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝44-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した用語候補の棚卸し（Markdown——語・正本節・種別）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の用語監査役。リポジトリ内の全設計書から、**用語集 docs/44（Issue #9）が収録すべき全用語**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. **世界観語**：固有名詞・世界の言葉（棄てられたものの国・没腐・拾得鍛錬・落慮王・ノミ・拾い人の村・縁の地・月中継点・異物・デカいゴミ箱・返礼・没の由来品・残影・写し・由来札・響界・白紙の名札・見得・幕・柝・拍子・物語の終わり・静まり・章名・月・沖の小島・結晶・記憶の欠片 等）
2. **システム語**：機構・仕様の名前（器スロット・段位・個人没腐度・没腐遺留物・拾い直し制・環礁・疑似ループ・発火抑制・イベント台帳・解禁チャネル・没腐度・リスポーン優先順位・変換表・迷子・導線・照準層・通知型・読み上げ・字幕名・配信モード・没腐コンパス・名札器 等）
3. **工程語**：開発内部語（垂直スライス・スライス外台帳・完成品質・検証3層・good enough・量産可否・先行ゲート・段間ゲート・解禁判定・巻き戻し・要承認・決裁・段 A〜F・工程 8-A〜N・PoC・L1/L2/L3・母集団・切り抜き瞬間 等）
4. **識別子規則**：N-ITEM/N-DEV/N-GEAR/N-ECO 接頭辞・`understory.<領域>.<主体>.<動作>`・`subtitles.*`・advancement・config・セーブ・lang キーの各命名規則の正本節
5. **英語名**：正典で既に使われている英語名の一覧（The Understory・anomaly 等）
6. **読みの非自明語**：ふりがなが必要な語（没腐＝ぼっぷ・落慮王・拾得・由来 等）
7. **異表記・衝突の兆候**：同じ物を指す別表記・同名異物・定義のずれが疑われる語
8. **docs/40 §9 の Issue #9 手渡し語**：垂直スライス・スライス外台帳・完成品質・検証3層・good enough・量産可否・月中継点

## 出力
inventory_md に Markdown で：「語｜読み（あれば）｜英語名/識別子（あれば）｜正本節（docs/NN §x.y——必ず実在を確認して書く）｜種別（世界観/システム/工程/識別子/英語名/読み語/異表記兆候）｜備考（異表記候補・正典間ずれの兆候）」。解釈・統一はしない——実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の用語集編集者。{unit['title']} を、調査基準（docs/61）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## 正典からの用語棚卸し（抽出済み——網羅的に回収せよ。ただし正本節は必ず自分で開いて確認すること）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/61 §3 の設計原則 P-GL-01〜10 に載せてから、語ごとの事情で具体化する
- 収録語は「正典で命名・定義済み」の語に限る（G-GL-06・P-GL-04）——一度きりの修辞句は除く
- 定義欄は正本節参照（`docs/NN §x.y`）＋ごく短い要旨のみ——数値・仕様の再掲禁止（G-GL-01）
- 非自明な読みは全件に読み仮名（G-GL-09）
- 英語名は正典実在のもののみ——未定は「未命名」（G-GL-03・P-GL-06）
- 異表記・衝突・未命名・同名異物は open_questions へ `44-U{{n}}-Q{{m}}` で起票（推奨案＋書き戻し先必須——G-GL-10）
- 表は Markdown テーブル：｜用語｜読み｜英語名/識別子｜定義の正本｜状態｜異表記・備考｜

## 出力形式（section_md）
docs/61 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の用語集レビューア。以下の設計を、docs/61 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/61 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点（3段分類）
1. **制約適合**：G-GL-01〜12 に反する記述がないか（特に引用のみ・命名権威・英語名の新造禁止・層別・識別子索引化・読み仮名）
2. **網羅性**：docs/61 §4 の担当 H 項目の語が全て収録されているか——正典で命名済みの語の漏れがないか（担当正典を実際に開いて拾い直せ）
3. **正本節の実在性**：各エントリの「定義の正本」参照が実在する節を指しているか（`docs/NN §x.y` の節番号を実際に確認）
4. **1概念1エントリ**：別表記が別行に散っていないか（P-GL-01）
5. **層別**：工程語が世界観語に混ざっていないか（G-GL-04・P-GL-10）
6. **衝突の取り扱い**：異表記・同名異物・定義ずれが黙って統一されていないか（要承認に上がっているか——P-GL-09）
7. **要承認管理**：ID・推奨案・書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の用語集編集者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/61 §4 の H-01〜10 が4ユニットのいずれかで回収されているか、§0〜§9 の必須節が揃っているか、正典で命名済みの語の漏れがないか（主要正典を実際に開いて拾い直せ）",
        "consistency": "整合——同一語が複数ユニットに重複収録されていないか、層別（世界観/システム/工程/識別子）が破れていないか、同一概念の正本節が書によって食い違わないか、ID 採番 44-U{n}-Q{m} に重複・欠番がないか",
        "canon": "正典整合——各エントリの正本節参照が実在するか、承認済みの名・ID を再定義していないか、英語名を新造していないか、定義欄が数値・仕様を再掲していないか、異表記・衝突が黙って統一されず要承認に上がっているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**用語集の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/61 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 用語候補の棚卸し（抽出） ===")
    inv = await agent_retry(
        extract_prompt(),
        phase="extract", label="extract-inventory",
        schema=EXTRACT_SCHEMA, repos=[REPO], soft_time_limit_minutes=50,
    )
    inventory = inv["inventory_md"]
    log(f"棚卸し完了（{len(inventory)} 文字）")

    log("=== Phase 2: 4ユニットの制作・レビュー・改訂ループ ===")
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
