import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/65_research_chapter_boards.md（本タスクの物差し——§2 正典制約 G-CB-01〜24・§3 原則 P-CB-01〜10・§4 棚卸し H-01〜12・§5 組版テンプレ・§7 レビュー観点は必須）
- docs/50_opening_storyboard.md（ボード書式の正本——ビート形式・運用メモ。本タスクはこれを各章へ展開する）
- docs/44_glossary.md（用語の正本——確定語彙・章名・場所名をここに揃える）
- docs/40_vertical_slice_plan.md §9（スライス範囲の手渡し——Issue #11 の受理済みスコープ）
- AGENTS.md（作業規範——Phase 0＝設計のみ・日本語・面白さの最終決定権＝ユーザー）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/65 §5 を厳守）：
- 担当ファイルの必須節を全て埋める。節構成を勝手に変えない
- **ボードを書くこと**——「〜という演出をする」という説明は成果物ではない。ビート表に画面・音・プレイヤーの行動・狙う感情・配信での見せ場を具体的に書く
- ビートは BD-ID で管理（docs/65 §5 規則：BD-{区画略号}-{連番}）。1ビート＝1枚の絵コンテ粒度
- 正典値（数値・ID・名称・確定文・SE名・TX-ID）は引用のみ・再定義禁止（G-CB-01/10/12/22）。変更が必要なら要承認へ
- 画面欄は環境語彙（docs/45/03 §3 の V1〜V8/C1〜C8）で記述。新規語彙を勝手に作らない（G-CB-21）
- 「要承認」は open_questions に集約し、本文側では `51-U{n}-Q{m}` の参照IDを括弧書きで示す（推奨案＋書き戻し先必須）
- Phase 0 制約：実装成果物（コード・JSON）は作らない
- 出力は複数ファイルの場合 `=== FILE: docs/51_chapter_boards/xxx.md ===` の区切り行で分割して section_md に入れる
"""

CONSTRAINTS = """絶対条件（docs/65 §2 の G-CB-01〜24）：
- G-CB-02/03：docs/50 書式継承・バニラの器のみ・操作体系不変（カットシーン化禁止）
- G-CB-05：環境が先・文字が後——文字要素は全て環境が先に語ったことの確認
- G-CB-06：一次チャネルはシェーダー OFF で成立
- G-CB-07：月は全環礁の空に共有——遠望欄はこの前提で書く
- G-CB-08：ノミは全章常時同行
- G-CB-09：順不同耐性——他章の結末・未訪問章の固有情報をボードに含めない
- G-CB-11：表示時間は docs/18 §2.6 の式（T_base=1.2s・τ=0.12s/字・T_max=10s・頁めくり0.30s）で検算
- G-CB-12：SE・字幕名は docs/19 §3.6 台帳の正典名のみ（新規名禁止）
- G-CB-13：ボス戦の拍子・見得・幕は docs/48/03・docs/38/03 §4.3 が正本——発火点と演出系列を引用し、内部構造を再設計しない
- G-CB-14：予告頁の確定値 Y-1〜Y-6（実シーン再生禁止・挿絵1枚・正方形・章基調色・写実/文字/情報を含まない・動的選択＝N-ECO-901）
- G-CB-15：予約色（朱＝拾得標識・琥珀の例外）を演出名に使わない。色指定は docs/20 §5 章パレット行を引用
- G-CB-16：共有層/個別層の区分（ADR-0004）を発火対象に明記
- G-CB-17：OP側（現実）に配置設計を書かない
- G-CB-19：迷子回帰4段（環境再提示→装置→最小語り→最終段明示増強）を導線欄へ
- G-CB-20：スライス外章（02〜05・終章）のボード詳細は作らない（Phase 3 送り——docs/40 §9 承認済み）
- G-CB-23：断片配置は docs/34 §8・docs/16 §4.x.4 の確定表が正本——配置自体の新設は要承認
- G-CB-24：配信モード（演出抑制）との差分を演出欄の備考に持つ
"""

UNITS = [
    {
        "id": "prologue",
        "title": "U1：序章「漂着浜」ボード（docs/51_chapter_boards/00_prologue.md）",
        "scope": "docs/50 Beat 1-5 の拡張——着弾→散在帯→共同堆積の丘→先人の磯→淀みの窪地→見晴らしの岬→ノミ出会い→村導線→林遠望の全ビート＋小遭遇「没腐した漂着物」。配置精査表には docs/16 §1 総覧表の序章区画構造物行（行16-24）を全件収める",
        "docs": "担当正典：docs/34_chapter_plots/00_prologue.md（§3 場所系列・§5・§6・§8 断片表・§10 切り抜き）・docs/50（書式正本）・docs/16 §3（序章構造物）・docs/19 §4.1（序章音設計）・docs/45/03 §3.1（序章語彙）・docs/52 §2（序章 TX-ID）",
    },
    {
        "id": "ch1",
        "title": "U2：第1章「満ちなかった月の林」ボード（docs/51_chapter_boards/01_moon_forest.md）",
        "scope": "場所系列6（手紙の径口→もうすぐ参道→果樹園→月見の小屋→月読みの丘→摘み取りの丘）＋寄り道3（二度棄ての物置・前任の露営・月下の小島——本ボードでは島への導線・遠望のみ、島上の詳細は U3）＋ミッドポイント覆り＋月欠狼ボス（拍子印・見得・幕の発火点を引用——内部構造は再設計しない）＋結末選択＋救出後差分。配置精査表には docs/16 §4.1.1 の9構造を全件収める",
        "docs": "担当正典：docs/34_chapter_plots/01_moon_forest.md（§3 場所系列・§4 MP・§5 ボス・§6 結末・§7 救出後・§8 断片表・§10 切り抜き）・docs/16 §4.1.1（9構造）・§4.1.4（確定配置）・docs/19 §4.2（01章音設計）・§6.3（ボスステム）・docs/45/03 §3.2（01章語彙）・docs/52 §3（01章 TX-ID）・docs/38/03 §4.3（月欠狼数値参照）・docs/18 §5.2（拍子印 HUD）",
    },
    {
        "id": "village_island",
        "title": "U3：村ボード＋月下の小島ボード（docs/51_chapter_boards/village.md・moon_island.md）",
        "scope": "village.md：拾い人の村の区画ボード——中核棟・図鑑部屋・掲示板・聞き役の場・縁の民・訪問客・共同鍛錬場・名付けの台・共同ゴミ箱/捨て場・jigsaw発展区画の空間・救出後の成長実演面（村機構の可視化）。moon_island.md：補助環礁1島の到達ビート（水平線上の色の変化→接近）・小試練・収容物・遠望（環礁群への視線・月の共有の絵）",
        "docs": "担当正典：docs/16 §1 総覧表（村行25-33・月下の小島行）・§3.4（jigsaw発展区画）・docs/40 §2.3（村のスライス範囲＝初期村＋農園増築1回）・§3（小島＝到達可能な小規模区画・導線気配最小形・コンパス指し先に含めない——U2-J 承認）・docs/25 §4-5（住人配置）・docs/34_chapter_plots/06_final_seat.md §6.3（村の最終形）・01_moon_forest.md §3.7（月下の小島）・docs/45/02 §8（村の語り）・docs/19 §4（村・小島の音——ある分のみ）",
    },
    {
        "id": "crosscutting",
        "title": "U4：横断規格（docs/51_chapter_boards/crosscutting.md＋README.md）",
        "scope": "crosscutting.md：§0 ボード共通規格（書式・BD-ID採番・ビート粒度・必須欄・参照記法・数値の権威一覧）・§1 予告頁挿絵素材割（→02/03/04 の3頁の声・色・一場面の確定表＋Y-1〜Y-6 適用注記——N-ECO-901 動的選択の運用も明記）・§2 世界転調マッチカット仕様（docs/09 §2 映画行の着地——転移・転調・結末の「切り替わる瞬間」を絵の連続性・音の反転・間の長さで形式定義——現在正典未定義のため本書が初出定義になる）・§3 通知型発火タイミング図（幕切れ→綴じ→着弾→由来判明の系列を1表に——docs/18 §2.5.1 手渡しの着地面）・§4 遠望・共有の空の規格・§5 迷子救済の演出系列の型。README.md：目次・制作プロセス・横断確定規則・範囲の整理・消費先・要承認集約",
        "docs": "担当正典：docs/48_fusion_elements/01_episode_production.md（予告頁 Y-1〜Y-6・§7-#7②⑥）・docs/09 §2（映画行・語り形式表）・docs/18 §2.5.1（通知型統一表）・§5.2/5.3/5.4（拍子印・照準時・由来札）・docs/13 §1（迷子回帰4段）・docs/45/02 §4.2・45/04 §2.3 B-3（迷子定量）・docs/50（書式）・docs/20 §5（章パレット）・docs/65 §5-§6",
    },
]

META = {
    "name": "chapter-boards",
    "description": "章ストーリーボード docs/51（Issue #11）——要素台帳化→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "ボード要素の棚卸し（場所・構造物・断片・SE・通知・語彙の統合台帳）", "count": 1},
        {"title": "write", "detail": "4ユニットのボード執筆", "count": 4},
        {"title": "review", "detail": "正典整合・演出実現性の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "整合・網羅・演出品質の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットのボード全文（Markdown——=== FILE: path === 区切り）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝51-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "ボード要素台帳（Markdown——場所系列・構造物・断片 TX-ID・SE発火・通知型・語彙・切り抜き瞬間）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の章ボード台帳の編集者。リポジトリ内の全設計書から、**章ストーリーボード docs/51（Issue #11）が供給すべきボード要素**を棚卸しせよ。**範囲はスライス内のみ**：序・第1章・村・月下の小島＋横断規格（docs/40 §9 承認済み——スライス外章 02〜05・終章のボードは Phase 3 送り）。

{MUST_READ}

## 抽出対象
1. **場所系列**：docs/34_chapter_plots/00_prologue.md・01_moon_forest.md の §3 場所系列＋寄り道＋ミッドポイント＋ボス＋結末＋救出後。docs/16 §1 総覧表の序章（行16-24）・村（行25-33）・第1章（行39-47・月下の小島含む）の構造物行を全件収める
2. **断片配置**：docs/34 §8 断片表のスライス内行＋docs/52 §2・§3 の TX-ID 対応——「どの場所で・何の情報が出るか」
3. **音・SE**：docs/19 §3.3 章別環境 SE・§4.1/§4.2 の序・01章音設計・§6.3 ボスステム——発火点になるものを正典名で収録（docs/40-Q5 のスライス選別があるならそれに従う）
4. **UI・通知**：docs/18 §2.5.1 通知型統一表・§5.2 拍子印（cue 3.0s・window ±0.35s）・§5.3 照準時動詞表示・§5.4 由来札「◯◯の物」——発火タイミングを整理
5. **環境語彙**：docs/45/03 §3.1（序章）・§3.2（第1章）の V1〜V8/C1〜C8 語彙行
6. **切り抜き瞬間**：docs/34 各章 §10・docs/17 §3 の指定
7. **救出後差分**：結末別の色・音・気配の差分要素
8. **横断の未着地要素**：docs/48/01 §7-#7②（予告頁挿絵素材割）・#7⑥（マッチカット——未定義であることを明記）・docs/18 §8 Issue #11 手渡し行・docs/16 §7.5 G18（構造物精査）・docs/19 §9（章別音設計の手渡し）・docs/52 §12（実文・頁区切り・表示時間検算の正本指定）

## 出力
inventory_md に Markdown テーブル群で：「B-ID｜要素名｜種別（場所/構造物/断片/SE/通知/語彙/切り抜き/差分/横断）｜区画（序/01/村/小島/横断）｜配置・発火条件｜出典節」。解釈・新規創作はしない——実在する指定を忠実に集めること。要素数の集計を末尾に付ける。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の章ボード（絵コンテ）の演出設計者。{unit['title']} を、調査基準（docs/65）と書式正本（docs/50）に基づき深い思考で執筆せよ。**仕様を説明するのでなく、プレイヤーの画面・耳・手に何が起きるかを時系列で固定する**。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## ボード要素台帳（B-ID 採番済み——担当区画分を全て回収せよ。配置・発火条件は台帳の指定どおり）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/65 §3 の原則 P-CB-01〜10（説明しないで発見させる・狙う感情を先に宣言・身体を止めない・音と画面を同じ発火点・1配信1章の切り抜き・欠損を設計する・マルチで破綻しない・救出後は色/音/気配の三層・遠望は装置）に載せてから、ビートごとに具体化する
- docs/65 §5 の必須節構成に従う。ビート表の行の形：｜BD-ID｜ビート名｜場所｜画面（見えるもの・最初に見える順序——V/C 語彙）｜音（SE正典名）｜プレイヤーの行動｜狙う感情｜配信での見せ場｜器・通知型｜参照ID｜
- 「画面」欄は「最初に見えるもの→歩くと見えるもの→見上げると見えるもの」の開示順で書く（docs/50・34/00 §2.2 の型）
- 断片は TX-ID 参照のみで実文は引用しない（G-CB-10）。表示時間は18 §2.6 の式で検算して検算値を書く（G-CB-11）
- ボス戦は発火点（拍子印キュー・見得・幕のタイミング）を docs/48/03・38/03 §4.3 から引用し、内部の数値設計は再設計しない（G-CB-13）
- 分からない・正典と衝突する点は open_questions へ `51-U{{n}}-Q{{m}}` で起票（推奨案＋書き戻し先必須）
- 「読まなくても遊べる」層構造：必須情報を文字に置かない（docs/26 §7）

## 出力形式（section_md）
docs/65 §5 の担当節構成をすべて埋めた Markdown 全文（複数ファイルは === FILE: path === 区切り）＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の章ボードレビューア。以下のボードを、docs/65 の基準と各正典に照らして厳しくレビューせよ（深い思考——正典の該当節（docs/16・18・19・34・45・48・50・52）を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点（3段分類）
1. **正典整合**：場所・構造物・断片・音の引用が各正典の該当節と一致するか。正典値の再定義・無断変更・新規SE名がないか（G-CB-01/10/12/22）
2. **書式適合**：docs/65 §5 の必須節が全て埋まっているか。ビートに画面・音・行動・狙う感情・配信の見せ場が揃っているか（G-CB-02）
3. **演出の実現性**：バニラの器で実現できるか・操作を奪う演出・カットシーン化していないか（G-CB-03・P-CB-03）
4. **層構造**：共有層/個別層の区分が発火対象に明記されているか。OP側に配置設計を書いていないか（G-CB-16/17）
5. **発火点の完全性**：docs/19 の章別 SE・docs/18 の通知型が全てビートへ着地しているか（欠落 SE の洗い出し）
6. **順不同耐性**：他章の未訪問情報・結末をボードに含んでいないか（G-CB-09）
7. **面白さ**：狙う感情が宣言され、配信の切り抜き瞬間が最低1つあるか。説明し切っていないか・欠損の設計があるか（P-CB-01/02/05/06）
8. **表示時間**：断片の頁区切り・間が docs/18 §2.6 の式で検算されているか（G-CB-11）
9. **開示順**：画面欄が「最初に見える→歩くと→見上げると」の順序で書かれているか（環境が先 G-CB-05）

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案——指摘にはボードの節または BD-ID を明記）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の章ボード演出設計者。以下のボードをレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行ボード
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
        "consistency": "正典整合の横断監査——全ボードを通じて正典値（場所名・構造物名・SE名・TX-ID・確定文）が docs/44・16・19・34・52 の正本と一致しているか、用語揺れ（「月下の小島」の呼び方等）がないか、順不同耐性（G-CB-09）が全ボードで守られているか",
        "coverage": "網羅性——台帳の全 B-ID がいずれかのボードでビートへ着地しているか、docs/65 §4 の H-01〜12 の各種が回収されているか、docs/40 §9 の手渡し（予告頁挿絵・マッチカット・通知タイミング・構造物精査・章別音設計・表示時間検算）が全て着地しているか",
        "dramaturgy": "演出品質の横断監査——狙う感情の勾配が章間で破綻していないか（静→動→急の呼吸）、切り抜き瞬間が各ボードに存在するか、遠望・共有の空・月の扱いが G-CB-07 どおり区画を跨いで一貫しているか、迷子救済・配信モード差分の型が共通か",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**章ボードの4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典（docs/16・18・19・34・44・45・48・50・52）と docs/65 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：ボード要素台帳
```markdown
{inventory}
```

## 全ユニットボード
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
    log("=== Phase 1: ボード要素の棚卸し（B-ID 台帳化） ===")
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

    consistency_check, cov_check, dramaturgy_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "consistency", inventory), phase="crosscheck", label="cc-consistency", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "dramaturgy", inventory), phase="crosscheck", label="cc-dramaturgy", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("consistency", consistency_check), ("coverage", cov_check), ("dramaturgy", dramaturgy_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"consistency": consistency_check, "coverage": cov_check, "dramaturgy": dramaturgy_check},
    }
    with open("/home/ubuntu/repos/the-understory/.devin-work/issue11/workflow_output.json", "w") as f:
        json.dump(output, f, ensure_ascii=False)
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
