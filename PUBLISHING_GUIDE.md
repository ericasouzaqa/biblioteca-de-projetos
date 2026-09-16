# Guia de publicação — biblioteca-de-projetos

Este diretório é um novo repositório independente. Não deve ser conectado ao repositório legado `biblioteca-de-prompts`.

## 1. Criar o repositório remoto

No GitHub, crie um repositório vazio chamado `biblioteca-de-projetos`. Não adicione README, licença ou `.gitignore` pelo site, pois esses arquivos já existem localmente.

## 2. Revisar localmente

Execute:

```bash
python -m pip install -r requirements.txt
ruff check .
pytest --cov=storage --cov-report=term-missing --cov-fail-under=80
```

No Linux, execute também `./build.sh`. No Windows, execute `build.bat`.

## 3. Criar o primeiro commit

```bash
git add .
git commit -m "Initial release v0.1.0"
```

Confirme que não há arquivos de dados pessoais, `dist/`, `build/` ou backups locais no commit.

## 4. Conectar o novo remoto

Substitua `<OWNER>` pela organização ou usuário correto:

```bash
git remote add origin https://github.com/<OWNER>/biblioteca-de-projetos.git
git push -u origin main
```

A sessão de migração não executa esse comando automaticamente.

## 5. Validar o CI

O workflow `ci.yml` executa Ruff, pytest, cobertura e build Linux. A matriz Windows executa Ruff, pytest e PyInstaller nos runners `windows-2025` e `windows-2022`. Aguarde todos os jobs passarem antes de criar a tag.

## 6. Publicar v0.1.0

Somente após CI aprovado:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

O workflow `release.yml` executará novamente lint e testes, gerará os executáveis Linux e Windows, criará os ZIPs portáteis e publicará a release automaticamente com as notas de `RELEASE_NOTES.md`.

## 7. Artefatos esperados

A release deve conter o executável Linux, o pacote Linux, o executável Windows e os pacotes ZIP Windows produzidos pela matriz. Se qualquer job falhar, a etapa `publish` não será executada.

## 8. Smoke test pós-release

Baixe o pacote da release em uma máquina Windows e em uma máquina Linux compatível. Abra o executável, crie um projeto, salve, feche, reabra e confirme que os dados permanecem. Teste também um backup e uma restauração antes de anunciar a release.

## Regra de segurança

Não usar a tag `v1.0.0` neste projeto. A versão inicial deste novo repositório é exclusivamente `v0.1.0`.
