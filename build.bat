@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo === Biblioteca de Projetos QA ===
echo Instalando dependencias de build...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    exit /b 1
)

echo Removendo builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Gerando executavel portatil...
python -m PyInstaller --noconfirm --clean BibliotecaDeProjetos.spec
if errorlevel 1 (
    echo Falha ao gerar executavel.
    exit /b 1
)

echo.
echo Executavel criado com sucesso:
echo %~dp0dist\BibliotecaDeProjetos.exe
endlocal
