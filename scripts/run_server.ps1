[CmdletBinding()]
param (
    [switch]$NoReload,
    [string]$HostIP = "127.0.0.1",
    [int]$Port = 8000
)

# 1. Ensure working directory is always the project root
Set-Location $PSScriptRoot

# 2. Set environment variables for UTF-8 and unbuffered output
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

# 3. Ensure the logs directory exists
$logDir = Join-Path $PSScriptRoot "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 4. Determine the next version number
$existingLogs = Get-ChildItem -Path $logDir -Filter "app_run_log_v*.md" | 
    ForEach-Object {
        if ($_.BaseName -match '^app_run_log_v(\d+)$') {
            [int]$Matches[1]
        }
    }

if ($existingLogs) {
    $nextVersion = ($existingLogs | Measure-Object -Maximum).Maximum + 1
} else {
    $nextVersion = 1
}

$logFileName = "app_run_log_v$nextVersion.md"
$logFile = Join-Path $logDir $logFileName

# 5. Build Uvicorn command arguments
$uvicornArgs = @("-u", "-m", "uvicorn", "src.agentic_rag.api.main:app", "--host", $HostIP, "--port", $Port)
if (-not $NoReload) {
    $uvicornArgs += "--reload"
}

Write-Host "==================================================" -ForegroundColor Green
Write-Host " Starting Agentic RAG Server" -ForegroundColor Green
Write-Host " Target Log File : $logFileName" -ForegroundColor Yellow
Write-Host " Endpoint        : http://$($HostIP):$($Port)" -ForegroundColor Cyan
Write-Host " Reload Mode     : $(-not $NoReload)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Green

# 6. Execute Python and stream output to console & new log file
python @uvicornArgs *>&1 | Tee-Object -FilePath $logFile -Encoding utf8