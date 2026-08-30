param(
    [string]$TargetPath = "",
    [switch]$InstallDependencies,
    [switch]$StartWatch
)

$ErrorActionPreference = "Stop"

$UpstreamRepo = "https://github.com/microsoft/vscode.git"
$PinnedCommit = "f291f3fd7a3aa047515c65348d8f674a009aba94"
$ExpectedNode = "v24.18.0"
$ExpectedPackageVersion = "1.136.0"
$ExpectedElectron = "42.10.0"

function Assert-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' is not available."
    }
}

Assert-Command git

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path

if ([string]::IsNullOrWhiteSpace($TargetPath)) {
    $WorkspaceRoot = Split-Path -Parent $RepoRoot
    $TargetPath = Join-Path $WorkspaceRoot "JARVIS_DEVELOPER_WORKBENCH_CODE_OSS"
}

$TargetPath = [System.IO.Path]::GetFullPath($TargetPath)

if ($TargetPath -match "\s") {
    throw "TargetPath contains whitespace. Use a path without spaces for native module build reliability: $TargetPath"
}

Write-Host "MAKSIMAR / JARVIS Code - OSS bootstrap"
Write-Host "Pinned upstream: $PinnedCommit"
Write-Host "Target: $TargetPath"

if (-not (Test-Path $TargetPath)) {
    git clone --filter=blob:none --no-checkout $UpstreamRepo $TargetPath
}

Push-Location $TargetPath
try {
    if (-not (Test-Path ".git")) {
        throw "Target exists but is not a Git repository: $TargetPath"
    }

    git remote set-url origin $UpstreamRepo
    git fetch --depth 1 origin $PinnedCommit
    git checkout --detach $PinnedCommit

    $ActualCommit = (git rev-parse HEAD).Trim()
    if ($ActualCommit -ne $PinnedCommit) {
        throw "Pinned commit verification failed. Expected $PinnedCommit, got $ActualCommit"
    }

    $NodeManifest = (Get-Content ".nvmrc" -Raw).Trim()
    if ("v$NodeManifest" -ne $ExpectedNode) {
        throw "Unexpected upstream Node version. Expected $ExpectedNode, manifest says v$NodeManifest"
    }

    $Package = Get-Content "package.json" -Raw | ConvertFrom-Json
    if ($Package.version -ne $ExpectedPackageVersion) {
        throw "Unexpected Code - OSS package version. Expected $ExpectedPackageVersion, got $($Package.version)"
    }

    $Npmrc = Get-Content ".npmrc" -Raw
    if ($Npmrc -notmatch ('target="' + [regex]::Escape($ExpectedElectron) + '"')) {
        throw "Unexpected Electron target. Expected $ExpectedElectron"
    }

    Write-Host "Pinned baseline verification: PASS"
    Write-Host "Code - OSS: $($Package.version)"
    Write-Host "Node manifest: v$NodeManifest"
    Write-Host "Electron target: $ExpectedElectron"

    if ($InstallDependencies -or $StartWatch) {
        Assert-Command node
        Assert-Command npm

        $ActualNode = (node --version).Trim()
        if ($ActualNode -ne $ExpectedNode) {
            throw "Wrong Node version. Expected $ExpectedNode, got $ActualNode"
        }

        Write-Host "Installing exact upstream dependencies via npm install..."
        npm install
    }

    if ($StartWatch) {
        Write-Host "Starting Code - OSS development watch. Launch the shell from a second terminal with scripts\code.bat."
        npm run watch
    }
}
finally {
    Pop-Location
}

Write-Host "Bootstrap completed without modifying MAKSIMAR core/runtime code."
