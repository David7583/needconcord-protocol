# 环境与复现

公开参考工程固定 CPython **3.12.7**、Windows x86_64，使用仓库内 `.venv` 隔离依赖。它不要求指定发行商、全局包、工作台或商业平台。运行者自行准备该版本解释器；不修改全局 PATH、系统 Python 或其他项目环境。

`.python-version` 声明解释器版本，`requirements.lock` 固定依赖与 wheel SHA-256（包括测试工具）。本锁覆盖 Windows CPython 3.12 x86_64，不声称跨操作系统重现；其他平台应单独审核锁文件并运行同一公开测试。依赖告知见 [许可清单](../LICENSES/dependency-licenses.json)。没有把版本锁定等同于已完成漏洞审计。

在解压或检出的仓库根目录执行：

```powershell
.\scripts\init.ps1 -Python python
.\.venv\Scripts\python.exe scripts/verify.py --public --report-dir evidence
```

`python` 必须指向 CPython 3.12.7；也可给 `-Python` 传入自己已安装的解释器路径。初始化会核实版本、创建/复用 `.venv` 并按 hash 锁安装依赖。无需激活虚拟环境。包安装需要索引访问；执行策略或网络限制应依运行者组织规则处理，不应绕过限制。

公开模式不读取或验证维护者的原始 ZIP、完整基线或内部报告。兼容性测试所需最小材料已在 [tests/fixtures/v0.1.2](../tests/fixtures/v0.1.2/README.md) 提供。项目源码与公开测试资产足以运行本阶段验证。

单独运行接口：

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp=.tmp/pytest-public
.\.venv\Scripts\python.exe scripts/conformance.py --report evidence/conformance-run.json -- .\.venv\Scripts\python.exe reference/conformance_adapter.py
.\.venv\Scripts\python.exe scripts/conformance.py --profile core --report evidence/conformance-core-run.json -- .\.venv\Scripts\python.exe reference/conformance_adapter.py
.\.venv\Scripts\python.exe reference/two_process_demo.py --work-dir .tmp/manual-demo-01 --report evidence/two-process-evidence.json
```

双节点演示每次使用新的空工作目录。`.tmp` 与 `runtime` 中可能包含临时测试凭据、SQLite 和完整模拟输入，禁止随源码上传。公开报告仅包含脱敏命令、合成数据与结构化事件；执行器不把预期结果写成实际通过。若本地系统禁止 loopback，网络测试会失败；获取合法执行权限后重跑，不可跳过后报告通过。

`rfc3339-validator` 是日期格式断言所需的锁定依赖；服务启动会检查非法日期确实被拒绝，依赖缺失时拒绝静默放行。公开验证结果及覆盖口径见 [VALIDATION.md](VALIDATION.md)。

配置 token 仅用于测试身份绑定，不代表真实组织认证。手工启动、重试与导出见 [参考节点](REFERENCE.md)。

## English

Use CPython 3.12.7 on Windows x86_64 and a project-local virtual environment. From the repository root, run the initialization command and `scripts/verify.py --public --report-dir evidence`. The public package contains the minimal compatibility fixtures and does not require private archives. The lock is platform-specific; it is not a production security assessment. Keep temporary credentials and databases out of published artifacts.
