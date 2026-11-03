# ADR-0010: 本体ライセンス — MIT（modpack 同梱許可の設計要件化）

- Status: Accepted（2026-11-03・ユーザー「承認します。」一括承認——Issue #12 要承認18件全件推奨案どおり採用）
- Date: 2026-11-03
- Deciders: 65banseki + Devin
- Related: docs/43 §4.1（LICENSE 確定行・43-U2-Q1 承認済み）、docs/43 §4.5（modpack 収録条件⑥）、docs/32 §9（条件⑥同梱許可ライセンス）、docs/46 §4.2、docs/42 §5.2（ADR 化トリガ）、ADR-0002

## Context

本体ライセンスは 43-U2-Q1 承認（2026-10-06）で **MIT** に確定済み。modpack 収録条件（D-4）の「同梱許可ライセンス」要件の根拠となる決定であり、ADR 化トリガ（docs/42 §5.2——緩和・対処の重要決定）の対象。12-U4-Q4 で ADR として記録することが承認された。

## Decision

**本体ライセンス＝MIT** とする（43-U2-Q1 承認値を ADR として記録）。

- modpack 同梱を許可する旨が明確なライセンスであること（ARR では個別許諾が要り収録が実質死ぬ——docs/46 §4.2）
- Modrinth/CurseForge の SPDX 識別子要件に対応する（docs/43 §4.1）
- **範囲**：本体コード・リソースが対象。オーディオ素材のライセンスは LICENSES-AUDIO で別管理（42-U3-Q4——Phase 1 着手までの収録前提条件）

## Alternatives Considered

- **ARR（All Rights Reserved）**：modpack 同梱に個別許諾が必要となり収録条件を満たせない——却下（43-U2-Q1）。
- **GPL 系**：同梱配布時のソース開示義務がパック運用を複雑化させる——却下（43-U2-Q1）。

## Consequences

- modpack 収録条件⑥（同梱許可ライセンス——docs/32 §9・docs/43 §4.5）が充足される。
- ライセンス変更は modpack 収録の前提を崩すため、変更する場合のみユーザー承認＋新 ADR（supersedes）で記録する。

## Open Questions

なし（12-U4-Q4＝本 ADR の起票自体が承認済み決定）。
