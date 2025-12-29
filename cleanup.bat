@echo off
echo ========================================
echo Cleaning Up for Render Deployment
echo ========================================
echo.

cd /d "d:\Py and ipynb\Employee Performance Prediction"

echo [1/5] Removing test scripts...
if exist "Flask\convert_model_to_json.py" (
    del /f "Flask\convert_model_to_json.py"
    echo   - Deleted: convert_model_to_json.py
)
if exist "Flask\fix_model.py" (
    del /f "Flask\fix_model.py"
    echo   - Deleted: fix_model.py
)
if exist "Flask\verify_model.py" (
    del /f "Flask\verify_model.py"
    echo   - Deleted: verify_model.py
)
if exist "Flask\retrain_and_save_properly.py" (
    del /f "Flask\retrain_and_save_properly.py"
    echo   - Deleted: retrain_and_save_properly.py
)
if exist "Flask\run_app.bat" (
    del /f "Flask\run_app.bat"
    echo   - Deleted: run_app.bat
)

echo.
echo [2/5] Removing backup and alternative models...
if exist "Flask\gwp_backup.pkl" (
    del /f "Flask\gwp_backup.pkl"
    echo   - Deleted: gwp_backup.pkl
)
if exist "Flask\gwp.xgb" (
    del /f "Flask\gwp.xgb"
    echo   - Deleted: gwp.xgb
)
if exist "Flask\gwp.json" (
    del /f "Flask\gwp.json"
    echo   - Deleted: gwp.json
)

echo.
echo [3/5] Removing Python cache...
if exist "Flask\__pycache__" (
    rmdir /s /q "Flask\__pycache__"
    echo   - Deleted: __pycache__
)
if exist ".venv" (
    rmdir /s /q ".venv"
    echo   - Deleted: .venv
)

echo.
echo [4/5] Removing extra documentation...
if exist "RENDER_TROUBLESHOOTING.md" (
    del /f "RENDER_TROUBLESHOOTING.md"
    echo   - Deleted: RENDER_TROUBLESHOOTING.md
)
if exist "RENDER_MODEL_FIX.md" (
    del /f "RENDER_MODEL_FIX.md"
    echo   - Deleted: RENDER_MODEL_FIX.md
)
if exist "JSON_ERROR_FIX.md" (
    del /f "JSON_ERROR_FIX.md"
    echo   - Deleted: JSON_ERROR_FIX.md
)
if exist "QUICK_FIX_COMMANDS.md" (
    del /f "QUICK_FIX_COMMANDS.md"
    echo   - Deleted: QUICK_FIX_COMMANDS.md
)
if exist "FINAL_FIX.md" (
    del /f "FINAL_FIX.md"
    echo   - Deleted: FINAL_FIX.md
)

echo.
echo [5/5] Verifying essential files...
if exist "Flask\app.py" (
    echo   - Found: Flask\app.py
) else (
    echo   - MISSING: Flask\app.py
)
if exist "Flask\gwp.pkl" (
    echo   - Found: Flask\gwp.pkl ^(CRITICAL!^)
) else (
    echo   - MISSING: Flask\gwp.pkl ^(CRITICAL!^)
)
if exist "requirements.txt" (
    echo   - Found: requirements.txt
) else (
    echo   - MISSING: requirements.txt
)
if exist "render.yaml" (
    echo   - Found: render.yaml
) else (
    echo   - MISSING: render.yaml
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. git add .
echo   2. git commit -m "Clean up for deployment"
echo   3. git push origin main
echo.
pause
