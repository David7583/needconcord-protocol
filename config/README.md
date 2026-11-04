# 配置边界

**简体中文** | [English](README.en.md)

配置仅在本地生成：`python scripts/prepare_local.py` 写入被 Git 忽略的 `runtime/manual/`。

配置字段：`participant_id` 是本地测试身份；`peers` 将对端 ID 映射到 `url` 与随机 `token`；`selected_recipients` 是允许发送 `selected_participants` 需求的显式清单。URL 只允许 `http://127.0.0.1:端口`，token 仅测试，不是生产凭据或身份体系。

不提交生成的 token、配置、数据库和导出记录。不预置通用共享密码；不改其他项目或全局配置。配置文件由本地操作者提供，不能从不可信消息动态加载。
