# NeedConcord Protocol 公开符合性测试资产

**简体中文** | [English](README.en.md)

本目录面向独立实现者。测试数据全部为模拟数据；身份、商品、报价与确认声明均不代表真实组织接入。公开名称为 NeedConcord Protocol，协议 wire 标识保留 `ODIP/0.1.3-exp.1`。文本合同见 [规范第 15 节](../SPEC-zh-CN.md)，结构合同见 [packet Schema](../schemas/packet.schema.json)。这些是实验版公开符合性测试资产。授权边界见 [来源记录](../docs/PROVENANCE.md)。

不要求使用 Python 实现协议；JSON 测试数据与预期结果不导入参考实现。`manifest.json` 中：

- `vectors`：`id` 为稳定案例名称；`file` 相对此目录；`layer` 是 schema 或 semantic；`schema_valid` 是单独结构层预期；`expected_code=null` 表示指定层接受；`rule` 对应规范规则；`requires` 列出该例依赖的可选 commerce/fulfillment 支持，空数组表示核心。
- `sequences`：文件中每例从空状态开始，按 `steps` 顺序处理。`packet` 是消息，`principal` 是外部测试夹具已认证的身份；每步的 `expected_status` 为 accepted/rejected/duplicate，`expected_code` 是错误或 null。身份认证不来自消息自报。序列的 `requires` 包含其中任何步骤依赖的可选能力；`core-lifecycle` 不要求履约扩展。
- 语义单包案例不要求建立业务历史；序列才验证已发布意图、权限和修订。这避免把 UNKNOWN_INTENT 当成结构校验失败。

文件集包含八种消息类型各自的有效与无效包、缺失关联、格式日期、跨字段冲突、推断不当断言、商务扩展约束、隐私范围以及生命周期、重复与冲突、授权、撤回和未知引用。更多网络故障、重启与资源上限测试由工程测试入口执行。单包负例仅包含需要验证的错误；多错误包不要求不同实现采取完全相同的第一条诊断顺序。

## 外部实现适配接口

`scripts/conformance.py` 使用外部命令的 JSONL 适配器，适配器可以由任意语言编写。每行输入一个 JSON 对象，每行输出一个 JSON 对象；stdout 仅输出结果，诊断写 stderr。脚本不应导入参考协议实现来决定外部实现的判断。

验证输入：`{"operation":"validate","packet":{...}}`。输出：`{"code":null}` 或 `{"code":"ID_MISMATCH"}` 等。适配器执行结构加单包网络语义校验；脚本不向适配器发送 manifest 的预期结果或规则标签。`schema_valid` 供独立结构测试使用，完整符合性入口以 `expected_code` 比较结果。

序列输入：`{"operation":"sequence","steps":[{"packet":{...},"principal":"..."}]}`。输出：`{"results":[{"status":"accepted","code":null},...]}`。每个 sequence MUST 创建空存储；脚本已剥离 expected_status/expected_code，不能让适配器读取测试目录后照抄答案。序列里相同 packet 重复输入时，应在适配器第一次序列化后复用同样字节；真实网络中的字节差异另行测试。

最终命令以 `scripts/conformance.py --help` 为准；实现者提供命令后取得可保存的 JSON 结果。通过参考适配器，只说明测试入口和参考实现一致；独立实现应公开自己的语言、源代码版本、适配器、配置与原始输出。不得以参考适配器转调参考库冒充跨实现互操作。

支持 `--profile core` 与 `--profile full`，默认 full。core 跳过标记依赖可选能力的包及整个序列，不把不支持可选扩展判为核心不符合；报告须区分执行与跳过，不能把跳过说成通过。例如：

```powershell
.\.venv\Scripts\python.exe scripts\conformance.py --profile core --report reports\conformance-core.json -- .\.venv\Scripts\python.exe reference\conformance_adapter.py
.\.venv\Scripts\python.exe scripts\conformance.py --profile full --report reports\conformance-full.json -- .\.venv\Scripts\python.exe reference\conformance_adapter.py
```

适配器、runner 和消息实现必须保留 JSON 十进制精度。高精度反例 `commerce-precision-overallocation` 的分账之和 `0.10000000000000000000000001 + 0.2` 严格大于 `0.3`，必须返回 COMMERCE_INVALID。若先将数值转换为二进制 float 再序列化，输入已经改变，不能据此声称通过原始向量。使用精确十进制或原始数字 token 处理即可，不要求某一种语言库。

## 覆盖边界

Schema 必须启用 Draft 2020-12 的 uuid/date-time 格式断言；仅加载 Schema 而不开启格式断言不能报告通过。commerce 在测试套件中为已支持扩展，因此必须验证，纯核心实现应注明该可选扩展未覆盖。测试不检查真实合同、商品质量、用户授权真实性、全球命名唯一性、支付安全、完整隐私法规符合性或第三方认证。

公开测试直接使用本目录的明文 JSON 资产与 manifest，无需内部研发生成器或完整历史档案。修改测试资产时须同时提供规范依据、预期行为与兼容性分析，不能根据某个实现的结果反向修改预期。
