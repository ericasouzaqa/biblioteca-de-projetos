from services.markdown import render_markdown
from storage.local_storage import LocalStorage


def test_markdown_preview_does_not_change_source_text():
    source = "# Título\n\n**importante**\n- item"
    preview = render_markdown(source)
    assert source == "# Título\n\n**importante**\n- item"
    assert "TÍTULO" in preview
    assert "• item" in preview
    assert "importante" in preview


def test_legacy_project_defaults_to_plain_without_conversion(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project = store.create_project("Legado", "# Não converter")
    path = store.projects_dir / project["id"] / "projeto.json"
    raw = path.read_text(encoding="utf-8").replace(',\n  "text_formats": {\n    "description": "plain",\n    "where_stopped": "plain",\n    "next_step": "plain",\n    "notes": "plain"\n  }', "")
    path.write_text(raw, encoding="utf-8")
    loaded = store.get_project(project["id"])
    assert loaded["description"] == "# Não converter"
    saved = store.save_project(loaded)
    assert saved["text_formats"]["description"] == "plain"


def test_markdown_format_is_persisted_for_project_and_prompt(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project = store.create_project("Markdown", "# Projeto", text_formats={"description": "markdown"})
    updated = store.update_project(project["id"], project["name"], project["description"], project["status"], text_formats={"description": "markdown", "notes": "markdown"}, prompts=[{"id": "p", "title": "Prompt", "content": "## Conteúdo", "format": "markdown"}])
    assert updated["text_formats"]["description"] == "markdown"
    assert store.get_project(project["id"])["prompts"][0]["format"] == "markdown"
