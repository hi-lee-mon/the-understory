import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/56_research_tech_verification.md（本タスクの物差し——§1 先行調査 API 実在性・§2 正典制約 G-TV-01〜13・§3 原則 P-TV-01〜07・§4 棚卸し H-01〜30・§5 組版テンプレ・§6 対応表は必須）
- docs/00_development_plan.md（Phase 1 技術検証の表——項目・予想・代替・着工ゲート）
- docs/40_vertical_slice_plan.md（§4.9 先行ゲート・§9 手渡し——本 Issue に投げられた検証項目の確定群）
- docs/16_structures_dungeons.md（§2.4 生成4型語彙・§7.5 手渡し——構造生成 JSON・個別層生成・L3 同一構造判定・灯台−座礁船連動）
- docs/18_ui_ux_detail.md（§8 手渡し——font プロバイダ・GuiLayerManager・ItemTooltipEvent・JEI・Patchouli・自前書物器・個別層由来札同期）
- docs/19_audio_direction.md（§9 手渡し——環境床コントローラ・発火抑制・サーバー権威発火±100ms・響界判定・sounds.json・ダッキング）
- docs/32_system_specs.md（§6 マルチ共有/個別層モデル——実体共有・表示個別化の確定値・ボス HP・月充填人数非依存）
- docs/23_discard_grammar.md（ゴミ箱転移機構——持ち込み可否の設計前提）
- docs/46_distribution_research.md（依存 MOD 確定値——JEI 必須・Patchouli soft-dep・収録条件5点・D-4② jarJar）
- docs/20_art_ui_design_system.md（色規則——H-29 カラー回帰の検証母本・シェーダー OFF 一次チャネル）
- docs/11_world_bible.md（世界設定——異物・二層構造の正典前提）
- docs/34_chapter_plots/01_moon_forest.md（第1章の構造物・環礁——生成検証の対象形状）
- docs/30_adr/（ADR-0002 技術選定・0003 ゴミ箱主機構・0004 状態モデル・0005 異物）
- AGENTS.md（作業規範——Phase 0＝設計のみ、実装コード禁止）
"""

RULES = """成果物の組版（docs/56 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- 各項目は項目カード形式（実現性評価／検証内容＝PoC 仕様／合格ライン／設計代替／依存・前提／Phase 1 タスク化／想定リスク・工数）を全部入れる
- 実現性評価は3段（高＝API 実在・先行実績あり／中＝実装パスはあるが未確認・性能未知数／低＝バニラ非対応・自前パケット加工等の重量級）＋根拠の出典明記（P-TV-03/05）
- 全判断に根拠（正典節／docs/56 の先行調査節・原則番号・制約番号）を付ける。感覚だけの提案は不可
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝57-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- 承認済みの正典値（生成4型・依存 MOD・マルチ確定値・音規格・40-Q 群の承認値）を再定義しない——引用のみ
- Phase 0/Phase 1 境界を明記：本書は検証の計画書であり、PoC 実装は Phase 1 タスクとして分離（P-TV-04）
- 合格ラインは測定方法つき（測る道具・単位・閾値——docs/40 §4 基盤要件への書き戻し導線を明記）
"""

CONSTRAINTS = """絶対条件（docs/56 §2 の正典制約 G-TV-01〜13）：
- G-TV-01 Phase 0＝設計のみ。実装コードを書かない（PoC 仕様は書くが実装ではない）
- G-TV-02 NeoForge/MC1.21.1/Java21 前提
- G-TV-03 先行ゲート5点（次元生成・転移骨格・個別化アイテム・転移持ち込み・異物可視性モデル）はスライス着工条件——残りは S1 並行として区別する
- G-TV-04 環礁配置＝ワールド固定・生成方式は本書で複数案比較して推奨を提示（要承認として確定を仰ぐ形）
- G-TV-05 個別層＝実体共有・表示のみ個別化（ADR-0004）。マルチ確定値の再定義禁止
- G-TV-06 異物可視性＝「発見者のみに見える」が正典目標。実現困難なら設計代替（初接触消滅／エンティティ化個別描画）を比較提示
- G-TV-07 ゴミ箱転移の持ち込み可否は正典設計に従属
- G-TV-08 依存 MOD 確定値：JEI 必須・Patchouli 図鑑のみ soft-dep・GeckoLib jarJar
- G-TV-09〜11 音・UI・構造の手渡し項目は検証項目として全件回収
- G-TV-12 完了条件＝検証結果の記録先まで設計に含める（docs/40 §4 数値着地の導線）
- G-TV-13 演出系はシェーダー OFF 一次チャネル保証・配信モード前提
"""

UNITS = [
    {
        "id": "dimension_terrain",
        "title": "U1：次元・地形系の検証（docs/57 §2）",
        "scope": "§2 次元・地形系——H-01 次元生成方式（noise ジェネレータ＋独自 noise_settings）・H-02 異物チャンク生成（混入表現の生成方式）・H-07 環礁本体生成方式（ワールド固定レイアウトの複数案比較——spread 固定/自前決定論配置/構造物駆動等・推奨案つき要承認として）・H-08 環礁生成パフォーマンス（測定設計）・H-09 没腐地形 processor（block_rot/rule/axis_aligned_linear_pos の構成案）・H-11 構造生成 JSON・jigsaw・H-14 灯台−座礁船連動生成。各項目は項目カード形式で実現性評価＋PoC 仕様＋合格ライン＋設計代替＋Phase 1 タスク化まで書く",
    },
    {
        "id": "transition_individual",
        "title": "U2：転移・個別層系の検証（docs/57 §3・§4）",
        "scope": "§3 転移・持ち込み系——H-03 転移骨格（DimensionTransition/PortalProcessor/ゴミ箱ブロック実装経路）・H-05 転移持ち込み可否（インベントリフィルタの実現経路）・H-30 転移 FX（暗転・モーションの描画経路・配信モード抑制との両立）＋§4 個別層・可視性系——H-04 個別化アイテム（DataComponent 由来情報・表示個別化）・H-06 異物の可視性モデル（3経路比較：チャンクパケット偽装/エンティティ化個別描画/初接触消滅——各経路の実装パス・副作用・推奨案つき要承認として。先行実装：Illusion/FibLib・anti-xray 系 sendMultiBlockChange 手法）・H-12 個別層生成（異物チャンク・自分の区画）・H-13 L3 同一構造判定・H-15 個別層データ構造（Attachment/SavedData 設計案）・H-24 ItemTooltipEvent 由来行＋由来札同期方式",
    },
    {
        "id": "ui_deps",
        "title": "U3：UI・書物・依存 MOD 系の検証（docs/57 §5）",
        "scope": "§5 UI・書物・依存 MOD 系——H-22 font プロバイダ（ttf 58 字形＋言語ファイル登録の到達経路）・H-23 GuiLayerManager カスタム層・H-25 JEI 連携（IRecipeCategory/IRecipeManager・隠し制御 18-U4-Q6）・H-26 Patchouli book.json 構成（18-U2-Q1・soft-dep 分離）・H-27 自前書物器 Screen（FB 端到端 40-Q9——Patchouli 非依存での綴じ込み・『あなたが捨てたもの』節・予告頁交付の実現経路）・H-28 GeckoLib ボス基盤（jarJar 同梱の検証——mods.toml 宣言・埋め込み・基本アニメーション表示）",
    },
    {
        "id": "audio_frame",
        "title": "U4：音・演出系＋全体枠（docs/57 §0・§1・§6〜§9）",
        "scope": "§0 位置づけ（Phase 0 成果物である明記・Issue 完了条件との対応）＋§1 検証対象マップ（H-01〜30→節の対応表・先行ゲート5点と S1 並行の区分・依存関係）＋§6 音・演出系——H-16 サーバー権威発火±100ms（ClientboundSoundPacket jitter 実測設計）・H-17 環境床コントローラ・H-18 発火抑制・H-19 響界判定・H-20 sounds.json 登録（調査のみ）・H-21 ダッキング・H-29 カラー回帰（docs/20 色規則の実装検証系——シェーダー OFF 一次チャネル保証の検証法と一体）・H-10 二層演出（現実側から国が見える——DimensionSpecialEffects/RenderLevelStageEvent 経路の比較）＋§7 検証環境・測定規格（開発環境・spark/timings・LAN2人・専用サーバー・測定単位一覧・実測着地→docs/40 §4 書き戻し導線）＋§8 未決・要承認集約（57-U{n}-Q{m}——環礁生成方式選択・可視性モデル経路選択・Phase 1 実施許可等）＋§9 手渡し一覧（docs/40 §4 への書き戻し・#6・#11・#34 等）",
    },
]

META = {
    "name": "tech-verification-plan",
    "description": "次元生成・異物チャンク技術検証計画 docs/57（Issue #13）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "正典からの検証項目棚卸し", "count": 1},
        {"title": "write", "detail": "4ユニットの執筆", "count": 4},
        {"title": "review", "detail": "基準適合の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "網羅性・整合・正典整合の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝57-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した検証項目・技術前提の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #13（次元生成・異物チャンク技術検証→docs/57 検証計画）が扱うべき全項目——技術検証項目・依存する正典の確定値・検証に必要な測定対象・現時点で未定義の値**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/00 Phase 1 技術検証表の全行（項目・予想・代替案）
2. docs/40 §4.9 先行ゲート・§9 手渡しで本 Issue 宛の全項目（先行ゲート5点＋S1 並行の全項目——環礁方式選択・性能測定含む）
3. docs/16 §7.5 の技術手渡し全項目（構造生成 JSON・jigsaw・processor・個別層生成・L3 同一構造判定・灯台−座礁船連動）＋§2.4 生成4型語彙
4. docs/18 §8 の実装手渡し全項目（font プロバイダ・GuiLayer・ItemTooltipEvent・JEI・Patchouli・自前書物器・由来札同期）
5. docs/19 §9 の実装手渡し全項目（環境床コントローラ・発火抑制・サーバー権威発火±100ms・響界判定・sounds.json・ダッキング）
6. docs/32 §6 のマルチ確定値（個別層データ構造・一人一ノミ・由来札・宝箱/ドロップ個別層・結末綴じ先着・ボス HP 係数・月充填人数非依存）
7. docs/23 のゴミ箱転移・持ち込み可否の設計前提（転移時の振る舞い確定値）
8. docs/46 の依存 MOD 確定値（JEI・Patchouli・jarJar・収録条件5点）
9. docs/20 の色規則・シェーダー OFF 一次チャネル保証（H-29 カラー回帰の母本）
10. docs/11 の異物・二層構造の正典前提（異物チャンク・現実側からの可視性の物語要件）
11. 「検証すべきだが仕様がない/数値が未定」の全項目（性能合格ライン・同期精度・生成負荷の閾値）
12. ADR の技術前提（0002〜0005——次元・ゴミ箱・状態モデル・異物の確定事項）

## 出力
inventory_md に Markdown で：各行「項目｜内容｜出典（ファイル・節）｜種別（次元/地形/構造/転移/個別層/UI/書物/音/演出/依存/測定）｜先行ゲート/S1並行/調査のみの示唆｜確定状況」。docs/56 §4 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のリードテックプランナー。{unit['title']} を、調査基準（docs/56）に基づき深い思考で執筆せよ。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 正典からの棚卸し（抽出済み——これを網羅的に回収せよ）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/56 §3 の設計原則 P-TV-01〜07 に載せてから、項目の事情で具体化する
- docs/56 §1 の先行調査（API 実在性・先行実装）を根拠に引く——クラス名・JSON パス・出典を明記する
- 実現性評価が「低」または「中」の項目は**必ず複数案比較＋推奨案つき要承認**として構造化する（環礁生成方式・異物可視性モデルは特に）
- PoC 仕様は「何を作り・どう動かし・何を測るか」を実装者が迷わない粒度まで——ただし実装コード自体は書かない（P-TV-04）
- 合格ラインは測定方法つき（ツール・単位・閾値）。docs/40 §4 の基盤要件に着地すべき数値は書き戻し導線を明記
- 「要承認」は 57-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/56 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の技術実現性レビューア。以下の検証計画を、docs/56 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/56 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（3段分類）
1. **正典制約適合**：G-TV-01〜13 に反する記述がないか（特に G-TV-01 実装コード未記述・G-TV-03 ゲート区分・G-TV-05/06 個別層・可視性の正典目標）
2. **網羅性**：担当 H 項目が全て項目カード形式で回収されているか、必須フィールド（実現性評価／PoC 仕様／合格ライン／設計代替／依存／Phase 1 タスク化／リスク・工数）に欠落がないか
3. **実在性**：API・仕組みの主張に docs/56 §1 または正典の出典があるか——実在しない API・推測の実装経路があれば major 以上
4. **検証可能性**：合格ラインが測定可能か（「ちゃんと動く」等の曖昧な記述がないか）・測定方法が書かれているか
5. **設計代替**：リスク帯の項目に逃げ道があるか——可視性モデル・環礁方式等の比較が網羅的か
6. **権威侵害**：承認済みの正典値（40-Q 群・依存 MOD・マルチ確定値・音規格）を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のリードテックプランナー。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/56 §4 の H-01〜30 が4ユニットのいずれかで項目カード形式で扱われているか、§0〜§9 の必須節・§6 対応表どおりの配置か、要承認に ID・書き戻し先があるか",
        "consistency": "整合——ユニット間で前提・方式の選択が食い違わないか（例：個別層データ構造の案と可視性モデルの案が矛盾しないか、環礁生成方式と構造生成 JSON 節の整合、転移骨格と持ち込みフィルタの接続点）、検証環境（§7）と各項目カードの測定方法の齟齬",
        "canon": "正典整合——4ユニット全体が docs/00/16/18/19/23/32/40/46 の記述と矛盾しないか、承認済みの確定値を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**技術検証計画の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/56 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 検証項目の棚卸し（抽出） ===")
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
