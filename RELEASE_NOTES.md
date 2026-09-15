# Release Notes — BibliotecaDeProjetos

## Status

Estas notas estão preparadas para a próxima release, mas a publicação permanece bloqueada até a conclusão e aprovação de todos os itens em `RELEASE_CHECKLIST.md`.

## Conteúdo

A versão reúne o cadastro e acompanhamento de projetos, prompts vinculados, busca global, dashboard, backup ZIP, restauração local e empacotamento portátil com PyInstaller.

## Validação obrigatória

A publicação depende de lint aprovado, cobertura mínima de 80%, testes de regressão aprovados, smoke test completo e builds Windows bem-sucedidos nos runners Windows 2019 e Windows 2022.

## Limitações da validação local

Este ambiente é Linux. Portanto, a execução real do executável Windows e a confirmação específica de Windows 10/11 dependem do workflow GitHub Actions configurado em `.github/workflows/validate.yml`. Nenhuma release deve ser publicada antes de esse workflow concluir com sucesso.
