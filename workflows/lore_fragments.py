import asyncio
import json

REPO = "hi-lee-mon/the-understory"

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/64_research_lore_fragments.md（本タスクの物差し——§2 正典制約 G-LF-01〜26・§3 原則 P-LF-01〜10・§4 棚卸し H-01〜27・§5 組版テンプレ・§7 レビュー観点は必須）
- docs/26_narrative_vectors.md（文体規範の権威——§4 Do/Don't・§4.2 形式別声色・§9 面白さの作法）
- docs/25_characters.md（登場人物の身上調査書——口癖・弱み・声の源泉）
- docs/44_glossary.md（用語の正本——確定語彙・読み仮名をここに揃える）
- docs/24_story_foundation.md（真実の構造——断片が運べる情報の上限）
- AGENTS.md（作業規範——Phase 0＝設計のみ・日本語・面白さの最終決定権＝ユーザー）
担当ユニットに割り当てられた正典ファイル群は別途指定する——指定されたものは全て実際に開いて読むこと。
"""

RULES = """成果物の組版（docs/64 §5 を厳守）：
- 担当ユニットの必須節を全て埋める。節構成を勝手に変えない
- **実文を書くこと**——「〜という内容の文」という説明は成果物ではない。全ての断片に日本語の実文を書く
- 断片は実文ID（TX-接頭辞・docs/64 §5 規則）で管理し、docs/34 §8 の断片表の行番号と対応付ける
- 行の形：｜TX-ID｜断片（34 §8 行番号）｜ベクター｜書き手/字癖系統｜実文（日本語・頁区切りは【頁1】）｜表示時間検算｜備考｜
- 確定済みの字面（G-LF-14）・口癖（G-LF-13）・命名規則は改変禁止——一字一句そのまま引用する
- 文体規範（G-LF-01/02）に合わない文は自分で書き直してから出す
- 「要承認」は open_questions に集約し、本文側では参照IDを括弧書きで示す
- Phase 0 制約：実装成果物（lang ファイル等）は作らない
"""

CONSTRAINTS = """絶対条件（docs/64 §2 の G-LF-01〜26）：
- G-LF-01/02：文体規範 Do/Don't・形式別声色（絵本/書簡/戯曲/日誌/詩/設計書）の厳守
- G-LF-03：全テキストに書き手が透ける（誰が・何のために・書いた）——無署名の説明文禁止
- G-LF-05：前任の落書きは「その場所での彼の状態」のみ——他章の事件・地名・時系列を書かない。各章1〜2箇所は誤答
- G-LF-06：手書き三系統（案内人筆/先達筆/王筆）を字癖の書き方指針として区別
- G-LF-07：招待状＝匿名・口癖は文末の癖と呼びかけの型のみ・断定的署名禁止
- G-LF-08：幻想文字解読文＝「没になった世界設計・世界案の断片」のみ。動機・正体の言明禁止
- G-LF-09：環境文字は「状態と数量」のみ——固有名詞・動機を書かない
- G-LF-11：1頁あたり概算73字以内（表示時間10秒上限の運用）
- G-LF-14：確定文（王の二つの問い・前任の確定一文・ノミ初挨拶）は一字一句変更不可
- G-LF-16：20%ルール——書きすぎない。明答度超過の文は削る
- G-LF-24：順不同耐性——他章の結末・未訪問章の固有情報を断片に含めない
"""

UNITS = [
    {
        "id": "prologue_village",
        "title": "U1：序章・漂着浜＋村・通年（docs/52 §2・§9）",
        "scope": "docs/52 §2（序章——書物断片6篇・前任の実用落書き5箇所・招待状の実文・ノミの導入語り）＋§9（村・通年——村報の定型と各号見出し・群像セリフ（拾い子・番人・住人一般）・誤配便・「◯◯に捨てられた」記録定型・拾い人の手記の綴じ文・「あなたが捨てたもの」節の記録文）。招待状は docs/23 §5.0・docs/26 §3.6 の仕様どおり「デカいゴミ箱のレシピ＋匿名の手紙」。誤配・村報・捨て記録は G-LF-17/18/19 の文体で",
        "docs": "担当正典：docs/34_chapter_plots/00_prologue.md（§8 断片表）・docs/23 §5.0/§7/§8.5・docs/26 §3.5/§3.6/§3.7・docs/16 §6（村の施設）・docs/40 §2（スライス範囲＝序章/1章/村の優先度）",
    },
    {
        "id": "ch1_ch2",
        "title": "U2：第1章 月の林＋第2章 読まれなかった港（docs/52 §3・§4）",
        "scope": "docs/52 §3（第1章——絵本の頁群〔翁の物語・頁を繍るほど歪みが滲む・隠された最終頁の草稿群〕・翁の立て札・前任の落書き・翁と林の獣のセリフ・拾得物フレーバー）＋§4（第2章——届かなかった手紙の束の実文群・灯台守のかすれた日誌断片・宛名書き殴りの壁の字・読む者の返信定型文・誤配便・「生涯でたった一度書いた手紙」の扱い〔ボス戦開示断片——内容の直接開示はしない形で書くか要承認〕）",
        "docs": "担当正典：docs/34_chapter_plots/01_moon_forest.md・02_unread_harbor.md（§8 断片表）・docs/25 §2.1/§2.2（翁・灯台守）・docs/36（F-ORIGIN-02/03・U2-Q5②）・docs/26 §4.2（絵本・書簡の声色）",
    },
    {
        "id": "ch3_ch4",
        "title": "U3：第3章 踊らなかった広場＋第4章 選ばれなかった坑道（docs/52 §5・§6）",
        "scope": "docs/52 §5（第3章——台本『第二幕・みんなの輪』等の演目断片・屋台の品書き・祭囃子のセリフ・『招待状の束』〔本物と文体で区別可能な模造——U2-Q6〕・前任落書き）＋§6（第4章——鍛冶師日誌篇1〜6〔実務的→日付消失→反復→走り書きの崩壊勾配〕・隔離区画の警告書き・前任落書き最密地帯〔確定一文「おれは帰れなかった。でも、物は届いていた」は変更不可〕・幻想文字気づき走り書き・鍛冶師セリフ）",
        "docs": "担当正典：docs/34_chapter_plots/03_unheld_square.md・04_unchosen_mine.md（§8 断片表・34/04 §8 の誤答配分）・docs/25 §2.3/§2.4（祭囃子・鍛冶師）・docs/36（U1-新4・U4-Q2・U2-Q6）・docs/26 §4.2（戯曲・日誌の声色）",
    },
    {
        "id": "ch5_final",
        "title": "U4：第5章 歌えなかった塔＋終章 原案の座（docs/52 §7・§8）",
        "scope": "docs/52 §7（第5章——詩の断片①〜④〔行の断ち・反復・余白〕・歌姫の歌詞断片〔彼女は歌詞で語る〕・鐘楼の刻印〔幻想文字解読文＝没案断片〕・前任落書き・後書き訂正〔鐘撞きの径〕）＋§8（終章——没企画書・「案：」の頁群〔設計書声色〕・玉座の間の王の語り全文〔二つの確定問いを含む〕・書庫の各項〔案内人の項・来訪者の項等〕・読む者の最後の手紙〔K10〕・最深部の書き入れ3〜5箇所〔系統不明・意図的未回収〕）",
        "docs": "担当正典：docs/34_chapter_plots/05_unsung_tower.md・06_final_seat.md（§5.2・§8 断片表）・docs/25 §2.5/§2.6（歌姫・落慮王）・docs/36（F-ORIGIN-03・U3-B・U2-Q4）・docs/28 §10.6・docs/26 §4.2（詩・設計書の声色）",
    },
    {
        "id": "crosscutting",
        "title": "U5：横断定型文（docs/52 §10）",
        "scope": "docs/52 §10（横断——フレーバーテキスト一覧〔docs/38/01 全アイテムの個別記憶対象に1〜2行〕・結末の記録定型文〔ノミ綴じの史記調・全章×結末分岐〕・名付け候補名の定型セット〔没素材系統別3〜5候補＋「自分で書く」〕・ノミの状況反応リスト〔拾う/捨てる/迷う/名付ける/没腐接近等のトリガー別〕・拾得図鑑の記録文）",
        "docs": "担当正典：docs/38_numeric_tables/01_items.md（全アイテム表）・docs/38/04（結末・経済）・docs/63 §4.6（名付け候補）・docs/26 §3.2/§3.5/§3.7・docs/22（選択の記憶）",
    },
]

META = {
    "name": "lore-fragments",
    "description": "ロア断片・実文集 docs/52（Issue #10）——断片台帳化→5ユニット制作→深い思考レビュー反復→横断監査",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "extract", "detail": "全断片の棚卸し（TX-ID 化台帳）", "count": 1},
        {"title": "write", "detail": "5ユニットの実文執筆", "count": 5},
        {"title": "review", "detail": "文体・正典適合の深い思考レビュー", "count": 10},
        {"title": "revise", "detail": "指摘の改訂", "count": 5},
        {"title": "crosscheck", "detail": "文体適合・正典整合・網羅性の横断監査", "count": 3},
    ],
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "section_md": {"type": "string", "description": "担当ユニットの節全文（Markdown——実文表）"},
        "open_questions": {"type": "string", "description": "未決・要承認事項（ID＝52-U{n}-Q{m}・推奨案・書き戻し先つき）"},
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
        "inventory_md": {"type": "string", "description": "全断片の棚卸し台帳（Markdown——TX-ID・断片・ベクター・配置・運ぶ情報）"},
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
    return f"""あなたは Minecraft MOD「The Understory」の断片台帳の編集者。リポジトリ内の全設計書から、**実文集 docs/52（Issue #10）が実文を供給すべき全断片**を棚卸しせよ。

{MUST_READ}

## 抽出対象
1. **docs/34_chapter_plots/ 各章 §8 の断片表の全行**（00〜06——断片名・ベクター・配置場所・運ぶ情報をそのまま収録）
2. **docs/26 §5 配分表の各ベクター**——章別の書物/フレーバー/セリフ/落書き/ノミ/手紙の配分に対応する断片
3. **「実文は Issue #10 へ委譲」の手渡し全件**（docs/36・40・48・63 等に散在——委譲元の記述を拾い、断片として起票）
4. **各断片への TX-ID 採番**（docs/64 §5 規則：`TX-{{章番号}}-{{種別}}{{連番}}`——例 TX-00-F01・TX-02-LET-03・TX-VIL-NP05・TX-END-WR01）

## 出力
inventory_md に Markdown テーブルで：「TX-ID｜断片名｜ベクター（書物/落書き/セリフ/フレーバー/ノミ語り/手紙/村報/解読文/記録文）｜配置（docs/34 §8 行番号または委譲元節）｜運ぶ情報・役割｜文体形式（絵本/書簡/戯曲/日誌/詩/設計書/定型）｜出典節」。解釈・新規創作はしない——実在する指定を忠実に集めること。断片数の集計を末尾に付ける。"""


def author_prompt(unit, inventory):
    return f"""あなたは Minecraft MOD「The Understory」の実文ライター。{unit['title']} を、調査基準（docs/64）と文体規範（docs/26）に基づき深い思考で執筆せよ。**仕様を説明するのでなく、ゲームに実際に表示される日本語の文を書く**。

{MUST_READ}

## 担当範囲
{unit['scope']}

## 読むべき正典
{unit['docs']}

## 断片台帳（TX-ID 採番済み——担当分を全て回収せよ。配置・運ぶ情報は台帳の指定どおり）
```markdown
{inventory}
```

{RULES}
{CONSTRAINTS}

## 執筆の作法
- まず docs/64 §3 の原則 P-LF-01〜10（二重運搬・言わないことを言う・口癖の意味変化・温度差の笑い・問いを投げる・具体的で小さい・書き手が透ける・プレイヤーに向くのはノミと返信のみ）に載せてから、断片ごとに具体化する
- 各断片に実文を書く——書物は頁区切り（【頁1】…）で1頁概算73字以内（G-LF-11）
- 口癖・確定文は一字一句正確に（G-LF-13/14）
- 「面白さ」は docs/26 §9 の構造で判断——二重運搬・言い淀み・問いを投げる文を狙う
- 分からない・正典と衝突する点は open_questions へ `52-U{{n}}-Q{{m}}` で起票（推奨案＋書き戻し先必須）

## 出力形式（section_md）
docs/64 §5 の担当節構成をすべて埋めた Markdown 全文＋open_questions"""


def review_prompt(unit, section_md):
    return f"""あなたは Minecraft MOD「The Understory」の実文レビューア。以下の実文集を、docs/64 の基準と docs/26 の文体規範に照らして厳しくレビューせよ（深い思考——正典の該当節と docs/64・docs/26 の該当節を実際に開いて突き合わせること。記憶で判定しない）。

{MUST_READ}

## 対象
{unit['title']}
（担当正典：{unit['docs']}）

## レビュー観点（3段分類）
1. **文体適合**：docs/26 §4.1 Do/Don't——説明し切っていないか・感情語の直説がないか・過去/未完の形か・具体的な名で書かれているか（1行ずつ突合）
2. **形式別声色**：docs/26 §4.2——絵本は素朴で歪みが滲むか・書簡は宛名敬語か・戯曲は台詞ト書きか・日誌は乱れの勾配か・詩は断ち反復か・設計書は箇条書きか
3. **書き手の識別**：字癖系統（案内人/先達/王）・口癖の滲み閾値（招待状は文末の癖のみ）——「誰が書いたか分かる」形か
4. **正典整合**：各断片の「運ぶ情報」が docs/34 §8・台帳の指定どおりか・他章の未訪問情報を含んでいないか（順不同耐性）
5. **禁止事項**：確定文の改変（G-LF-14）・環境文字への固有名詞（G-LF-09）・幻想文字文の動機言明（G-LF-08）・明答度超過（20%ルール G-LF-16）
6. **分量**：1頁73字の目安・朗読に耐える長さか
7. **網羅性**：担当範囲の断片（台帳の担当 TX-ID）が全て実文を持つか

## レビュー対象
```markdown
{section_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（severity は blocker/major/minor、issue に問題、suggestion に修正案——指摘には実文の行または TX-ID を明記）。指摘がなければ空配列。"""


def revise_prompt(unit, section_md, findings, retry_note=""):
    return f"""あなたは Minecraft MOD「The Understory」の実文ライター。以下の実文集をレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。棄却する指摘には理由を明記（open_questions に記す）。{retry_note}

{MUST_READ}

## 対象：{unit['title']}

{CONSTRAINTS}
{RULES}

## 現行実文集
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
        "style": "文体適合の横断監査——全ユニットを通じて docs/26 §4.1 Do/Don't と §4.2 形式別声色が一貫して守られているか、同一書き手の字癖（先達筆の乱れ方・案内人筆の口癖滲み）が章を跨いで統一されているか、「あんた/あなた」に向く文がノミと返信以外に漏れていないか",
        "canon": "正典整合——確定文（王の二つの問い・前任の確定一文・ノミ初挨拶）が一字一句一致しているか、用語が docs/44 の正本と一致しているか（没腐・拾得・淀み等）、順不同耐性（他章の結末・未訪問情報を断片が含まないか）、環境文字に固有名詞が混ざっていないか",
        "coverage": "網羅性——断片台帳の全 TX-ID がいずれかのユニットで実文を持っているか、docs/64 §4 の H-01〜27 の各種が回収されているか、docs/34 §8 の断片行との対応が揃っているか",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**実文集の5ユニット全て**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ（深い思考——正典（docs/26・25・34・36・44）と docs/64 を実際に開いて突き合わせること）。

{MUST_READ}

## 参照：断片台帳
```markdown
{inventory}
```

## 全ユニット実文集
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
    log("=== Phase 1: 断片の棚卸し（TX-ID 台帳化） ===")
    inv = await agent_retry(
        extract_prompt(),
        phase="extract", label="extract-inventory",
        schema=EXTRACT_SCHEMA, repos=[REPO], soft_time_limit_minutes=50,
    )
    inventory = inv["inventory_md"]
    log(f"棚卸し完了（{len(inventory)} 文字）")

    log("=== Phase 2: 5ユニットの制作・レビュー・改訂ループ ===")
    results = []
    for batch in (UNITS[:2], UNITS[2:4], UNITS[4:]):
        results.extend(await pipeline(batch, lambda u: unit_flow(u, inventory)))
    log("=== 5ユニット完了。横断監査へ ===")

    all_sections_text = "\n\n---\n\n".join(
        f"## {r['title']}\n\n{r['section_md']}" for r in results
    )
    log(f"全セクション合計 {len(all_sections_text)} 文字")

    style_check, canon_check, cov_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "style", inventory), phase="crosscheck", label="cc-style", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "canon", inventory), phase="crosscheck", label="cc-canon", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_sections_text, "coverage", inventory), phase="crosscheck", label="cc-coverage", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    for name, chk in (("style", style_check), ("canon", canon_check), ("coverage", cov_check)):
        log(f"横断監査（{name}）: accepted={chk['accepted']} findings={len(chk['findings'])}")

    output = {
        "inventory": inventory,
        "units": results,
        "crosscheck": {"style": style_check, "canon": canon_check, "coverage": cov_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
