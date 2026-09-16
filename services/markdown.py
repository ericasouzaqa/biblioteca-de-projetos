import re


def render_markdown(text: str) -> str:
    """Renderiza uma visualização textual segura de Markdown, sem alterar o conteúdo salvo."""
    lines = []
    in_code = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            lines.append("──────── código ────────" if in_code else "──── fim do código ────")
            continue
        if in_code:
            lines.append(line)
            continue
        if line.startswith("### "):
            lines.append(line[4:].upper())
        elif line.startswith("## "):
            lines.append(line[3:].upper())
        elif line.startswith("# "):
            lines.append(line[2:].upper())
        elif re.match(r"^\s*[-*]\s+", line):
            lines.append("• " + re.sub(r"^\s*[-*]\s+", "", line))
        else:
            lines.append(re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m.group(1) or m.group(2), line))
    return "\n".join(lines)
