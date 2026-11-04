# 版本与迁移

**简体中文** | [English](MIGRATION.en.md)

公开名称为 **NeedConcord Protocol**，历史工作名为 Open Demand Interoperability Protocol（ODIP）。本次名称调整只影响文档展示与发布包名称；wire 标识仍为 `ODIP/0.1.3-exp.1`，Schema 标识、消息字段、测试数据及 `odip` Python 模块均不改名。已经使用该 wire 版本的实现无需为公开名称变更转换消息；不要替换存储消息中的 `ODIP` 字样或改变原字节摘要。未来如统一机器标识，将另行定义版本、迁移步骤与兼容性测试。

本次从 `ODIP/0.1.2` 草案修订，实验版 wire 标识为 `ODIP/0.1.3-exp.1`，Python 工程版本映射为 `0.1.3.dev1`。完整历史档案由维护者离线保留；公开包中的 `tests/fixtures/v0.1.2/` 提供迁移所需最小旧版 Schema 与模拟输入。

候选对一部分原 Schema 接受的输入收紧校验，**不是透明兼容补丁**。0.x 实验版允许显式记录破坏性验证变化；原版节点必须明确拒绝不支持的版本，新节点也不自动接受原版。没有协商或字段猜测。具体字段/语义变化与影响见 [修订表](docs/PROTOCOL-DELTA.md)。原 v0.1.2 之前的 IRP/ODIP 仍不自动兼容。

保守迁移工具只在旧 Schema 与新无状态校验均通过时替换协议标识，并写入全新文件：

```powershell
.\.venv\Scripts\python.exe scripts/migrate.py tests/fixtures/v0.1.2/examples/intent.publish.json .tmp/migrated-intent.json
```

源文件永不修改、目标存在则拒绝。缺失关联 ID、非候选 UTC 格式、未知证据/过度分账等必须人工审查；工具不会造 ID、改原话、捏造用户确认或推断授权。此转换只是无状态验证，不证明目标节点存在相关意图、发布者权限或用户真实授权。迁移后的消息是新版本交换，原始 byte digest 变化；不得拿它当原版的重试。

实现者升级建议：先存档版本与原字节；离线运行两个版本的公开校验；人工处理拒绝项；双方显式启用候选版本；在独立状态空间重放经过审查的生命周期；保留失败与转换记录。不要把生产数据库原地批量改版。

分账 `share_rate` 候选沿用原例含义：与 `fee_rate` 共用基数，合计不超过总费率；不是“服务费收入的百分比”。另一种含义应新扩展/新字段，不可复用现字段。只披露不收费，`consent_recorded=false` 可以披露未获同意，但不得执行收费。这项解释及状态权限策略可通过公开 RFC 提出修订，兼容性影响必须明确说明。
