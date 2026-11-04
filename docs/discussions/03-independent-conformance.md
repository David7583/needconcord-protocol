# 讨论 3：怎样证明不同独立实现符合规范？
# Discussion 3: How can different independent implementations demonstrate conformance?

定位 / Scope: NeedConcord Protocol 实验版开放问题；wire `ODIP/0.1.3-exp.1`。Open questions for the experimental protocol; not a normative decision.

当前公开测试候选提供语言无关 JSON 向量、状态序列与外部命令适配接口。本地两进程仍使用同一参考代码库；这不是跨实现证明。我们希望讨论什么证据足以支持范围明确、可复现的符合性声明，也寻找会让当前测试误报成功的案例。

The candidate test suite provides language-neutral JSON vectors, state sequences and an external-command adapter. The local two-process run still uses one reference codebase; it is not cross-implementation evidence. We seek reproducible, scoped evidence criteria and cases that could make current tests report misleading success.

## 分开讨论这些声明 / Distinguish these claims

| 声明 / Claim | 至少应提交的证据 / Minimum proposed evidence |
|---|---|
| Schema 符合 / Schema conformance | 校验器版本、格式断言开启、原始正反结果 / Validator version, format assertions and raw positive/negative results |
| 语义与状态符合 / Semantic/state conformance | 公开单包与序列结果、错误码、拒绝后状态不变 / Vector and sequence output, errors and unchanged state after rejection |
| 本地进程互通 / Local process communication | 两 PID、独立存储、真实序列化通信、故障与重启证据 / Two PIDs, separate stores, serialized communication, failure and restart evidence |
| 跨实现互操作 / Cross-implementation interoperability | 两套独立代码、语言/版本、实际互发、双方观察日志与不一致项 / Independent codebases, languages/revisions, actual exchanges, both observations and discrepancies |
| 真实网络安全 / Real-network security | 单独威胁模型、身份/授权/传输/滥用安全审查和明确范围 / Separate threat model and scoped identity, authorization, transport and abuse review |

这张表是讨论起点，不是认证制度。通过有限测试不证明所有合法输入、所有领域、所有组织或互联网部署都符合。

This table is a starting proposal, not a certification scheme. Passing finite tests does not establish conformance for all inputs, domains, organizations or Internet deployments.

## 请尝试反驳当前测试 / Challenge the current tests

- 两个不同外壳实际都调用参考库，却报告“跨语言实现”。如何合理披露共享组件，又不强制重复造轮子？Two wrappers use the same reference library but claim cross-language independence. How should shared components be disclosed without demanding unnecessary reinvention?
- 对固定向量照抄预期答案，或者只接受样例 UUID，仍能通过有限套件。是否增加种子可复现生成测试、变形测试或双方设计新案例？A hardcoded adapter or sample-ID allowlist passes finite vectors. Should reproducibly generated, metamorphic or peer-designed tests be added?
- 同一消息 key 顺序、空白或数字写法不同，双方对幂等结果不同。当前精确字节重试约定是否足够清晰，是否值得另议规范化？Implementations disagree after key order, whitespace or numeric spelling changes. Is the exact-byte replay rule clear enough, or should canonicalization be separately proposed?
- 一端接受后断线，另一端重试；重启后丢失幂等记录或错误应用状态。哪些故障注入必须有可重复步骤，哪些只能声明未覆盖？One endpoint commits before disconnection and the other retries; restart loses deduplication or reapplies state. Which fault injections need repeatable procedures, and which remain untested?
- Schema 对格式采取注释行为、数字精度截断、未知扩展被误执行，普通正例却都通过。应增加哪些最小反例？A validator treats formats as annotations, truncates decimals or executes unknown extensions while ordinary examples pass. Which minimal counterexamples are missing?

## 提交证据的方式 / How to submit evidence

请公开协议与测试套件提交号、实现来源、所用共享库、可选功能、适配器、重现命令、操作系统/运行时、输入输出与失败项。隐私或知识产权限制导致无法公开源代码时，请说明哪些独立性或可复现性声明因而受限，不能用保密替代证据。

Publish protocol/test revisions, implementation provenance, shared libraries, optional features, adapter, commands, OS/runtime, inputs/outputs and failures. If privacy or IP prevents source disclosure, state the resulting limitations on independence or reproducibility; confidentiality is not a substitute for evidence.

只使用授权的本地或专用测试节点与模拟数据，不要求公开生产端口、真实合同、付款或第三方凭据。发现语义歧义时附双方合理解释；不要仅把参考实现的行为当作裁决。

Use authorized local or dedicated test nodes and synthetic data. No production ports, contracts, payments or third-party credentials are required. For ambiguities, include both plausible interpretations rather than treating reference behavior as the ruling.

## 开放决定 / Open decisions

“独立实现”的最低披露标准是什么？符合性结果应按能力组合还是一个总分展示？失败是否源于测试、规范还是实现？如何防止测试套件成为特定实现的私有准入门槛？是否需要多语言验证者，以及谁能够审核新增向量？

What disclosure establishes implementation independence? Should results be capability-specific or aggregated? Is a failure in the test, specification or implementation? How can the suite avoid becoming one implementation's private gate? Are multiple-language validators needed, and who reviews new vectors?

讨论可以改进测试和声明格式，但不会自动授予第三方认证或官方兼容标志。任何新增规则仍需公开评审与兼容性说明。

Discussion may improve tests and claim formats; it does not award certification or an official compatibility mark. New rules still require open review and compatibility analysis.
