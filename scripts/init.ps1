param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
New-Item -ItemType Directory -Force .tmp | Out-Null
$env:TEMP = Join-Path $PWD '.tmp'
$env:TMP = $env:TEMP
$env:PYTHONIOENCODING = 'utf-8'
$expected = (Get-Content .python-version).Trim()
$actual = & $Python -c 'import platform; print(platform.python_version())'
if ($LASTEXITCODE -ne 0 -or $actual -ne $expected) { throw "Python $expected required; found $actual. Specify -Python with an existing interpreter path." }
if (!(Test-Path .venv/Scripts/python.exe)) {
    & $Python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'venv creation failed' }
}
$venvVersion = & ./.venv/Scripts/python.exe -c 'import platform; print(platform.python_version())'
if ($venvVersion -ne $expected) { throw 'Existing venv has a different Python version' }
& ./.venv/Scripts/python.exe -m ensurepip --upgrade
if ($LASTEXITCODE -ne 0) { throw 'pip bootstrap failed' }
& ./.venv/Scripts/python.exe -m pip install --disable-pip-version-check --no-cache-dir --require-hashes -r requirements.lock
if ($LASTEXITCODE -ne 0) { throw 'Locked installation failed' }
if ((Test-Path scripts/verify_baseline.py) -and (Test-Path baseline/ODIP-v0.1.2) -and (Test-Path reports/baseline-manifest.json)) {
    & ./.venv/Scripts/python.exe scripts/verify_baseline.py
    if ($LASTEXITCODE -ne 0) { throw 'Baseline verification failed' }
} else {
    Write-Output 'Public source checkout initialized; original research archive is not required.'
}
