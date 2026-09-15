#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
rm -rf build dist
python3 -m PyInstaller --noconfirm --clean BibliotecaDeProjetos.spec
printf 'Executável Linux criado em %s\n' "$PWD/dist/BibliotecaDeProjetos"
