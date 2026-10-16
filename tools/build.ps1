param([string]$Python = 'python', [switch]$SkipTests)
$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot\..
& $Python tools/validate_content.py
if($LASTEXITCODE -ne 0){throw 'Content validation failed'}
& $Python -m unittest discover -s tools -p 'test_*.py'
if($LASTEXITCODE -ne 0){throw 'Python tests failed'}
if($SkipTests){ & .\gradlew.bat assembleDebug }else{ & .\gradlew.bat assembleDebug testDebugUnitTest lintDebug assembleDebugAndroidTest }
if($LASTEXITCODE -ne 0){throw 'Android build failed'}
Write-Host "APK: $((Resolve-Path 'app/build/outputs/apk/debug/app-debug.apk').Path)"
