# 参与贡献 / Contributing

NeedConcord Protocol 当前为实验性协议，沿用 `ODIP/0.1.3-exp.1` wire 标识。欢迎规范、Schema、语言无关测试、独立实现、文档与安全建议。贡献目标是让他人能够阅读规范、独立实现并验证符合性，不要求接入某个产品或运营商。社区入口和可用状态以托管仓库为准。

NeedConcord Protocol is experimental and retains the `ODIP/0.1.3-exp.1` wire identifier. Contributions should help others read, implement and test the protocol independently. No operator, product integration, paid account or central service is required. Check the hosting repository for available community entry points.

## 开始前 / Before you start

1. 阅读 [规范](SPEC-zh-CN.md)、[商业边界](BUSINESS-BOUNDARY.md)、[治理](GOVERNANCE.md)、[许可证来源记录](docs/PROVENANCE.md) 和 [行为准则](CODE_OF_CONDUCT.md)。Read the specification, boundaries, governance, provenance and code of conduct.
2. 检查现有问题与公开讨论，说明可复现问题或希望解决的互操作障碍。提出方案时同时提交反例和影响范围。Describe a reproducible issue or interoperability gap, with counterexamples and affected implementations.
3. 大的规范变更先使用 [RFC 模板](docs/rfcs/0000-template.md)，不要把实现便利当作改变核心原则的理由。Use the RFC template before major specification changes; implementation convenience does not override protocol principles.
4. 从独立分支提交最小相关改动，运行 README 的验证命令，附原始输出与环境。Submit focused changes and include actual validation output and environment information.

## 必需证据 / Required evidence

涉及消息格式、状态语义或错误行为的改动，必须列出规范条款、修改前后案例、向后/向前兼容影响、迁移方法以及正反测试。修改文字也要检查 Schema、公开向量与参考实现是否一致。只修文档错字不要求增加镜像实现的测试。

Changes to message shape, state semantics or errors must identify normative clauses, before/after examples, backward and forward compatibility, migration and positive/negative tests. Check consistency across prose, schemas, public vectors and implementation. Typographic corrections do not need redundant tests.

独立实现报告必须声明语言、实现版本、实际执行命令、支持的可选能力及未验证项目。两份进程使用同一参考库不能当作跨实现证据。可使用模拟身份与数据，但必须标明；不要提交个人需求原文、生产业务数据、密钥、token、私有合同或未获许可的样例。

Independent implementation reports must identify language, revision, actual commands, optional capabilities and unverified areas. Two processes sharing the reference code do not establish cross-implementation interoperability. Label synthetic data and exclude personal demand text, production data, credentials, private contracts and unlicensed examples.

## 许可与来源 / Licensing and provenance

拟提交的代码、Schema、测试按仓库 Apache-2.0 范围；有权授权的原创文档按 CC BY 4.0 范围。提交者必须有权提供该贡献并如实说明第三方来源、原许可和修改。AI 辅助内容应披露使用范围，并由提交者核查来源、准确性及权利；AI 辅助不自动证明无侵权或归属完备。不得把未知来源材料标为原创。

Contributions follow the repository's applicable Apache-2.0 scope for code, schemas and tests, and CC BY 4.0 scope for authorized original documentation. Contributors must have the right to submit their work and disclose third-party sources, licenses and modifications. Disclose the scope of AI assistance and review accuracy, provenance and rights; AI assistance does not establish clear title. Do not label unknown-source material as original.

贡献不会授予赞助商技术否决权，也不会自动授予规范维护权。维护者可要求补充证据、拆分变更、公开讨论或暂缓合并。安全问题使用 [安全政策](SECURITY.md)，不要在公开 Issue 放入可利用细节或秘密。

Contributions do not grant sponsors a veto or confer maintainership automatically. Maintainers may request evidence, smaller changes, discussion or deferral. Follow the security policy for sensitive findings.
