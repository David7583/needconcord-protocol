# v0.1.2 兼容性样本 / Selected compatibility fixtures

这里只包含迁移和版本兼容测试所需的最小历史子集：原 `packet.schema.json`，以及 `intent.publish`、`outcome.no_purchase`、`commerce.example` 三个合成示例。不包含完整研发基线、原压缩包、旧日志或内部环境记录。公开测试和迁移工具仅依赖此目录，无需获取内部档案。

四个 JSON 文件逐字节取自发起者指定的 `ODIP-v0.1.2-complete-draft.zip`，未修改；包内原路径与 SHA-256 见 `manifest.json`。这是兼容性来源记录，不是第三方授权或原创性证明。样例中的身份、用户确认、商品与交易状态均为测试数据。

这些 Schema/测试样例按项目根目录 `LICENSE` 的 Apache-2.0 适用范围处理，仅及于发起者原创或依法有权许可的部分。历史创作链和可能的第三方/AI辅助输入未被完全独立核实；不得据此宣称全部由发起者原创。正式公开仍须由发起者确认授权范围。保留此来源说明与根目录许可文件。

This directory contains only the original packet schema and three synthetic examples needed for explicit migration and version-compatibility tests. The four JSON files are unchanged extracts from the designated v0.1.2 source archive, identified by original archive paths and SHA-256 values in `manifest.json`. No complete private baseline is required to run the public test suite.

The root Apache-2.0 license applies only to content the initiator is entitled to license. Historical authorship and possible third-party or AI-assisted input are not conclusively established by these fixtures. Preserve this notice and the root license; publication requires confirmation of the applicable rights. Example identities and confirmation statements are synthetic, not evidence of real adoption or consent.
