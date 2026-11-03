import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/71_research_phase0_review.md（本タスクの物差し——§1 4観点の論点・§2 正典制約 G-RV-01〜07・§3 原則 P-RV-01〜05・§4 棚卸し H-RV・§5 組版テンプレは必須）
- docs/00_development_plan.md（レビュー工程の定義）・docs/42_risk_register.md（既存リスク・ブロッキング条件）
- AGENTS.md（Phase 0＝設計のみ・日本語・推奨案まで作り決定権はユーザー）
担当観点に割り当てられた設計書群は別途指定する——指定された全ファイルを実際に開いて読み、各書への監査済みマークを残すこと（P-RV-04）。
"""

RULES = """成果物の形：
- 担当観点のレビュー報告を section_md に書く——観点名・各書への監査結果・指摘台帳
- 指摘行の形式：`| severity | 対象書・節 | 論点 | 根拠（正典参照） | 処置区分 | 推奨案 |`（severity＝blocker/major/minor、処置区分＝設計書反映/Issue化/要承認/既存Issue追記）
- G-RV-01：曖昧な印象批評は禁止——「どの節が・何と矛盾/欠落するか」具体化
- G-RV-02：承認済み決定・Accepted ADR を覆さない——矛盾はどちら側が書き換わるべきかの形で指摘
- G-RV-05：監査のみ——新規設計・新規コンテンツの提案はしない
- G-RV-06：問題なしの書は「監査済み・指摘なし」として台帳に残す（未読の書を作らない）
- 面白さの根幹級のみ open_questions へ `01-U{n}-Q{m}` で起票（推奨案＋書き戻し先必須——P-RV-05）
"""

UNITS = [
    {
        "id": "gamedesign",
        "title": "U1：ゲームデザイン観点（面白さ・一貫性）",
        "scope": "「棄てられたものへの愛惜」「捨てる→届く→記録」の文法の全書一貫性／面白さ5系統（愛惜と物語性・同席者配信・章エピソード・群像劇・沈黙と余白）の系統立ち／機構の被覆（没腐・個別層・拾得・名付け・転移・境界——定義の重複・衝突・欠落）／数値系とシステム仕様・章設計の整合",
        "docs": "担当設計書：docs/09・10・11・13・14・16・23・26・32・34/（概観レベル）・36・38/全4本・45/全5本・63・67/全5本・44・40 §3",
    },
    {
        "id": "story",
        "title": "U2：物語観点（各章プロット・結末分岐）",
        "scope": "docs/34 各章プロット・docs/51 ボード・docs/12 骨格・docs/28 フルフローの接続整合／結末分岐（綴じる/見届ける・先着・共有層）の一貫性／伏線配置（docs/36・36a）の回収被覆／キャラ（25）・ロア断片（52）・融合要素（48）の物語上の役割と矛盾／設計的沈黙と単なる欠落の区別",
        "docs": "担当設計書：docs/12・24・25・26・27・28・34/全7本・35・36・36a・48/全5本・50・51/全6本・52・15 §5・33（調査）",
    },
    {
        "id": "streaming",
        "title": "U3：配信映え観点（クリップ性・エピソード構造）",
        "scope": "docs/70（台帳・イベント・観客参加）が docs/51・34・48 の実演出に被覆されているか——CM-ID と BD-ID の対応齟齬／30秒ルール・同席者方針・沈黙ポリシーの横断遵守／章＝エピソード構造の時間設計（docs/38 演出時間・13 進行）と配信尺／観戦/俯瞰不採用・配信モード差分の一貫適用",
        "docs": "担当設計書：docs/08・17・19・20・40 §5.2.4・41・43・46・51/（U1 と重複読み）・63・70/全4本・38 演出時間系",
    },
    {
        "id": "tech",
        "title": "U4：技術実現性観点（NeoForge 実装難度）",
        "scope": "ADR-0006〜0010 の前提と各設計書の齟齬——ADR 決定を暗黙に覆す記述の検出／先行ゲート（docs/57・40 §4.9）前提行の着地状況と「Issue #13/#15 着地」注記の棚卸し／個別層生成・可視性モデル・ワールド固定生成の技術整合（docs/16・32・40・57・30_adr）／modpack 収録条件・性能閾値と設計負荷（docs/43・46・40 §4.8）／集約レポート §1 総評の叩き台も作成",
        "docs": "担当設計書：docs/30_adr/ 全 ADR＋README・40・41 §3・42・43・46・55・56・57・16 §6.4/§7.5・32 §6/§9・60・61・62（存在すれば）",
    },
]

META = {
    "name": "phase0-review",
    "description": "Phase 0 設計書群の多観点レビュー（Issue #1）——棚卸し→4観点レビュー→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "全設計書・承認済み決定・未着地前提の棚卸し", "count": 1},
        {"title": "write", "detail": "4観点の監査レポート", "count": 4},
        {"title": "review", "detail": "指摘の妥当性・severity の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "整合・被覆・品質の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当観点のレビュー報告 Markdown 全文"},
        "open_questions": {"type": "string", "description": "面白さの根幹級のみの要承認（ID＝01-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "レビュー対象の棚卸し（全設計書リスト＋承認済み決定の束ね＋未着地前提・条件付き改訂の束ね＋手渡し依存の束ね）"},
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
    return f"""{MUST_READ}

タスク：レビュー対象の棚卸しを行い、inventory_md に出力せよ。

1. **全設計書リスト**：docs/ 直下の番号付きファイル＋サブディレクトリ（34/・38/・45/・48/・51/・67/・70/・30_adr/）を実際に ls して全件列挙。各書に「監査対象」「参照材料」区分を付す（docs/71 §0・H-RV-01）。
2. **承認済み決定の束ね**：各書の要承認集約・承認済み注記・ADR Accepted 一覧・STATE.md の承認履歴を台帳化（H-RV-02）——レビューの判定基線として使う。
3. **未着地前提・条件付き改訂の束ね**：docs/42 §2・docs/57 §8・docs/40 §4.9・「Issue #13 検証」「Issue #15 着地」注記を収集（H-RV-03）。
4. **手渡し依存の束ね**：未消費の手渡しコメント・書き戻し先（H-RV-04）。
出力は Markdown 台帳で。"""


def author_prompt(unit, inventory):
    return f"""{MUST_READ}

{RULES}

# 棚卸し（参照）

{inventory}

# 担当観点

{unit['title']}

観点の論点：{unit['scope']}
担当設計書：{unit['docs']}

指定された設計書を**全件実際に開いて読み**、観点の論点で監査せよ。指摘は severity・対象書/節・論点・根拠・処置区分・推奨案の形式で台帳化し、問題なしの書は「監査済み・指摘なし」マークを残せ。面白さの根幹級のみ `01-U{{unit-id}}-Q{{n}}` で open_questions 起票。"""


def review_prompt(unit, section_md):
    return f"""{MUST_READ}

タスク：以下の観点レビュー報告（{unit['title']}）を**深い思考で監査**せよ。

1. 指摘の妥当性——根拠（正典参照）が実在するか・severity が G-RV-03 どおりか・曖昧批評が混ざっていないか
2. 正典整合——承認済み決定を覆す指摘/報告になっていないか・指摘が正典の誤読に基づいていないか
3. 被覆——担当設計書に監査済みマークが全件ついているか（未読の書がないか）
4. 処置区分の適切さ——設計変更級が「設計書反映」になっていないか・面白さの根幹が要承認に昇格しているか

# レビュー対象

{section_md}

指摘（accepted=false）は severity・issue・suggestion 形式で返せ。問題なければ accepted=true。"""


def revise_prompt(unit, section_md, findings):
    return f"""{MUST_READ}

{RULES}

タスク：{unit['title']} のレビュー報告を以下の指摘に基づき改訂せよ。

# 指摘

{json.dumps(findings, ensure_ascii=False, indent=2)}

# 現行報告

{section_md}

指摘全件を反映した改訂版を section_md で返せ。open_questions は必要に応じて更新。"""


def crosscheck_prompt(all_sections, kind, inventory):
    focus = {
        "consistency": "観点間で同じ問題が別 severity/別処置で記録されていないか・指摘同士が矛盾していないか・同一論点の重複起票を整理",
        "coverage": "棚卸しの全設計書に監査済みマークがついているか・4観点の論点が全て少なくとも1つの観点で検証されているか",
        "quality": "全指摘が G-RV-01 の形式（対象書/節・根拠・処置区分・推奨案）を満たすか・severity 判定の一貫性・曖昧批評の残存",
    }
    return f"""{MUST_READ}

タスク：4観点のレビュー報告を横断監査せよ（観点＝{kind}）：{focus[kind]}

# 棚卸し（参照）

{inventory}

# 全観点のレビュー報告

{all_sections}

指摘は severity・issue・suggestion 形式で返せ（accepted=true/false 両方可）。"""


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
            log(f"{unit['id']}: ラウンド{r+1}で受理")
            return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs}
        findings_key = json.dumps(sorted(review["findings"], key=lambda f: f.get("issue", "")), ensure_ascii=False)
        if findings_key == previous_findings:
            log(f"{unit['id']}: 同一指摘の繰り返し——受理")
            return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs}
        previous_findings = findings_key
        log(f"{unit['id']}: ラウンド{r+1}で指摘{len(blocking)}件——改訂へ")
        draft2 = await agent_retry(
            revise_prompt(unit, section_md, review["findings"]),
            phase="revise", label=f"revise-{unit['id']}-r{r+1}",
            schema=SECTION_SCHEMA, repos=[REPO], soft_time_limit_minutes=45,
        )
        section_md = draft2["section_md"]
        open_qs = draft2.get("open_questions", open_qs)
    return {"unit": unit["id"], "title": unit["title"], "section_md": section_md, "open_questions": open_qs + "\n[レビュー3ラウンド後も残存指摘あり]"}


async def main():
    await register_workflow(META)
    log("=== Phase 1: レビュー対象の棚卸し ===")
    inv = await agent_retry(
        extract_prompt(),
        phase="extract", label="extract-inventory",
        schema=EXTRACT_SCHEMA, repos=[REPO], soft_time_limit_minutes=50,
    )
    inventory = inv["inventory_md"]
    log(f"棚卸し完了（{len(inventory)} 文字）")

    log("=== Phase 2: 4観点のレビュー・改訂ループ ===")
    results = []
    for batch in (UNITS[:2], UNITS[2:]):
        results.extend(await pipeline(batch, lambda u: unit_flow(u, inventory)))
    log("=== 4観点完了。横断監査へ ===")

    all_sections_text = "\n\n---\n\n".join(
        f"## {r['title']}\n\n{r['section_md']}" for r in results
    )

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
    import os
    os.makedirs("/home/ubuntu/repos/the-understory/.devin-work/issue1", exist_ok=True)
    with open("/home/ubuntu/repos/the-understory/.devin-work/issue1/workflow_output.json", "w") as f:
        json.dump(output, f, ensure_ascii=False)
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)[:500]}")


asyncio.run(main())
