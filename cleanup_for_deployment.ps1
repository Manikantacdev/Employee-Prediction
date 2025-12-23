# Quick Cleanup Script for Render Deployment
# Run this before deploying to remove all unwanted files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleaning Up for Render Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Change to project directory
Set-Location "d:\Py and ipynb\Employee Performance Prediction"

Write-Host "`n[1/5] Removing test scripts..." -ForegroundColor Yellow
$testScripts = @(
    "Flask\convert_model_to_json.py",
    "Flask\fix_model.py",
    "Flask\verify_model.py",
    "Flask\retrain_and_save_properly.py",
    "Flask\run_app.bat"
)

foreach ($file in $testScripts) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Deleted: $file" -ForegroundColor Green
    }
}

Write-Host "`n[2/5] Removing backup and alternative models..." -ForegroundColor Yellow
$backups = @(
    "Flask\gwp_backup.pkl",
    "Flask\gwp.xgb",
    "Flask\gwp.json"
)

foreach ($file in $backups) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Deleted: $file" -ForegroundColor Green
    }
}

Write-Host "`n[3/5] Removing Python cache..." -ForegroundColor Yellow
if (Test-Path "Flask\__pycache__") {
    Remove-Item "Flask\__pycache__" -Recurse -Force
    Write-Host "  ✓ Deleted: Flask\__pycache__" -ForegroundColor Green
}

Write-Host "`n[4/5] Removing extra documentation..." -ForegroundColor Yellow
$extraDocs = @(
    "RENDER_TROUBLESHOOTING.md",
    "RENDER_MODEL_FIX.md",
    "JSON_ERROR_FIX.md",
    "QUICK_FIX_COMMANDS.md",
    "FINAL_FIX.md"
)

foreach ($file in $extraDocs) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Deleted: $file" -ForegroundColor Green
    }
}

Write-Host "`n[5/5] Verifying essential files..." -ForegroundColor Yellow

# Check essential files
$essential = @{
    "Flask\app.py" = "Main application"
    "Flask\gwp.pkl" = "ML Model (CRITICAL!)"
    "requirements.txt" = "Dependencies"
    "render.yaml" = "Render config"
    ".gitignore" = "Git ignore rules"
}

$allGood = $true
foreach ($file in $essential.Keys) {
    if (Test-Path $file) {
        Write-Host "  ✓ Found: $file - $($essential[$file])" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MISSING: $file - $($essential[$file])" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ Cleanup Complete!" -ForegroundColor Green
    Write-Host "✓ All essential files present" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. git add ." -ForegroundColor White
    Write-Host "  2. git commit -m 'Clean up for Render deployment'" -ForegroundColor White
    Write-Host "  3. git push origin main" -ForegroundColor White
} else {
    Write-Host "⚠ Cleanup complete but some files are missing!" -ForegroundColor Yellow
    Write-Host "Please check the missing files above." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
