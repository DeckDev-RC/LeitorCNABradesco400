@echo off
REM Script de build para Windows - Sistema CNAB Bradesco
REM Versão: 1.2.0

echo.
echo ================================================
echo   BUILD SISTEMA CNAB BRADESCO v1.2.0
echo ================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado no PATH
    echo    Instale Python 3.8+ e adicione ao PATH
    pause
    exit /b 1
)

REM Verificar se pip está disponível
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: pip não encontrado
    echo    Instale pip ou reinstale Python
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar argumentos
if "%1"=="gui" goto BUILD_GUI
if "%1"=="console" goto BUILD_CONSOLE
if "%1"=="clean" goto CLEAN_ONLY
if "%1"=="deps" goto INSTALL_DEPS

:BUILD_ALL
echo 🔨 Executando build completo...
python build.py
goto END

:BUILD_GUI
echo 🎨 Executando build GUI apenas...
python build.py --gui-only
goto END

:BUILD_CONSOLE
echo 💻 Executando build console apenas...
python build.py --console-only
goto END

:CLEAN_ONLY
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec" 2>nul
if exist "file_version_info.txt" del "file_version_info.txt"
echo ✅ Limpeza concluída
goto END

:INSTALL_DEPS
echo 📦 Instalando dependências...
pip install -r requirements.txt
echo ✅ Dependências instaladas
goto END

:END
echo.
echo ================================================
echo   Build finalizado!
echo ================================================
echo.
echo Comandos disponíveis:
echo   build.bat           - Build completo
echo   build.bat gui       - Apenas interface gráfica
echo   build.bat console   - Apenas versão console
echo   build.bat clean     - Limpar builds anteriores
echo   build.bat deps      - Instalar dependências
echo.
pause 