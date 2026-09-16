from pathlib import Path

from services.markdown import render_markdown


def project_to_markdown(project: dict) -> str:
    formats = project.get("text_formats", {})
    def text(key: str) -> str:
        value = project.get(key, "")
        return render_markdown(value) if formats.get(key) == "markdown" else value

    lines = [f"# {project.get('name', '')}", "", f"**Status:** {project.get('status', '')}", ""]
    if project.get("description"):
        lines += ["## Descrição", "", text("description"), ""]
    for key, heading in (("where_stopped", "Onde parei"), ("next_step", "Próximo passo"), ("notes", "Observações")):
        if project.get(key): lines += [f"## {heading}", "", text(key), ""]
    if project.get("completed_checks"):
        lines += ["## O que já rodei", ""] + [f"- [x] {item}" for item in project["completed_checks"]] + [""]
    if project.get("pending_checks"):
        lines += ["## O que falta executar", ""] + [f"- [ ] {item}" for item in project["pending_checks"]] + [""]
    if project.get("prompts"):
        lines += ["## Prompts", ""]
        for prompt in project["prompts"]:
            content = render_markdown(prompt.get("content", "")) if prompt.get("format") == "markdown" else prompt.get("content", "")
            lines += [f"### {prompt.get('title', '')}", "", f"**Categoria:** {prompt.get('category', '')}", "", content, ""]
    return "\n".join(lines).rstrip() + "\n"


def export_project_markdown(project: dict, destination: str | Path) -> Path:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(project_to_markdown(project), encoding="utf-8")
    return destination
