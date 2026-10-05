param([string]$OutputDirectory = 'D:\迅雷下载\vibe coding', [switch]$Force)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'manifest.json') -Raw | ConvertFrom-Json
$zipPath = Join-Path $OutputDirectory "terracotta-sunset-theme-$($manifest.version).zip"
if (Test-Path -LiteralPath $zipPath) {
  if (-not $Force) { throw "Archive already exists: $zipPath" }
  Remove-Item -LiteralPath $zipPath -Force
}
$items = @('manifest.json', 'logo', 'README.md', 'scripts', 'store-assets', 'PACKAGING.md', 'LICENSE', '.gitignore') | ForEach-Object { Join-Path $projectRoot $_ }
Compress-Archive -LiteralPath $items -DestinationPath $zipPath -Force
Get-Item -LiteralPath $zipPath | Select-Object FullName,Length,LastWriteTime

