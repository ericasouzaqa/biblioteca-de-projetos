# Release Notes — BibliotecaDeProjetos v0.2.0

## Novidades

A versão v0.2.0 adiciona suporte opcional a Markdown em descrições de projetos, observações, continuidade e conteúdos de prompts. O usuário pode escolher entre Texto simples e Markdown, visualizar um preview local e exportar o projeto para um arquivo `.md`.

## Compatibilidade e privacidade

O formato JSON existente foi preservado. Registros antigos sem metadados continuam sendo tratados como Texto simples, sem conversão automática. Backups, restauração, funcionamento offline e armazenamento local permanecem inalterados. Nenhum conteúdo é enviado para APIs, nuvem ou serviços externos.

## Validação

A release foi validada com Ruff, Pytest, cobertura superior a 80%, testes de acessibilidade, backup, restauração, Markdown, exportação, smoke test Tkinter e builds PyInstaller para Ubuntu, Windows 2022 e Windows 2025.
