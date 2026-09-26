import asyncio
import json

REPO = "hi-lee-mon/the-understory"

# 各章の固定事実（docs/12, 24, 25, 28 の確定内容）
CHAPTERS = [
    {
        "id": "00_prologue",
        "title": "序「漂着浜」",
        "narrative_form": "環境語り（語り形式なし——打ち上げられた物自体が語る）",
        "emotion": "不気味さ→好奇心",
        "boss": "なし（導入章。没腐した漂着物との小遭遇のみ）",
        "master": "なし（ノミとの出会いが主体）",
        "role": "世界の法則の体験学習：自分の捨て物との対面、捨て場の発見、帰還の仕組み",
        "chapter_facts": "プレイヤーは招待状（デカいゴミ箱のレシピ＋匿名の手紙）を得て自分で箱に入って転移。漂着浜に打ち上げられる。自分が捨ててきた物が風景になっている。光る頁めいた小さな精霊ノミと出会う（「来たか。待っていた」）。自分の捨て場を見つけ、そこから現実へ帰還できることを学ぶ。拾い人の村の場所の示唆。",
    },
    {
        "id": "01_moon_forest",
        "title": "第1章「満ちなかった月の林」",
        "narrative_form": "絵本（ページを繍うように読み進められる）",
        "emotion": "温かい奇妙さ→静かな哀愁",
        "boss": "月欠狼（月齢で弱点・攻撃が変化、満月の瞬間が大ダメージ窓）",
        "master": "月見翁（「満月の夜に実を摘む」物語の主人公。月が満ちないまま没になり永遠に待つ者。ボス＝翁の待ち続けた心が獣になった姿）",
        "role": "プレイヤーへの「待ち続けた者」の原型提示・没腐の教師・拾得鍛錬の導入",
        "chapter_facts": "常夜の森。欠けた月が止まっている。同じ手紙「もうすぐですよ」が何百通もある。翁の小屋。救出後は村の農園担当に。結末選択：月を満ちさせる（予定通りの結末）／新月を受け入れる（別の実りを祝う）。第1章で拾得の携行品の原型が手に入る想定。",
    },
    {
        "id": "02_unread_harbor",
        "title": "第2章「読まれなかった港」",
        "narrative_form": "書簡（宛名・敬語・届かない想い）",
        "emotion": "切なさの頂点",
        "boss": "未読の座礁船（届くはずだった言葉の重みが攻撃になる）",
        "master": "灯台守（「必ず届く」手紙を守り続けたが誰も読まず、手紙の山に呑まれて没腐）",
        "role": "「読まれる側」の物語。救出後＝「読む者」に変わり、ゴミ箱返信機構に顔がつく（機構×物語の接続点）",
        "chapter_facts": "届かなかった手紙が霧になって港を閉ざしている。灯台。救出後、灯台守は村の手紙屋になり返信が届くようになる。プレイヤーの手紙が初めて「読まれた」体験。",
    },
    {
        "id": "03_unheld_square",
        "title": "第3章「踊らなかった広場」",
        "narrative_form": "戯曲（賑やかな台詞・ト書き・役割名）",
        "emotion": "滑稽・歓楽→不意の喪失（笑いの後の静けさ）",
        "boss": "中止の人形劇（滑稽な振付で踊る人形の列——倒すほど「誰も観ていなかった」が滲む）",
        "master": "祭囃子（「みんなが踊る日」を指揮するはずだったが踊る相手がいないまま没腐）",
        "role": "感情の振れ幅担当（哀愁一辺倒を崩す）。救出後＝村に祭り場・イベント",
        "chapter_facts": "中止になった祭りの広場。飾りはあるが誰もいない。救出後は村の祭り場で時折イベント。",
    },
    {
        "id": "04_unchosen_mine",
        "title": "第4章「選ばれなかった坑道」",
        "narrative_form": "日誌（実務的・日付・次第に乱れる筆致）",
        "emotion": "恐怖→勇気（ホラー寄りの章）",
        "boss": "棄材のゴーレム（没素材の巨体。剥がれた部位を拾って使う戦闘）",
        "master": "鍛冶師（「世界一の道具を作る」はずだったが素材が全て没になり何も作れないまま没腐）",
        "role": "拾得鍛錬の深化・灼熱の埋立て地（ごみ処理場の届き先）への橋・前任の拾い人の落書きが濃くなる転調点",
        "chapter_facts": "没になった鉱石・道具の坑道。使われなかった道具・恐れられて棄てられた物が恨みを持って蠢く。日誌の筆致が深部で乱れる。救出後＝村の拾得鍛錬の名人・灼熱の埋立て地を知っている。前任の拾い人の落書き「おれは帰れなかった。でも、物は届いていた」。この章から落慮王の存在が断片で見え始める。",
    },
    {
        "id": "05_unsung_tower",
        "title": "第5章「歌えなかった塔」",
        "narrative_form": "詩（行の断ち・反復・余白）",
        "emotion": "畏怖・荘厳",
        "boss": "無音の歌姫（音のない領域で戦う。鐘・楽器で音を取り戻すギミック）",
        "master": "歌姫（「鐘を鳴らして国を呼び覚ます」物語だったが鐘は鳴らず無音の中で没腐）",
        "role": "国の目覚め（音を取り戻す）＝終章への導線役",
        "chapter_facts": "無音の塔。救出後、村に歌と鐘が戻る＝国が音を取り戻し始める。歌姫は「鐘が鳴るとき、原案の座が開く」と告げる。",
    },
    {
        "id": "06_final_seat",
        "title": "終章「原案の座」",
        "narrative_form": "設計書（箇条書き・仕様書語・「案：」）",
        "emotion": "畏怖→選択の重さ→カタルシス",
        "boss": "落慮王（対峙——戦うかは選択次第）",
        "master": "落慮王＝世界の最初の原案の人格化、ノミ＝その原案の案内人、前任の拾い人の結末",
        "role": "全伏線の収束。ノミと落慮王の再会（最大の感情点）。3結末（書き換える/見届ける/拾う）",
        "chapter_facts": "国の最深部。世界の最初の設計図（原案）が残る場所。落慮王の問い「選ばれなかったものに価値はなかったのか」。前任の拾い人の最後の記録（拾うに辿り着けなかった者）。ノミの正体開示と再会。名付けの結末分岐。ポストクレジット＝村に救われた者たち・読む者が手紙を書く・祭囃子が準備。「まだ拾われていない物語がある」示唆。",
    },
]

TEMPLATE = """各章の詳細プロットは以下の構造で書くこと（docs/33 §7 テンプレート）：
1. 章の目的（担う感情・物語機能・配信反応）
2. 到着〜導入（環礁への着き方、最初に見えるもの、ノミの反応）
3. 探索の流れ（場所の系列：クリティカルパスを場所単位で列挙、各所で何を見つけ・何を学ぶか）
4. ミッドポイント（認識が覆る転換点——知っているつもりだったことが変わる）
5. ボス設計（没腐した正体・ギミック・倒し方・teach-test-twist）
6. 結末選択（両方が「最善の悪い選択」になる選択肢）
7. 救出後（主の行き先・村への変化・次への引き）
8. ロア断片の配置（拾える断片の個数・場所・各断片が運ぶ情報）
9. 伏線の受け渡し（この章が撒く伏線・回収する伏線——どの順で読まれても成立する形）
10. 配信の切り抜き瞬間（クリップになる場面）
"""

CONSTRAINTS = """絶対条件（反するとレビューで弾かれる）：
- ボスは「倒す敵」でなく「待ち続けた者の没腐した姿」——撃破＝理解して救う
- 第2〜4章は順不同：他章の攻略を前提にしない。伏線はどの順で読まれても成立する断片に
- 「感動は狙い撃ちしない」：主軸は推理（なぜ未完か・誰の物か）と人物の魅力
- 文体規範：かすれた・欠けた・継がれた（docs/26 §4）
- 層構造：表層＝非言語で分かる／深読み層＝断片収集で見える。両方が独立に成立
- 用語は正典どおり：拾い人/ノミ/拾得物/没腐/縁の地/漂着浜/落慮王/異物/捨て場/読む者/原案の座 等
- 世界観を壊す行為・機構を追加しない（入口はゴミ箱/異物のみ・ADR-0005）
- セリフは書かない——配置と役割のみ（セリフ自体は Issue #10 範囲外）
"""

MUST_READ = """まず以下を全て読め（リポジトリ内）：
- docs/11_world_bible.md（世界法則）
- docs/12_story_outline.md（章概要・感情マップ）
- docs/23_discard_grammar.md（ゴミ箱文法・往復仕様）
- docs/24_story_foundation.md（真実の構造・伏線工学）
- docs/25_characters.md（登場人物）
- docs/26_narrative_vectors.md（語りベクター・文体規範）
- docs/28_story_full_flow.md（全編ストーリー詳細——正典）
- docs/32_system_specs.md（システム仕様）
- docs/33_research_narrative_craft.md（このプロットで従う物語構造の基準）
- docs/50_opening_storyboard.md（オープニング）
- AGENTS.md（作業規範）
"""

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


META = {
    "name": "chapter-plot-forge",
    "description": "各章の詳細プロットを制作→レビュー→修正（指摘が尽きるまで反復）",
    "product": "The Understory（棄てられたものの国）",
    "phases": [
        {"title": "write", "detail": "各章の詳細プロット執筆", "count": 7},
        {"title": "review", "detail": "正典整合・物語構造基準でのレビュー", "count": 14},
        {"title": "revise", "detail": "指摘の修正", "count": 7},
        {"title": "crosscheck", "detail": "全章を通した横断整合レビュー", "count": 2},
    ],
}

PLOT_SCHEMA = {
    "type": "object",
    "properties": {
        "plot_md": {"type": "string", "description": "章の詳細プロット全文（Markdown）"},
        "open_questions": {"type": "string", "description": "プロット上の未決・要承認事項"},
    },
    "required": ["plot_md"],
}

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "accepted": {"type": "boolean", "description": "ブロッカー/メジャー指摘がなければtrue"},
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


def author_prompt(ch):
    return f"""あなたは Minecraft MOD「The Understory（棄てられたものの国）」の物語作家。以下の章の**詳細プロット**を、プロの物語構造技法に基づき深い思考で執筆せよ。

{MUST_READ}

## 対象章
- 章：{ch['title']}
- 語り形式：{ch['narrative_form']}
- 主感情：{ch['emotion']}
- ボス：{ch['boss']}
- 主（救出対象）：{ch['master']}
- 章の役割：{ch['role']}
- 確定済みの事実：{ch['chapter_facts']}

{TEMPLATE}

{CONSTRAINTS}

出力：plot_md に章の詳細プロット全文（テンプレート10節すべてを埋めた Markdown）、open_questions に残った未決・要承認事項。
"""


def review_prompt(ch, plot_md):
    return f"""あなたは Minecraft MOD「The Understory」の物語レビューア。以下の章プロットを、正典ドキュメントと物語構造基準に照らして厳しくレビューせよ。

{MUST_READ}

## 対象章
{ch['title']}（語り形式：{ch['narrative_form']}／主感情：{ch['emotion']}）

## レビュー観点（すべて確認）
1. **正典との整合**：docs/24 の真実構造・docs/28 の流れ・docs/11 の世界法則・用語に矛盾しないか
2. **構造基準**：docs/33 のテンプレート10節が全て埋まっているか、ミッドポイントはあるか、シーン-シークエルの連鎖になっているか
3. **順不同制約**：第2〜4章は他章攻略を前提にしていないか（独立して読めるか）
4. **ボス原則**：ボスが「主の没腐した姿」として機能し「理解して救う」になっているか
5. **選択の重み**：結末選択が「最善の悪い選択」になっているか（安易な正解がないか）
6. **伏線の受け渡し**：撒く伏線・回収する伏線がどの順でも成立するか、終章への供給になっているか
7. **層構造**：表層（非言語）と深読み層が両方成立しているか
8. **面白さ**：推理の余地・人物の魅力・配信切り抜き瞬間があるか
9. **文体規範**：かすれた・欠けた・継がれたに反しないか
10. **具体的な抜け**：ロア断片の個数・配置が書かれているか、次への引きがあるか

## レビュー対象のプロット
```markdown
{plot_md}
```

出力：accepted（blocker/major の指摘がなければ true）、findings（指摘の配列。severity は blocker/major/minor、issue に問題、suggestion に修正案）。指摘がなければ findings は空配列、accepted は true。"""


def revise_prompt(ch, plot_md, findings):
    return f"""あなたは Minecraft MOD「The Understory」の物語作家。以下の章プロットをレビュー指摘に基づき改訂せよ。全体を書き直すのではなく、指摘箇所を正確に修正した完成版を出力せよ。

{MUST_READ}

## 対象章：{ch['title']}

{CONSTRAINTS}

## 現行プロット
```markdown
{plot_md}
```

## レビュー指摘
```json
{json.dumps(findings, ensure_ascii=False)}
```

出力：改訂後の plot_md 全文（テンプレート10節を全て保持）、open_questions。"""


def crosscheck_prompt(all_plots_text, focus):
    focus_desc = {
        "story": "物語・伏線の整合（各章の伏線の受け渡しが閉じているか、前任の拾い人・落慮王・ノミの情報開示のペースが崩れていないか、用語・人物の一貫性、終章への収束）",
        "system": "システム・進行の整合（順不同制約の遵守、ボスギミックと拾得物の整合、村の発展要素の重複・欠落、docs/32 の仕様との齟齬、章間の難度・情報量のバランス）",
    }[focus]
    return f"""あなたは Minecraft MOD「The Understory」の全体整合レビューア。以下に**7章すべての詳細プロット**を示す。これらを横断して、{focus_desc} の観点だけを厳しくレビューせよ。

{MUST_READ}

## 全章プロット
{all_plots_text}

出力：accepted、findings（章横断の問題のみ——単一章内の問題は各章レビューの責任なので挙げない）。"""


async def chapter_flow(ch):
    """1章を author→review→revise で指摘が尽きるまで回す"""
    draft = await agent_retry(
        author_prompt(ch),
        phase="write",
        label=f"write-{ch['id']}",
        schema=PLOT_SCHEMA,
        repos=[REPO],
        soft_time_limit_minutes=55,
    )
    plot_md = draft["plot_md"]
    open_qs = draft.get("open_questions", "")
    rounds = 0
    previous_findings = None
    for r in range(3):
        review = await agent_retry(
            review_prompt(ch, plot_md),
            phase="review",
            label=f"review-{ch['id']}-r{r+1}",
            schema=REVIEW_SCHEMA,
                repos=[REPO],
            soft_time_limit_minutes=40,
        )
        rounds = r + 1
        blocking = [f for f in review["findings"] if f.get("severity") in ("blocker", "major")]
        if review["accepted"] and not blocking:
            log(f"{ch['id']}: ラウンド{r+1}で受理（minor {len([f for f in review['findings'] if f.get('severity')=='minor'])}件のみ）")
            return {"chapter": ch["id"], "title": ch["title"], "plot_md": plot_md, "open_questions": open_qs, "rounds": rounds}
        findings_key = json.dumps(sorted(review["findings"], key=lambda f: f.get("issue", "")), ensure_ascii=False)
        if findings_key == previous_findings:
            log(f"{ch['id']}: 同一指摘の繰り返し——受理して人間レビューへ")
            return {"chapter": ch["id"], "title": ch["title"], "plot_md": plot_md, "open_questions": open_qs + "\n[レビュー未解決の指摘あり]", "rounds": rounds}
        previous_findings = findings_key
        log(f"{ch['id']}: ラウンド{r+1}で指摘{len(blocking)}件——改訂へ")
        draft2 = await agent_retry(
            revise_prompt(ch, plot_md, review["findings"]),
            phase="revise",
            label=f"revise-{ch['id']}-r{r+1}",
            schema=PLOT_SCHEMA,
                repos=[REPO],
            soft_time_limit_minutes=45,
        )
        plot_md = draft2["plot_md"]
        open_qs = draft2.get("open_questions", open_qs)
    log(f"{ch['id']}: レビュー3ラウンド消化——最終版を採用")
    return {"chapter": ch["id"], "title": ch["title"], "plot_md": plot_md, "open_questions": open_qs + "\n[レビュー3ラウンド後も残存指摘あり]", "rounds": 3}


async def main():
    await register_workflow(META)
    log("=== Phase 1-3: 7章のプロット制作・レビュー・改訂ループ ===")
    # SWE-2無料枠=最大8セッション（自セッション含む）のため4+3に分割
    results = []
    for batch in (CHAPTERS[:4], CHAPTERS[4:]):
        results.extend(await pipeline(batch, chapter_flow))
    log(f"=== 7章完了。横断レビューへ ===")

    all_plots_text = "\n\n---\n\n".join(
        f"## {r['title']}\n\n{r['plot_md']}" for r in results
    )
    log(f"全プロット合計 {len(all_plots_text)} 文字")

    story_check, system_check = await parallel([
        lambda: agent_retry(crosscheck_prompt(all_plots_text, "story"), phase="crosscheck", label="crosscheck-story", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
        lambda: agent_retry(crosscheck_prompt(all_plots_text, "system"), phase="crosscheck", label="crosscheck-system", schema=REVIEW_SCHEMA, repos=[REPO], soft_time_limit_minutes=60),
    ])
    log(f"横断レビュー（物語）: accepted={story_check['accepted']} findings={len(story_check['findings'])}")
    log(f"横断レビュー（システム）: accepted={system_check['accepted']} findings={len(system_check['findings'])}")

    output = {
        "chapters": results,
        "crosscheck": {"story": story_check, "system": system_check},
    }
    log(f"=== 完了 ===\n{json.dumps(output, ensure_ascii=False)}")


asyncio.run(main())
