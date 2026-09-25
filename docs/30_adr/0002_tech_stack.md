# ADR-0002: 技術基盤 NeoForge / Minecraft 1.21.1 / Java 21

- Status: Proposed（要ユーザー承認）
- Date: 2025-XX
- Deciders: Devin提案 → ユーザー承認待ち
- Related: docs/02_research_mod_landscape.md（技術選定の根拠調査）

## Context
大型次元MODを実装するローダーと対象バージョンを確定する必要がある。要件：カスタム次元＋独自地形生成＋ボスAI＋カスタムUI/フォント＋シェーダーMOD互換＋マルチプレイ対応。

## Decision（提案）
- **ローダー：NeoForge** — Fabricより多機能（カスタム次元・高度なレンダリング・能力システム）。黄昏の森・Cataclysm・Create等の大型MOD実績。ドキュメント/コミュニティの厚さが単独開発に有利
- **対象：Minecraft 1.21.1** — 現行安定系。シェーダー系（Iris/Complementary/BSL）・Distant Horizons・最重要周辺MODの対応が揃う。新バージョン追随はリリース後に判断
- **言語：Java 21** — 1.21系の標準。Kotlin不採用（エコシステムが薄い）
- **配布：Modrinth＋CurseForge** 両チャネル
- **アプローチ：データ駆動ワールドジェネ** — 章構造・構造物・ロア配置を極力JSON/Datapack的に記述し、章量産フェーズの速度を上げる

## Alternatives Considered
- **Fabric**：軽量・最新版追随が速いが、大規模次元MODの実績と機能面でNeoForgeに劣る
- **Forge（旧来）**：NeoForgeに事実上置き換わっている
- **MC 1.20.x**：周辺MODが最も成熟しているが、新規大型MODとして1世代古い

## Consequences
- Iris+シェーダー・Distant Horizonsとの互換検証が必須（`20` 要件）
- NeoForgeのAPI変更追従コストを見込む（保守方針を別途決める）
- Fabric版は出さない（スコープ限定、ユーザー層への説明が必要）
