# NeedConcord Protocol 社区 / Community

社区首先依托 GitHub，欢迎中英文参与，不另建论坛或社区网站。Issue、PR、Discussions 与报告入口的可用性以所在仓库的实际配置为准；源码中的模板不证明入口已经启用。公开名称为 NeedConcord Protocol，当前机器协议标识仍为 `ODIP/0.1.3-exp.1`。

The community starts on GitHub and welcomes Chinese and English participation, without a separate forum or website. Issues, pull requests, discussions and reporting depend on the repository's actual configuration; source templates do not establish active channels. The public name is NeedConcord Protocol; the wire identifier remains `ODIP/0.1.3-exp.1`.

发起者与初始维护者为 David7583，采用维护者主导的开放治理，随社区发展调整。仓库拥有者身份不自动赋予对所有贡献的著作权。

David7583 is the project initiator and initial maintainer. Governance begins as maintainer-led and open to future evolution. Repository ownership does not transfer copyright in other contributions.

## 拟用 Discussions 分类 / Proposed Discussions categories

| 分类 / Category | 目的 / Purpose | 推荐形式 / Suggested format |
|---|---|---|
| Announcements / 公告 | 经审核的版本、规范与治理决定 / Reviewed releases and decisions | 公告 / Announcement |
| Specification / 规范讨论 | 核心语义、领域表达和 RFC 前置讨论 / Semantics, domain expression and RFC preparation | 开放讨论 / Open discussion |
| Extensions / 可选扩展 | 扩展边界、命名、降级和互通 / Boundaries, names, degradation and interoperability | 开放讨论 / Open discussion |
| Implementations / 独立实现 | 实现经验、符合性报告和最小互通 / Implementation experience and evidence | 开放讨论 / Open discussion |
| Questions / 问答 | 读规范、运行测试、适配器问题 / Reading, testing and adapters | 问答 / Q&A |
| Governance / 治理 | 贡献流程、利益披露与审议记录 / Contribution process, interests and decisions | 开放讨论 / Open discussion |

缺陷、可执行修改任务和审阅应落到 Issues/PR；讨论用于探索问题，不自动成为规范。敏感漏洞和行为投诉不能放入公开讨论。私密漏洞报告和行为举报具有不同的接收方与范围，见下方政策。

Use issues and pull requests for defects, actionable changes and review. Discussions explore questions and do not amend the specification automatically. Keep sensitive vulnerabilities and conduct complaints out of public discussions. Vulnerability and conduct reports have different recipients and scopes; follow the policies below.

## 三个开放讨论草稿 / Three open discussion drafts

1. [跨领域需求表达是否充分 / Domain expressiveness](discussions/01-domain-expressiveness.md)
2. [哪些字段属于核心或扩展 / Core versus extension](discussions/02-core-vs-extension.md)
3. [怎样证明不同独立实现符合 / Independent conformance evidence](discussions/03-independent-conformance.md)

草稿包括反例、证据请求与开放选择，不预设结论。实际发布时应保留当地讨论语言并提供中英文摘要；参与者可以任一语言提供证据。维护者应避免把“能跑示例”说成“适合所有领域”，也不能把未参与组织写入兼容或采用名单。

The drafts ask for counterexamples, evidence and choices without predetermined conclusions. Preserve contributors' language and provide Chinese/English summaries where practical. Do not infer universal domain coverage from sample execution, or list uninvolved organizations as adopters.

## 审阅与私密安全入口 / Review and private security reporting

核心规范变更必须关联公开问题或 RFC，说明兼容性、替代方案与正反测试，由维护者审核并记录决定。投票不会自动修改规范。独立实现报告需声明语言、版本、共享库、适配器、原始结果与未验证范围；维护者记录证据不等于第三方认证。

Core changes require a public issue or RFC, compatibility analysis, alternatives, positive/negative tests and a recorded maintainer decision. Votes do not amend the specification. Independent implementation reports must identify language, revision, shared libraries, adapter, actual results and unverified areas; recording evidence is not certification.

敏感漏洞使用实际启用的 GitHub 私密漏洞报告入口，按钮不可用时不要公开细节，见 [SECURITY.md](../SECURITY.md)。普通 Issue、PR 和 Discussions 不接收密钥、真实个人数据或未脱敏漏洞利用材料。首期平台违规行为举报直接提交 GitHub Support；这不是项目维护者私密收件箱，其他投诉的渠道限制见 [行为准则](../CODE_OF_CONDUCT.md)。不能冒用漏洞报告表单处理一般行为投诉。

Use an actually enabled private vulnerability-reporting channel and do not disclose details publicly if its button is unavailable. Ordinary issues, pull requests and discussions must not contain credentials, personal data or sensitive exploit details. Initial reporting of platform misconduct goes to GitHub Support, not a confidential project inbox. See the code of conduct for limits on other complaints. Do not use vulnerability reports for general conduct complaints.
