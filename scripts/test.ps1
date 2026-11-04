param([switch]$Public, [string]$ReportDir = '')
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$verifyArgs = @('scripts/verify.py')
if ($Public -or !(Test-Path baseline/ODIP-v0.1.2)) { $verifyArgs += '--public' }
if ($ReportDir) { $verifyArgs += @('--report-dir', $ReportDir) }
& ./.venv/Scripts/python.exe @verifyArgs
if ($LASTEXITCODE -ne 0) { throw 'ODIP verification failed; inspect the reported verification-run.json path' }
