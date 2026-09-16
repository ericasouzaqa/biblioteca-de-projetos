from services.export_markdown import export_project_markdown, project_to_markdown


def test_project_markdown_export_respects_formats(tmp_path):
    project = {"name": "QA", "status": "Em andamento", "description": "# Descrição", "text_formats": {"description": "markdown"}, "where_stopped": "Etapa 1", "next_step": "Validar", "notes": "**Nota**", "completed_checks": ["Smoke"], "pending_checks": ["Regressão"], "prompts": [{"title": "Login", "category": "Web", "content": "## Prompt", "format": "markdown"}]}
    output = project_to_markdown(project)
    assert "# QA" in output
    assert "DESCRIÇÃO" in output
    assert "- [x] Smoke" in output
    assert "- [ ] Regressão" in output
    assert "PROMPT" in output
    destination = export_project_markdown(project, tmp_path / "qa.md")
    assert destination.read_text(encoding="utf-8") == output


def test_plain_text_is_not_converted_on_export(tmp_path):
    project = {"name": "QA", "status": "Não iniciado", "description": "# Texto literal", "text_formats": {"description": "plain"}}
    output = project_to_markdown(project)
    assert "# Texto literal" in output
    assert "TEXTO LITERAL" not in output
    assert export_project_markdown(project, tmp_path / "qa.md").exists()
