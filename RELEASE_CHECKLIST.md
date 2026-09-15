# Checklist de Release — BibliotecaDeProjetos

A release só pode ser publicada quando todos os itens estiverem confirmados.

## Qualidade

- [ ] Nenhuma funcionalidade existente foi removida sem justificativa.
- [ ] `ruff check .` passou.
- [ ] `pytest --cov=storage --cov-fail-under=80` passou.
- [ ] Cobertura mínima de 80% confirmada.
- [ ] Casos de projeto vazio e prompt vazio validados.
- [ ] Caminhos inválidos e arquivos ausentes validados.
- [ ] Backup corrompido rejeitado.
- [ ] Falha de gravação/permissão não ignorada.

## Funcionalidades

- [ ] Criar, editar, excluir e reabrir projeto.
- [ ] Criar, editar, excluir, duplicar, favoritar e copiar prompt.
- [ ] Busca global validada.
- [ ] Backup ZIP completo validado.
- [ ] Restauração validada.
- [ ] Dashboard atualizado.

## Plataformas e execução

- [ ] Código-fonte Python validado.
- [ ] Smoke test completo: abrir, criar, salvar, fechar, reabrir e manter dados.
- [ ] Workflow Windows 2019 concluído com sucesso (aproximação Windows 10).
- [ ] Workflow Windows 2022 concluído com sucesso (aproximação Windows 11).
- [ ] `BibliotecaDeProjetos.exe` gerado no Windows.
- [ ] Executável abre sem console e sem instalação da aplicação.

## Publicação

- [ ] README atualizado.
- [ ] Versão definida e tag revisada.
- [ ] Release notes geradas.
- [ ] Todos os testes e builds passaram.
- [ ] Só então criar e publicar a release.

**Regra:** se qualquer item falhar, interromper a publicação.
