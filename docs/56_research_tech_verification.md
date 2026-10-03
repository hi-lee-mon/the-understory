# 56 次元生成・異物チャンク技術検証の調査基準（Issue #13）

> **役割**：Issue #13（次元生成・異物チャンクの技術検証 → 成果物 docs/57 技術検証計画書）の制作・レビュー全エージェントが共有する物差し。NeoForge 1.21.1 の API 実在性調査・先行実装パターン・正典制約（G-TV 群）・設計原則（P-TV 群）・棚卸し項目（H 群）・組版テンプレを集約する。制作側は本書と正典を読み、テンプレに従って執筆する。
>
> **Phase 0 制約**：実装コードを書かない。本フェーズの成果は「Phase 1 で何を作り・何を測り・何を合格とするか」を実装可能な粒度まで設計した**技術検証計画書**＋調査ベースの**実現性評価**（実在 API と先行実装の根拠付き）。実機 PoC の実施は Phase 1 許可待ちとして明示する。

---

## 1. 先行調査：NeoForge 1.21.1 の技術実在性

### 1.1 次元生成スタック（確認済み）

- **次元登録はデータパック駆動**：`data/<ns>/dimension_type/`・`data/<ns>/dimension/`・`data/<ns>/worldgen/noise_settings/` の JSON で定義。NeoForge は `DatapackBuiltinEntriesProvider`＋`RegistrySetBuilder` で datagen 可能（NeoForge commit ad6bf94——LevelStem 出力対応済み）。
- **次元タイプ**：`DimensionType`（固定時刻・天空光・天井有無・自然環境・座標スケール・ベッド可否・minY/height・ambientLight 等）。Twilight Forest 先例（`TFDimensionData.java`）：固定時刻13000（黄昏）・座標 1/8・minY -32・ambientLight 0.01 を JSON で定義し、`bootstrapStem` で LevelStem を生成。
- **地形生成**：`minecraft:noise` ジェネレータ＋noise_settings JSON——`noise_router`（final_density 等の密度関数列）＋`surface_rule`（地表ブロック規則）＋`spawn_target`。独自地形は density function 群を自前設計する。ネザー型（caves）・エンド型（floating_islands）等の既成プリセットを流用する手もある。
- **1.21 のチャンク生成再編**：生成処理は `ChunkGenerationTask`/`GeneratingChunkMap`/`GenerationChunkHolder` へ分離され**ほぼ非同期化**（`ChunkPyramid` がステップ依存を管理）。カスタムジェネレータの性能検証はこの非同期前提で設計する。
- **バイオーム**：`worldgen/biome` JSON＋`MultiNoiseBiomeSource`（気候パラメータ配置）または `FixedBiomeSource`/`TheEndBiomeSource` 型の決定論的配置。BiomeModifier（`data/<ns>/neoforge/biome_modifier/`）で追記可能。

### 1.2 構造物システム（確認済み）

- **Jigsaw 系**：`worldgen/structure`（start_pool・max_distance_from_center・project_start_to_heightmap 等）＋`worldgen/template_pool`（要素＋重み＋processors＋fallback）＋`worldgen/processor_list` の JSON 三重構造。`JigsawPlacement#addPieces` は 1.21 で `DimensionPadding` を取る。
- **processor 全型**（Java）：`rule`（input/position/output 述語＋block_entity_modifier）・`block_rot`（確率でブロック除去＝荒廃表現の定石）・`block_age`（石系の経年置換）・`block_ignore`・`gravity`・`protected_blocks`・`blackstone_replace`・`jigsaw_replacement`・`lava_submerged_block`・`capped`（処理数上限）・`nop`。position_predicate に `axis_aligned_linear_pos`（構造起点からの距離で確率変化——**「中心ほど没腐が深い」地形変調の標準手段**）。
- **配置**：`worldgen/structure_set`（spread 型＝塩・間隔・分離度／concentric 型＝同心円）。**ワールド固定配置**（40-Q24）は spread の salt 固定＋確定的 spacing で近似可能；完全固定は自前の配置関数（TF 先例：major feature をチャンク座標に決定論配置）。
- **正典の生成4型**（docs/16 §2.4）：①固定テンプレ②jigsaw モジュラー③地形依存埋没④手組み領域——①②はバニラ JSON で到達、③は processor＋feature 組み合わせ、④は構造物を介さない直接設置（コード生成）。

### 1.3 次元転移（確認済み・1.21 で刷新）

- `PortalInfo` → **`DimensionTransition` レコード**に統一（転移先 ServerLevel・座標・速度・向き・respawnBlock 判定・PostDimensionTransition コールバック）。`Entity#changeDimension(DimensionTransition)` で遷移。
- **ポータル経路**：`Portal` インタフェースを Block が実装→`Entity#setAsInsidePortal` に `PortalProcessor` 登録→転移時間・遷移先・転移エフェクト（`getPortalTransitionTime`/transition effect）を制御可能。`canUsePortal`/`canChangeDimensions` で条件付け可。
- **本作の転移＝ゴミ箱投入**（docs/23）：アイテムの転移は EntityItem の次元遷移または手動テレポートで実装可。**持ち込み可否の制御**＝転移時にインベントリ走査して禁止品を弾くフィルタを PostDimensionTransition または専用フックに実装。

### 1.4 個別層・プレイヤー別可視性（鍵技術・リスク帯）

- **ブロックの個人差分**：バニラに API は存在しないが、**サーバー側で送信パケットを加工する手法は実績がある**——Fabric の FibLib/**Illusion**（ブロック状態をプレイヤー述語で偽装送信）、Paper プラグインの `sendMultiBlockChange()` によるチャンク単位置換（anti-xray 系）。NeoForge では自前実装：`ClientboundSectionBlocksUpdatePacket`/`ClientboundLevelChunkPacketData` の送信フック（パケットインターセプト or `ServerPlayer` への送出段階で差し替え）で「A には異物が見え、B には見えない」を実現。**検証必須項目**：チャンク送信経路の安定フック有無・ブロック更新時の追従・副作用（採掘音・当たり判定はワールド実体なので偽装のみだと体験破綻し得る）。
- **代替案（正典の設計代替）**：異物をブロックでなく**エンティティ/BlockEntity＋カスタム描画**にして個別描画する（エンティティの per-player 可視性＝スポーンパケット送信制御で実現可・EntityTracker 相当の追跡対象フィルタ）。または docs/32 の既決「全員に見えるが初接触で消滅」＝一期一会物理成立案。
- **個別化アイテム**：`DataComponent`（CUSTOM_NAME/LORE/カスタム component）で所有者 UUID・由来文字列を保持し、ツールチップ/名称を表示時に差し替え（`ItemTooltipEvent` はクライアント側で改変可——18-U 系の手渡しどおり）。実体は共有・表示のみ個別化（docs/32 §6 確定値どおり）。
- **永続データ**：`AttachmentType`（NeoForgeRegistries.ATTACHMENT_TYPES——ブロック・チャンク・エンティティ・レベルへ付加、serializer＋`copyOnDeath`＋`sync` でクライアント同期）＋`SavedData`（レベル単位の保存）。**個別層データ構造＝プレイヤー毎の attachment＋ワールド側の差分レコード**で設計できる。

### 1.5 クライアント演出・二層演出（確認済み）

- `DimensionSpecialEffects`（renderSky/renderClouds/renderSnowAndRain/tickRain/adjustLightmapColors——`IDimensionSpecialEffectsExtension`）で次元別の空・雲・ライトマップを完全に差し替え可。
- `RenderLevelStageEvent`（AFTER_SKY＝スカイボックス描画・AFTER_PARTICLES 等の Stage）で任意ジオメトリをワールド描画に差し込める。
- **二層演出の実現形**：現実側から「国が見える」演出＝①オーバーワールド側のカスタム天空描画（遠景シルエットをテクスチャ/疑似3D で描く）②転移装置の窓的描画（ポータル面に別次元をレンダリング＝Immersive Portals 型は重量級、スターシップ型の「絵として見せる」軽量案が現実解）③配信モード・シェーダー OFF 一次チャネル保証（40-Q21）に従いコア描画は非シェーダーパスで実装。

### 1.6 音機構（確認済み）

- `SoundEvent` 登録＋`sounds.json`（docs/19 §2.1 規格）。再生は `playSeededSound`（サーバー発→対象外クライアント全員）、`playLocalSound`（カスタムパケット経由のクライアント単独）、`playSound` 等。
- **サーバー権威発火**＝サーバーが `ClientboundSoundPacket`（sound/category/xyz/volume/pitch/**seed**）を送出→クライアントは受信して再生。±100ms（19-U4-Q4）はネットワークラグ内で実現可能だが**実測検証項目**（ティック同期・パケット送出タイミングの jitter 測定）。
- **発火抑制**（19 §1.1.1：消音＝発火させない）＝再生呼出側で条件分岐する自前コントローラ（環境床コントローラ docs/19 §2.4＝自前・サーバー権威）。

### 1.7 UI・書物・フォント（確認済み）

- **フォント**：`assets/<ns>/font/<name>.json` に provider 配列（`bitmap`/`ttf`/`space`/`unihex`/`reference`）——幻想文字（18 §5.11）・和文カスタム字形は ttf/bitmap provider＋言語ファイル登録で到達可（58 字形の手渡しどおり）。
- **UI 層**：`GuiLayerManager`/カスタム GuiLayer 登録、`ItemTooltipEvent`（由来行の挿入——docs/18 手渡し）。
- **Patchouli**（1.21.1 以降は NeoForge のみ・docs/46 D-2 確定）：`book.json` を data 側・コンテンツ（categories/entries/templates）を assets 側に配置。`compileOnly vazkii.patchouli:patchouli-neoforge:<v>:api`＋`runtimeOnly` 同 jar で soft-dep 連携（maven.blamejared.com）。`patchouli:book` コンポーネントで本アイテムに書物を割当。
- **JEI**：`mezz.jei:jei-1.21-neoforge-api` compileOnly＋`IModPlugin#registerCategories`（`IRecipeCategory`）＋`IRecipeManager` で登録レシピの**隠し制御**可（18-U4-Q6——レシピ表示をフラグ制御）。
- **自前書物器**：`Screen` サブクラス＋`Menu`/`SimpleContainerData` 系で独自書物 UI を構築（40-Q9 FB 端到端の検証対象）。

### 1.8 依存 MOD・配備（確認済み）

- **GeckoLib**（40-Q25 承認＝jarJar 同梱）：`com.geckolib:geckolib-neoforge-<mc>:<v>` を `jarJar` 依存設定で mod jar 内埋め込み（NeoGradle/ModDevGradle 標準機能）＋`mods.toml` の依存宣言調整。外部必須依存を増やさずボスアニメーション基盤を確保。
- **JEI/EMI**：JEI は D-1 どおり必須対応（EMI は JEI 互換レイヤで概ね追従——docs/46）。modpack 収録条件5点（D-5）に反しない配備形態。

### 1.9 性能・検証環境

- チャンク生成性能の測定は **spark**（tick/profiler・生成時間ヒストグラム）＋`chunk_generation_stats` デバッグ出力（新版）＋`DebugStick`/timings。環礁生成パフォーマンス（docs/40 §4.9 ゲート）は「生成に要する ms/chunk・初期生成半径の所要時間・TPS 影響」を測る。
- 検証環境＝**NeoForge MDK（ModDevGradle）1.21.1 開発環境**＋統合サーバー（単一）＋LAN2 人接続（40-Q2 検証最小形）＋専用サーバー（第2層マルチ観測）。

---

## 2. 正典制約（G-TV 群）——検証計画が外してはいけない線

| ID | 制約 | 出典 |
|---|---|---|
| G-TV-01 | **Phase 0＝設計のみ**。実装コード作成は Phase 1 以降・ユーザー明示許可まで禁止。本書の成果は検証計画＋調査ベース実現性評価 | AGENTS.md |
| G-TV-02 | 技術基盤：NeoForge / MC 1.21.1 / Java 21 | ADR-0002 |
| G-TV-03 | 先行ゲート5点＝次元生成・転移骨格・個別化アイテム・転移持ち込み・異物の可視性モデル（スライス着工条件）。残りゲートは S1 並行 | docs/00・40-Q8 承認 |
| G-TV-04 | 環礁配置＝ワールド固定レイアウト（地形肌のみシード依存）・環礁生成方式は本 Issue で複数案比較検証して選択 | 40-Q24・docs/16 §2.4・docs/40 §9 |
| G-TV-05 | 個別層＝実体共有・表示のみ個別化（ワールド状態分岐は不可 ADR-0004）。個別層データ構造・一人一ノミ随伴・由来札・宝箱/ドロップ個別層・結末綴じ先着・ボス HP×(1+0.5n)・月充填の人数非依存は全実装 | docs/32 §6・40-Q2 |
| G-TV-06 | 異物可視性の正典目標＝「発見した人にしか見えない」。代替＝全員に見えるが初接触で消滅／エンティティ化個別描画 | docs/00 Phase1 表・docs/40 §9 |
| G-TV-07 | ゴミ箱転移＝持ち込み可否の設計は正典に従属（検証で実現性を確認） | docs/23・40 §9 |
| G-TV-08 | 依存：JEI 必須・Patchouli 採用（図鑑系のみ soft-dep・FB端到端は自前書物器 40-Q9）・GeckoLib jarJar 同梱（40-Q25） | docs/46 D-1/D-2・docs/00 |
| G-TV-09 | 音：サーバー権威発火・環境床コントローラ自前・発火抑制・響界半径12B±8・sounds.json ID 規格・ダッキング（19 §9 手渡し） | docs/19・19-U1-Q3/U4-Q4 |
| G-TV-10 | UI：幻想文字 font provider（ttf 58 字形・言語ファイル登録）・GuiLayerManager カスタム層・ItemTooltipEvent 由来行・JEI 隠し制御・自前書物器 Screen（18 §8 手渡し） | docs/18・18-U4-Q10/Q6・18-U2-Q1 |
| G-TV-11 | 構造：生成4型語彙（固定テンプレ/jigsaw/埋没/手組み）・構造生成 JSON・個別層生成（異物チャンク・自分の区画）・L3 同一構造判定・灯台−座礁船連動（16 §7.5 手渡し） | docs/16 §2.4/§7.5 |
| G-TV-12 | 完了条件＝検証結果を Issue コメントまたは ADR に記録（正典書き戻し先：docs/40 §4 基盤要件の数値ラインは実測で着地） | Issue #13・docs/40 §9 |
| G-TV-13 | 配信前提：シェーダー OFF で一次チャネル保証（40-Q21）・配信モード config（40-Q20）——演出系検証は非シェーダー経路を主とする | docs/40・docs/20 |

## 3. 設計原則（P-TV 群）——計画書の判定基準

| ID | 原則 |
|---|---|
| P-TV-01 | **検証項目は「潰す詰み」に集中**——実現性が明白なものは調査評価のみで閉じ、実機 PoC は「不明点・リスク帯」に絞る（計画は最小コストで最大の不確実性を削る） |
| P-TV-02 | **各項目に合格ラインと設計代替を必置**——「作れるか」だけでなく「ダメならどこへ逃げるか」を同じ行に書く（docs/00 Phase1 表の形式に倣う） |
| P-TV-03 | **API の実在性は出典つきで記す**——クラス名・パッケージ・バージョン・URL を明記し、記憶や推測で実在性を主張しない |
| P-TV-04 | **Phase 0/Phase 1 の境界を明記**——計画内の「作るもの」は Phase 1 タスクとして分離し、本書自体は設計成果物（PoC 仕様）である |
| P-TV-05 | **リスク評価は3段**——実現性：高（API実在・先行実績あり）/中（実装パスはあるが未確認箇所あり・性能未知数）/低（バニラ非対応・自前パケット加工等の重量級）＋各項目に検証手順と想定工数 |
| P-TV-06 | **マルチ前提で設計**——個別層・発火・可視性は全てマルチ環境（2人→専用サーバー）での振る舞いを検証対象に含める（40-Q2 確定値どおり） |
| P-TV-07 | **数値の合格ラインは実測着地**——docs/40 §4 の基盤要件（生成 ms/chunk・発火±100ms 等）に暫定値を置き、本 Issue の実測で確定して書き戻す導線を明記する |

## 4. 棚卸し（検証項目の全一覧——出典必須）

| H | 項目 | 内容 | ゲート区分 | 出典 |
|---|---|---|---|---|
| H-01 | 次元生成方式 | noise ジェネレータ＋独自 noise_settings による国の地形生成 | **先行ゲート** | docs/40 §9・Issue 本文 |
| H-02 | 異物チャンク生成 | 「現実と国の間に混入する異物のチャンク」生成方式 | **先行ゲート**（可視性モデルと一体） | Issue 本文・docs/40 §4.9 |
| H-03 | 転移骨格 | DimensionTransition/PortalProcessor によるゴミ箱転移の骨格 | **先行ゲート** | docs/40 §9・docs/23 |
| H-04 | 個別化アイテム | DataComponent 由来情報＋表示個別化（実体共有） | **先行ゲート** | docs/32 §6・docs/40 §4.9 |
| H-05 | 転移持ち込み可否 | 転移時インベントリフィルタの実現性 | **先行ゲート** | docs/40 §9 |
| H-06 | 異物の可視性モデル | 「発見者にのみ見える」の技術経路比較（パケット偽装/エンティティ化/初接触消滅） | **先行ゲート** | docs/00 Phase1・docs/40 §4.9 |
| H-07 | 環礁本体生成方式 | ワールド固定レイアウトの実現方式の比較選択（複数案） | S1 並行 | 40-Q24・docs/40 §9 |
| H-08 | 環礁生成パフォーマンス | 生成 ms/chunk・初期生成所要時間・TPS 影響の測定 | S1 並行 | docs/40 §4.9/§9 |
| H-09 | 没腐地形 processor | 荒廃・没腐変調の processor 構成（block_rot/rule/axis_aligned_linear_pos 等） | S1 並行 | Issue 本文・docs/16 §2 |
| H-10 | 二層演出 | 現実側から国が見える描画経路（DimensionSpecialEffects/RenderLevelStageEvent） | S1 並行 | Issue 本文 |
| H-11 | 構造生成 JSON・jigsaw | structure/template_pool/processor_list の JSON 系・pool/depth | S1 並行 | docs/16 §7.5 |
| H-12 | 個別層生成 | 異物チャンク・自分の区画の個別層生成ロジック | S1 並行 | docs/16 §7.5・32 §6 |
| H-13 | L3 同一構造判定 | 配信者層での同一構造物判定ロジック実装値（16-U4-Q5） | S1 並行 | docs/16 §7.5 |
| H-14 | 灯台−座礁船連動生成 | 連動構造物の生成参照方式（16-U2-Q09） | S1 並行 | docs/16 §7.5 |
| H-15 | 個別層データ構造 | Attachment/SavedData によるプレイヤー毎状態のデータ構造 | S1 並行（個別化と一体） | docs/32 §6・docs/40 §9 |
| H-16 | サーバー権威音発火 ±100ms | ClientboundSoundPacket 送出タイミングの jitter 実測 | S1 並行 | docs/19 §9・19-U4-Q4 |
| H-17 | 環境床コントローラ | 自前・サーバー権威の環境音床制御機構 | S1 並行 | docs/19 §9 |
| H-18 | 発火抑制機構 | 消音＝発火させない制御の実装経路 | S1 並行 | docs/19 §9 |
| H-19 | 響界判定 | 半径12B±8・到達頭打ちの判定実装 | S1 並行 | docs/19 §9 |
| H-20 | sounds.json 登録 | ID 命名規格の実装適合確認 | 調査のみ | docs/19 §9 |
| H-21 | ダッキング | サウンドダッキング実装経路 | S1 並行 | docs/19 §9 |
| H-22 | font プロバイダ | ttf 58 字形＋言語ファイル登録（18-U4-Q10） | S1 並行 | docs/18 §8 |
| H-23 | GuiLayerManager カスタム層 | HUD 層の登録・描画順 | S1 並行 | docs/18 §8 |
| H-24 | ItemTooltipEvent 由来行 | ツールチップ改変（個別層由来札同期含む） | S1 並行 | docs/18 §8 |
| H-25 | JEI 連携 | IRecipeCategory/IRecipeManager・隠し制御（18-U4-Q6） | S1 並行 | docs/18 §8・D-1 |
| H-26 | Patchouli book.json | 図鑑系の書物構成（18-U2-Q1） | S1 並行 | docs/18 §8・D-2 |
| H-27 | 自前書物器 Screen | FB 端到端の UI 実装方式 | S1 並行 | docs/18 §8・40-Q9 |
| H-28 | GeckoLib ボス基盤 | jarJar 同梱での導入確認・基本モブアニメーション | S1 並行 | 40-Q25・docs/40 §9 |
| H-29 | カラー回帰 | 色規則（docs/20）実装時の色値検証系 | S1 並行 | docs/40 §4.9 |
| H-30 | 転移 FX | 転移時演出（暗転・モーション）の描画経路 | S1 並行 | docs/40 §4.9 |

（H 群は統合時に漏れがないか §6 の対応表で照合する）

## 5. 組版テンプレ（成果物 docs/57_tech_verification_plan.md の節構成）

```
# 57 次元生成・異物チャンク技術検証計画（Issue #13）
§0 位置づけ（Phase 0 設計成果物／Phase 1 の実機 PoC は許可待ちと明記・完了条件の対応）
§1 検証対象マップ（H 群→節への対応表・先行ゲート5点と S1 並行の区分・依存関係図）
§2 次元・地形系の検証（H-01/02/07/08/09/11/14——各項目カード形式）
§3 転移・持ち込み系の検証（H-03/05/30）
§4 個別層・可視性系の検証（H-04/06/12/13/15/24）
§5 UI・書物・依存 MOD 系の検証（H-22/23/25/26/27/28）
§6 音・演出系の検証（H-16〜21/29）
§7 検証環境・測定規格（環境・ツール・測定単位・実測着地→docs/40 §4 書き戻し導線）
§8 未決・要承認集約（表：ID・論点・推奨案・書き戻し先・統合元）
§9 手渡し一覧（消費先 Issue/文書への引き継ぎ項目）

## 項目カード形式（§2〜§6 共通）
### <H-ID> <項目名>
- **実現性評価**：高/中/低＋根拠（API・先行実装・出典）
- **検証内容**：Phase 1 で作る PoC の仕様（何を作り・どう動かすか）
- **合格ライン**：定量的/定性的合格条件（docs/40 §4 の暫定値に接続するものは明記）
- **設計代替**：ダメな場合の逃げ道（複数案あるものは比較表）
- **依存・前提**：他項目・正典値・依存 MOD
- **Phase 1 タスク化**：実機検証の作業粒度（小さな検証単位に切る）
- **想定リスク/工数**：リスク帯・相対工数（小/中/大）
```

---

## 6. 棚卸し→成果物節の対応表

| H | 57 の節 |
|---|---|
| H-01/02/07/08/09/11/14 | §2 |
| H-03/05/30 | §3 |
| H-04/06/12/13/15/24 | §4 |
| H-22/23/25/26/27/28 | §5 |
| H-16/17/18/19/20/21/29 | §6 |
| 全項目の測定・合格ライン体系 | §7 |

> 本基準にない正典値は原則「要承認」へ回す。制作・レビュー全エージェントは本書＋正典（docs/00・16・18・19・23・32・40・46・ADR-0002/0003/0004）を読んでから作業すること。
