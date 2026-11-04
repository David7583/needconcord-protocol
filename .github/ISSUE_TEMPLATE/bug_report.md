---
name: 技术缺陷 / Technical bug
about: 报告可复现的非敏感实现或规范缺陷 / Reproducible non-sensitive defects
title: '[Bug] '
labels: ''
assignees: ''
---

请勿公开漏洞利用细节、私人需求或凭据；敏感问题先阅读 SECURITY.md。
Do not include exploit details, private demand text or credentials; read SECURITY.md for sensitive findings.

### 版本与环境 / Version and environment

协议标识、实现名称与提交、语言/解释器、系统、可选扩展：
Protocol, implementation revision, language/runtime, OS and optional extensions:

### 最小复现 / Minimal reproduction

使用模拟数据，列出可直接运行的命令及最小消息（必要时附独立文件）。
Use synthetic data and provide exact commands and minimal packets.

### 预期与实际 / Expected and actual

引用规范规则 ID、预期错误或状态、实际输出及影响。
Include normative rule IDs, expected codes/states, actual output and impact.

### 证据与范围 / Evidence and scope

- [ ] 数据已脱敏 / Data is sanitized.
- [ ] 已说明是真实运行还是推测 / Actual execution is distinguished from inference.
- [ ] 未把同一参考库的多个进程称为跨实现 / Multiple reference processes are not called independent implementations.

相关日志、发生频率、受影响消息类型、可能回归版本：
Logs, frequency, affected message types and possible regression revision:
