# ADR（Architecture / Design Decision Records）

「なぜそう決めたか」を残す決定記録。コード・設計の「何を」は設計書が担い、「なぜ」はここに置く。

## ルール
- ファイル名：`NNNN_タイトル.md`（連番4桁）
- ADRは**immutable**：書いた後は本文を修正しない。決定を覆すときは新しいADRを作り、旧ADRのStatusを `Superseded by ADR-XXXX` に更新する
- 1ADR = 1決定。複数の決定を混ぜない

## テンプレート
```markdown
# ADR-NNNN: タイトル

- Status: Proposed / Accepted / Deprecated / Superseded by ADR-XXXX
- Date: YYYY-MM-DD
- Deciders: 65banseki + Devin
- Related: docs/XX（関連設計書）

## Context
この決定が必要になった背景・制約・論点。

## Decision
採用した選択肢と、その理由。

## Alternatives Considered
検討して却下した選択肢と、却下理由。

## Consequences
この決定による影響（良い面・悪い面・今後の制約）。
```

## 既存ADR
- ADR-0001: 方向性「棄てられたものの国」（案E）の採用
- ADR-0002: 技術基盤 NeoForge / MC 1.21.1 / Java 21
- ADR-0003: 「あなたが捨てたもの」機構 — クラフト可能な「ゴミ箱」
- ADR-0004: ストーリー状態モデル — 物語/村共有＋個人差分個別
