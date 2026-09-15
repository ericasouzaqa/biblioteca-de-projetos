from storage.local_storage import LocalStorage


def project_with_prompts(store):
    project = store.create_project("Projeto Prompts", "Descrição pesquisável")
    prompts = [{"id": "p1", "title": "Login", "category": "Regressão", "content": "Validar autenticação", "favorite": False}]
    store.update_project(project["id"], project["name"], project["description"], project["status"], prompts=prompts)
    return project["id"]


def test_create_edit_favorite_and_delete_prompt(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca")
    project_id = project_with_prompts(store)
    project = store.get_project(project_id)
    assert project["prompts"][0]["title"] == "Login"
    project["prompts"][0].update(title="Login editado", category="Smoke", favorite=True)
    store.update_project(project_id, project["name"], project["description"], project["status"], prompts=project["prompts"])
    assert store.get_project(project_id)["prompts"][0]["favorite"] is True
    project = store.get_project(project_id); project["prompts"].clear()
    store.update_project(project_id, project["name"], project["description"], project["status"], prompts=project["prompts"])
    assert store.get_project(project_id)["prompts"] == []


def test_duplicate_prompt_has_new_id(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca"); project_id = project_with_prompts(store); project = store.get_project(project_id)
    original = project["prompts"][0]; duplicate = {**original, "id": "p2", "title": "Login (cópia)", "favorite": False}; project["prompts"].append(duplicate)
    store.update_project(project_id, project["name"], project["description"], project["status"], prompts=project["prompts"])
    assert [p["id"] for p in store.get_project(project_id)["prompts"]] == ["p1", "p2"]


def test_global_search_fields(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca"); project_id = project_with_prompts(store)
    project = store.get_project(project_id); project.update(notes="Nota especial", completed_checks=["Executado"], pending_checks=["Pendente"])
    store.update_project(project_id, project["name"], project["description"], project["status"], notes=project["notes"], completed_checks=project["completed_checks"], pending_checks=project["pending_checks"], prompts=project["prompts"])
    data = store.get_project(project_id); searchable = " ".join([data["name"], data["description"], data["notes"], *data["completed_checks"], *data["pending_checks"], *(p["title"] + " " + p["content"] for p in data["prompts"])])
    for term in ("Projeto", "Descrição", "Nota", "Executado", "Pendente", "Login", "autenticação"):
        assert term.casefold() in searchable.casefold()


def test_empty_prompt_content_is_storable_without_crashing(tmp_path):
    store = LocalStorage(tmp_path / "Biblioteca"); project_id = store.create_project("QA")["id"]; project = store.get_project(project_id); project["prompts"] = [{"id": "p", "title": "Título", "category": "", "content": "", "favorite": False}]
    store.update_project(project_id, project["name"], project["description"], project["status"], prompts=project["prompts"])
    assert store.get_project(project_id)["prompts"][0]["content"] == ""
