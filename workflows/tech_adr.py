import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/68_research_tech_adr.md（本タスクの物差し——§2 正典制約 G-ADR-01〜10・§3 原則 P-ADR-01〜06・§4 棚卸し H-ADR-01〜17・§5 組版テンプレは必須）
- docs/30_adr/README.md（ADR 規則・テンプレ——immutable・1ADR=1決定）・docs/30_adr/0002_tech_stack.md（ADR の実例——Status 昇格の前例）・docs/30_adr/0004_story_state_model.md（上位決定——共有/個別モデル）
- docs/57_tech_verification_plan.md（Issue #13 承認済み28件——§2 H-01〜H-14・§4 H-15/H-06・§6 H-16〜H-30・§8 要承認表全行——ADR の Decision の一次出典）
- docs/40_vertical_slice_plan.md §4.2〜4.9（基盤要件・先行ゲート・個別層・データ構造 §4.7）・§5.2.2（計測規格 T-1〜T-7）・§9（手渡し）
- docs/32_system_specs.md §2.2（リスポーン優先順位）・§4（異物チャンク生成）・§6（共有/個別確定表）・§9（解禁）
- docs/16_structures_dungeons.md §2.4（構造生成4型語彙）・§3.2/§3.7（決定論的生成・生成トリガ）・§7.5（手渡し）
- docs/19_audio_direction.md §2.5（層割当——転移SE）・docs/18_ui_ux_detail.md（通知・由来札の配信側）
- docs/43_release_plan.md §4.1/§7.1（LICENSE=MIT・移植評価トリガ——ADR 化候補）
- docs/42_risk_register.md §5.2（ADR 化トリガ規則）
- AGENTS.md（作業規範——Phase 0＝設計のみ・日本語・重要な決定はADR）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/68 §5 を厳守）：
- ADR テンプレどおり：Status（Proposed）/Date（2026-10-25）/Deciders（65banseki + Devin）/Related＋Context/Decision/Alternatives Considered/Consequences＋Open Questions（`12-U{n}-Q{m}` 参照表）
- **決定記録を書くこと**——「検討する」は成果物ではない。Decision には承認済み正典の出典 ID（57-U{n}-Q{m}・40-Q{n}・docs/NN §X）を必ず明記する（P-ADR-01）
- 正典値（承認済み決定・数値・ID・名称）は引用のみ・再定義禁止（G-ADR-01）
- 承認済み決定を覆さない——Decision は「承認済み決定の束ね」であり、新規仕様の創作を混ぜない（G-ADR-02）
- 未確定値（スパイクで着地）は「暫定値＋着地先（Issue #15・Issue #13 コメント等）」と明記（G-ADR-05）
- 条件付き確定項（57-U2-Q11）は Consequences に条件付きで記す（G-ADR-06）
- Phase 0 制約：実装成果物（コード・JSON・クラス名確定）は書かない——方式・構造・責務分割まで（G-ADR-04）
- 出力は複数ファイルの場合 `=== FILE: docs/30_adr/NNNN_xxx.md ===` の区切り行で分割して section_md に入れる
"""

CONSTRAINTS = """絶対条件（docs/68 §2 の G-ADR-01〜10）：
- G-ADR-02：承認済み決定を覆さない（57-U1-Q1 案C・57-U1-Q2 案C・40-Q24 固定レイアウト・57-U2-Q6 決定論的生成・57-U2-Q7 リスポーン順位・19-U4-Q4 ±100ms・57-U2-Q12 SE層割当・57-U4-Q1 二層経路・57-U4-Q5 カラー回帰・57-U1-Q4 暫定閾値）
- G-ADR-03：ADR-0004 が上位決定——個別層2系統（表示のみ個別化＋個別層生成）と矛盾しない
- G-ADR-07：1ADR=1決定——4領域を1本にまとめない
- G-ADR-08：Alternatives は実在の検討経緯（docs/57 §2 H-07 案A/B/C・H-06 案A/B/C・ADR-0002 の代替案）から——創作の代替案を並べない
- G-ADR-10：検証結果の記録欄は設けない（Results 節なし）——検証計画への接続は Consequences に
"""

UNITS = [
    {
        "id": "adr0006",
        "title": "U1：ADR-0006 次元生成方式（docs/30_adr/0006_dimension_generation.md）",
        "scope": "次元生成の方式決定記録——Decision：①1つのカスタムディメンション＋ワールド固定レイアウト（場所系列固定・地形肌のみシード依存——40-Q24）②環礁本体＝案C ハイブリッド（環礁アンカー配置関数＋島体骨格コード生成＋肌は noise_settings——57-U1-Q1・TF型）③異物チャンク＝案C（共有希少配置＋個別層の圏内1箇所保証＋棄て極まり追加生成——57-U1-Q2）④構造生成4型語彙との対応（①固定テンプレ②jigsaw増築③地形依存埋没④手組み——docs/16 §2.4）⑤データ駆動方針との関係（ADR-0002）。Alternatives：案A（ノイズ・バイオーム主導）・案B（全手組みテンプレ）の却下理由は docs/57 §2 H-07 の比較から引用。Consequences：案A縮退の条件・Phase 1 スパイク H-01/H-02/H-07 の合格条件・個別層生成（ADR-0007/0008 への接続）・埋立て地＝③+①・L3＝④の所掌外注記",
        "docs": "担当正典：docs/57 §2 全部（H-01/H-02/H-07/H-08/H-11/H-14——案A/B/C の比較表は忠実に引用）・§8（57-U1-Q1〜Q4）・docs/40 §4.2（環礁生成方式・ワールド固定）・docs/16 §2.4/§3.2/§3.7/§6.4（語彙規約③・決定論的生成・生成トリガ・構造カード）・docs/32 §4.1（異物生成ルール）・docs/11 §4（異物定義）・ADR-0002・ADR-0005",
    },
    {
        "id": "adr0007",
        "title": "U2：ADR-0007 セーブ・状態同期（docs/30_adr/0007_save_state_sync.md）",
        "scope": "永続化・状態同期の決定記録——Decision：①共有層＝ワールドデータ／個別層＝プレイヤーデータの分離保存（ADR-0004 Consequences の技術化）②個別層2系統の実装責務（表示のみ個別化＝実体共有・個別層生成＝所有者別内容分岐——異物チャンク・自分の区画・自分の捨て場区画）③永続化する状態の台帳（章進行レジストリ＝予告頁選択・淀み指標／拾得登録／個人没腐度カウンタ／死亡・リスポーン3点＝57-U2-Q7 確定順位／転移機構状態／異物発見者集合——docs/40 §4.7・docs/57 §4 H-15）④自分の区画＝集約漂着統計からの決定論的生成（再生成・ログ照合可能——57-U2-Q6）⑤データ構造は拡張前提（P-VS-04）。Alternatives：個別層縮退（表示のみ個別化への全退避——57 §4 H-15 の「主題装置の根幹」判定）・全共有保存（個人差分なしモデル——ADR-0004 棄却済み）。Consequences：スライス最大の技術リスク（40-Q15 先行スパイク）・H-15 合格条件・セーブ形式の後方互換方針・章量産時のスキーマ拡張規則",
        "docs": "担当正典：docs/40 §4.7/§4.9/§4.3/§9（データ構造一覧・個別層・手渡し）・docs/57 §4 全部（H-15・H-12——決定論的生成・発見者集合の永続化）・docs/32 §6（共有/個別確定表）・§2.2（リスポーン3点——57-U2-Q7 適用済み本文）・§4（異物の残存・再入）・ADR-0004・docs/23 §12 D1（個別記憶対象範囲）・docs/18 §5.4/§5.9（表示側接続）",
    },
    {
        "id": "adr0008",
        "title": "U3：ADR-0008 マルチプレイ仕様（docs/30_adr/0008_multiplayer.md）",
        "scope": "マルチプレイの決定記録——Decision：①サーバー前提の協力プレイ（物語/村は共有・結末は先着——ADR-0004）②個別層の見え方モデル＝「発見した人にしか見えない」前提（H-06——案選択は Phase 1 スパイク確定。条件付き改訂連鎖 57-U2-Q11 を Consequences に）③共有層イベントの配信精度 ±100ms 目標（19-U4-Q4）④配信層割当：イベント発火点の配信は共有層・転移 SE 等の演出実体は個別層ローカル再生（57-U2-Q12）⑤「1人が捨てた物が全員に届く」の配信モデル（由来物→処理場→着弾の共有イベント系列）⑥マルチ時の見え方差分の判定言語化（誰に何が見えるか——個別層の3系統ごとに）。Alternatives：全員同一視認モデル（個別層なし——ADR-0004 棄却）・案C 全員視認＋初接触消滅（16-U1-Q14 衝突で条件付き——57-U2-Q11）。Consequences：T-7 計測条件・マルチ検証2人構成・配信モード（映え）との関係・専用サーバー必須かLAN可かの所掌",
        "docs": "担当正典：docs/40 §5.2.2 T-7/§4.9（±100ms・先行ゲート）・docs/57 §4 H-06/§3 H-30・§8（57-U2-Q11/Q12）・docs/19 §2.5（SE 層割当——転移SE4件）・§3.6（共有層音の同時配信）・docs/32 §6（共有/個別表）・docs/00 §3.1（個別層の物語定義）・docs/17 §3（配信の儀式——捨てる/届くの見せ場）・docs/23 §8.4〜8.6（他人を捨てる儀式＝マルチ固有の機能）・ADR-0004・docs/46（配布前提のマルチ動作保証の有無）",
    },
    {
        "id": "adr0009",
        "title": "U4：ADR-0009 パフォーマンス方針＋README 更新＋要承認集約（docs/30_adr/0009_performance_policy.md＋README.md）",
        "scope": "0009：パフォーマンス方針の決定記録——Decision：①暫定合格閾値の採用（ms/chunk p95≦50ms・生成中 MSPT≤50ms・初回転移 burst≤10s——57-U1-Q4）②計測規格（T-1〜T-7 の測定系・共有層イベント ±100ms・合成定位源の断り）③互換検証方針（Iris+シェーダー・Distant Horizons——ADR-0002 Consequences）④重い演出のフォールバック構造（二層演出①天空描画本線＋③疑似表現を OFF 一次チャネル必置——57-U4-Q1・カラー回帰＝バイオーム置換本線→擬似着色フォールバック——57-U4-Q5）⑤a11y/配信モードとの係数連動（57-U2-Q10 暗転0.6・63 の描画負荷関連行の確認）。Alternatives：閾値未設定（計測なき運用）・実測のみ逐次判断——スパイクの判定不能として却下。Consequences：T-6 超過時のフォールバック発動・閾値は暫定（実測着地＝Issue #15/#13 コメント）。README.md：既存ADR一覧に 0006〜0009 を追加＋依存関係（0004→0007/0008・0002→0006/0009）の短い注記＋本 Issue で集約された要承認一覧（12-U{n}-Q{m}）を README または所要ファイルに集約",
        "docs": "担当正典：docs/40 §4.8/§5.2.2（閾値・計測規格 T-1〜T-7）・docs/57 §2 H-08/§6 H-10/H-16/H-17/H-29・§7（測定規格・環境バリアント表・合成定位源断り）・§8（57-U1-Q4・U4-Q1/Q4/Q5/Q7）・docs/20（Iris/DH 要件）・docs/63（a11y 描画負荷関連行の確認）・docs/19 §6.1（ダッキング——57-U4-Q7 着地項）・docs/30_adr/README.md 全文・docs/43 §4.1/§7.1（LICENSE・移植評価の ADR 化候補——要承認へ）",
    },
]

META = {
    "name": "tech-adr",
    "description": "技術ADR追加 docs/30_adr（Issue #12）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "技術決定材料の棚卸し（承認済み決定・条件付き項・暫定値の統合台帳）", "count": 1},
        {"title": "write", "detail": "4ユニットの ADR 執筆", "count": 4},
        {"title": "review", "detail": "正典整合・ADR 品質の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "整合・被覆・ADR 品質の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの ADR 全文（Markdown——=== FILE: path === 区切り）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝12-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "技術決定台帳（Markdown——承認済み決定・条件付き項・暫定値・代替案検討史・手渡し入力の統合台帳）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の設計台帳の編集者。リポジトリ内の全設計書から、**技術 ADR（Issue #12——docs/30_adr/0006〜0009）の Decision/Alternatives/Consequences の材料**を棚卸しせよ。範囲＝次元生成方式・セーブ/状態同期・マルチプレイ・パフォーマンス。

{MUST_READ}

## 抽出対象
1. **承認済み決定の全文収集**：docs/57 §8 の承認済み28件（57-U1-Q1〜Q4・U2-Q2〜12・U3-Q1〜5・U4-Q1〜8——各 ID の論点・採用推奨案・書き戻し先を正確に）＋ docs/40 の承認済み決定（40-Q8/Q15/Q19/Q24・T-1〜T-7）＋ ADR-0002/0003/0004/0005 の Decision と Consequences（上位決定として引用されるもの）
2. **複数案比較の検討史**：docs/57 §2 H-07（案A/B/C の比較表全文）・§4 H-06（可視性モデル3案）・§4 H-15（個別層縮退）——Alternatives Considered の一次情報
3. **条件付き・暫定項**：57-U2-Q11（条件付き正典改訂連鎖）・暫定値と着地先（57-U1-Q4 閾値・57-U2-Q8 近接範囲・57-U4-Q7 ダッキング量——「暫定・PoC で着地」の一覧）
4. **セーブ/同期の台帳材料**：docs/32 §6 の共有/個別確定表・docs/40 §4.7 のデータ構造入力一覧・57-U2-Q6/Q7——永続化対象の全列挙（章進行レジストリ・拾得登録・個人没腐度・リスポーン3点・転移機構・異物発見者集合・自分の区画/捨て場区画）
5. **マルチの台帳材料**：docs/32 §6（マルチ時の見え方行）・19-U4-Q4 ±100ms・57-U2-Q12（層割当疑義の裁断）・docs/23 §8.4〜8.6（他人を捨てる＝マルチ固有の儀式）・docs/46（配布時のマルチ動作保証の有無）
6. **パフォーマンスの台帳材料**：57-U1-Q4 暫定閾値・T-1〜T-7 計測規格（docs/40 §5.2.2）・57-U4-Q1/Q5（経路選択・フォールバック）・Iris/DH 要件（docs/20・ADR-0002）・docs/63 の描画負荷関連行
7. **ADR 化候補の手渡し**：docs/43 §4.1（LICENSE=MIT）・§7.1（移植評価トリガ）・docs/42 §5.2（ADR 化トリガ）——要承認へ載せる候補の洗い出し
8. **既存 ADR の体裁**：docs/30_adr/0001〜0005 の記述粒度・Related の書き方・README 一覧の行形式

## 出力
inventory_md に Markdown テーブル群で：「E-ID｜要素名｜種別（承認済み決定/検討史/条件付き/暫定値/セーブ材料/マルチ材料/性能材料/ADR化候補/体裁）｜領域（生成/セーブ/マルチ/性能/横断）｜内容｜出典節」。解釈・新規創作はしない——実在する決定を忠実に集めること。要素数の集計を末尾に付ける。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の技術決定記録の編集者。{unit['title']} を、調査基準（docs/68）と確定正典に基づき深い思考で執筆せよ。**承認済みの技術決定を「なぜそう決めたか」の記録として束ねる ADR**——新しい設計判断ではなく、すでに承認された判断の根拠・却下案・影響を判定可能な言語で書く。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## 技術決定台帳（E-ID 採番済み——担当領域分を全て回収せよ。承認済み決定は台帳の記載どおり）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/68 §3 の原則 P-ADR-01〜06（出典明記・Consequences 3層・ADR 間接続・曖昧さの解消・要承認採番・README 更新は成果物）に載せてから、Context/Decision/Alternatives/Consequences に具体化する
- docs/68 §5 のテンプレ構成に従う——Status=Proposed
- Decision は「何を採用し、なぜか」を判定可能な言語で。「個別層が動いたとは何を指すか」「マルチで誰に何が見えるか」のような判定可能な言語化を含める（P-ADR-04）
- 承認済み決定の出典 ID（57-U{{n}}-Q{{m}}・40-Q{{n}}・docs/NN §X）を Decision の各項目に明記（P-ADR-01）
- 暫定値は「暫定・着地先」を明記。条件付き項（57-U2-Q11）は Consequences で発動条件つき記述（G-ADR-05/06）
- 「正典で未規定」な点は、選択肢＋推奨案つきで open_questions へ `12-U{{n}}-Q{{m}}` で起票（書き戻し先必須）
- 既存 ADR-0001〜0005 の本文は触らない（immutable）

## 出力形式（section_md）
docs/68 §5 のテンプレ構成をすべて埋めた Markdown 全文（複数ファイルは === FILE: path === 区切り）＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の技術決定記録のレビューア。以下の ADR を、docs/68 の基準と各正典に照らして厳しくレビューせよ（深い思考——正典の該当節（docs/57・40・32・16・19・23・00・43・30_adr）を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点
1. **正典整合**：承認済み決定（57-U{{n}}-Q{{m}}・40-Q{{n}}）を正確に引用しているか。決定内容の改変・推奨案以外の案の混入・新規仕様の創作がないか（G-ADR-01/02）
2. **上位決定整合**：ADR-0004（共有＋個人差分）と矛盾する記述がないか（G-ADR-03）。ADR-0002 のデータ駆動方針・保守方針と整合しているか
3. **1決定性**：1ADR=1決定か——複数の独立決定が混ざっていないか（G-ADR-07）。ただし1領域の主決定＋その副次前提は許容
4. **Decision の言語化**：判定可能な言語で書かれているか（「〜できる」でなく「〜が成立するとは X を指す」）——P-ADR-04
5. **暫定・条件付きの扱い**：暫定値に着地先があるか（G-ADR-05）・57-U2-Q11 が発動条件つきで記されているか（G-ADR-06）
6. **Alternatives の実在性**：実際に検討された案（docs/57 の比較表・ADR の判断史）のみが並び、却下理由がその経緯に忠実か（G-ADR-08）
7. **Consequences**：良い面・悪い面・今後の制約の3層＋Phase 1 スパイクへの合格条件があるか（P-ADR-02）
8. **組版**：Status=Proposed・テンプレの全節が埋まっているか・Open Questions が `12-U{{n}}-Q{{m}}` で採番されているか
9. **範囲規律**：Phase 0 として実装コード・クラス名確定を書いていないか（G-ADR-04）・既存 ADR の本文に触れていないか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案——指摘には ADR の節を明記）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の技術決定記録の編集者。以下の ADR をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行 ADR
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
        "consistency": "正典整合の横断監査——全 ADR を通じて承認済み決定の引用が正典正本（docs/57 §8・docs/40・32・ADR-0002/0004）と一致しているか、ADR 間の記述（生成方式→個別層→セーブ→マルチ→性能の依存連鎖）が矛盾していないか、同一決定が複数 ADR で異なる表現になっていないか",
        "coverage": "網羅性——Issue #12 要求の4領域（次元生成方式・セーブ/状態同期・マルチプレイ・パフォーマンス）に各1 ADR があるか、台帳の全 E-ID がいずれかの ADR の Context/Decision/Consequences へ着地しているか、docs/68 §4 の H-ADR-01〜17 が全て回収されているか、手渡し入力（docs/40 §4.7・57 §9.2・42 §5.2・43 の ADR 化候補）が消費または要承認に載っているか",
        "quality": "ADR 品質の横断監査——各 ADR が1決定として読めるか、Decision が判定可能な言語か、Alternatives が実在の検討史に忠実か、ADR 群として上位決定（ADR-0002/0004）との整合が保たれているか、README 索引の更新が4 ADR 分あるか、Status=Proposed が一貫しているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**技術 ADR 4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典（docs/57・40・32・16・19・23・00・43・30_adr）と docs/68 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：技術決定台帳
```markdown
{inventory}
```

## 全ユニット ADR
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
    log("=== Phase 1: 技術決定材料の棚卸し（E-ID 台帳化） ===")
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
    with open("/home/ubuntu/repos/the-understory/.devin-work/issue12/workflow_output.json", "w") as f:
        json.dump(output, f, ensure_ascii=False)
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
