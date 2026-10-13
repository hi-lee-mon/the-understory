import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/66_research_next_regions.md（本タスクの物差し——§2 正典制約 G-NR-01〜20・§3 原則 P-NR-01〜08・§4 棚卸し H-NR-01〜14・§5 組版テンプレは必須）
- docs/16_structures_dungeons.md §6.4（補助領域——埋立て地・L3 の確定構造範囲）・§2.7（環礁縁の没腐濃層の構造表現）・§7.5（手渡し一覧）
- docs/23_discard_grammar.md §8.4〜§8.6（焼却・処理の届き先・他人を捨てる・破壊と容量）・§10（QoL 整合・喪失境界の概念）
- docs/32_system_specs.md §5（灼熱の埋立て地からの帰還——処理口・焦げ跡つき片道）
- docs/34_chapter_plots/04_unchosen_mine.md §3（隔離区画の気配）・§7.3（響炉の窓——埋立て地の初視認点・鍛冶師の言及）
- docs/15_mobs_bosses.md §3・§6（U4-10 継続課題——敵性個体の扱い）
- docs/38_numeric_tables/04_mobs_economy.md §2（没腐度の増減・段階効果・フェア性の体系）・§6（継続課題）
- docs/40_vertical_slice_plan.md §7.2・§9（保留領域台帳——L3・灼熱・喪失境界の消費先）
- docs/44_glossary.md（仮称「灼熱の埋立て地」の扱い・用語正本）
- docs/36a_foreshadow_inventory.md §7（F-MECH-14——埋立て地の物語回収は意図的未回収の明示管理）
- AGENTS.md（作業規範——Phase 0＝設計のみ・日本語・面白さの最終決定権＝ユーザー）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/66 §5 を厳守）：
- 担当ファイルの必須節（§5「各設計書の共通見出し」1〜10）を全て埋める。節構成を勝手に変えない
- **設計書を書くこと**——「〜を検討する」という方針文は成果物ではない。判定・発火条件・状態遷移・空間構成・演出系列を具体的に書く
- 正典値（数値・ID・名称・確定文・SE名・TX-ID・N-ITEM/N-DEV/N-ECO/N-MOB ID）は引用のみ・再定義禁止（G-NR-01）。変更が必要なら要承認へ
- 正典にない数値・ID・名称は**型と変数のみ定義し確定値は手渡し**（G-NR-13/14/15/20——Issue #15・docs/19・docs/44・docs/52 へ送る）
- 「要承認」は open_questions に集約し、本文側では `67-U{n}-Q{m}` の参照IDを括弧書きで示す（推奨案＋書き戻し先必須）
- Phase 0 制約：実装成果物（コード・JSON）は作らない
- 出力は複数ファイルの場合 `=== FILE: docs/67_next_regions/xxx.md ===` の区切り行で分割して section_md に入れる
"""

CONSTRAINTS = """絶対条件（docs/66 §2 の G-NR-01〜20）：
- G-NR-02：本編の分離線を侵さない——本編側（16 §6.4.1・23 §8.4・34/04）の記述を書き換えない。本書系は次コンテンツ側の仕様
- G-NR-03：片道機構の確定値（到達＝処理口片道／帰還＝逆流口から焦げ跡つき・往復不可）は基盤——「片道である」こと自体を変更しない
- G-NR-04：他人を捨てる＝クレーンのみ。落とされた側は死でなく転移＝特権・「◯◯に捨てられた」記録
- G-NR-05/06：喪失境界＝越えられるが刻まれる帯・烙印は没腐度体系（38/04 §2）内の一段——不可逆の罰にしない
- G-NR-07：独自素材＝燃えなかった煤（N-ITEM-015）のみ——新規独自素材は要承認
- G-NR-08：住人候補の人格・救出物語は設計するが本編側への回収を約束しない（F-MECH-14 明示管理）
- G-NR-09：審美「かすれた・欠けた・継がれた」枠内・橙＝差し色・光演出は輪郭にも複合表現
- G-NR-10：生成方式の確定（埋立て地＝③地形依存埋没型＋①固定テンプレ、L3＝④手組み）を変えない
- G-NR-11：結末非依存——結末分岐に依存する設計を書かない
- G-NR-12：環礁縁の構造表現は docs/16 §2.7 が正本——喪失境界はゲーム規則（判定・刻み・戻り）のみ担当
- G-NR-13：数値絶対値は Issue #15 へ手渡し（型と変数のみ定義）
- G-NR-14：「灼熱の埋立て地」は仮称——正式名案は要承認として起票、確定扱いしない
- G-NR-16：順不同耐性——他章の結末・固有情報に依存しない設計
- G-NR-17：L3 は灼熱接続点のみ——L3 本体の構造設計（16 §6.4.2 確定済み）を再設計しない
- G-NR-18：配信の見せ場を捨てる側・届く側の双方で設計
- G-NR-19：説明しないで発見させる——ゲーム内説明を避け造形・気配・記録で語る
"""

UNITS = [
    {
        "id": "landfill",
        "title": "U1：灼熱の埋立て地 設計書（docs/67_next_regions/burning_landfill.md）",
        "scope": "埋立て地の領域設計——到達経路（処理口の実構造・片道機構の発火条件・クレーン以外の到達経路の有無を検討して推奨）・空間構造（焦層の丘・焼却堆積区画・住人候補の場・独自素材区画の区画割りと導線）・迷子回帰（処理口への視線・煙目印）・収容物・生成方式の詳細・到着→探索→帰還（焦げ跡）の体験弧。「他人を捨てられた者」の到着シーケンス（着弾の絵・記録の残り方）も含める",
        "docs": "担当正典：docs/16 §6.4.1（埋立て地カード全項）・§2.7（環礁縁の構造表現）・docs/23 §8.4/§8.5/§8.6（届き先・捨てる儀式・破壊と容量）・docs/32 §5（処理口・焦げ跡・片道）・docs/34/04 §3 #4・§7.3（隔離区画の気配・鍛冶師の言及・響炉の窓の初視認点）・docs/49 §2.5（迷子回帰規格）・docs/20 §5（章パレット——橙の扱い）・docs/19 §3/§4（該当する SE・環境床の有無を確認——新規 SE 型の要否を要承認へ）",
    },
    {
        "id": "inhabitants",
        "title": "U2：埋立て地の敵性個体・住人候補・物語配置（docs/67_next_regions/landfill_inhabitants.md）",
        "scope": "U4-10 引き継ぎの着地——埋立て地の敵性個体設計（種別・振る舞い・発火条件——「襲う怖さでなく存在の怖さ」の型。本編「気配のみ」との接続：次コンテンツで何を置くか／置かないかの推奨）・住人候補（人格の型・救出物語の構成・F-MECH-14 明示管理どおりの撒き方）・怖い物・消したかった物のロア配置（由来紐付け「◯◯の処理場から来た」の群像劇燃料としての設計）・断片/ログ/警告文の発火点（実文は docs/52 へ手渡し——型のみ定義）",
        "docs": "担当正典：docs/15 §3・§6（敵性個体の規格・U4-10）・docs/16 §6.4.1-4/8/10（住人候補・収容物・敵性個体未規定の確定）・docs/36a §7（F-MECH-14——未回収の明示管理）・docs/23 §8.4（設置者紐付け・群像劇燃料）・docs/38/04 §1（モブ発生・中立⇔敵対遷移表——環礁の住人との住み分け）・§6（継続課題行）・docs/25（人物規格——救出住人の型があるなら引用）・docs/34/04 §7（鍛冶師の言及——埋立て地を知っている者としての語り口）・docs/52 §1.1（TX-ID 規格——断片は型のみ定義）",
    },
    {
        "id": "boundary",
        "title": "U3：没腐の喪失境界 システム仕様（docs/67_next_regions/lost_boundary.md）",
        "scope": "喪失境界のゲーム規則の正本化——帯域構造（環礁縁の没腐濃層の内側/帯内/外側の3区分）・越え判定（何が「越えた」か——位置・速度・手段）・刻まれる形（烙印の種別・没腐度への加算・可視化＝造形/気配/ログで語る）・戻りのルール（帯内での滞在・引き返し・越えて戻るの3系統）・没腐度連動（38/04 §2 体系内での一段としての位置づけ・回復余地）・フェア性（意図しない越えの保護——「帰れない状態を作らない」原則との整合）・帯内で起きること（何が見える・何が得られる/失われる・越えた先に何があるか——世界の外縁の描き方）",
        "docs": "担当正典：docs/23 §10（喪失境界の概念・QoL 整合）・§4.2（「帰れない状態を作らない」原則）・docs/16 §2.7（環礁縁の没腐濃層の構造表現——造形は引用、規則は本書）・docs/38/04 §2.1〜2.3（没腐度の増減イベント・段階効果・フェア性上限——烙印はこの体系内の一段）・docs/13 §1（迷子・導線の一般則）・docs/45/02（境界の非言語警告の型——近づく者への気配）・docs/32 §2.2（帰還フォールバック原則）・docs/11 §5（月の共有——境界を越えても月は見えるか）",
    },
    {
        "id": "l3_cross",
        "title": "U4：L3 灼熱接続点＋横断・README（docs/67_next_regions/l3_connection.md＋README.md）",
        "scope": "l3_connection.md：L3 ごみ処理場と埋立て地の接続仕様——処理口の実構造（投入→焼却→国側着弾の系列・処理口が埋立て地側に持つ逆流口の実体）・「処理された者」の到着シーケンス（クレーン掴み→落下→着弾の全工程を届く側の視点で）・焦げ跡の刻み方（どこに・どう見える・記録の形式）・L3 側との境界責務（L3 本体構造は 16 §6.4.2 確定——本書は接続点のみ）・クレーン以外の到達経路の有無の検討結果（U1 側と矛盾しない結論をまとめる）。README.md：目次・3領域の関係図・制作プロセス・範囲の整理（所掌/所掌外）・消費先（docs/44 正式名化・docs/15 敵性個体表・Issue #15 数値・docs/52 実文・Issue #13 生成技術）・要承認集約（67-U{n}-Q{m}）",
        "docs": "担当正典：docs/16 §6.4.2（L3 処理場カード全項——確定部品・儀式・破壊・容量・同一構造判定）・§6.5（手渡し表）・docs/23 §8.3〜8.6（処理場の文法・捨てる儀式・容量）・docs/32 §5（処理口・帰還）・docs/17 §3（配信の儀式としての捨てる/届く）・docs/40 §7.2/§9（L3 の消費先＝本 Issue）・docs/44（仮称の扱い・44-U4-Q2 所掌外の明記）・docs/42 §5.2（R-41 着地記録の要件）・docs/66 §5（組版テンプレ・README 構成）",
    },
]

META = {
    "name": "next-regions",
    "description": "次コンテンツ領域 docs/67（Issue #37）——棚卸し→4ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "領域要素の棚卸し（確定制約・未規定点・手渡し一覧の統合台帳）", "count": 1},
        {"title": "write", "detail": "4ユニットの設計書執筆", "count": 4},
        {"title": "review", "detail": "正典整合・設計実現性の深い思考レビュー", "count": 8},
        {"title": "revise", "detail": "指摘の改訂", "count": 4},
        {"title": "crosscheck", "detail": "整合・網羅・設計品質の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの設計書全文（Markdown——=== FILE: path === 区切り）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝67-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "領域要素台帳（Markdown——確定制約・未規定点・手渡し一覧・参照節の統合台帳）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の設計台帳の編集者。リポジトリ内の全設計書から、**次コンテンツ領域 docs/67（Issue #37）が供給すべき要素**を棚卸しせよ。範囲＝灼熱の埋立て地・没腐の喪失境界・L3 ごみ処理場の灼熱接続点（docs/40 §7.2・docs/44 手渡しの所掌どおり）。

{MUST_READ}

## 抽出対象
1. **確定制約の全文収集**：埋立て地（到達・内部構成・導線・演出・収容物・生成方式）・L3（構成パーツ・儀式・破壊・容量・同一構造判定）・喪失境界（概念・環礁縁の構造表現）の確定記述を docs/16 §6.4・§2.7・23 §8.4〜8.6・§10・32 §5 から正確に収める（要約でなく引用に近い粒度）
2. **未規定点の網羅**：各所で「未規定」「次コンテンツへ手渡し」「open_questions」「Issue #37」へ送られた項目を全件集める（16 §7.5・15 §3/§6・38/04 §6・40 §7.2/§9・42 §5.2・44 §7.2・36a §7）
3. **没腐度体系**：38/04 §2.1〜2.3 の増減イベント・段階効果・フェア性上限——烙印が「体系内の一段」として整合するための正典数値枠
4. **関連 SE・UI・断片規格**：docs/19 §3/§4（適用可能な SE・環境床）・docs/18（通知・由来札）・docs/52 §1.1（TX-ID 規格——断片は型のみ定義するため）
5. **敵性個体の規格**：docs/15 §3（モブ設計の型）・38/04 §1.4（中立⇔敵対遷移表）——埋立て地に適用可能な型
6. **導線・迷子規格**：docs/49 §2.5・docs/13 §1・45/02 §4.2（4段系列）——埋立て地の迷子回帰・境界の警告に適用する型
7. **手渡し先の一覧**：本設計書が成果を渡す先（docs/44 正式名・docs/15 敵性個体・Issue #15 数値・docs/52 実文・Issue #13 生成技術・docs/42 R-41 着地）と各先が要求する形

## 出力
inventory_md に Markdown テーブル群で：「E-ID｜要素名｜種別（確定制約/未規定点/数値枠/SE・UI/敵性規格/導線規格/手渡し先）｜領域（埋立て地/L3/喪失境界/横断）｜内容｜出典節」。解釈・新規創作はしない——実在する指定を忠実に集めること。要素数の集計を末尾に付ける。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の次コンテンツ領域の設計者。{unit['title']} を、調査基準（docs/66）と確定正典に基づき深い思考で執筆せよ。**方針の説明でなく、判定・発火条件・状態遷移・空間構成・演出系列を具体的に固定する設計書**を書く。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## 領域要素台帳（E-ID 採番済み——担当領域分を全て回収せよ。確定制約は台帳の記載どおり）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/66 §3 の原則 P-NR-01〜08（届く側の絵・怖さは物と気配・片道の不安を燃料・境界は帯・烙印は体系内の一段・配信の見せ場を双方で・設置者紐付け・未回収の明示管理）に載せてから、仕様ごとに具体化する
- docs/66 §5「各設計書の共通見出し」1〜10 の節構成に従う
- 確定済みの値は引用のみ（G-NR-01）。正典にない値は型と変数を定義して Issue #15・docs/19・docs/44・docs/52 へ手渡し（G-NR-13/14/15/20）
- 「正典で未規定」な点は、選択肢＋推奨案つきで open_questions へ `67-U{{n}}-Q{{m}}` で起票（書き戻し先必須）。推奨案は面白さの根拠まで書く
- 分離線を侵す設計（本編への到達経路・本編側の敵性個体配置など）は絶対に書かない（G-NR-02）

## 出力形式（section_md）
docs/66 §5 の担当節構成をすべて埋めた Markdown 全文（複数ファイルは === FILE: path === 区切り）＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の次コンテンツ領域設計のレビューア。以下の設計書を、docs/66 の基準と各正典に照らして厳しくレビューせよ（深い思考——正典の該当節（docs/16・23・32・34/04・15・38/04・40・44・36a）を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点
1. **正典整合**：確定制約（片道機構・クレーンのみ・気配のみ・生成方式・没腐度体系・F-MECH-14）への抵触がないか。正典値の再定義・無断変更・新規ID/SE名/名称の創作がないか（G-NR-01/03/04/05/06/07/08/10/11）
2. **分離線**：本編側の記述を書き換えていないか。次コンテンツ側の仕様として書けているか（G-NR-02）
3. **設計の具体性**：判定・発火条件・状態遷移・区画構成が実装者が読める粒度で書かれているか。「検討する」「詳細は別途」で逃げていないか
4. **未規定点の扱い**：正典で未規定の点が要承認（67-U{{n}}-Q{{m}}・推奨案＋書き戻し先）へ起票されているか。勝手に確定値を書いていないか（G-NR-13）
5. **面白さ**：P-NR-01〜08 の原則が体現されているか——届く側の絵があるか・怖さが物と気配に由来するか・片道の不安が緊張として設計されているか
6. **フェア性**：喪失境界の烙印が没腐度体系内の一段として整合しているか・「帰れない状態を作らない」原則と矛盾しないか（G-NR-06・23 §4.2）
7. **配信**：捨てる側・届く側の双方の見せ場が設計されているか（G-NR-18）
8. **命名**：仮称「灼熱の埋立て地」を確定扱いしていないか。正式名案があれば要承認として適切に起票されているか（G-NR-14）
9. **組版**：docs/66 §5 の必須節が全て埋まっているか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案——指摘には設計書の節を明記）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の次コンテンツ領域の設計者。以下の設計書をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行設計書
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
        "consistency": "正典整合の横断監査——全設計書を通じて正典値（構造物名・ID・SE名・確定文・没腐度体系）が docs/16・23・32・38/04・44 の正本と一致しているか、領域間の記述（埋立て地↔L3 接続点・喪失境界↔環礁縁表現）が矛盾していないか",
        "coverage": "網羅性——台帳の全 E-ID がいずれかの設計書へ着地しているか、docs/66 §4 の H-NR-01〜14 が全て回収されているか、Issue #37 完了条件（埋立て地の到達経路・敵性個体・構造物の設計書＋喪失境界の帯域・刻まれる形・戻りルール・没腐度連動）が全て満たされているか",
        "dramaturgy": "設計品質の横断監査——「届く側の絵」と「捨てる側の儀式」が対として成立しているか、怖さが「物と気配」に一貫して由来しているか、片道の不安・境界の刻み・未回収の明示管理が各設計書で同じ思想で書かれているか、手渡し先への出力が全設計書で揃っているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**次コンテンツ領域の4ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典（docs/16・23・32・34/04・15・38/04・40・44・36a）と docs/66 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：領域要素台帳
```markdown
{inventory}
```

## 全ユニット設計書
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
    log("=== Phase 1: 領域要素の棚卸し（E-ID 台帳化） ===")
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
    with open("/home/ubuntu/repos/the-understory/.devin-work/issue37/workflow_output.json", "w") as f:
        json.dump(output, f, ensure_ascii=False)
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
