# Release Notes — BibliotecaDeProjetos v0.1.1

## Conteúdo

A versão inicial reúne cadastro e acompanhamento de projetos, prompts vinculados, checklists, busca global, dashboard, backup ZIP, restauração local segura e empacotamento portátil com PyInstaller para Linux e Windows.

## Validação local concluída

Ruff passou sem erros. A suíte pytest passou com 20 testes e cobertura de 100% do núcleo de armazenamento, acima do mínimo exigido de 80%. Foram validados CRUD de projetos, prompts, busca, dashboard, backup, restauração, arquivos ausentes, ZIP corrompido, caminhos inválidos, projeto vazio, prompt vazio e persistência após fechamento e reabertura.

O build PyInstaller Linux foi concluído e o smoke test da aplicação Tkinter foi aprovado. O smoke test confirma abertura, criação, salvamento, fechamento, reabertura e preservação de dados.

## Validação remota pendente

A validação real dos executáveis Windows nos runners `windows-2025` e `windows-2022` ainda depende da criação do repositório remoto e da execução dos workflows GitHub Actions. Nenhuma release deve ser publicada antes de ambos os jobs Windows passarem, incluindo Ruff, pytest, cobertura, build e smoke test do executável.

## Regra de publicação

A tag inicial deve ser exclusivamente `v0.1.1`. A tag `v1.0.0` não pertence a este novo projeto.
