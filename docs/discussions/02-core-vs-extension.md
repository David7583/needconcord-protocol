# 讨论 2：哪些字段属于核心，哪些应放入扩展？
# Discussion 2: Which fields belong in the core or an extension?

定位 / Scope: NeedConcord Protocol 实验版开放问题；wire `ODIP/0.1.3-exp.1`。Open questions for the experimental protocol; not a normative decision.

核心越大，实现成本和兼容性负担可能越高；核心过小，双方又可能各自发明语义，无法互通。当前候选关闭核心对象的未知字段，允许忽略未知非关键 extensions；尚无关键扩展协商。这个边界是否合适，需要具体反例与独立实现反馈。

A larger core can increase implementation and compatibility costs; an underspecified core can cause incompatible meanings. The current candidate rejects unknown core fields and permits ignoring unknown noncritical extensions. It does not define critical-extension negotiation. This boundary needs counterexamples and implementation evidence.

## 当前边界 / Present boundary

需求原话、关联、准备度、隐私声明、提案类型与独立结果状态属于核心；commerce 披露与 fulfillment.quote 为可选。支持一个扩展的实现必须验证它，未知扩展不能改变核心含义、执行脚本或提升权限。参考实现支持可选功能，不等于核心符合性要求所有实现都支持它们。

Original wording, relationships, readiness, privacy declarations, proposal types and separate outcome states are core. Commerce disclosure and fulfillment quotations are optional. Implementations claiming an extension must validate it. Unknown extensions cannot alter core meaning, run scripts or grant authority. Reference support does not make optional features mandatory for all core implementations.

## 需要反例的边界 / Boundaries to challenge

- **证据引用 / Evidence references:** confirmed 目前要求说明文本，但可验证证据引用可能含访问控制与个人数据。它是否应成为核心必需字段、标准可选扩展，还是保持领域自定？Confirmed currently requires explanatory text. Verifiable evidence references can reveal protected data. Should references be mandatory core, a standard optional extension or domain-defined?
- **授权与接收者 / Authorization and recipients:** 本地 selected allowlist 不构成跨组织用户授权证明。将接收者列表放入消息会不会泄露参与关系？不放会不会无法审计？A local allowlist does not prove user consent across organizations. Would wire recipient lists expose relationships, and would omitting them prevent audit?
- **商业分账 / Revenue disclosure:** 同基数费率还是收入份额必须讲清楚，但是否需要在基本需求收发中出现？一个完全无交易实现应该能忽略多少？Split semantics must be explicit, but how much belongs in basic demand exchange? How much can a wholly non-transactional implementation ignore?
- **单位、位置与分类 / Units, locations and taxonomies:** 过度自由字段可能不可比；绑定某个商业分类库又可能形成锁定。怎样使可选词汇可验证且不强制中心？Free-form data may not be comparable; a mandatory commercial taxonomy can create lock-in. How can optional vocabularies remain verifiable without a mandatory center?

## 评估同一提案的三个选择 / Compare three choices for each proposal

1. 不修改核心，以文档约定或现有字段表达。说明接收方能否无损理解和验证。Leave the core unchanged and use documented conventions or existing fields; explain lossless understanding and validation.
2. 使用可选、具备版本和 Schema 的扩展。说明缺失或不认识时的安全退化；不能把非关键标签用于偷偷传递关键授权。Use a versioned optional extension with a Schema; define safe degradation when absent or unknown. Do not hide critical authorization in a noncritical extension.
3. 修改核心并发布新实验版本。证明为何所有核心实现都必须承担成本，列出旧生产者/消费者组合和迁移失败场景。Amend the core with a new experimental version; justify why all core implementations need it and document old/new interactions and migration failures.

请附同一场景在三种选择下的包、预期结果、隐私影响及测试向量。没有安全退化路径可能支持核心化，也可能说明该领域应保持独立协议；本讨论不预设哪种结论。

Submit packets, expected results, privacy effects and vectors for the same scenario under all three choices. A missing safe fallback might favor a core requirement, or indicate a separate protocol. Neither conclusion is predetermined.

## 希望获得的证据 / Evidence requested

独立实现所需的最小代码与依赖、另一语言能否理解、扩展缺失时是否仍能完成需求表达、未知扩展是否泄露或改变状态、谁控制命名空间与版本。不要用“已经有某平台字段”作为它必须进核心的理由，也不要以抽象通用性掩盖实际无法互通。

Provide implementation and dependency costs, interpretation in another language, behavior without the extension, unknown-extension effects on data/state, and namespace/version ownership. Existing platform fields do not automatically belong in the core; abstract generality is not evidence of interoperability.

讨论后应形成可审核的候选 RFC 或保留问题。用户授权、隐私及免费开放协议原则不能靠多数投票取消。

The outcome may be a reviewable RFC or an unresolved issue. Votes cannot waive authorization, privacy or free/open protocol principles.
