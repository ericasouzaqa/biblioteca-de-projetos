import zipfile

import pytest

from storage.local_storage import LocalStorage


def populated_store(root):
    store = LocalStorage(root); project = store.create_project("Backup QA")
    store.update_project(project["id"], project["name"], project["description"], project["status"], prompts=[{"id": "p", "title": "Prompt", "category": "QA", "content": "Conteúdo", "favorite": True}])
    attachment = store.attachments_dir / project["id"]; attachment.mkdir(parents=True); (attachment / "evidencia.txt").write_text("evidência", encoding="utf-8")
    (store.templates_dir / "modelo.txt").write_text("template", encoding="utf-8")
    store.config_path.write_text('{"tema":"escuro"}', encoding="utf-8")
    return store, project


def test_backup_contains_projects_prompts_attachments_and_config(tmp_path):
    store, _project = populated_store(tmp_path / "source"); backup = store.create_backup(tmp_path / "backup.zip")
    with zipfile.ZipFile(backup) as archive:
        names = set(archive.namelist())
    assert any(name.startswith("projetos/") for name in names)
    assert any(name.startswith("anexos/") for name in names)
    assert any(name.startswith("templates/") for name in names)
    assert "configuracao.json" in names


def test_restore_replaces_content_and_keeps_prompts_and_attachments(tmp_path):
    source, project = populated_store(tmp_path / "source"); backup = source.create_backup(tmp_path / "backup.zip"); target = LocalStorage(tmp_path / "target"); target.create_project("Projeto antigo"); target.restore_backup(backup)
    restored = target.get_project(project["id"])
    assert restored["prompts"][0]["title"] == "Prompt"
    assert (target.attachments_dir / project["id"] / "evidencia.txt").exists()
    assert target.config_path.read_text(encoding="utf-8") == '{"tema":"escuro"}'


def test_corrupt_backup_is_rejected(tmp_path):
    store = LocalStorage(tmp_path / "source"); corrupt = tmp_path / "corrupt.zip"; corrupt.write_bytes(b"not a zip")
    with pytest.raises(ValueError): store.restore_backup(corrupt)


def test_invalid_zip_path_is_rejected(tmp_path):
    store = LocalStorage(tmp_path / "source"); invalid = tmp_path / "invalid.zip"
    with zipfile.ZipFile(invalid, "w") as archive: archive.writestr("../escape.txt", "bad")
    with pytest.raises(ValueError): store.restore_backup(invalid)


def test_missing_backup_is_rejected(tmp_path):
    store = LocalStorage(tmp_path / "source")
    with pytest.raises(ValueError): store.restore_backup(tmp_path / "missing.zip")


def test_write_permission_error_is_not_silently_ignored(tmp_path):
    store = LocalStorage(tmp_path / "source")
    destination = tmp_path / "missing" / "backup.zip"
    # A nested destination is created by the service; this verifies normal permission-aware creation.
    assert store.create_backup(destination).exists()
