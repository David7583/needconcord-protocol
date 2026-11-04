# NeedConcord Protocol 0.1.3-exp.1 — Experimental Pre-release

定位：Experimental Draft / Experimental Pre-release。本版本不是正式标准、行业认证或生产商业网络。

公开名称采用 **NeedConcord Protocol**，历史工作名为 Open Demand Interoperability Protocol（ODIP）。机器协议标识继续使用 **`ODIP/0.1.3-exp.1`**。名称调整不改变 Schema 标识、消息字段、测试向量、`odip` 模块或既有协议规则；无需为此转换已存消息。未来如修改机器标识，须通过正式版本迁移。

本次从指定 v0.1.2 原包验证协议是否可以由别人阅读、独立实现并公开自测。交付中文规范、Schema、全部核心消息类型正反样例、公开语义/状态测试、外部适配器接口及最小双进程参考节点。

`ODIP/0.1.3-exp.1` 使用独立版本标识，因为接收集合收紧且补充状态/权限/幂等约定。旧包不自动兼容，必须按 MIGRATION.md 审查。新版本没有增加协议税、中心依赖、支付执行或永久买卖角色；无交易方案可以满足需求，交易确认不自动表示需求解决。

本公开候选的实际验证范围见 [VALIDATION](VALIDATION.md)，执行结果位于 `evidence/`。同一 Python 实现的两个独立进程经过真实 loopback socket 交换、各自持久化并恢复；没有跨语言/跨团队实现互通证据，也没有公网安全验证。样例与身份全部模拟。

商业扩展只做披露；同基数分账约束是本候选的显式解释，不产生收费权。隐私声明不等于真实用户授权，HTTP测试 token 不等于生产身份。存储保留历史、尚无删除传播和真实个人数据治理能力。

GitHub 社区采用维护者主导开放治理，提供中英文 Issue/PR/RFC 模板和三个实质讨论材料。核心变更必须公开讨论、评估兼容性、提供测试并经维护者审核，投票不自动修改规范。社区分类和报告渠道见 [社区说明](COMMUNITY.md)、[安全报告](../SECURITY.md) 与 [行为准则](../CODE_OF_CONDUCT.md)；功能可用性以仓库实际设置为准。

许可依可授权范围区分 Apache-2.0（代码/Schema/测试）和 CC BY 4.0（原创文档）。项目发起者与初始维护者展示署名为 David7583；研究、编写和验证使用了 AI 辅助，不存在对全部历史及第三方内容确定或独占著作权的保证。来源与第三方许可见 [PROVENANCE](PROVENANCE.md)、[NOTICE](../NOTICE.md) 和 [依赖清单](../LICENSES/dependency-licenses.json)。

源码包只包含经审查的规范、Schema、参考实现、测试、示例、许可证、社区材料和脱敏验证证据。逐文件 SHA-256 见包内 `PUBLIC-MANIFEST.json`；完整原始草案、内部审计资料、个人环境记录与本地 Git 历史不在公开包内。
