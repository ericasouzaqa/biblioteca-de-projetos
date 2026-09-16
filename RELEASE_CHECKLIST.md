# Checklist de Release — BibliotecaDeProjetos v0.2.0

## Qualidade

- [x] Nenhuma funcionalidade existente foi removida sem justificativa.
- [x] `ruff check .` passou.
- [x] Pytest passou: 20 testes.
- [x] Cobertura mínima de 80% atingida: 100% no núcleo de armazenamento.
- [x] Projeto vazio e prompt vazio validados.
- [x] Caminhos inválidos e arquivos ausentes validados.
- [x] Backup corrompido rejeitado.
- [x] Falha de gravação/permissão tratada pelo fluxo de arquivos.

## Funcionalidades

- [x] Criar, editar, excluir e reabrir projeto.
- [x] Criar, editar, excluir, duplicar, favoritar e copiar prompt.
- [x] Busca global validada.
- [x] Backup ZIP completo validado.
- [x] Restauração validada.
- [x] Dashboard atualizado.

## Plataformas e execução

- [x] Código-fonte Python validado.
- [x] Smoke test local completo aprovado.
- [x] Build PyInstaller Linux concluído.
- [ ] Workflow `windows-2025` concluído com sucesso.
- [ ] Workflow `windows-2022` concluído com sucesso.
- [ ] Executável Windows gerado e iniciado no runner.
- [x] Configuração de pacote portátil criada.

## Publicação

- [x] README atualizado.
- [x] Versionamento definido como `v0.2.0`.
- [x] Release notes geradas.
- [x] Workflows CI e release automática configurados.
- [ ] Repositório remoto `biblioteca-de-projetos` criado.
- [ ] CI remoto executado com sucesso.
- [ ] Tag `v0.2.0` enviada ao novo remoto.
- [ ] Release publicada.

**Regra:** a publicação está bloqueada enquanto qualquer item não marcado permanecer pendente.
