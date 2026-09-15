import json

from storage.local_storage import LocalStorage


def test_storage_creates_local_structure(tmp_path):
    root = tmp_path / "Biblioteca"
    store = LocalStorage(root)
    assert store.projects_dir.is_dir()
    assert store.attachments_dir.is_dir()
    assert store.templates_dir.is_dir()
    assert store.config_path.exists()
    assert json.loads(store.config_path.read_text(encoding="utf-8")) == {}


def test_storage_ignores_missing_or_malformed_project_json(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    (store.projects_dir / "missing").mkdir()
    malformed = store.projects_dir / "malformed"; malformed.mkdir(); (malformed / "projeto.json").write_text("{invalid", encoding="utf-8")
    assert store.list_projects() == []


def test_storage_saves_utf8_and_sorted_projects(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    store.create_project("Zebra", "Descrição com acentuação: ação")
    store.create_project("Árvore")
    projects = store.list_projects()
    assert {project["name"] for project in projects} == {"Zebra", "Árvore"}
    zebra = next(project for project in projects if project["name"] == "Zebra")
    assert "acentuação" in zebra["description"]
