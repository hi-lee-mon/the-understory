import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/58_research_playtest.md（本タスクの物差し——§1 先行調査 GUR 方法論・§2 正典制約 G-PT-01〜12・§3 原則 P-PT-01〜08・§4 棚卸し H-01〜17・§5 組版テンプレは必須）
- docs/40_vertical_slice_plan.md（§5 検証計画——検証3層・E-1〜E-9・T-1〜T-9・A-1〜A-7・S-1〜S-4 の測定方法と合格ラインが正。値は引用のみで再定義禁止・§4.9 先行ゲート・§7 台帳・§9 手渡し——本 Issue 宛の入力群）
- docs/13_progression_map.md（§1 迷子規則・§2 章＝配信回の時間帯域）
- docs/17_streaming_design.md（配信設計——30秒ルール・切り抜き候補・配信モード）
- docs/18_ui_ux_detail.md（§6.1 #7 配信モード係数0.6・通知・字幕仕様）
- docs/19_audio_direction.md（共有層発火±100ms・演出同期の検証前提）
- docs/32_system_specs.md（§2.2 リスポーン3点・§6 個別層/共有層モデル——マルチ観測の正典値）
- docs/34_chapter_plots/01_moon_forest.md（§10 切り抜き瞬間9件・モーメント対応）
- docs/45_nonverbal_guidance/（迷子判定・気配〜示唆段階・多重化規則——E-5・A-1 の母本）
- docs/38_numeric_tables/04_environment_residents.md（没腐度閾値・放置逓増・N-ECO-210——長期観測の正典値）
- docs/00_development_plan.md（Phase 2→3 ゲート・「面白いかを実プレイで検証」の位置づけ）
- docs/30_adr/（0004 状態モデル——個別層観測の前提）
- AGENTS.md（作業規範——Phase 0＝設計のみ）
"""

RULES = """成果物の組版（docs/58 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- docs/40 §5.2 の測定方法・合格ラインは**引用のみ**で数値を変えない。docs/41 が書くのは「誰が・いつ・どう記録し・どう判定するか」の運用形
- 各検証項目は運用カード形式（実施手順／記録者・実施主体／記録形〔ログ・聴取・録画〕／母集団・分母の明記／合格判定の担当）を全部入れる
- 全判断に根拠（正典節／docs/58 の先行調査節・原則番号・制約番号）を付ける。感覚だけの提案は不可
- 未確定・正典変更が絡むものは「要承認」として open_questions へ（**ID＝41-U{n}-Q{m}**・推奨案つき・書き戻し先を明記。本文で正典を直接改変しない）
- 承認済みの正典値（40-Q2/Q6/Q7/Q10/Q20・57-U1-Q4 暫定閾値・マルチ係数・没腐度閾値）を再定義しない——引用のみ
- Phase 0/Phase 1 境界を明記：本書は運用計画書であり、実施は Phase 1 実装完了後
- ログ設計は「記録するイベント一覧・フィールド・紐付け（テスターID/ビルド/シード）」まで具体化（P-PT-01）
"""

CONSTRAINTS = """絶対条件（docs/58 §2 の正典制約 G-PT-01〜12）：
- G-PT-01 Phase 0＝設計のみ。実施は Phase 1 実装後
- G-PT-02 検証3層：L1＝内部・L2＝限定招待非配信3〜8名・L3＝配信者1〜2組（最小形——実機1構成の実配信または収録）
- G-PT-03 外部テスト＝招待パッケージ＋Discord 観測・定点アンケート・自由記述。募集＝Issue #17 配信者網＋クローズド募集
- G-PT-04/05 定量ライン＝40-Q7 の9項目・検証項目表の測定方法/合格ラインは docs/40 §5.2 が正——値の変更禁止
- G-PT-06 マルチ検証は限定形（2人疎通＋係数数値確認＋完走1ケース観測）。L3 合格条件にはしない
- G-PT-07 長期観測項目（没腐度自然到達・放置逓増・リプレイ動機）を本計画で運用設計
- G-PT-08 実配信テスト・公開アルファは Issue #8 へ手渡し——本計画の対象外
- G-PT-09 配信モード係数0.6（概算0.5s/0.7s）は L3 で実効検証
- G-PT-10 不通過＝量産へ移行しない。判定運用ルールを本計画で定める
- G-PT-11 技術閾値は 57-U1-Q4 暫定値（p95≤50ms・MSPT≤50ms・burst≤10秒）を引き継ぎ実測着地は本計画内
- G-PT-12 日本語・要承認は 41-U{n}-Q{m} で §9 集約・推奨案と書き戻し先明記
"""

UNITS = [
    {
        "id": "layers_testers",
        "title": "U1：§0 位置づけ・§1 検証3層の運用設計・§2 テスター要件と募集（docs/41 §0〜§2）",
        "scope": "§0 位置づけ（本書の役割——docs/40 §5 の運用細則版・Phase 0 制約・Issue 完了条件との対応）＋§1 検証3層の運用設計（L1/L2/L3 の目的・対象・実施形〔リモート観察／非同期録画／Discord 中継〕・実施順・各層の前提条件と通過の意味——H-01・H-05）＋§2 テスター要件と募集（L2 募集条件：層・人数・機材・時間・属性バランス＝配信視聴者に近い非配信層を含む設計（H-02）・スクリーニング項目（能力/プレイスタイル/動機の3要素——docs/58 §1.1）・L3 配信者要件（Issue #17 配信者網との接続）・招待パッケージの内容（H-04）・倫理/権利：録画取扱い・公開禁止期間・報酬方針（H-16））",
    },
    {
        "id": "collection_ops",
        "title": "U2：§3 回収設計・§4 検証項目の運用（docs/41 §3〜§4）",
        "scope": "§3 回収設計（回収物3点セット＝録画・イベントログ・聴取の運用形・イベントログ設計——記録するイベント一覧とフィールド・テスターID/ビルド/シード紐付け・セッション再現性（H-06）・定点アンケート設計——転移直後/ボス撃破後/結末後/終了時の4定点＋自由記述・項目とスケール（7件法・逆得点項目）・「やめたい点」検出（H-07）・終了後構造化インタビュー項目——核心モーメント気づき・逡巡・拾い直し・死に学習（H-08））＋§4 検証項目の運用（E-1〜E-9・T-1〜T-9・A-1〜A-7 を運用カード形式へ展開——実施手順・記録者・記録形・母集団/分母の明記〔E-3 の由来物初投入経由限定等〕・合格判定担当。測定方法と合格ラインは docs/40 §5.2 を引用して変えない。H-09〜H-11）",
    },
    {
        "id": "stream_longterm",
        "title": "U3：§5 配信環境検証の運用・§6 長期観測項目（docs/41 §5〜§6）",
        "scope": "§5 配信環境検証の運用（L3 実施形の選定——実機1構成での実配信/収録の比較と推奨・S-1〜S-4 の運用化：切り抜き候補≥3の観測手順・「配信1回＝第1章クリア」収まりの測り方・視聴者/配信者の状況言語化検証・同時性の配信目線確認・配信モード係数0.6（0.8s/1.2s→概算0.5s/0.7s）の実効確認方法・演者負荷を考慮した E 系分離（P-PT-07）・H-12）＋§6 長期観測項目（没腐度自然到達・放置逓増〔初回7日/次5日/以後3日・合計+4cap——38/04 §2.2〕・リプレイ動機の追跡設計：追跡期間・回収方法・L2 反復参加の扱い・強制到達検証との住み分け（40-Q10）・H-14）",
    },
    {
        "id": "judgment_handoff",
        "title": "U4：§7 判定運用ルール・§8 スケジュール・§9 要承認集約・§10 手渡し（docs/41 §7〜§10）",
        "scope": "§7 判定運用ルール（合格/一部不合格/巻き戻しの判定手順——P-PT-06「判定を先に書く」・40-Q7 定量9項目の集計規則・中央値/分母の集計定義・判定基準の事後変更禁止・再試行の扱い（何人まで・何回目で判定保留か）・判定権者＝ユーザー最終決定の位置づけ・書き戻し先——不合格時の巻き戻し導線を docs/40 §7 台帳・Issue #15・#34 等へ明示（H-13））＋§8 スケジュールと前提（実施順——先行ゲート5点通過・Phase 1 実装完了を前提とした L1→L2→L3 の順・各層の所要見積・H-15）＋§9 未決・要承認集約（41-U{n}-Q{m}——唯一の台帳・推奨案・書き戻し先・統合元つき）＋§10 手渡し一覧（上流消費＝docs/40 §5・下流提供＝Issue #8・#34・#15・Phase 3 判定——H-17）",
    },
]

META = {
    "name": "playtest-plan",
    "description": "プレイテスト計画 docs/41（Issue #6）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
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
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝41-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "抽出した検証項目・運用前提の棚卸し（Markdown）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の仕様監査役。リポジトリ内の全設計書から、**Issue #6（プレイテスト計画→docs/41）が扱うべき全項目——検証項目・テスター要件・観測対象・判定ルールの入力・配信環境検証・長期観測項目・上流からの確定値**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. docs/40 §5 検証計画の全項目（検証3層の定義・E-1〜E-9・T-1〜T-9・A-1〜A-7・S-1〜S-4——測定方法と合格ラインの確定値を各行忠実に）
2. 40-Q2/Q6/Q7/Q10/Q20/Q21/Q25 の承認値（外部テスト形態・定量ライン9項目・長期観測項目・配信モード・マルチ限定検証——§8 承認済み行から）
3. docs/40 §7 台帳のうち本 Issue へ引き継がれる項目（長期観測・マルチ観測・量産判定の前提）
4. docs/40 §9 手渡しの本 Issue 宛行（L2 募集条件・定点アンケート骨格・観測項目の手渡し）
5. docs/13 §1 迷子規則（迷子判定の発火条件・回帰手段——E-5 の母本）・§2 章時間帯域（E-2・S-2 の母本）
6. docs/17 配信設計（30秒ルール・切り抜き候補・配信モード・エピソード構造——S-1〜S-4 の母本）
7. docs/34/01 §10 切り抜き瞬間9件・§1.3 モーメント26点（E-3・S-1 の観測対象リスト）
8. docs/45 の導線規則（勾配圏外滞留90秒・未消化淀み周回——迷子判定の発火条件・多重化規則）
9. docs/32 §2.2 リスポーン3点・§6 個別層モデル（T-2・T-5 の観測前提）
10. docs/38/04 の没腐度閾値・放置逓増（初回7日/次5日/以後3日・+4cap——長期観測の正典値）
11. docs/18 §6.1 配信モード係数0.6・通知/字幕仕様（S 系と A-3 の前提）
12. docs/19 の±100ms 同期目標（T-7/S-4 の前提）
13. Issue #17 配信者網の前提（D-7：配信者到達はサーバーイベント主経路——募集経路の正典）
14. 「運用化すべきだが仕様がない」項目（募集条件・スクリーニング・倫理/権利・判定手順・再試行規則）

## 出力
inventory_md に Markdown で：各行「項目｜内容｜出典（ファイル・節）｜種別（層運用/テスター/回収/検証運用/配信/長期/判定/スケジュール/倫理/手渡し）｜確定状況」。docs/58 §4 と重複してよい——正典実記述の検証が目的。解釈・判断はせず実在する記述を忠実に集めること。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」のリードプレイテストプランナー。{unit['title']} を、調査基準（docs/58）に基づき深い思考で執筆せよ。

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
- まず docs/58 §3 の設計原則 P-PT-01〜08 に載せてから、項目の事情で具体化する
- docs/58 §1 の先行調査（GUR 方法論・レシピ検証・テレメトリ・調査票設計・リモート運用・倫理）を根拠に引く
- docs/40 §5.2 の測定方法・合格ラインは引用のみ——値を変えたり独自の新ラインを書かない。運用化で「何をもって測定と見なすか」は具体化してよい（例：迷子発火のログイベント定義）
- イベントログ設計は「記録イベント一覧（イベント名・発火点・フィールド）」を表にする——40-Q7 の定量ラインを全部ログで賄えることを確認してから残りを聴取へ振る
- 選択肢がある運用判断（L3 実配信 vs 収録・テスター人数内訳・報酬方針・再試行規則）は**複数案比較＋推奨案つき要承認**として構造化する
- 「要承認」は 41-U{{n}}-Q{{m}} 形式の ID・推奨案・書き戻し先つきで open_questions に集約

## 出力形式（section_md）
docs/58 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」のプレイテスト計画レビューア。以下の計画を、docs/58 の基準に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/58 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}

## レビュー観点（3段分類）
1. **正典制約適合**：G-PT-01〜12 に反する記述がないか（特に G-PT-04/05 の値の引用のみ・G-PT-06 マルチ限定・G-PT-07 長期項目の回収・G-PT-08 対象外の境界）
2. **網羅性**：担当 H 項目が全て回収されているか、運用カードの必須フィールド（実施手順/記録者/記録形/母集団・分母/判定担当）に欠落がないか
3. **測定可能性**：「何をもって測定か」が具体か——ログイベントが未定義・「確認する」で終わる項目がないか
4. **40-Q7 カバレッジ**：定量ライン9項目の全てが、ログ計測か聴取かに対応づいているか——抜けた観測対象がないか
5. **運用実在性**：手順が実施可能か（人数・機材・Discord 運用・聴取時間の負荷見積）——机上の空論でないか
6. **権威侵害**：承認済みの正典値（測定方法・合格ライン・マルチ係数・没腐度閾値）を独自に再定義していないか
7. **状態管理**：要承認に ID・推奨案・書き戻し先があるか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」のリードプレイテストプランナー。以下の設計をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

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
        "coverage": "網羅性——棚卸しと docs/58 §4 の H-01〜17 が4ユニットのいずれかで運用化されているか、§0〜§10 の必須節・対応表どおりの配置か、要承認に ID・書き戻し先があるか",
        "consistency": "整合——ユニット間で前提・運用定義が食い違わないか（例：§1 の層定義と §4 運用カードの実施主体、§3 のログ設計と §7 集計規則で使うイベント定義、§5 配信者分母と §4 E系の適用範囲）、定点アンケート設置点と E系検証項目の対応",
        "canon": "正典整合——4ユニット全体が docs/40 §5・docs/13/17/32/34/38/45 の記述と矛盾しないか、承認済みの確定値を再定義していないか、正典を事実上書き換える提案が『要承認』になっているか、用語が正典どおりか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**プレイテスト計画の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典と docs/58 を実際に開いて突き合わせること）。

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
    log("=== Phase 1: 検証項目・運用前提の棚卸し（抽出） ===")
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
