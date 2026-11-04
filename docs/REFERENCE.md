# 独立进程参考节点

本教程只使用模拟数据、loopback HTTP 和临时测试凭据。两节点采用同一 Python 实现，但进程和 SQLite 存储分离。准备环境后，最短证据命令为：

```powershell
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/demo-02 --report evidence/two-process-evidence.json
```

报告记录实际服务进程 PID、端口、请求 SHA-256、回执、重启与独立数据库统计；不输出 token。测试控制器只发字节请求/读取健康状态并检查数据库证据，不替两个节点直接搬运业务状态或共享 Python 对象。

## 手工启动

先在已解压或检出的仓库根目录准备新配置：

```powershell
.\.venv\Scripts\python.exe scripts/prepare_local.py
```

终端 A：

```powershell
.\.venv\Scripts\python.exe -m odip.node serve --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --port 8761
```

终端 B：

```powershell
.\.venv\Scripts\python.exe -m odip.node serve --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --port 8762
```

第三个终端按顺序发送（发送 CLI 与本节点服务共享**本节点**数据库，不与另一节点共用）：

```powershell
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --peer test-node-b --message runtime/manual/intent.publish.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --peer test-node-a --message runtime/manual/proposal.goods.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/b.local.json --db runtime/manual/b.sqlite3 --peer test-node-a --message runtime/manual/proposal.nontransaction.json
.\.venv\Scripts\python.exe -m odip.node send --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --peer test-node-b --message runtime/manual/outcome.no_purchase.json
```

每个 HTTP 响应是 Schema 定义的 `receipt.ack`，不代表成交或事实认证。再次发送未修改的同一文件返回 duplicate；用同 ID 修改内容被拒绝。重启 B 并保留其数据库，再发原文件仍为 duplicate。

## 失败恢复和导出

连接失败或超时保留 durable outbox。恢复对端后，手动执行：

```powershell
.\.venv\Scripts\python.exe -m odip.node retry --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3
.\.venv\Scripts\python.exe -m odip.node export --config runtime/manual/a.local.json --db runtime/manual/a.sqlite3 --output runtime/manual/export.json
```

重试使用原始 UTF-8 字节，不重新格式化消息。成功回执丢失时，重试应得到 duplicate 并完成 outbox。永久拒绝保留 rejected 记录，不无限循环重试；操作者须理解原因，修复前序或配置后可显式 send 原文件，或按当前修订状态构造新消息。本地发送状态不会因远端拒绝自动回滚。导出文件必须不存在，含已授权本地数据，默认不通过网络提供。此原型不提供导入/删除/保留周期管理，不宣称已实现完整数据迁移或隐私撤回执行。

消息须通过字节层、Schema、跨字段语义、当前状态与授权校验。`private` 意图不允许跨节点发送；selected 授权由操作者配置，声明本身无法证明现实用户同意。未知扩展按规范忽略业务含义，已知 commerce 扩展校验但从不执行收费。

Ctrl+C 停止节点。不要开放公网端口、建立隧道或将此 HTTP/静态测试 token 用作生产安全方案。详见 [安全模型](SECURITY.md)。
