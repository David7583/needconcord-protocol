---
name: 符合性或文档问题 / Conformance or documentation
about: 报告歧义、测试缺口与独立阅读障碍 / Ambiguities, coverage gaps and implementation obstacles
title: '[Conformance/Docs] '
labels: ''
assignees: ''
---

### 相关条款与文件 / Relevant clauses and files

版本、规则 ID、Schema 路径或向量 ID：
Revision, rule ID, Schema path or vector ID:

### 歧义或缺口 / Ambiguity or gap

至少两个合理但不同的解释是什么？独立实现会因此出现什么不同结果？
What are at least two plausible interpretations and how would independent implementations differ?

### 最小案例 / Minimal case

模拟输入、预期层次和结果；说明现有测试是否通过但没有覆盖此问题。
Synthetic input, expected layer/result and whether existing tests pass while missing this issue:

### 修改建议 / Suggested change

文本澄清、Schema 修订、语义/状态测试或运行层测试；解释为何放在该层。
Text clarification, Schema change, semantic/state test or transport test, and why that layer is appropriate:

不要仅因参考实现这样做就把它当作规范；指出需要维护者裁定的部分。
Do not infer normative behavior solely from the reference implementation; identify decisions requiring review.
