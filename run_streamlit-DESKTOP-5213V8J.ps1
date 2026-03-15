param(
    [int]$Port = 8503
)

$ErrorActionPreference = 'Stop'

Set-Location -Path $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$uvLocal = Join-Path $HOME ".local\bin\uv.exe"

$pythonCommand = $null
$pythonBaseArgs = @()

$candidates = @()
if (Test-Path $venvPython) {
    $candidates += @{ Command = $venvPython; Args = @() }
}
$candidates += @{ Command = "py"; Args = @("-3") }
$candidates += @{ Command = "py"; Args = @() }
$candidates += @{ Command = "python"; Args = @() }

foreach ($candidate in $candidates) {
    try {
        & $candidate.Command @($candidate.Args + @("-V")) *> $null
        if ($LASTEXITCODE -eq 0) {
            $pythonCommand = $candidate.Command
            $pythonBaseArgs = $candidate.Args
            break
        }
    } catch {
        # try next candidate
    }
}

if ($pythonCommand) {
    Write-Host "Using Python: $pythonCommand $($pythonBaseArgs -join ' ')"

    function Invoke-Python {
        param([string[]]$Args)
        & $pythonCommand @($pythonBaseArgs + $Args)
    }

    # Ensure Streamlit is available. If not, install from requirements.txt when present.
    Invoke-Python -Args @("-c", "import streamlit") 2>$null
    if ($LASTEXITCODE -ne 0) {
        if (Test-Path (Join-Path $PSScriptRoot "requirements.txt")) {
            Write-Host "Installing dependencies from requirements.txt..."
            Invoke-Python -Args @("-m", "pip", "install", "-r", (Join-Path $PSScriptRoot "requirements.txt"))
        } else {
            Write-Host "Installing Streamlit..."
            Invoke-Python -Args @("-m", "pip", "install", "streamlit")
        }
    }

    Write-Host "Starting Streamlit on port $Port..."
    Invoke-Python -Args @("-m", "streamlit", "run", (Join-Path $PSScriptRoot "app.py"), "--server.port", "$Port")
    exit $LASTEXITCODE
}

$uvCommand = $null
if (Get-Command uv -ErrorAction SilentlyContinue) {
    $uvCommand = "uv"
} elseif (Test-Path $uvLocal) {
    $uvCommand = $uvLocal
}

if (-not $uvCommand) {
    throw "Neither Python nor uv was found. Install Python 3 or uv and try again."
}

Write-Host "Using uv: $uvCommand"
Write-Host "Starting Streamlit on port $Port via uv..."

if (Test-Path (Join-Path $PSScriptRoot "requirements.txt")) {
    & $uvCommand run --with-requirements (Join-Path $PSScriptRoot "requirements.txt") streamlit run (Join-Path $PSScriptRoot "app.py") --server.port $Port
} else {
    & $uvCommand run --with streamlit streamlit run (Join-Path $PSScriptRoot "app.py") --server.port $Port
}
