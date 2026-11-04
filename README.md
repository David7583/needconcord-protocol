# NeedConcord Protocol（NCP）

开放需求互操作协议。**版本 `0.1.3-exp.1`，Experimental Draft / Experimental Pre-release。** 公开名称为 **NeedConcord Protocol**；沿用已验证的机器协议标识 **`ODIP/0.1.3-exp.1`**。

**验证状态：已通过 Schema 验证和本地独立进程验证；生产网络安全与跨实现互操作尚未验证，未宣称通过。** 实验版结果为 91/91 工程测试、53/53 完整符合性、42/42 核心符合性（另 11 项可选能力跳过）。证据对应已发布的 `v0.1.3-exp.1` 快照，见 [验证范围](docs/VALIDATION.md)。

本项目从 Open Demand Interoperability Protocol（ODIP）草案演进而来。本次只调整公开名称和文档展示；Schema 标识、消息字段、`odip` Python 模块及命令保持不变，文中的 ODIP 技术简称仍指同一协议。名称不构成商标排他权或第三方认可声明；未来若调整 wire 标识，将通过明确版本和迁移规则进行。

项目发起者与初始维护者 / Project Initiator and Initial Maintainer：**David7583**。研究、编写和验证过程中使用了 AI 辅助；具体版权范围见 [NOTICE](NOTICE.md)，不把全部历史或第三方材料宣称为发起者独有。

第一阶段交付：一份别人能够阅读、遵循、独立实现，并通过公开测试验证是否符合规范的开放协议。协议交换需求、能力、提案、需求结果与回执；商品、服务、定制与非交易解决方案都可参与。

需求表达不等于采购承诺；需求满足与交易状态相互独立。协议免费，不要求中心节点、平台账号、指定运营商或协议税。用户原话应保留，推断、确认与核验事实应区分。商业服务可自愿收费。本项目独立于 CONTINUUM 及具体需求端产品。

## 从规范开始

- [中文规范及确定性规则](SPEC-zh-CN.md)、[机器可读 Schema](schemas/packet.schema.json)
- [公开符合性测试与外部实现接口](conformance/README.md)：JSON 向量、状态序列、实现无关执行器
- [版本迁移](MIGRATION.md)、[修订明细](docs/PROTOCOL-DELTA.md)、[变更记录](CHANGELOG.md)
- [参考节点与运行教程](docs/REFERENCE.md)、[环境与复现](docs/ENVIRONMENT.md)
- [安全模型与限制](docs/SECURITY.md)、[公开候选验证范围与证据](docs/VALIDATION.md)

## 本地验证

在 Windows x86_64、CPython 3.12.7 下：

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/demo-01 --report evidence/two-process-evidence.json
```

本地演示启动两个真实 Python 进程，使用不同 SQLite 文件，经 loopback HTTP 传输 UTF-8 JSON。支持重复、冲突、失败重试、丢失回执和重启恢复。示例身份、商品与服务均为模拟数据；两个进程共用同一参考实现，**不构成跨实现、跨组织或互联网安全验证**。公开测试可以交由其他语言或团队的适配器执行，无需复制参考实现。

本候选从发起者提供的 v0.1.2 草案继续修订。完整原始档案与内部审计由维护者离线保留，不作为公开仓库的默认内容。公开源码只携带迁移测试所需的最小旧版 Schema 与模拟数据，见 [夹具来源](tests/fixtures/v0.1.2/README.md)；第三方运行符合性测试不需要取得内部档案。实验候选拒绝一部分原 Schema 接受的输入，因此使用新 wire 标识，不自动声称与 v0.1.2 互通。

## 贡献、治理和许可

中文和英文贡献均可，见 [贡献指南](CONTRIBUTING.md)、[治理](GOVERNANCE.md)、[行为准则](CODE_OF_CONDUCT.md)、[安全报告](SECURITY.md)。GitHub 社区分类与三项开放讨论见 [社区说明](docs/COMMUNITY.md)；功能可用性以仓库实际设置为准。核心规范变更需公开讨论、兼容性分析、测试和维护者审核。

对发起者原创或依法有权授权的内容：代码、Schema、参考实现、测试采用 [Apache-2.0](LICENSE)；原创规范与技术文档采用 [CC BY 4.0](LICENSE-DOCS.md)。第三方材料保留原许可，完整适用范围与 AI 辅助来源限制见 [NOTICE](NOTICE.md) 和 [来源记录](docs/PROVENANCE.md)。这不是对所有材料著作权归属的无条件保证。

## English

NeedConcord Protocol is an experimental, demand-first, role-neutral protocol for exchanging intents, capabilities, proposals, outcomes and receipts. Its former working name was Open Demand Interoperability Protocol (ODIP); the wire identifier remains `ODIP/0.1.3-exp.1`. The public-name change does not alter schemas, messages or the `odip` module. It requires no central operator or mandatory protocol fee. Demand fulfillment and transaction status are independent. Start with the JSON schemas and [public conformance contract](conformance/README.md); Chinese is the current normative prose, and bilingual questions/contributions are welcome. David7583 is the Project Initiator and Initial Maintainer. AI assisted research, drafting and validation; this does not establish exclusive ownership of every historical or third-party contribution. The local two-process Python demo is not evidence of independent implementations or production network security.
