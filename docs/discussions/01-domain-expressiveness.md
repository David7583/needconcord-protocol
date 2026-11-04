# 讨论 1：核心消息能否表达不同领域的需求？
# Discussion 1: Can the core express needs across domains?

定位 / Scope: NeedConcord Protocol 实验版开放问题；wire `ODIP/0.1.3-exp.1`。Open questions for the experimental protocol; not a normative decision.

我们希望 NeedConcord Protocol 能让不同参与者交换需求、能力、提案和结果，但现在的示例与本地验证不足以证明它适合所有领域。这篇讨论邀请找出表达失败或产生歧义的案例，不寻求对现有设计的默认认可。

NeedConcord Protocol aims to let different participants exchange needs, capabilities, proposals and outcomes. Current examples and local tests do not establish that it works in every domain. This discussion asks for failures and ambiguities, not automatic endorsement of the present design.

## 当前可以检查什么 / What can be inspected now

当前候选含七种核心消息，另有可选履约报价。需求原话、期望结果、约束、替代性、隐私范围和准备度可以交换；需求满足与交易状态分开；方案可为商品、服务、定制、非交易或无匹配。公开 Schema、单包与状态向量能验证这些结构与一部分语义，不验证领域知识或真实效果。

The candidate has seven core messages and optional fulfillment quotations. It exchanges original wording, desired outcomes, constraints, alternatives, privacy and readiness; need and transaction states remain separate. Solutions may involve goods, services, customization, non-transactional paths or no match. Public tests check these structures and some semantics, not domain expertise or real outcomes.

## 请尝试击穿这些表达 / Try these counterexamples

- **社区互助 / Community assistance:** 一名居民希望有人陪同办事，不涉及采购；时间、无障碍需求和私密联系信息能否最小披露？有人提供帮助但本人认为需求未解决，该如何记录？A resident seeks accompaniment without a purchase. Can timing and accessibility be represented without exposing private contact details? What if help occurs but the resident remains unsatisfied?
- **工业定制 / Industrial customization:** 多项尺寸存在公差、相互依赖和保密限制；提案只满足部分需求。自由文本与 specifications 对象足够互操作，还是只让双方“都能存储”但无法理解？Specifications include tolerances, dependencies and confidentiality; a proposal satisfies only some requirements. Do free text and an opaque specifications object enable understanding, or merely storage?
- **学习与研究协作 / Learning and research:** 结果可能是更好的问题定义、未得到答案或共享知识，无法用成交衡量。四种 need_status 是否过粗？An outcome may refine the question, leave it unanswered or share knowledge without a transaction. Are the four need states too coarse?
- **分阶段服务 / Staged services:** 同一需求同时有多个参与者、子目标、进度与相反反馈，单 owner 严格顺序配置是否遮蔽合法协作？Multiple participants and subgoals produce progress and conflicting feedback. Does the single-owner ordered profile exclude legitimate collaboration?

这些是测试问题，不代表协议已支持对应领域，也不要求把任何领域的敏感数据公开。不要用未经专业验证的医疗、法律或高风险建议作为“已满足”的证据。

These are test questions, not claims of support. Do not share sensitive domain data or treat unverified high-stakes advice as evidence of satisfaction.

## 有价值的提交方式 / Useful submissions

请给出：①明确标注的模拟场景与原话；②拟编码的 JSON；③每个字段的含义和必须依赖的背景知识；④两个独立阅读者可能得出的不同解释；⑤当前公开测试的结果；⑥最小改进建议与不改核心的替代方案。

Provide: (1) a labeled synthetic scenario and original wording; (2) proposed JSON; (3) each field's meaning and required background knowledge; (4) differing interpretations by independent readers; (5) current public test results; and (6) a minimal improvement plus an alternative that leaves the core unchanged.

一个 Schema 有效但语义无法互通的包，同样是重要反例。也欢迎证明不需要新字段：说明现有字段如何无损表达、接收方如何验证，而不是只展示参考实现能接受它。

A Schema-valid packet that cannot be understood interoperably is a useful counterexample. Evidence that no new field is needed is equally welcome: explain lossless representation and receiver validation, not merely reference acceptance.

## 未定问题 / Open questions

核心是否只保证可验证地交换声明，还是应保证更多可计算的领域含义？哪些缺口应成为可选领域扩展？是否需要多结果、多作者或子需求关系；它们会怎样影响隐私、撤回与状态冲突？哪些新增复杂性会让第一阶段更难独立实现？

Should the core guarantee exchange of verifiable declarations only, or more computable domain meaning? Which gaps belong in optional domain extensions? Are multiple outcomes/authors or sub-needs necessary, and how would they affect privacy, withdrawal and conflicts? Which complexity would make first-stage independent implementation harder?

讨论结果将整理为证据与未决问题；只有经过 RFC、兼容性分析、公开测试和维护者审核的变更才可能进入后续候选。赞同人数不自动决定规范。

We will record evidence and unresolved issues. Only reviewed changes with an RFC, compatibility analysis and tests may enter a later candidate. Votes do not amend the specification.
