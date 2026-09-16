# biblioteca-de-projetos

Aplicação desktop offline para analistas de QA organizarem projetos, prompts, checklists, observações e histórico de trabalho. Esta é a versão inicial **v0.2.0** do novo projeto, independente do repositório legado `biblioteca-de-prompts`.

## Princípios

O projeto usa Python e Tkinter, não usa banco de dados, login, autenticação, servidor ou API externa. Os dados são gravados somente em arquivos JSON locais.

## Funcionalidades v0.2.0

A versão inicial oferece cadastro, edição, abertura e exclusão de projetos; campos de acompanhamento; checklists; prompts vinculados com edição, duplicação, favoritos e cópia; busca global; dashboard; backup ZIP; restauração segura e tema escuro.

## Estrutura local de dados

Por padrão, os dados ficam em `%USERPROFILE%\\Biblioteca` no Windows ou `~/Biblioteca` no Linux. A estrutura criada é:

```text
Biblioteca/
├── projetos/
├── anexos/
├── templates/
└── configuracao.json
```

## Execução pelo código-fonte

Requer Python 3.10+ e Tkinter.

```bash
python -m pip install -r requirements.txt
python app.py
```

## Build local

No Windows:

```bat
build.bat
```

No Linux:

```bash
chmod +x build.sh
./build.sh
```

Os artefatos são criados em `dist/`:

```text
BibliotecaDeProjetos.exe       # Windows
BibliotecaDeProjetos           # Linux
```

O build é portátil e não instala a aplicação no sistema de destino. Python é necessário somente para compilar.

## Testes e qualidade

```bash
ruff check .
pytest --cov=storage --cov-report=term-missing --cov-fail-under=80
```

A cobertura mínima exigida no CI é 80% para o núcleo de armazenamento. O smoke test Tkinter deve ser executado em um ambiente com display.

## CI e releases

O workflow em `.github/workflows/ci.yml` executa Ruff e pytest no Ubuntu e gera o executável Linux. A matriz Windows executa Ruff, pytest e PyInstaller em Windows 2025 e Windows 2022. O workflow `.github/workflows/release.yml` gera e publica os pacotes quando uma tag `v*` é criada.

A primeira versão usa a tag `v0.2.0`. A tag `v1.0.0` não faz parte deste projeto.

## Licença

Distribuído sob a licença MIT. Consulte `LICENSE`.
