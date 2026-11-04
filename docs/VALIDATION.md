# 验证范围 / Validation scope

**简体中文** | [English](VALIDATION.en.md)

公开名称与版本：**NeedConcord Protocol 0.1.3-exp.1**（Experimental Draft / Pre-release）；wire 标识：`ODIP/0.1.3-exp.1`。本目录与 `evidence/` 描述经审查公开文件树的实际运行结果，不要求读者获取内部研发档案。公开名称调整没有修改 Schema、消息字段或符合性规则。

| 声明 / Claim | 状态 / Status |
|---|---|
| 已通过 Schema 验证 / Schema validation | 以本包 `evidence/verification-run.json` 的成功退出码和公开向量结果为依据，覆盖全部核心类型及声明支持的扩展。 |
| 已通过本地独立进程验证 / Local independent processes | 使用同一 Python 实现的两个实际服务进程、独立 SQLite、loopback HTTP；原始事件见双进程证据。 |
| 已通过真实网络安全验证 / Production network security | **尚未验证 / Not verified**。无公网认证、TLS 或生产安全审计结论。 |
| 已通过跨实现互操作验证 / Cross-implementation interoperability | **尚未验证 / Not verified**。两个进程不等于两个独立实现。 |
| 尚未验证 / Other unverified areas | 真实用户授权、外部来源及交易事实、删除传播、持续攻击/容量与完整供应链审计等。 |

公开证据：

- [完整执行命令与退出码](../evidence/verification-run.json)
- [工程测试 JUnit](../evidence/pytest.xml)
- [完整符合性配置](../evidence/conformance-run.json)、[核心配置及明确跳过项](../evidence/conformance-core-run.json)
- [本地双进程、回执、重启与恢复](../evidence/two-process-evidence.json)
- [父进程代码覆盖数据](../evidence/coverage.json)

报告中的路径、机器名与运行时测试凭据经过脱敏；用例判定、错误码、时间与计数保留。所有身份、需求、商品与交易描述均为模拟数据。回执及 `user_confirmed` 字段不是实际用户同意证明。父进程覆盖数据不采集参考节点和适配器子进程，不能解释为全系统覆盖率。

在支持的 Windows x86_64 / CPython 3.12.7 环境，安装哈希锁定依赖后运行：

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
```

Public evidence covers this exact source snapshot. Reports omit local machine identities, absolute paths and generated test credentials, while retaining actual outcomes. The public package contains a small attributed v0.1.2 compatibility fixture subset; it does not require private archives, complete historical baselines or local Git history. See the [conformance contract](../conformance/README.md) for independent implementations and the [security model](SECURITY.md) for limitations.
