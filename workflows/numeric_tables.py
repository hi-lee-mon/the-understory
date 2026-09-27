import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/37_research_numeric_design.md（数値設計の調査基準——本タスクの物差し。§3の正典制約C1〜C15・§4の帯域表・§5の組版テンプレ・§6のレビュー基準・§7の棚卸しH1〜H17は必須）
- docs/11_world_bible.md（世界法則）
- docs/12_story_outline.md（章概要）
- docs/13_progression_map.md（進行・難度・報酬構造）
- docs/14_items_crafting.md（アイテム・クラフト——本Issueの更新対象）
- docs/15_mobs_bosses.md（モブ・ボス——本Issueの更新対象）
- docs/23_discard_grammar.md（ゴミ箱・選別・返礼——§8.1/§14 の宿題あり）
- docs/28_story_full_flow.md（全編ストーリー詳細——ボスの物語文脈）
- docs/30_adr/（ADR-0003/0004/0005 等の確定決裁）
- docs/32_system_specs.md（拾い直し制・没腐度・マルチ）
- docs/34_chapter_plots/ 全7本＋README.md（各章 §5 ボス・ギミック・§7 報酬・§8 断片・open_questions）
- docs/36_foreshadow_map.md・docs/36a_foreshadow_inventory.md（伏線台帳——F-MECH/U4-Q3 等の手渡し項目あり）
- AGENTS.md（作業規範）
"""

TABLE_RULES = """成果物の組版（docs/37 §5 を厳守）：
- 全行に「状態」列（確定／暫定／要承認）。要承認には書き戻し先の正典節を明記
- ID規則：N-ITEM-xxx（素材・拾得物）/ N-GEAR-xxx（装備・道具）/ N-DEV-xxx（装置）/ N-BOS-xx（ボス）/ N-MOB-xxx（モブ）/ N-ECO-xxx（経済・環境）。章固有は中綴じ可
- 全数値に「根拠」列または節内注記（バニラ換算／黄昏の森・Cataclysm帯域／正典条項C#）。感覚値不可
- HP表記はHP基準（ハート併記任意）。実効ダメージは「推奨装備帯を通った後」の値で書く
- 表はMarkdown。一つの表は一つの責務（素材・装備・装置・ボス・モブ・経済を混ぜない）
"""

CONSTRAINTS = """絶対条件（docs/37 §3 の正典制約）：
- C2 護石式マラソン禁止：進行ゲートは物語・発見・知識で。ドロップ率・素材数は「1周回で揃う」範囲
- C3 「一段強化すれば届く」：各ボスに推奨装備帯と -1段ペナルティを必須記載
- C4 死に学習：即死なし。推奨装備帯での一撃実効 3〜5HP標準・上限6〜9HP（予備動作長めの必殺のみ）
- C5 拾い直し制：装備・クラフト品は死亡喪失なし。未登録拾得物のみ25%・最大8個
- C7/C8 難度勾配：序・1章 < 第2〜4章（同一帯域・順不同で破綻しないこと）< 5章 < 終章
- C11 特殊ゲージ分離：HP列と「進行ゲージ」列は別（上演の進行／楽章の進行／体力=未使用部位総量）
- C12 段位三層：「仮の姿」は差替可能な暫定記述（要承認P4前提）と明記
- C10 マルチ係数：ボスHP＝基準×(1+0.5×追加人数)・上限×4.0。報酬は欠片以外全員分
- 正典を変更する提案は「要ユーザー承認」と明記し、直接変更しない
- 用語は正典どおり（拾い人/ノミ/拾得物/没腐/落慮王/没素材/結末の欠片 等）
"""

UNITS = [
    {
        "id": "items",
        "title": "U1：素材・拾得物全表（01_items.md相当）",
        "scope": "没素材の系統全表（docs/14 §2 の系統を起点に素材個別化）・宝物/ガラクタ区分の判定基準（由来鑑定の権限：ノミ=由来の嗅ぎ分け／灯台守=届きもの宛先／鍛冶師=素材価値）・結末の欠片の総数と仕様（34 README #2：第1〜5章各4個=20個・序0・終章は集積の間で回収演出——H1）・携行品の容量系列（摘み籠の系譜——H12）・拾得鍛錬の段位三層（基本位/仮の姿/上位特別鍛錬——C12）・食料・回復品の数値。docs/37 §5.1 の必須列で全表化し、行数は実用レベル（各分類で網羅性を担保——単発アイテムは『種別』でまとめてよい）。",
    },
    {
        "id": "gear_devices",
        "title": "U2：装備・道具・装置全表（02_gear_devices.md相当）",
        "scope": "武器・道具（拾い人の鉤・届いた手紙の刃・没の楽器・満ちた月の弓・縁の羅針盤 等 docs/14 §3 起点＋章別没素材武器）に攻撃力・DPS換算（§4.1帯域T0〜T4に載せる）・耐久・レシピを全表化。防具＝章別没素材シリーズの防御値。装置：ゴミ箱L1/L2/L3の詳細レシピ・個別記憶上限・名づけ版差分（H4）・処理場構成部品の必要素材（H5）・物への名付け手続（名札可否・手順・戦闘中可否——H3）・梱包アイテム（バンドル/シュルカー類似）。docs/37 §5.2 の必須列で。",
    },
    {
        "id": "bosses",
        "title": "U3：ボス数値全表（03_bosses.md相当）",
        "scope": "6ボス＋序章小遭遇の全数値表：月欠狼（月齢3ループの周期秒・各月齢係数——H6）・未読の座礁船（手紙の嵐頻度・波回避猶予）・中止の人形劇（上演の進行ゲージ上限・拍子判定窓——H7）・棄材のゴーレム（体力=未使用部位総量の内訳：部位総数・1部位価値・剥離頻度——H8）・無音の歌姫（楽章の進行ゲージ・聞き手規則の判定範囲/距離/持続——H2）・落慮王（多段構成・特殊勝利条件の数値化——H16）・ボス再戦ハードモードの係数（H17）。各ボスに推奨装備帯・-1段ペナルティ・標準戦闘時間（§4.2の帯に合わせる）・固有報酬＝新動詞・マルチ係数を必須記載。docs/37 §5.3 の必須列で。",
    },
    {
        "id": "mobs_economy",
        "title": "U4：モブ・経済・環境数値表（04_mobs_economy.md相当）",
        "scope": "通常モブ全表（棄てられた素材の精・読まれなかった文字・踊り損ねた者・環礁住人の中立/敵対・没腐時強化係数——H14）・没腐度の数値化（死亡+1起点・逓増・捨て場歪み閾値・村滞在回復速度・上限——H11）・宝箱構成（固定枠+レア枠比）・返礼頻度（住人便・誤配の発生条件と頻度——H9）・拾得物密度（各環礁の個数目安・隠し配置）・ノイズ比率（1/4〜1/3・最深部1/2の採否を明記——H10）・『届かない』2段階の発生条件数値（H15）・マルチ難度調整の経済側（素材配分・共有村の扱い——H13）。docs/37 §5.4 の必須列で。",
    },
]

META = {
    "name": "numeric-tables-forge",
    "description": "アイテム全表・ボス/モブ数値表の設計（Issue #15）——抽出→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典から数値手渡し項目・制約の棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの数値表執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・帯域整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの数値表セクション全文（Markdown・全表を含む）"},
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
        "inventory_md": {"type": "string", "description": "抽出した全手渡し項目・数値制約の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #15（アイテム全表・ボス/モブ数値表）へ手渡されている全ての項目・数値制約・未定義の物差し**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. 各所で「Issue #15」「数値表」「全表」に言及されている箇所（grep で「Issue #15」「#15」「数値」「全表」「未決」「要追記」「宿題」「TODO」相当を総当たり）
2. docs/37 §7 の棚卸し H1〜H17 の確認と、その裏にある元記述（出典節）の精査——棚卸しの漏れ・誤読を指摘
3. docs/14・15 の現状記述で「数値が未定」のまま放置されている全項目
4. docs/23・32・34・36 の「後で決める」系の記述（ゴミ箱レシピ・没腐度閾値・誤配頻度・聞き手規則・ノイズ比率等）
5. 正典側で既に確定している数値・制約（例：死亡ペナルティ 25%/最大8個・結末の欠片 各章4個・没腐度の仕組み）
6. ボス・モブ・装備の既存の物語的制約（第2〜4章順不同・撃破=救出・護石式禁止等）のうち数値設計に効くもの

## 出力
inventory_md に Markdown で：各行「項目｜要求されている内容｜出典（ファイル・節）｜種別（素材/装備/装置/ボス/モブ/経済/環境/制約）｜優先度（必須/任意）」。docs/37 §7 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の数値設計者。{unit['title']} を、調査基準（docs/37）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 正典からの手渡し棚卸し（抽出済み——これを網羅的に回収せよ）
```markdown
{inventory}
```

{TABLE_RULES}
{CONSTRAINTS}

## 執筆の作法
- 数値はまず docs/37 §4 の帯域（T0〜T4・HP目安帯・被弾標準帯・マルチ係数）に載せてから、章固有の事情で微調整する
- 黄昏の森・Cataclysm の参照値（§2）を根拠に引く——「○○帯域に準じる」等の参照明記
- 表は「実用レベルの網羅性」：装備なら各Tier・各部位、ボスなら攻撃一覧の各行まで
- 進行ゲージ系ボスは HP 換算値と本来ゲージ値の両方を書く（C11）
- 「仮の姿」関連は暫定記述である旨を明記（C12）
- 未確定・正典変更が絡むものは「要承認」列＋open_questions へ（書き戻し先を明記）

## 出力形式（section_md）
1. **ユニットの目的**：この表群が Issue #15 で担う機能
2. **全表**（上記必須列の Markdown 表——複数表に分けてよい）
3. **設計上の判断**：帯域から外れた値の根拠、トレードオフの説明
4. **未決・要承認**（open_questions へも出力）"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の数値レビューア。以下の設計を、docs/37 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/37 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（docs/37 §6 の3段分類を適用）
1. **正典制約適合**：C1〜C15 の各条項に反する値・仕組みがないか（特に C2 護石式禁止・C3 一段強化・C4 死に学習・C5 拾い直し制・C7 順不同帯域・C11 ゲージ分離・C12 仮の姿暫定）
2. **網羅性**：棚卸し項目（docs/37 §7 H1〜H17 と抽出結果）が全て回収されているか、必須列（§5）に欠落がないか
3. **数値の根拠**：全数値に参照（バニラ換算/TF・Cataclysm帯域/正典条項）があるか、§4 の帯域から外れた値に正当な理由があるか
4. **実用レベル**：実装者がこの表だけで作業できる具体度か（レシピの素材数・フェーズ閾値・係数まで）
5. **表内整合**：HP×DPSで戦闘時間が標準帯に収まるか、推奨装備帯の装備が U1/U2 側に存在する想定か
6. **状態管理**：要承認行に書き戻し先があるか、暫定（仮の姿等）が明記されているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の数値設計者。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{TABLE_RULES}

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
        "coverage": "網羅性——棚卸しと docs/37 §7 の全項目が4ユニットのいずれかで扱われているか、各表の必須列が揃っているか、『要承認』行に書き戻し先があるか",
        "bands": "帯域整合——ユニット間で数値の前提が食い違わないか（ボスの推奨装備帯に対応する装備がU2に存在するか・素材の入手先がU1の拾得物と整合するか・経済頻度が護石式禁止に反しないか・難度勾配 C7/C8 が全表で一貫しているか）",
        "canon": "正典整合——4ユニット全体が docs/11/13/14/15/23/32/34 の記述と矛盾しないか、正典を事実上書き換える値が『要承認』になっているか、暫定前提（仮の姿P4・K16ノミ常時同行）が明記されているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**数値表の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/37 を実際に開いて突き合わせること）。

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
        # gear_devices の r2 revise は中断時に子セッションが死亡し「paused child could not be woken」で固着したため、
        # 当該コールのみプロンプトに識別子を混ぜてハッシュを変え、新規セッションに振り替える（他コールの再生を維持）。
        _retry_note = "（中断からの再実行：同一内容で新規ドラフトとして処理せよ）" if unit["id"] == "gear_devices" and r == 1 else ""
        draft2 = await agent_retry(
            revise_prompt(unit, section_md, review["findings"], retry_note=_retry_note),
            phase="revise", label=f"revise-{unit['id']}-r{r+1}",
            schema=SECTION_SCHEMA, repos=[REPO], soft_time_limit_minutes=45,
        )
        section_md = draft2["section_md"]
        open_qs = draft2.get("open_questions", open_qs)
    log(f"{unit['id']}: レビュー3ラウンド消化——最終版を採用")
    return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs + "\n[レビュー3ラウンド後も残存指摘あり]"}


async def main():
    await register_workflow(META)
    log("=== Phase 1: 手渡し項目・数値制約の棚卸し（抽出） ===")
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

    cov_check, band_check, canon_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "bands", inventory), phase="crosscheck", label="cc-bands", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("coverage", cov_check), ("bands", band_check), ("canon", canon_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"coverage": cov_check, "bands": band_check, "canon": canon_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
