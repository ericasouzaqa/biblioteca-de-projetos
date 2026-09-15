import pytest

from storage.local_storage import STATUSES, LocalStorage


def test_create_project_persists_all_base_fields(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project = store.create_project("Projeto QA", "Descrição", "Em andamento")
    saved = store.get_project(project["id"])
    assert saved["name"] == "Projeto QA"
    assert saved["description"] == "Descrição"
    assert saved["status"] == "Em andamento"
    assert (store.projects_dir / project["id"] / "projeto.json").exists()


def test_edit_project_preserves_and_updates_data(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project = store.create_project("Original")
    store.update_project(project["id"], "Editado", "Nova descrição", "Finalizado", where_stopped="Etapa 2", next_step="Encerrar", notes="OK", completed_checks=["Login"], pending_checks=["Relatório"], prompts=[{"id": "p1"}])
    saved = store.get_project(project["id"])
    assert saved["name"] == "Editado"
    assert saved["status"] == "Finalizado"
    assert saved["where_stopped"] == "Etapa 2"
    assert saved["completed_checks"] == ["Login"]
    assert saved["prompts"] == [{"id": "p1"}]


def test_delete_project_removes_json_directory(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project = store.create_project("Excluir")
    store.delete_project(project["id"])
    assert store.get_project(project["id"]) is None
    assert store.list_projects() == []


@pytest.mark.parametrize("name", ["", "   "])
def test_empty_project_is_rejected(tmp_path, name):
    store = LocalStorage(tmp_path / "Biblioteca")
    with pytest.raises(ValueError):
        store.create_project(name)


def test_invalid_status_is_rejected(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    with pytest.raises(ValueError):
        store.create_project("QA", status="Status inexistente")


def test_missing_project_and_missing_file_are_handled(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    assert store.get_project("ausente") is None
    with pytest.raises(FileNotFoundError):
        store.update_project("ausente", "x", "", STATUSES[0])
    with pytest.raises(FileNotFoundError):
        store.delete_project("ausente")
