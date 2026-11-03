import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/69_research_streaming_detail.md（本タスクの物差し——§2 正典制約 G-SD-01〜10・§3 原則 P-SD-01〜08・§4 棚卸し H-SD-01〜14・§5 組版テンプレは必須）
- docs/17_streaming_design.md 全文（v0.2——確定方針書。本追補の上位決定。§3 クリップ瞬間列挙・§6 同席感・§8 未決）
- docs/08（配信者・視聴者調査——「同席者」方針の一次根拠）
- docs/46_distribution.md §5.4・docs/43_release_plan.md（配信者到達＝サーバーイベント主経路・解禁判定・運用設計）
- docs/51_chapter_boards/ 全6本（各章ボード——ビート列・B-STD 見せ場規格）
- docs/34_chapter_plots/ 全7本（各章プロット——演出・転調点・結末選択）
- docs/48_fusion_elements/（幕切れ・見得・予告頁・エンドロールの劇的構造）
- docs/23_discard_grammar.md（捨てる文法——ゴミ箱転移・他人を捨てる儀式）
- docs/38_numeric_tables/（演出時間規格・ボス戦数値の劇的要素）
- docs/19_audio_direction.md（音演出の配信面）・docs/52_lore_fragments.md（考察素材の形態）
- docs/63_accessibility_config.md（配信面での a11y 連動）
- docs/42_risk_register.md（配信・保守・ネタバレ関連のリスク行）
- AGENTS.md（Phase 0＝設計のみ・日本語・推奨案まで作り決定権はユーザー）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/69 §5 を厳守）：
- `docs/70_streaming_detail/` 配下の担当ファイルを執筆——複数ファイルは `=== FILE: docs/70_streaming_detail/xxx.md ===` の区切り行で分割して section_md に入れる
- 正典値は引用のみ・再定義禁止（G-SD-01）・承認済み決定を覆さない（G-SD-02）
- 新規演出・新規コンテンツの創作はしない——正典（docs/51・34・48・38）に実在する演出を配信面で言語化する（G-SD-06）
- 観客参加・期間限定・イベント要素は「採る/採らない」の判定を論点化（P-SD-05）——全採用前提で書かない
- 判定可能な言語化（P-SD-02）：「クリップになる」とは何を指すか・発生条件・配信者反応・視聴者反応を具体的に
- 未着地・暫定値は「暫定＋着地先」を明記（G-SD-09）
- Phase 0 制約：実装コード・JSON・確定イベント名は書かない（G-SD-04）
- 「正典で未規定」は選択肢＋推奨案つきで open_questions へ `17-U{n}-Q{m}` で起票（書き戻し先必須）
"""

CONSTRAINTS = """絶対条件（docs/69 §2 の G-SD-01〜10）：
- G-SD-02：配信者到達＝サーバーイベント主経路・専用配信モード画面なし・観戦/俯瞰視点新設しない・予告点新設しない・予告頁＝ノミ語り＋挿絵・ARG接点＝現実側ガラのみ——これらを覆す記述をしない
- G-SD-03：視聴者＝同席者——視聴者にだけ別の景色/情報を出す機構を創作しない
- G-SD-05：面白さの根幹は要承認起票——推奨案まで作るが採否はユーザー
- G-SD-07：30秒ルール（配信を知らない人にも30秒で状況が分かる）を判定基準に
- G-SD-08：保守コスト・サーバー運用負荷を配慮として明記
"""

UNITS = [
    {
        "id": "clip",
        "title": "U1：クリップ瞬間台帳（docs/70_streaming_detail/clip_moments.md）",
        "scope": "章別＋横断のクリップ瞬間台帳。docs/17 §3 の列挙を起点に、docs/51 ボード（ビート・B-STD）・docs/34 プロット（転調点・結末選択）・docs/48（幕切れ・見得・エンドロール）から、各章の「配信を知らない人にも30秒で状況が分かる」劇的瞬間を全抽出して判定可能な言語化——各エントリに①瞬間名②発生条件（どのビート/トリガで起きるか）③配信者本人の反応④視聴者の反応（30秒で何が分かるか）⑤出典 ID⑥切り抜きタイトル例。§3 横断クリップ（章非依存：捨てる→届く・異物初接触・ゴミ箱転移・自分の捨て場対面・他人を捨てる儀式・返事が届く転換）。§4 に切り抜きタイトル・サムネポイントの型",
        "docs": "担当正典：docs/51_chapter_boards/ 全6本・docs/34_chapter_plots/ 全7本・docs/48_fusion_elements/ 全5本・docs/17 §3・docs/38 03_bosses（演出時間規格・形態変化）・docs/23（儀式の瞬間）・docs/45（非言語導線の見せ場）",
    },
    {
        "id": "events",
        "title": "U2：イベント・期間限定要素設計（docs/70_streaming_detail/events.md）",
        "scope": "サーバーイベント運用（主経路＝Issue #22 D-7）の形態設計——期間限定テーマ鯖・共同進行・群像劇蓄積の見せ方。期間限定要素（docs/17 §6「期間限定の没素材/異物を入れられるよう設計」）の設計枠——収録ルール（何が期間限定に適するか：正典の「没になったもの」語彙と整合する拡張余地の構造）・非収録ルール（本編に混ぜない）・解禁/復刻の規格。コラボ・イベント規格。保守コスト（単独開発——サーバー運用・期間切替の運用負荷）の判定。docs/43 の運用設計・8-K 契機との接続",
        "docs": "担当正典：docs/17 §6・docs/46 §5.4（配信者到達）・docs/43（リリース運用・解禁判定・8-K）・docs/42（保守・運用リスク行）・docs/32 §6（共有村・群像劇）・docs/67_next_regions/（次コンテンツ——イベント候補地との関係）・docs/16（構造物・空き環礁の拡張余地）",
    },
    {
        "id": "audience",
        "title": "U3：観客参加・同席感設計（docs/70_streaming_detail/audience.md）",
        "scope": "「視聴者＝同席者」（G-SD-03）の詳細設計——①考察班設計：幻想文字・断片ロア・「拾い人とは」「落慮王とは」の素材供給形態（docs/52 の断片のどこまでを解読材料にするか・答えを出さない規則・ARG接点規則の適用範囲）②議論できる結末：各章の結末選択で視聴者が「書き換える派？見届ける派？」を議論できる論点台帳（章ごとの議論ポイント・コメント誘発設計）③マルチ視点差分の見せ方（「推しには何が見えたか」——各配信者の別視点を観に行く動機設計）④視聴者参加要素の要否判定：コメント投票・チャット連動・視・視聴者の捨てたもの等の候補を列挙し「採る/採らない」を論点化（保守コスト・技術的実現性・同席者方針との整合で判定）",
        "docs": "担当正典：docs/08 §2（同席者3要件）・docs/17 §1/§5/§6・docs/52（断片ロア形態）・docs/48/04（幻想文字・ARG接点規則）・docs/34（結末選択場面）・docs/24（答え合わせ表・伏線）・docs/25（キャラ——考察対象）・docs/36（伏線配置）",
    },
    {
        "id": "readme",
        "title": "U4：README・要承認集約・手渡し表（docs/70_streaming_detail/README.md）",
        "scope": "README.md——索引・docs/17（方針書）との関係定義（本書＝v0.3 追補として位置づけ・docs/17 §8 未決行のどれが本書で消費されたかの注記）・要承認集約（全ユニットの `17-U{n}-Q{m}` を集約した唯一集約表）・手渡し表（docs/17 更新注記・docs/51 ボードへの照合・docs/43 運用・docs/42 台帳宛・Issue #6 の S-1 クリップ瞬間検証項目への接続）",
        "docs": "担当正典：docs/17 全文（§8 未決行の消費判定）・docs/69 全文・docs/40 §5.2.4（S-1 クリップ瞬間検証項目）・docs/42（手渡し行の形）",
    },
]

META = {
    "name": "streaming-detail",
    "description": "配信詳細 docs/70_streaming_detail（Issue #17）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "配信材料の棚卸し（クリップ瞬間・同席感要素・イベント余地の統合台帳）", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "正典整合・品質の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "整合・被覆・品質の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの Markdown 全文（=== FILE: path === 区切り）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝17-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "配信材料台帳（Markdown——クリップ瞬間候補・同席感要素・イベント余地・承認済み方針の統合台帳）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の設計台帳の編集者。リポジトリ内の全設計書から、**配信詳細（Issue #17——docs/70_streaming_detail/）の材料**を棚卸しせよ。範囲＝クリップ瞬間・観客参加/同席感・イベント/期間限定要素。

{MUST_READ}

## 抽出対象
1. **docs/17 の確定方針全文**：§1 3要件・§2 シリーズ構造・§3 クリップ瞬間列挙10項・§5 マルチ・§6 同席感・§7 提供素材・§8 未決行（残りの扱い判定）
2. **クリップ瞬間候補**：docs/51 各ボードの見せ場ビート・docs/34 各章の転調点/結末選択/演出瞬間・docs/48 の劇的構造（幕切れ・見得・予告頁・エンドロール）——章ごとに「瞬間名・発生条件・出典節」を列挙
3. **同席感・観客参加の材料**：docs/08 §2 の3要件・docs/52 の断片形態・docs/36 伏線・docs/24 答え合わせ表・「議論できる結末」の素材（各章の結末選択構造）
4. **イベント・期間限定の材料**：docs/17 §6・docs/46 §5.4（主経路確定）・docs/43 の運用設計・解禁判定・docs/16 の空き環礁/拡張余地・docs/67 の次領域
5. **承認済みの制約**：18-U4-Q13（観戦/俯瞰不採用）・U4-11（配信モード画面なし）・U2-D/U4-#2（予告頁方式）・U4-9（ARG接点）・44-U3-Q5（用語棲み分け）——覆せない決定の正確な内容
6. **マルチ視点差分の材料**：docs/32 §6（共有/個別表）・docs/17 §5——「別視点を観に行く動機」の正典
7. **検証接続**：docs/40 §5.2.4 S-1（クリップ瞬間の検証項目）・docs/41（プレイテストの配信面）
8. **保守/リスク**：docs/42 の配信・運用・ネタバレ関連行

## 出力
inventory_md に Markdown テーブル群で：「E-ID｜要素名｜種別（確定方針/クリップ候補/同席感材料/イベント材料/承認制約/検証接続/リスク）｜領域（クリップ/観客/イベント/横断）｜内容｜出典節」。解釈・新規創作はしない——実在する決定・演出を忠実に集めること。要素数の集計を末尾に付ける。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の配信設計の編集者。{unit['title']} を、調査基準（docs/69）と確定正典に基づき深い思考で執筆せよ。**正典に実在する演出・機構を「配信でどう映えるか」の詳細仕様に降ろす**——新しいゲーム仕様の創作ではなく、確定した面白さの配信面言語化。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## 配信材料台帳（E-ID 採番済み——担当領域分を全て回収せよ）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/69 §3 の原則 P-SD-01〜08 に載せてから各節に具体化する
- docs/69 §5 のテンプレ構成に従う
- 「クリップになる」判定は30秒ルール＋配信者反応の両面で言語化（P-SD-02/03）
- 観客参加・イベント要素は候補列挙＋採否判定構造（P-SD-05）——全部採る前提で書かない
- 「正典で未規定」は選択肢＋推奨案つきで open_questions へ `17-U{{n}}-Q{{m}}` で起票（書き戻し先必須）

## 出力形式（section_md）
docs/69 §5 のテンプレ構成をすべて埋めた Markdown 全文（=== FILE: path === 区切り）＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の配信設計のレビューア。以下の成果物を、docs/69 の基準と各正典に照らして厳しくレビューせよ（深い思考——正典の該当節（docs/17・51・34・48・23・38・08・46・43・52・36・24・32・42）を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点
1. **正典整合**：引用された演出・決定が正典正本と一致するか。新規演出・新規コンテンツの創作がないか（G-SD-01/02/06）
2. **上位方針整合**：「同席者」方針・サーバーイベント主経路・配信モードなし・観戦/俯瞰なしの確定を覆していないか（G-SD-02/03）
3. **判定可能な言語化**：各クリップ瞬間に発生条件・配信者反応・30秒で分かる内容があるか（P-SD-02/03）
4. **採否判定構造**：観客参加・期間限定要素が「採る/採らない」の論点化になっているか——全採用前提・要否検討なしの記述は不可（P-SD-05・G-SD-05）
5. **出典明記**：各エントリに出典 ID があるか（P-SD-01）
6. **保守コスト**：単独開発の運用負荷が配慮として明記されているか（G-SD-08）
7. **組版**：docs/69 §5 テンプレの全節・要承認が `17-U{{n}}-Q{{m}}` で採番・書き戻し先つき
8. **範囲規律**：Phase 0 として実装コード・確定イベント名を書いていないか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案——指摘には節を明記）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の配信設計の編集者。以下の成果物をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行稿
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
        "consistency": "正典整合の横断監査——全ファイルを通じて引用が正典正本（docs/17・51・34・48・23・46・43）と一致しているか、ファイル間の記述（クリップ台帳台帳⇄イベント⇄観客参加で同一演出の扱い）が矛盾していないか、docs/17 確定方針の表現が揃っているか",
        "coverage": "網羅性——台帳の全 E-ID がいずれかのファイルへ着地しているか、docs/17 §3 のクリップ列挙10項が全て台帳行化されているか、§8 未決行（結末/村同期・イベント拡張余地）が消費または要承認に載っているか、全章（序〜終章＋村/拠点）にクリップ瞬間があるか",
        "quality": "品質の横断監査——各クリップ瞬間の判定可能性（30秒ルール・発生条件・反応）が揃っているか、観客参加/イベントの採否判定が論点として成立しているか（全採用前提がないか）、README 集約と各 §5 の Q-ID が一致しているか、文体が docs 系に揃っているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**配信詳細 4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典（docs/17・51・34・48・23・46・43・52・36・24・32・42）と docs/69 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：配信材料台帳
```markdown
{inventory}
```

## 全ユニット成果物
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
    log("=== Phase 1: 配信材料の棚卸し（E-ID 台帳化） ===")
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

    consistency_check, cov_check, quality_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "consistency", inventory), phase="crosscheck", label="cc-consistency", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "quality", inventory), phase="crosscheck", label="cc-quality", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("consistency", consistency_check), ("coverage", cov_check), ("quality", quality_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"consistency": consistency_check, "coverage": cov_check, "quality": quality_check},
    }
    with open("/home/ubuntu/repos/the-understory/.devin-work/issue17/workflow_output.json", "w") as f:
        json.dump(output, f, ensure_ascii=False)
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
