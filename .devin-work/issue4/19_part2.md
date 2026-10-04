
---

## 3. SE 全登録表（登録台帳の正本）

本節は独自 SoundEvent の**唯一の登録台帳**である。章別表（§4）・素材表（§7）の SE は全て本節の行への参照として扱い、本節と別名・別諸元で二重登録しない。

**列定義**：登録ID（SoundEvent ID＝正本）｜字幕名（§3.6 台帳の正典名——「新規」印は台帳未収録の新規登録）｜カテゴリ（§2.2）｜stream（§2.1.2）｜定位（mono/stereo＝§2.3）｜層（世界/器/楽曲——§1.1）｜トリガー（発火条件）｜音色要件（収録・合成の要件）｜共有/個別｜素材ID（§7 突合）｜根拠

### 3.0 登録規格

- **1 イベント＝1 ID・1 字幕名・1 諸元**。同一音の別 ID 並立は禁止（§4 章表・§7 素材表は全て本節 ID への参照）
- **無音を演出とする局面（音がないこと自体が正体・無音の頁・響界外の世界音）では SE・字幕とも発火しない**——SE 行を持たない（§1.2.1）。例外は「無音への遷移」の一拍のみ（`event.silence.dome`）
- **疑似ループ規格**（19-U2-Q1 推奨として統一——§2.1.2）：ループ・周期音は stream:false の短〜中尺素材の間隔再発火。ジッタ ±0.2〜0.4s で機械的周期性を殺す
- **VOICE 不使用＝19-U1-Q1 係留**——歌姫声部・ノミ語りの行はカテゴリ欄に「VOICE 保留」を記し、決裁まで実登録しない（不採用なら各行の代替カテゴリは欄内に併記）
- **層列**：05 環礁の消音・響界フィルタを行単位で適用するための必須列（§1.1.1 機構）
- **字幕名**：§3.6 の台帳が権威。本表の名は全て台帳名と一致する（新規は印つき）

### 3.1 器・UI・器機 SE

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ui.page.turn` | 頁：めくれる | UI | false | stereo | 器 | 書物器の頁めくり | 乾いた紙擦れ ≦0.30s/頁・連続 0.18s 追従・打切り可 | 個別 | SE-PAGE-01 | 18 §1.5.1・§2.6 |
| `understory.ui.page.open` | 頁：開く | UI | false | stereo | 器 | 書物器を開く | 綴じ目の軋み＋革表紙擦れ ≈0.4s | 個別 | SE-PAGE-02 | 18 §1.5.1 |
| `understory.ui.page.close` | 頁：閉じる | UI | false | stereo | 器 | 書物器を閉じる | 綴じ紐を締める一連 ≈0.4s | 個別 | SE-PAGE-03 | 18 §1.5.1・18-U3-Q8 台帳 |
| `understory.ui.page.bind` | 頁：綴じる | UI | false | stereo | 器 | 新頁綴じ込み完了（拾得物項・結末記録・予告頁・村報・再演頁）＋暗転ツナギの持続再発火（1.5〜2.5s 間隔・volume 0.4） | 綴じ音——糸を通して締める 0.8〜1.2s | 内容で両層（個人綴じ＝個別・進行通知＝共有） | SE-PAGE-04 | 18 §1.5.1・§2.5.1・§3.1・48/01 I-3 |
| `understory.ui.paper.rustle` | 紙：擦れる | UI | false | stereo | 器 | 手記・断片・書き込みの紙面操作 | 乾いた低音擦れ ≈0.3s | 個別 | SE-PAGE-05 | 18 §5.6・§1.5.1 |
| `understory.ui.seal.break` | 封：切れる | UI | false | stereo | 器 | 封じられた手紙・招待状の開封 | 蝋・糊の剥がれ ≈0.4s | 個別 | SE-PAGE-06 | 18 §1.5.2・34/02 §3 |
| `understory.ui.scroll.rewind` | 巻：戻る | UI | false | stereo | 器 | 書き込み・命名・綴じ操作の取消・幕巻き戻し演出 | 短い逆行擦り ≈0.5s | 個別 | SE-PAGE-07 | 18 §1.5.1・§4.0 共通仕様 |
| `understory.ui.naming.write` | 名：記す | PLAYERS | false | mono | 器（世界内器） | 名付けの台・戦闘中 2 秒チャネル命名の書き込み確定（被弾中断可） | 書き込み擦り＋綴じの締め | 個別 | SE-NAM-01 | 38/02 §3.6.4②③・18 §4.2・34/04 §4 |
| `understory.ui.map.open` | 写：開く | UI | false | stereo | 器 | 地図・写頁を開く | 紙の開き＋擦れ ≈0.4s | 個別 | SE-PAGE-08 | 18 §1.5.1 |
| `understory.ui.notify.pickup` | 拾得物：届く | UI | false | stereo | 器 | 拾得物入手の Toast 通知 | 拾得トークン統一音色（かすれた小鐘系）全章同一 | 個別 | SE-TOK-PICK | 18 §2.5.1・14 §3 U1-Q3・G-AU-06 |
| `understory.ui.notify.release` | 鐘：鳴る | UI | false | stereo | 器 | 図鑑頁・要素の解放通知 Toast | かすれた鐘・音量小・残響短め | 個別 | SE-BELL-UI | 18 §2.5.1 解放型・§5.8 |
| `understory.ui.notify.bulletin` | 村報：発行される | UI | false | stereo | 器 | 村報の新号発行通知 | 綴じ音＋紙擦れの連なり ≈0.8s | 共有（各人端末へ） | SE-POST-01 | 18 §2.5.1・§3.6・32 §6 |
| `understory.ui.nomi.narrate` | ノミ：語る | UI（19-U1-Q1 連動） | false | stereo | 器 | 予告頁交付の語り再生 | 「声らしきもの」気配——音節的な短い声の気配で構成（VO 不採用時） | 個別 | SE-NOMI-02 | 18 §3.4・§2.6.3 |
| `understory.world.bin.insert` | 物：落ちる **（新規）** | BLOCKS | false | mono | 世界 | ゴミ箱への投入 | 木軋み＋物が底に落ちる軽い残響 ≈0.5s | 共有 | SE-BIN-01 | 23 §11・18 §5.6 列挙 |
| `understory.world.bin.lid` | 箱：軋む | BLOCKS | false | mono | 世界 | 箱の蓋の開閉（投入口・着弾気づき） | 木軋み＋蓋の微かな動き ≈0.4s | 共有 | SE-BIN-02 | 18 §1.5.2・23 §11 |
| `understory.world.bin.arrive` | ゴミ箱：鳴る | BLOCKS | false | mono | 世界 | 届きものの箱への着弾（返礼・住人便・誤配・最後の手紙含む） | 木箱内に物が落ちる鈍い一音＋小さな紙擦れ ≈0.6s | 個別（自分の箱）／共同箱＝共有（近傍のみ・遠方は Toast——19-U2-Q5） | SE-DLV-01 | 18 §5.8・§2.5.1・23 §7・32 §6 |
| `understory.world.bin.sink` | 物：沈む | PLAYERS | false | stereo | 器（世界内・本人返答） | 投入した物が国へ流れ着く（投入者のみ） | 国へ落ちる音＋下方へ伸びる残響尾 1.0〜1.5s | 個別 | SE-TR-02 | 23 §10/§11 |
| `understory.world.invite.pop` | 招待状：届く | BLOCKS | false | mono | 世界 | 招待状発火（箱を開くと返礼——ポップ音＋朱のレシピカード） | 乾いたポップ音＋かすれ仕上げ ≈0.3s | 個別 | SE-DLV-02 | 45/02 §5.1・32 §3.1 |
| `understory.world.mailboat.creak` | 郵便船：軋む | AMBIENT | false | mono | 世界 | 届きもの便の接近——到着前の気配として 1 回 | 木造小舟のかすれた軋み 1.0〜1.5s・遠方からの擬似減衰 | 共有 | SE-BOAT-01 | 18 §5.6・32 §6 |
| `understory.world.board.post` | 紙：貼る | BLOCKS | false | mono | 世界 | 掲示板への貼付・延期貼り紙のめくり | 紙擦れ＋板への軽い接触 ≈0.3s | 共有 | SE-POST-02 | 16 §3.4・34/03 |
| `understory.world.chime.small` | 小さな鐘：微かに鳴る | PLAYERS | false | mono | 世界 | N-GEAR-4-03 掌サイズの鐘——由来のある物・名のある物への接近で微かに鳴る | かすれた小鐘・単発 ≈0.8s・近づくほど微かに増す | 個別 | SE-BELL-02 | 38/02・14 §3・18 §5.6 |
| `understory.world.instrument.ring` | 楽器：鳴らす | PLAYERS | false | mono | 世界 | 鳴る楽器（N-GEAR-004・復調楽器）の演奏——05 では響界発生源 | 古い楽器のかすれた一音・05 では 10s 上限の連続型（疑似ループ保持） | 共有 | SE-INST-01 | 38/02・38/03 §4.5・34/05 §3.2 |
| `understory.world.reforge.pickup` | 素材：拾い直す | PLAYERS | false | mono | 世界 | 拾得鍛錬台での拾い直し確定 | 綴じ音＋拾得トークン音色の合成 ≈0.8s | 個別 | SE-FRG-01 | 14 §3・15 §3 |
| `understory.world.compass.edge` | 羅針盤：縁を指す **（新規）** | PLAYERS | false | mono | 世界（所持者位置） | 縁の羅針盤が縁の地を指している間・間欠 | 澄んだ小さな共鳴（安全な指し） | 個別 | SE-CMP-01 | 32 §4.2 U1-Q4・14 §3 |
| `understory.world.compass.foreign` | 羅針盤：異物を指す **（新規）** | PLAYERS | false | mono | 同上 | 異物を指している間 | かすれた昔の音残響系の短い一音（MU-MOTIF-OLD 系） | 個別 | SE-CMP-02 | 同上 |
| `understory.world.compass.molder` | 羅針盤：淀みを指す **（新規）** | PLAYERS | false | mono | 同上 | 没腐遺留物・自分の捨て場を指している間（港風セット/没腐度≥5） | 淀んだ低い共鳴 | 個別 | SE-CMP-03 | 同上・38/04 §2.3・18 §5.7 |
| `understory.world.festival_bell.ring` | 鈴：鳴る **（新規）** | PLAYERS | false | mono | 世界 | N-GEAR-3-01 祭りの鈴——世の拍子に合わせて鳴る（章の拍子キューと同期・判定窓＋20%） | 小さな鈴のかすれた一鳴り | 個別 | SE-BELL-03 | 38/02・34/03 §7 |
| `understory.world.seat.resonance` | 座：応える **（新規）** | BLOCKS | false | mono | 世界 | 原案シリーズ装備の所持者が座に近づくほど間隔短縮・微増 | 第三の質感（19-U1-Q4＝泛音・純音系の澄んだ共鳴） | 個別 | SE-RES-01 | 34/06 §3.7・38/02 N-GEAR-6 系 |
| `understory.world.crane.warn` | クレーン：動く **（新規）** | BLOCKS | false | mono | 世界 | クレーン腕の掴み予備動作（逃走余地の告知） | 機械駆動音＋警告の短音（かすれた労働機械質感） | 共有 | SE-CRN-01 | 23 §8.5・§8.3 |
| `understory.world.crane.grab` | クレーン：掴む **（新規）** | BLOCKS | false | mono | 世界 | クレーン腕の掴み動作 | 掴み・締め付けの実音 | 共有 | SE-CRN-02 | 23 §8.3 |
| `understory.world.remnant.hum` | 部位：響く **（新規）** | BLOCKS | false | mono | 世界 | 名の残る部位（04）への接近 | 微かな共鳴——名が残る部位の鳴動 | 個別 | SE-REMN-02 | 34/04・18 §5.10 |
| `understory.world.remnant.warp` | 遺留物：歪む **（新規）** | BLOCKS | false | mono | 世界 | 没腐した死亡遺留物の近傍 | 場所が小さく歪む気配——淀み系の濁り | 個別 | SE-REMN-01 | 32 §2.1 |
| `understory.world.backstage_door.open` | 楽屋の門：開く | BLOCKS | false | mono | 世界 | 03 楽屋の門の開閉 | 重い木門の軋み＋開放 | 共有 | SE-DOOR-01 | 34/03 |
| `understory.mob.nomi.talk` | ノミ：話す | NEUTRAL | false | mono | 世界 | ノミの最小語り（没腐コンパスの指し等） | 声らしき気配（発語でない音節的な短い声の気配——19-U1-Q1 連動） | 個別 | SE-NOMI-01 | 18 §5.1・45/01 §2.2-9 |
| `understory.mob.nomi.write` | 頁：書き込む **（新規）** | NEUTRAL | false | mono | 世界 | 05 以降のノミの字退避（頁への書き込みで導く） | 頁への書き込み音（紙擦れ系） | 個別 | SE-NOMI-03 | G-AU-14・34/05 §2-3 |

### 3.2 イベント・演出 SE

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.event.curtain.fall` | 幕：落ちる | AMBIENT | false | stereo | 世界 | 幕切れ（結末確定→暗転約 10s の環境演出一拍） | 重い布の落ちる音＋残響 ≈2s | 共有 | SE-EVT-01 | 18 §5.6・38/03 §4.3・48/03 §6 |
| `understory.event.bell.final` | 鐘：座に届く | AMBIENT | true | mono | 世界 | 結末の一音——05 最終連・終章特殊幕で鳴る鐘が座へ届く | 大鐘の深い一打ち・残響 6〜8s——**第三領域の澄んだ残響を帯びる特例**（19-U1-Q4 連動） | 共有 | SE-BELL-FINAL | 34/05 §6・38/03 §4.6 |
| `understory.event.bell.sweep` | 鐘：渡る | AMBIENT | true | stereo | 世界 | 救出復帰の鐘が環礁を渡る（≈8s） | 鐘の残響が遠くへ渡る音像 | 共有 | SE-BELL-04 | 34/05・45/02 §7 |
| `understory.event.transit.close` | 蓋：閉まる | BLOCKS | false | mono | 世界 | 転移箱の蓋が閉まる（小幕・転移の一拍目） | 木蓋の閉じる乾いた音 ≈0.5s | 個別 | SE-TR-01a | 50 Beat 2・48/03 §6 |
| `understory.event.transit.break` | 世界：壊れる | AMBIENT | false | stereo | 世界 | 転移暗転中の世界破壊音（ゴミ箱転移・異物欠損接触の片道転移に共通使用） | 逆再生感＋落下感＋残響の尾 2.5〜3.0s | 個別 | SE-TR-01b | 50 Beat 2・11 §4 |
| `understory.event.transit.land` | 水面：着く | BLOCKS | false | mono | 世界 | 転移着地——着弾点の初景音 | 着水・着地の実音＋環境床の立ち上がり ≈1.5s | 個別 | SE-TR-01c | 50 Beat 2 |
| `understory.event.transit.open` | 蓋：開く | BLOCKS | false | mono | 世界 | 転移先の箱の蓋が開く | 木蓋の開く軋み ≈0.5s | 個別 | SE-TR-01d | 50 Beat 2 |
| `understory.event.silt.crack` | 淀み：割れる | BLOCKS | false | mono | 世界 | 淀みの窪地の割れ・消化イベント | 淀んだものが割れる湿った音 | 共有 | SE-YOD-02 | 34/00・45/04 §5.3 |
| `understory.event.rescue.return` | 環礁：鳴る | AMBIENT | false | stereo | 世界 | 救出復帰——環礁の音が戻る一拍 | 環礁固有音の一斉復帰（床＋定位音の立ち上がり） | 共有 | SE-EVT-02 | 34/05・45/02 §7 |
| `understory.event.forge.final` | 打鍵：届く | BLOCKS | false | mono | 世界 | 04 終幕の一打ち——最深部から届く | 遠い打鍵の正体が届く一打ち | 共有 | SE-HAMMER-FIN | 34/04 §5 |
| `understory.event.letter.final` | 手紙：届く | BLOCKS | false | mono | 世界 | 最後の手紙の着弾（K9/K10——現実のプレイヤーのゴミ箱へ） | 着弾音＋紙擦れ（bin.arrive と同族・別登録で結末の特別感を持たせる） | 個別 | SE-DLV-03 | 34/06 §6.3・§7.3・18 §5.8 |
| `understory.event.mechanism.release` | 機構：緩む | AMBIENT | false | mono | 世界 | 03 救出——指揮台の機構が緩む | 歯車・発条の緩む実音 | 共有 | SE-EVT-03 | 34/03 §6 |
| `understory.event.silence.dome` | 音：消える | AMBIENT | false | stereo | 世界 | 06 段 5 沈黙の域への突入の一拍（フェードアウトの可聴化＋字幕——**沈黙中は字幕なし**） | 全音が減衰して消える 1.5〜2.0s の境界イベント | 共有 | SE-EVT-04 | 38/03 §4.6・U3-N7・G-AU-03 例外注記 |
| `understory.event.light.fold` | 灯り：畳まれる | AMBIENT | false | mono | 世界 | 章の灯りの畳み（救出後変化・幕の余韻） | 灯りの光が畳まれる軽い実音——各灯りごとに逐次 | 共有 | SE-EVT-05 | 34/02・45/02 |
| `understory.event.mark.stamp` | 印：打たれる | AMBIENT | false | stereo | 世界 | 06「書き換える」確定の頁への印 | 印を押す乾いた一音 | 共有 | SE-EVT-06 | 34/06 §5 |
| `understory.event.depth.answer` | 底：応える | AMBIENT | false | stereo | 世界 | 座の開放——最深部からの応答 | 第三領域の深い共鳴 | 共有 | SE-EVT-07 | 34/06 §3 |
| `understory.event.phantom.scene` | 幻影：展開する | AMBIENT | false | stereo | 世界 | 06 段 4 幻影の展開（借用章の音の残影を含む） | 過去章の音色の幽かな残影の重なり | 共有 | SE-EVT-08 | 38/03 §4.6 |
| `understory.event.heavy.step` | 足：重い | PLAYERS | false | mono | 世界 | 06「拾う」経路——原案を抱えて歩く重い足音 | 重量のある靴音・微かな頁擦れ | 個別 | SE-EVT-09 | 34/06 §6 |
| `understory.event.mayoi.guide` | 鐘：導く **（新規）** | BLOCKS | false | mono | 世界 | 迷子再提示一次チャネル——章の一次音の再発火＋柔らかい導き鐘 | かすれた小鐘系・微かな導き音（コンフィグ 45/04 §6#6 連動抑制） | 個別 | SE-MAYOI-01 | 45/02 §4.2・45/04 §6 |
| `understory.event.gate.wait` | 門：開く | BLOCKS | false | mono | 世界 | 06 待つの門——月齢 SE 系の静かな開門 | 月齢 SE 借用音色の開門 | 共有 | SE-GATE-01 | 34/06 §2・45/02 §3.3 |
| `understory.event.gate.post` | 投函：届く **（新規）** | BLOCKS | false | mono | 世界 | 06 届ける門——投函動作で門が開く | 投函の実音＋門の開放 | 共有 | SE-GATE-02 | 同上 |
| `understory.event.gate.beat` | 拍子：鳴る | BLOCKS | false | mono | 世界 | 06 合わせる門——拍に乗って区画進行で門が開く | 拍子同期の開門音 | 共有 | SE-GATE-03 | 同上 |
| `understory.event.gate.name` | 名：記す | BLOCKS | false | mono | 世界 | 06 名を与える門——命名動作で門が開く | 命名書き込み音＋門の開放（`ui.naming.write` の世界側転用） | 共有 | SE-GATE-04 | 同上 |
| `understory.event.gate.hear` | 門：聞かれる | BLOCKS | false | mono | 世界 | 06 聞かせる門——音を立てれば開く | 音応答の開門（鐘・楽器の残響に続く軋み） | 共有 | SE-GATE-05 | 同上 |

#### 3.2.1 章別キュー音色対応（柝機能＝機能共通・音色章固有——U3-N2 承認済み）

知らせ（開幕一拍）・ツナギ（幕間連打）・ツケ（見得一打ち）は機能全編共通だが、**音色は章固有**（docs/48/03 §3.3 U3-N2 承認済み）。各章のキューは独立した SoundEvent として登録する：

| 機能 | 字幕名 | 01 | 02 | 03 | 04 | 05 | 06 |
|---|---|---|---|---|---|---|---|
| 開幕一拍 | 拍子：開幕の一音 | `event.moon.cue_open` | `event.wave.cue_open` | `event.hyoushigi.cue_open` | `event.forge.cue_open` | **なし特例**（柝を出せない） | 段別借用 |
| 幕間連打 | 拍子：幕間を繋ぐ **（新規）** | `event.moon.cue_bridge` | `event.wave.cue_bridge` | `event.hyoushigi.cue_bridge` | `event.forge.cue_bridge` | 同上 | 同上 |
| 見得一打ち | 拍子：見得 | 同上 `_pose` | 同上 `_pose` | 同上 `_pose` | 同上 `_pose` | 同上 | 同上 |

全行共通：カテゴリ BLOCKS・stream false・mono・共有層・疑似ループ（連打は間隔仕様に従う）。音色＝章固有楽器/環境音（01＝月齢SE 型・02＝波/帆型・03＝柝型・04＝打鍵型・05＝なし・06＝借用）。根拠：48/03 §3.3 U3-N2・16 §4.x。

### 3.3 章別環境・固有 SE（00〜06＋横断）

#### 00 序章・横断

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.wave_raspy.bed` | 波：砕ける | AMBIENT | false | stereo | 世界 | 序章の環境床 | かすれた波の疑似ループ（10〜30s 素材の重なり再生） | 共有 | SE-AMB-00 | 34/00・§2.4 |
| `understory.world.pickup.aura` | 拾得物：微かに鳴る **（新規）** | BLOCKS | false | mono | 世界 | 拾得トークン（世界配置の拾得物）への接近気配 | かすれた小鐘系の微かな共鳴——通知音より一段静か | 個別 | SE-TOK-AURA | 45/04 §5.3・§2.3.2 |
| `understory.world.presence.stir` | 何か：蠢く | AMBIENT | false | mono | 世界 | 淀みの窪地への接近気配 | 微かな蠢き——正体不明の気配 | 個別（接近者） | SE-YOD-03 | 34/00・45/04 §5.3 |
| `understory.world.silt.hollow` | 淀み：響く | AMBIENT | false | mono | 世界 | 淀みの窪地（全章共通の淀み音像・04 以降の没腐音の基盤） | 淀んだ低い共鳴の疑似ループ | 個別（接近者） | SE-YOD-01 | 18 §5.6・45/04 §5.2・38/04 §2 |
| `understory.world.foreign.noise` | 何か：歪む | AMBIENT | false | mono | 世界 | 異物への近接ノイズ（接近で増す） | 異物の歪み気配——位相のずれた短いノイズ | 個別 | SE-TR-03a | 45/04 §5.2・G-AU-11 |
| `understory.world.foreign.echo` | 昔の音：残響 | AMBIENT | false | mono | 世界 | 異物への接近継続・近傍での間欠 | かすれた昔の音の残響（MU-MOTIF-OLD 系の短い片鱗） | 個別 | SE-TR-03b | G-AU-11・34/04 §4 |

#### 01 月（月齢の環礁）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.forest_moon.bed` | 林：静まる **（新規）** | AMBIENT | false | stereo | 世界 | 01 の環境床 | 月齢林の静まり——夜の林・微かな気配音の疑似ループ | 共有 | SE-AMB-01 | 34/01 |
| `understory.world.moon.phase` | 月：移る | AMBIENT | false | stereo | 世界 | 月齢転相（環境イベント＋ボス周期マーカー兼用） | 月齢 SE 型の短い推移音 | 共有 | SE-MOON-01 | 34/01・38/03 §4.4 |

（01 のキュー音＝`event.moon.cue_*`＝§3.2.1、ボス音＝§3.4 を参照）

#### 02 港（届かない港）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.wave_harbor.bed` | 波：砕ける | AMBIENT | false | stereo | 世界 | 02 の環境床（序章と別素材——港の波は樽・帆を含む） | 港の波＋帆のはためきの疑似ループ | 共有 | SE-AMB-02 | 34/02 |
| `understory.world.whistle.far` | 汽笛：遠くで鳴る | AMBIENT | false | stereo | 世界 | 02 の遠方汽笛・不規則間欠 | かすれた汽笛——遠方からの擬似減衰 | 共有 | SE-EVT-10 | 45/04 §5.2 列挙 |
| `understory.world.paper.drift` | 手紙：擦れる **（新規）** | BLOCKS | false | mono | 世界 | 手紙の吹き溜まりの風動 | 紙束の擦れ——堆積物の定位 | 個別 | SE-PAPER-DR | 34/02 |

#### 03 広場（開かれない広場）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.beat.bed` | 拍子：鳴り続ける | AMBIENT | false | mono | 世界 | 03 の環境拍子床——**発生源はボス（祭囃子の指揮台）**（環境音の正体＝ボスの一体型・04 打鍵と同型） | 拍子の疑似ループ（≈3.0s 間隔再発火・ジッタ小） | 共有 | SE-BEAT-01 | 34/03 §3・38/03 §4.4 |
| `understory.world.stall.clap` | 拍子：合わせる **（新規）** | PLAYERS | false | mono | 世界 | 屋台の拍子合わせ teach 動作 | 手拍子・柝型の短い一拍 | 個別 | SE-BEAT-02 | 34/03・45/02 |
| `understory.mob.applause.canned` | 客席：拍手する | AMBIENT | false | mono | 世界 | 03 幕間の缶詰拍手（空の客席から） | 録られた拍手のかすれた残響 | 共有 | SE-EVT-11 | 34/03 §6 |

#### 04 坑道（選べない坑道）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.forge.bed` | 打鍵：遠くで響く | AMBIENT | false | mono | 世界 | 04 の環境打鍵床——**最深部ボスの一打ちそのもの**（ボス作業周期と同期・剥落基準 ≈7s） | 規則正しい鈍い一打ちの疑似ループ（≈7s 間隔）——ボス戦移行で環境打鍵がボス動作音へ連続する継ぎ目仕様 | 共有 | SE-HAMMER-ENV | 34/04 §3.1・§5・38/03 §4.4 |
| `understory.world.babel.hum` | 坑道：ざわめく **（新規）** | AMBIENT | false | stereo | 世界 | 04 アリーナ周辺のゾーン床 | 労働のざわめき・遠い道具音の疑似ループ | 共有 | SE-AMB-04 | 34/04 |

#### 05 汀（歌姫の汀——無音の章）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.world.bell.kyoukai` | 鐘：鳴る | BLOCKS | false | mono | 世界 | 径の鐘の鳴動（響界発生源——鳴らせるのは聞き手のみ・15s 上限） | かすれた大きめの鐘 | 共有 | SE-BELL-05 | 38/03 §4.5・34/05 §3.2 |
| `understory.ambient.echo_hollow.bed` | 残響：淀む **（新規）** | AMBIENT | false | stereo | 世界 | 05 残響の窪地（音の淀み場）の区画床 | 溜まった残響の微かな渦——疑似ループ | 共有 | SE-AMB-05 | 34/05・16 §6.2 |
| `understory.world.song.frag` | 歌：微かに響く | BLOCKS | false | mono | 世界 | 響界内の歌のかけら（拾得物として定位する歌の断片） | 詞なし声楽の短い断片（MU-UTA-FRAG 素材） | 個別 | MU-UTA-FRAG | 34/05 §4・38/03 §4.5 |

（05 ボス・大鐘・結末音は §3.4/§3.2 を参照。05 の環境床は存在しない——世界の音がない章）

#### 06 座（終章・座の階層）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.strata.bed` | 地層：沈む | AMBIENT | false | stereo | 世界 | 06 段別下降の層床 | 地層下降の重い疑似ループ | 共有 | SE-AMB-06 | 34/06・38/03 §4.6 |
| `understory.ambient.archive.bed` | 書庫：静まる **（新規）** | AMBIENT | false | stereo | 世界 | 06 書庫区画の床 | 静まり＋微かな紙気配の疑似ループ | 共有 | SE-AMB-06b | 34/06 |
| `understory.event.page.shed` | 頁：剥がれる | HOSTILE | false | mono | 世界 | 06 ボス——頁排出演出（各段で頁が剥がれて落ちる） | 頁の剥がれ＋ひらひら落ちる紙音 | 共有 | SE-EVT-12 | 38/03 §4.6 |
| `understory.event.phantom.voice` | 声：重なる **（新規）** | AMBIENT | false | stereo | 世界 | 06 段 4 幻影——条件で重なる声部（MU-UTA-DUET 系素材） | 詞なし声楽の重なり | 共有 | MU-UTA-DUET | 38/03 §4.6 |

#### 横断（異物・没腐・救出後）

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.ambient.molder.bed` | 没腐：歪む | AMBIENT | false | stereo | 世界 | 個人没腐度≥5 以降の世界側レイヤー（没腐の歪み音が薄く重なる——19-U4-Q6 連動） | 淀み系の濁った歪みレイヤー | 個別 | SE-YOD-04 | 45/04 §5.2・38/04 §2・18 §5.7 |
| `understory.event.letter.peel` | 手紙：剥がれる | HOSTILE | false | mono | 世界 | N-BOS-02 撃破演出——積まれた手紙が剥がれて落ちる | 紙束の剥がれ落ちる音 | 共有 | SE-BOS-09 | 34/02 §5 |

### 3.4 モブ・ボス SE

| 登録ID | 字幕名 | カテゴリ | stream | 定位 | 層 | トリガー | 音色要件 | 共有/個別 | 素材ID | 根拠 |
|---|---|---|---|---|---|---|---|---|---|---|
| `understory.mob.beast.growl` | 獣：唸る | HOSTILE | false | mono | 世界 | N-MOB 系獣の接近・威嚇 | かすれた低い唸り | 共有 | SE-MOB-01 | 38/04 |
| `understory.mob.wolf.howl` | 狼：咆哮する | HOSTILE | false | mono | 世界 | N-BOS-01 月欠狼の咆哮・月齢転相キュー（`world.moon.phase` と同期） | 狼の咆哮＋月齢 SE の残響尾 | 共有 | SE-BOS-01 | 38/03 §4.4・34/01 |
| `understory.mob.letters.swarm` | 文字：舞う | HOSTILE | false | mono | 世界 | N-MOB-003 読まれなかった文字の群れの舞い（着地時は無音） | 紙群の舞う擦れの疑似ループ | 共有 | SE-MOB-03 | 38/04 |
| `understory.mob.dancer.steps` | 人形：踊る | HOSTILE | false | mono | 世界 | N-MOB-004 踊り損ねた者の移動（拍に乗る） | 木製関節の軋み＋拍同期の足音 | 共有 | SE-MOB-04 | 38/04・18 §5.6 |
| `understory.mob.dancer.collapse` | 人形：崩れる | HOSTILE | false | mono | 世界 | 同・撃破時の崩落 | 木片の崩れる音 | 共有 | SE-MOB-05 | 38/04 |
| `understory.mob.material.drag` | 素材：引きずる | HOSTILE | false | mono | 世界 | N-MOB-005 素材の精の移動 | 重い素材の引きずり音 | 共有 | SE-MOB-06 | 38/04 |
| `understory.mob.eater.suck` | 間：喰われる **（新規）** | HOSTILE | false | mono | 世界 | N-MOB-007 間を喰う者の吸収予備（2.0s テレグラフ＋周辺 SE −30%） | 音が吸い込まれる渦音——吸収中は無防備（反撃窓の可読性のため発火する） | 共有 | SE-MOB-07 | 38/04 N-MOB-007 |
| `understory.mob.resident.breathe` | 住人：息づく | NEUTRAL | false | mono | 世界 | N-MOB-008 中立住人の動き・気配 | 衣擦れ・気配の微音 | 共有 | SE-MOB-08 | 38/04 |
| `understory.mob.resident.warp` | 住人：歪む | HOSTILE | false | mono | 世界 | N-MOB-009 敵対化住人 | 声にならない歪んだ気配 | 共有 | SE-MOB-09 | 38/04 |
| `understory.mob.shape.stir` | 形：うごめく | HOSTILE | false | mono | 世界 | N-MOB-010 二度棄て形の動作 | 捨てられた形の蠢き | 共有 | SE-MOB-10 | 38/04 |
| `understory.mob.ship.sail` | 帆：張る | HOSTILE | false | mono | 世界 | N-BOS-02 座礁船の帆の展開・攻撃予備 | 帆のはためき＋船体軋み | 共有 | SE-BOS-02 | 34/02 |
| `understory.mob.letter.storm` | 紙：舞う | HOSTILE | false | mono | 世界 | 同・手紙嵐攻撃 | 大量の紙の舞う音 | 共有 | SE-BOS-03 | 34/02 |
| `understory.mob.mailbag.throw` | 郵袋：飛ぶ | HOSTILE | false | mono | 世界 | 同・郵袋投擲 | 重い袋の飛来音 | 共有 | SE-BOS-04 | 34/02 |
| `understory.mob.beat.cue` | 拍子：合図 | HOSTILE | false | mono | 世界 | N-BOS-03 祭囃子のキュー（攻撃合図・拍の変化） | 柝型の合図一拍 | 共有 | SE-BOS-05 | 38/03 §4.4 |
| `understory.mob.part.detach` | 素材：落ちる | HOSTILE | false | mono | 世界 | N-BOS-04 ゴーレムの部位剥落 | 金属・素材の剥落音 | 共有 | SE-BOS-06 | 34/04 |
| `understory.mob.part.use` | 素材：使われる | PLAYERS | false | mono | 世界 | 剥落了素材の拾得・使用 | 素材の拾い上げ音 | 個別 | SE-BOS-07 | 34/04 |
| `understory.mob.reabsorb.pull` | 塊：吸い込む | HOSTILE | false | mono | 世界 | 同・剥落物の再吸収 | 素材が引き戻される渦音 | 共有 | SE-BOS-08 | 34/04 |
| `understory.mob.songstress.attack` | 歌姫：放つ | HOSTILE | false | mono | 世界 | N-BOS-05 歌姫の攻撃（**響界内のみ**——響界外は全攻撃無音・見得のみ） | 詞なし声楽の放つ一音＋空間歪みの被弾気配（3 攻撃パターンを同一 SE のバリアントで） | 共有 | MU-UTA-ATK＋SE-UTA-FX | 34/05 §3.7・45/02 §7.1 |
| `understory.mob.songstress.phrase` | 歌：響く | HOSTILE | false | mono | 世界 | 同・第二連のフレーズ応答 | 詞なし声楽の短いフレーズ | 共有 | MU-UTA-PHR | 34/05 §3.7 |
| `understory.event.bell.great` | 大鐘：鳴る | BLOCKS | false | mono | 世界 | 05 幕間の大鐘初鳴（鐘楼） | 大鐘の初鳴——**かすれを残す**（19-U2-Q4 推奨＝かすれ維持） | 共有 | SE-BELL-06 | 34/05 §5 |

**登録しない（無音・流用）**：音無しの靄（N-MOB-006）＝接近音なし（§1.2.1）／揺れて鳴らない鐘＝発火しない／落慮王（N-BOS-06）の段別キュー＝段別借用（§4.6 借用表——各段の章 SE をそのまま流用・借用先字幕名がそのまま出る）／名付けの台の器音＝`ui.naming.write`／読み上げ演出音＝§6.2 の読み BGM（MUSIC 領域）。

### 3.5 定位必須一覧（§2.3.2 との突合）

§2.3.2 の定位必須音は全て本節に登録行を持つ——§3.1（鐘・羅針盤・鈴・座・クレーン・部位・遺留物・楽屋門・ノミ×2）・§3.2（転移・門・結末鐘・迷子導き）・§3.3（定位床・気配）・§3.4（全モブ/ボス音）。

### 3.6 字幕名台帳（字幕名 → SoundEvent ID）

| 字幕名 | 登録ID | 種別 |
|---|---|---|
| 頁：めくれる | `ui.page.turn` | 正典（18 §5.6） |
| 頁：開く／頁：閉じる／頁：綴じる | `ui.page.open`/`close`/`bind` | 正典 |
| 紙：擦れる | `ui.paper.rustle` | 正典 |
| 封：切れる | `ui.seal.break` | 正典 |
| 巻：戻る | `ui.scroll.rewind` | 正典 |
| 写：開く | `ui.map.open` | 正典（U2-R-7 系） |
| 名：記す | `ui.naming.write`・`event.gate.name` | 新規（命名動作の統一名） |
| 拾得物：届く | `ui.notify.pickup` | 正典（18 §2.5.1） |
| 拾得物：微かに鳴る | `world.pickup.aura` | 新規（世界トークン気配） |
| 鐘：鳴る | `ui.notify.release`（解放通知）・`world.bell.kyoukai`（径の鐘） | 正典——同一音色種別の別発火点として共用 |
| 村報：発行される | `ui.notify.bulletin` | 正典 |
| ノミ：語る | `ui.nomi.narrate` | 正典（18 §3.4） |
| ノミ：話す | `mob.nomi.talk` | 正典（18 §5.1） |
| 頁：書き込む | `mob.nomi.write` | 新規 |
| 物：落ちる | `world.bin.insert` | 新規（ゴミ箱投入） |
| 箱：軋む | `world.bin.lid` | 正典 |
| ゴミ箱：鳴る | `world.bin.arrive` | 正典（着弾側＝18 §2.5.1） |
| 物：沈む | `world.bin.sink` | 正典系（23 §11） |
| 招待状：届く | `world.invite.pop` | 新規 |
| 郵便船：軋む | `world.mailboat.creak` | 正典 |
| 紙：貼る | `world.board.post` | 正典 |
| 小さな鐘：微かに鳴る | `world.chime.small` | 正典 |
| 楽器：鳴らす | `world.instrument.ring` | 新規（動作側） |
| 素材：拾い直す | `world.reforge.pickup` | 正典 |
| 羅針盤：縁を指す／異物を指す／淀みを指す | `world.compass.edge`/`foreign`/`molder` | 新規（複合識別——対象別字幕・U1-Q4） |
| 鈴：鳴る | `world.festival_bell.ring` | 新規 |
| 座：応える | `world.seat.resonance` | 新規 |
| クレーン：動く／掴む | `world.crane.warn`/`grab` | 新規 |
| 部位：響く | `world.remnant.hum` | 新規 |
| 遺留物：歪む | `world.remnant.warp` | 新規 |
| 楽屋の門：開く | `world.backstage_door.open` | 正典系 |
| 幕：落ちる | `event.curtain.fall` | 正典（U2-Q2 棄却済み——「下りる」案不採用） |
| 拍子：開幕の一音 | `event.*.cue_open` | 正典（18-U3-Q8 台帳） |
| 拍子：幕間を繋ぐ | `event.*.cue_bridge` | 新規 |
| 拍子：見得 | `event.*.cue_pose` | 正典系 |
| 拍子：鳴り続ける | `ambient.beat.bed` | 正典 |
| 拍子：合図／合わせる／鳴る | `mob.beat.cue`/`world.stall.clap`/`event.gate.beat` | 正典系 |
| 鐘：座に届く | `event.bell.final` | 新規（結末の一音——「届く」系） |
| 鐘：渡る | `event.bell.sweep` | 新規 |
| 大鐘：鳴る | `event.bell.great` | 新規（鐘楼・径の鐘と区別） |
| 蓋：閉まる／開く | `event.transit.close`/`open` | 正典系（50 Beat 2） |
| 世界：壊れる | `event.transit.break` | 正典（50 Beat 2——転移・異物接触に共用） |
| 水面：着く | `event.transit.land` | 正典系 |
| 淀み：響く | `world.silt.hollow` | 正典 |
| 淀み：割れる | `event.silt.crack` | 正典系 |
| 環礁：鳴る | `event.rescue.return` | 新規 |
| 打鍵：遠くで響く | `ambient.forge.bed` | 正典（18 §5.6） |
| 打鍵：届く | `event.forge.final` | 正典（34/04 §5「届いた一打ち」） |
| 坑道：ざわめく | `world.babel.hum` | 新規 |
| 手紙：届く | `event.letter.final` | 正典系（K9/K10） |
| 手紙：擦れる | `world.paper.drift` | 新規 |
| 手紙：剥がれる | `event.letter.peel` | 正典系 |
| 機構：緩む | `event.mechanism.release` | 新規 |
| 音：消える | `event.silence.dome` | 新規（沈黙の域突入の一拍のみ） |
| 灯り：畳まれる | `event.light.fold` | 正典系 |
| 印：打たれる | `event.mark.stamp` | 新規 |
| 底：応える | `event.depth.answer` | 新規 |
| 幻影：展開する | `event.phantom.scene` | 新規 |
| 声：重なる | `event.phantom.voice` | 新規 |
| 足：重い | `event.heavy.step` | 新規 |
| 鐘：導く | `event.mayoi.guide` | 新規 |
| 門：開く | `event.gate.wait`（＋post/beat/name/hear は各行名） | 正典系 |
| 門：聞かれる | `event.gate.hear` | 新規 |
| 投函：届く | `event.gate.post` | 新規 |
| 月：移る | `world.moon.phase` | 正典系 |
| 林：静まる | `ambient.forest_moon.bed` | 新規 |
| 波：砕ける | `ambient.wave_raspy.bed`/`wave_harbor.bed` | 正典系 |
| 汽笛：遠くで鳴る | `world.whistle.far` | 正典（45/04 §5.2） |
| 何か：蠢く | `world.presence.stir` | 新規 |
| 何か：歪む | `world.foreign.noise` | 新規（異物近接） |
| 昔の音：残響 | `world.foreign.echo` | 正典（G-AU-11） |
| 没腐：歪む | `ambient.molder.bed`（§4.7 横断層） | 正典（45/04 §5.2 没腐の歪み音） |
| 残響：淀む | `ambient.echo_hollow.bed` | 新規 |
| 歌：微かに響く | `world.song.frag` | 新規 |
| 歌姫：放つ／歌：響く | `mob.songstress.attack`/`phrase` | 新規 |
| 地層：沈む | `ambient.strata.bed` | 新規 |
| 書庫：静まる | `ambient.archive.bed` | 新規 |
| 頁：剥がれる | `event.page.shed` | 新規 |
| 獣：唸る | `mob.beast.growl` | 正典 |
| 狼：咆哮する | `mob.wolf.howl` | 正典 |
| 文字：舞う | `mob.letters.swarm` | 正典 |
| 人形：踊る | `mob.dancer.steps` | 正典 |
| 人形：崩れる | `mob.dancer.collapse` | 正典 |
| 素材：引きずる | `mob.material.drag` | 正典 |
| 間：喰われる | `mob.eater.suck` | 新規 |
| 住人：息づく／歪む | `mob.resident.breathe`/`warp` | 正典 |
| 形：うごめく | `mob.shape.stir` | 正典 |
| 帆：張る | `mob.ship.sail` | 正典 |
| 紙：舞う | `mob.letter.storm` | 正典 |
| 郵袋：飛ぶ | `mob.mailbag.throw` | 正典 |
| 素材：落ちる／使われる | `mob.part.detach`/`use` | 正典 |
| 塊：吸い込む | `mob.reabsorb.pull` | 正典 |

> **新規名の取り扱い**：「新規」印の名は全て二項型・内容言明禁止の規格に従う（18 §5.6）。Issue #34 の台帳管理へそのまま登録対象として引き渡す。
