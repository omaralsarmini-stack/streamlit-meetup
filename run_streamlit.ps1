param(
	[int]$Port = 8503
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$uvLocal = Join-Path $HOME ".local\bin\uv.exe"

$uvCommand = $null
if (Get-Command uv -ErrorAction SilentlyContinue) {
	$uvCommand = "uv"
} elseif (Test-Path $uvLocal) {
	$uvCommand = $uvLocal
}

if (-not $uvCommand) {
	Write-Error "uv is not installed. Either install uv or run: python -m streamlit run app.py"
	exit 1
}

Write-Host "Using uv: $uvCommand"
Write-Host "Starting Streamlit on port $Port via uv..."

if (Test-Path (Join-Path $PSScriptRoot "requirements.txt")) {
	& $uvCommand run --with-requirements (Join-Path $PSScriptRoot "requirements.txt") streamlit run (Join-Path $PSScriptRoot "app.py") --server.port $Port
} else {
	& $uvCommand run --with streamlit streamlit run (Join-Path $PSScriptRoot "app.py") --server.port $Port
}
