import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from uuid import uuid4

STATUSES = ("Não iniciado", "Em andamento", "Bloqueado", "Finalizado")


class LocalStorage:
    """Persistência local de projetos em arquivos JSON, sem banco de dados."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.projects_dir = self.root / "projetos"
        self.attachments_dir = self.root / "anexos"
        self.templates_dir = self.root / "templates"
        self.config_path = self.root / "configuracao.json"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists(): self.config_path.write_text("{}\n", encoding="utf-8")

    def list_projects(self) -> list[dict]:
        projects = []
        for path in self.projects_dir.glob("*/projeto.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if data.get("id") and data.get("name"):
                    projects.append(data)
            except (OSError, json.JSONDecodeError):
                continue
        return sorted(projects, key=lambda item: item["name"].casefold())

    def get_project(self, project_id: str) -> dict | None:
        path = self.projects_dir / project_id / "projeto.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def create_project(self, name: str, description: str = "", status: str = "Não iniciado") -> dict:
        project = {"id": uuid4().hex, "name": name.strip(), "description": description.strip(), "status": status, "where_stopped": "", "next_step": "", "notes": "", "completed_checks": [], "pending_checks": [], "prompts": []}
        self.save_project(project)
        return project

    def save_project(self, project: dict) -> dict:
        if not project.get("id") or not project.get("name", "").strip():
            raise ValueError("Nome do projeto é obrigatório")
        if project.get("status") not in STATUSES:
            raise ValueError("Status de projeto inválido")
        project = {"id": project["id"], "name": project["name"].strip(), "description": project.get("description", "").strip(), "status": project["status"], "where_stopped": project.get("where_stopped", "").strip(), "next_step": project.get("next_step", "").strip(), "notes": project.get("notes", "").strip(), "completed_checks": list(project.get("completed_checks", [])), "pending_checks": list(project.get("pending_checks", [])), "prompts": list(project.get("prompts", []))}
        folder = self.projects_dir / project["id"]
        folder.mkdir(parents=True, exist_ok=True)
        temp = folder / "projeto.json.tmp"
        temp.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(folder / "projeto.json")
        return project

    def update_project(self, project_id: str, name: str, description: str, status: str, where_stopped: str = "", next_step: str = "", notes: str = "", completed_checks: list[str] | None = None, pending_checks: list[str] | None = None, prompts: list[dict] | None = None) -> dict:
        if not self.get_project(project_id):
            raise FileNotFoundError("Projeto não encontrado")
        current = self.get_project(project_id) or {}
        return self.save_project({"id": project_id, "name": name, "description": description, "status": status, "where_stopped": where_stopped, "next_step": next_step, "notes": notes, "completed_checks": current.get("completed_checks", []) if completed_checks is None else completed_checks, "pending_checks": current.get("pending_checks", []) if pending_checks is None else pending_checks, "prompts": current.get("prompts", []) if prompts is None else prompts})

    def delete_project(self, project_id: str):
        project_dir = self.projects_dir / project_id
        if not project_dir.is_dir():
            raise FileNotFoundError("Projeto não encontrado")
        for child in project_dir.iterdir():
            if child.is_file(): child.unlink()
        project_dir.rmdir()

    def create_backup(self, destination: str | Path) -> Path:
        destination = Path(destination); destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
            for source in (self.projects_dir, self.attachments_dir, self.templates_dir, self.config_path):
                if source.is_file(): archive.write(source, source.relative_to(self.root))
                elif source.is_dir():
                    for file in source.rglob("*"):
                        if file.is_file(): archive.write(file, file.relative_to(self.root))
        return destination

    def restore_backup(self, source: str | Path):
        source = Path(source)
        if not source.is_file() or not zipfile.is_zipfile(source): raise ValueError("Arquivo de backup inválido")
        allowed = {"projetos", "anexos", "templates", "configuracao.json"}
        with zipfile.ZipFile(source) as archive:
            members = archive.namelist()
            for member in members:
                path = Path(member)
                if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] not in allowed: raise ValueError("Backup contém caminho inválido")
            with tempfile.TemporaryDirectory() as temp:
                extract = Path(temp); archive.extractall(extract)
                for name in ("projetos", "anexos", "templates"):
                    incoming = extract / name
                    if incoming.exists():
                        target = self.root / name; shutil.rmtree(target, ignore_errors=True); shutil.copytree(incoming, target)
                incoming_config = extract / "configuracao.json"
                if incoming_config.exists(): shutil.copy2(incoming_config, self.config_path)
