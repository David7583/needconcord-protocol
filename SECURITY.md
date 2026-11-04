# 安全政策 / Security policy

NeedConcord Protocol 是实验协议，当前 wire 标识保留为 `ODIP/0.1.3-exp.1`。参考节点只允许本地回环，不代表生产级身份、加密、授权、隐私合规或互联网抗滥用能力。详细限制见 [安全模型](docs/SECURITY.md) 和 [验证范围](docs/VALIDATION.md)。没有受承诺支持的生产版本；初始维护者为 David7583。

NeedConcord Protocol is experimental and retains the wire identifier `ODIP/0.1.3-exp.1`. Its reference nodes are loopback-only and do not establish production identity, encryption, authorization, privacy compliance or Internet abuse resistance. See the security model and validation scope. No production release has a support commitment. The initial maintainer is David7583.

## 报告敏感问题 / Reporting sensitive issues

私密漏洞报告使用 GitHub 的 **Private vulnerability reporting**。请从项目所在仓库进入 **Security and quality / Security → Advisories → Report a vulnerability**，以实际可见且可打开的报告按钮为准。此文件随源码分发，不能单独证明任何仓库或 fork 已开启该功能。[GitHub 官方报告说明](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately)

Use GitHub **Private vulnerability reporting** through the project's repository: **Security and quality / Security → Advisories → Report a vulnerability**. Use an actually available report button. This file travels with source copies; its presence does not establish that any repository or fork has enabled the feature.

**若按钮不存在或无法使用，不要在公开 Issue、PR 或 Discussions 披露漏洞细节、个人数据、密钥或 token。** 只以不含敏感内容的方式询问维护者可用的私密联系途径，在核验前保留本地证据。本项目未指定独立安全邮箱，不应从用户名推测邮箱或使用占位地址。行为举报另见 [行为准则](CODE_OF_CONDUCT.md)。

**If the button is absent or unusable, do not disclose vulnerabilities, personal data, credentials or tokens in public issues, pull requests or discussions.** Ask only for a working private contact without sensitive details and keep evidence local until verified. No separate security email is designated; do not infer an address from a username or use placeholders. Conduct reports follow the [code of conduct](CODE_OF_CONDUCT.md).

可公开的非敏感加固建议可用普通技术问题模板，说明影响范围和脱敏复现。不得为了证明问题而访问未授权数据或攻击他人节点。维护者在启用社区时必须开启并核验私密报告及通知设置，在真实仓库首发记录中注明核验结果；仅上传本文件不会启用它。[GitHub 配置说明](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)

Non-sensitive hardening suggestions may use the technical issue template with a sanitized reproduction. Do not access unauthorized data or attack other nodes to prove a finding. At community launch the maintainer must enable and verify private reporting and notifications, then record the result in the actual repository's launch record. Uploading this file alone does not enable reporting.

报告建议包含候选版本、受影响规则/组件、威胁模型、最小脱敏复现、预期与实际行为、影响和可行缓解措施。现阶段不承诺固定响应时限、赏金或 CVE 分配。修复应包含回归测试、兼容性说明与适当的协调披露；不要把一次本地测试通过宣传为完整安全审计。

Reports should include candidate revision, affected rules/components, threat model, minimal sanitized reproduction, expected and actual behavior, impact and possible mitigation. No response deadline, bounty or CVE assignment is promised. Fixes should include regression tests, compatibility notes and appropriate coordinated disclosure; a local test pass is not a complete security audit.
