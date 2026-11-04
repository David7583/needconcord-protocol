---
name: 独立实现报告 / Independent implementation report
about: 提交独立实现与互操作证据 / Report independent implementation evidence
title: '[Implementation] '
labels: ''
assignees: ''
---

### 实现来源 / Implementation provenance

名称、语言、版本/提交、可访问源代码或可重复构建说明；哪些部分独立编写，是否使用本仓库参考库？
Name, language, revision, available source or reproducible build; which parts were independently written and whether the reference library is used:

### 声明范围 / Claimed scope

协议版本、核心消息覆盖、可选 commerce/fulfillment 支持及未实现功能：
Protocol version, core message coverage, optional commerce/fulfillment support and omissions:

### 复现证据 / Reproduction evidence

公开向量版本、适配器、命令、环境、原始输出、总数/通过/失败以及失败原因。若做了两实现通讯，列出双方独立代码与实际交换包。
Public vector revision, adapter, command, environment, raw output, totals/passes/failures and reasons. For cross-implementation communication identify both independent codebases and actual exchanged packets.

### 分层结果 / Separate results

| 验证层 / Layer | 通过/失败/尚未验证 / Pass, fail or unverified | 证据 / Evidence |
|---|---|---|
| Schema | | |
| 单包语义 / Stateless semantics | | |
| 本地独立进程 / Local independent processes | | |
| 跨实现互操作 / Cross-implementation interoperability | | |
| 真实网络安全 / Real-network security | | |

明确标注模拟身份与数据，不暗示第三方认证、真实商业接入或独占兼容权。
Label synthetic identities/data and do not imply certification, real commercial adoption or exclusive compatibility rights.
