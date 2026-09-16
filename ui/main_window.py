import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from uuid import uuid4

from services.markdown import render_markdown
from storage.local_storage import STATUSES

BG = "#0B1020"
SURFACE = "#16213E"
SURFACE_RAISED = "#16213E"
TEXT = "#00E5FF"
MUTED = "#F59E0B"
ACCENT = "#00E5FF"
FOCUS = "#FF4FD8"


def show_markdown_preview(parent, text, fmt):
    preview = tk.Toplevel(parent)
    preview.title("Preview — " + ("Markdown" if fmt == "markdown" else "Texto simples"))
    preview.geometry("700x500")
    preview.transient(parent)
    area = tk.Text(preview, bg=SURFACE_RAISED, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word")
    area.pack(fill="both", expand=True, padx=16, pady=16)
    area.insert("1.0", render_markdown(text) if fmt == "markdown" else text)
    area.configure(state="disabled")
    ttk.Button(preview, text="Fechar", command=preview.destroy).pack(anchor="e", padx=16, pady=(0, 16))


class ProjectDialog(tk.Toplevel):
    def __init__(self, parent, project=None):
        super().__init__(parent)
        self.result = None
        self.title("Editar Projeto" if project else "Novo Projeto")
        self.geometry("560x390")
        self.minsize(480, 340)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=BG)
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text=self.title(), style="Section.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", padx=22, pady=(20, 14))
        ttk.Label(self, text="Nome").grid(row=1, column=0, sticky="w", padx=22, pady=7)
        self.name = ttk.Entry(self); self.name.grid(row=1, column=1, sticky="ew", padx=(0, 22), pady=7)
        ttk.Label(self, text="Descrição").grid(row=2, column=0, sticky="nw", padx=22, pady=7)
        self.description = tk.Text(self, height=6, bg="#202d46", fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word")
        self.description.grid(row=2, column=1, sticky="nsew", padx=(0, 22), pady=7)
        ttk.Label(self, text="Formato").grid(row=3, column=0, sticky="w", padx=22, pady=7)
        self.description_format = ttk.Combobox(self, state="readonly", values=("Texto simples", "Markdown")); self.description_format.grid(row=3, column=1, sticky="ew", padx=(0, 22), pady=7); self.description_format.set("Texto simples")
        ttk.Button(self, text="Preview", command=lambda: show_markdown_preview(self, self.description.get("1.0", "end").strip(), "markdown" if self.description_format.get() == "Markdown" else "plain")).grid(row=3, column=1, sticky="e", padx=22, pady=7)
        ttk.Label(self, text="Status").grid(row=4, column=0, sticky="w", padx=22, pady=7)
        self.status = ttk.Combobox(self, state="readonly", values=STATUSES); self.status.grid(row=4, column=1, sticky="ew", padx=(0, 22), pady=7)
        buttons = ttk.Frame(self); buttons.grid(row=5, column=0, columnspan=2, sticky="e", padx=22, pady=20)
        ttk.Button(buttons, text="Cancelar", command=self.destroy).pack(side="left", padx=5)
        ttk.Button(buttons, text="Salvar", command=self.save).pack(side="left", padx=5)
        if project:
            self.name.insert(0, project["name"]); self.description.insert("1.0", project.get("description", "")); self.status.set(project.get("status", STATUSES[0]))
        else: self.status.set(STATUSES[0])
        self.description_format.set("Markdown" if project and project.get("text_formats", {}).get("description") == "markdown" else "Texto simples")
        self.name.focus_set()
        self.bind("<Return>", lambda _: self.save())
        self.bind("<Escape>", lambda _: self.destroy())

    def save(self):
        name = self.name.get().strip()
        if not name:
            messagebox.showwarning("Projeto", "Informe o nome do projeto.", parent=self); self.name.focus_set(); return
        self.result = {"name": name, "description": self.description.get("1.0", "end").strip(), "status": self.status.get(), "text_formats": {"description": "markdown" if self.description_format.get() == "Markdown" else "plain"}}
        self.destroy()


class ProjectWorkspace(tk.Toplevel):
    def __init__(self, parent, storage, project):
        super().__init__(parent); self.storage = storage; self.project = project; self.title("Projeto — " + project["name"]); self.geometry("900x680"); self.minsize(700, 520); self.transient(parent); self.grab_set(); self.columnconfigure(1, weight=1); self.rowconfigure(4, weight=1)
        ttk.Label(self, text=project["name"], style="Section.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))
        self.fields = {}
        for row, (label, key) in enumerate((("Onde parei", "where_stopped"), ("Próximo passo", "next_step"), ("Observações", "notes")), 1):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="nw", padx=20, pady=6); text = tk.Text(self, height=3 if key != "notes" else 4, bg="#202d46", fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word"); text.grid(row=row, column=1, sticky="ew", padx=(0, 20), pady=6); text.insert("1.0", project.get(key, "")); self.fields[key] = text
        lists = ttk.Frame(self); lists.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=10); lists.columnconfigure((0, 1), weight=1); lists.rowconfigure(1, weight=1)
        self.completed = self._checklist(lists, 0, "O que já rodei", project.get("completed_checks", [])); self.pending = self._checklist(lists, 1, "O que falta executar", project.get("pending_checks", []))
        actions = ttk.Frame(self); actions.grid(row=5, column=1, sticky="e", padx=20, pady=14); ttk.Label(actions, text="Formato:").pack(side="left", padx=4); self.text_format=ttk.Combobox(actions, state="readonly", values=("Texto simples","Markdown"), width=14); self.text_format.set("Markdown" if project.get("text_formats", {}).get("notes")=="markdown" else "Texto simples"); self.text_format.pack(side="left", padx=4); ttk.Button(actions, text="Preview", command=self.preview_text).pack(side="left", padx=4); ttk.Button(actions, text="Prompts", command=lambda: PromptManager(self, self.storage, self.project)).pack(side="left", padx=4); ttk.Button(actions, text="Salvar", command=self.save).pack(side="left", padx=4); self.bind("<Control-s>", lambda _: self.save()); self.bind("<Escape>", lambda _: self.destroy())

    def _checklist(self, parent, column, title, values):
        box = ttk.LabelFrame(parent, text=title, padding=8); box.grid(row=0, column=column, rowspan=2, sticky="nsew", padx=(0, 8) if column == 0 else (8, 0)); box.columnconfigure(0, weight=1); box.rowconfigure(0, weight=1); listbox = tk.Listbox(box, bg="#202d46", fg=TEXT, selectbackground="#285e61", relief="flat", height=10); listbox.grid(row=0, column=0, columnspan=3, sticky="nsew"); [listbox.insert("end", value) for value in values]
        ttk.Button(box, text="Adicionar", command=lambda: self._add_item(listbox)).grid(row=1, column=0, sticky="w", pady=(8, 0)); ttk.Button(box, text="Editar", command=lambda: self._edit_item(listbox)).grid(row=1, column=1, pady=(8, 0)); ttk.Button(box, text="Excluir", command=lambda: self._delete_item(listbox)).grid(row=1, column=2, sticky="e", pady=(8, 0)); return listbox

    def preview_text(self):
        text = "\n\n".join(self.fields[key].get("1.0", "end").strip() for key in ("where_stopped", "next_step", "notes"))
        show_markdown_preview(self, text, "markdown" if self.text_format.get() == "Markdown" else "plain")

    @staticmethod
    def _add_item(listbox):
        dialog = tk.Toplevel(listbox); dialog.title("Novo item"); entry = ttk.Entry(dialog, width=50); entry.pack(padx=14, pady=12); entry.focus_set(); ttk.Button(dialog, text="Salvar", command=lambda: (listbox.insert("end", entry.get().strip()) if entry.get().strip() else None, dialog.destroy())).pack(pady=(0, 12)); dialog.bind("<Return>", lambda _: (listbox.insert("end", entry.get().strip()) if entry.get().strip() else None, dialog.destroy()))

    @staticmethod
    def _edit_item(listbox):
        selection = listbox.curselection()
        if not selection: return
        dialog = tk.Toplevel(listbox); dialog.title("Editar item"); entry = ttk.Entry(dialog, width=50); entry.insert(0, listbox.get(selection[0])); entry.pack(padx=14, pady=12); entry.focus_set(); ttk.Button(dialog, text="Salvar", command=lambda: (listbox.delete(selection[0]), listbox.insert(selection[0], entry.get().strip()), dialog.destroy())).pack(pady=(0, 12)); dialog.bind("<Return>", lambda _: (listbox.delete(selection[0]), listbox.insert(selection[0], entry.get().strip()), dialog.destroy()))

    @staticmethod
    def _delete_item(listbox):
        selection = listbox.curselection()
        if selection and messagebox.askyesno("Checklist", "Excluir o item selecionado?", parent=listbox.winfo_toplevel()): listbox.delete(selection[0])

    def save(self):
        values = {key: text.get("1.0", "end").strip() for key, text in self.fields.items()}; values["text_formats"] = {key: ("markdown" if self.text_format.get() == "Markdown" else "plain") for key in self.fields}; values["completed_checks"] = list(self.completed.get(0, "end")); values["pending_checks"] = list(self.pending.get(0, "end")); self.storage.update_project(self.project["id"], self.project["name"], self.project.get("description", ""), self.project.get("status", STATUSES[0]), **values); messagebox.showinfo("Projeto", "Informações e checklists salvos em JSON.", parent=self); self.destroy()


class PromptDialog(tk.Toplevel):
    def __init__(self, parent, prompt=None):
        super().__init__(parent); self.result = None; self.title("Editar Prompt" if prompt else "Novo Prompt"); self.geometry("650x500"); self.minsize(520, 400); self.transient(parent); self.grab_set(); self.columnconfigure(1, weight=1); self.rowconfigure(3, weight=1)
        ttk.Label(self, text=self.title(), style="Section.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 12)); ttk.Label(self, text="Título").grid(row=1, column=0, sticky="w", padx=20, pady=6); self.title_entry=ttk.Entry(self); self.title_entry.grid(row=1,column=1,sticky="ew",padx=(0,20),pady=6); ttk.Label(self,text="Categoria").grid(row=2,column=0,sticky="w",padx=20,pady=6); self.category=ttk.Entry(self); self.category.grid(row=2,column=1,sticky="ew",padx=(0,20),pady=6); ttk.Label(self,text="Conteúdo").grid(row=3,column=0,sticky="nw",padx=20,pady=6); self.content=tk.Text(self,bg="#202d46",fg=TEXT,insertbackground=TEXT,relief="flat",wrap="word"); self.content.grid(row=3,column=1,sticky="nsew",padx=(0,20),pady=6); ttk.Label(self,text="Formato").grid(row=4,column=0,sticky="w",padx=20,pady=6); self.format=ttk.Combobox(self,state="readonly",values=("Texto simples","Markdown")); self.format.grid(row=4,column=1,sticky="ew",padx=(0,20),pady=6); self.format.set("Texto simples"); ttk.Button(self,text="Preview",command=lambda: show_markdown_preview(self,self.content.get("1.0","end").strip(),"markdown" if self.format.get()=="Markdown" else "plain")).grid(row=4,column=1,sticky="e",padx=20,pady=6); buttons=ttk.Frame(self); buttons.grid(row=5,column=0,columnspan=2,sticky="e",padx=20,pady=14); ttk.Button(buttons,text="Cancelar",command=self.destroy).pack(side="left",padx=4); ttk.Button(buttons,text="Salvar",command=self.save).pack(side="left",padx=4)
        if prompt: self.title_entry.insert(0,prompt.get("title","")); self.category.insert(0,prompt.get("category","")); self.content.insert("1.0",prompt.get("content",""))
        self.title_entry.focus_set(); self.format.set("Markdown" if prompt and prompt.get("format")=="markdown" else "Texto simples"); self.bind("<Return>",lambda _:self.save()); self.bind("<Escape>",lambda _:self.destroy())
    def save(self):
        title=self.title_entry.get().strip()
        if not title: messagebox.showwarning("Prompt","Informe o título.",parent=self); return
        self.result={"title":title,"category":self.category.get().strip(),"content":self.content.get("1.0","end").strip(),"format":"markdown" if self.format.get()=="Markdown" else "plain"}; self.destroy()


class PromptManager(tk.Toplevel):
    def __init__(self, parent, storage, project):
        super().__init__(parent); self.storage=storage; self.project=project; self.title("Prompts — "+project["name"]); self.geometry("900x560"); self.minsize(700,420); self.transient(parent); self.grab_set(); self.columnconfigure(0,weight=1); self.rowconfigure(1,weight=1)
        ttk.Label(self,text="Prompts do projeto",style="Section.TLabel").grid(row=0,column=0,sticky="w",padx=18,pady=(18,10)); bar=ttk.Frame(self); bar.grid(row=0,column=0,sticky="e",padx=18,pady=(18,10)); ttk.Button(bar,text="＋ Novo",command=self.new_prompt).pack(side="left"); ttk.Button(bar,text="Editar",command=self.edit_prompt).pack(side="left",padx=4); ttk.Button(bar,text="Duplicar",command=self.duplicate_prompt).pack(side="left"); ttk.Button(bar,text="Favoritar",command=self.toggle_favorite).pack(side="left",padx=4); ttk.Button(bar,text="Copiar",command=self.copy_prompt).pack(side="left"); ttk.Button(bar,text="Excluir",command=self.delete_prompt).pack(side="left",padx=4)
        self.tree=ttk.Treeview(self,columns=("favorite","title","category"),show="headings"); self.tree.heading("favorite",text="★"); self.tree.heading("title",text="Título"); self.tree.heading("category",text="Categoria"); self.tree.column("favorite",width=50); self.tree.column("title",width=380); self.tree.column("category",width=220); self.tree.grid(row=1,column=0,sticky="nsew",padx=18,pady=(0,18)); self.tree.bind("<Double-1>",lambda _:self.edit_prompt()); self.refresh()
    def prompts(self): return self.project.setdefault("prompts",[])
    def refresh(self):
        self.tree.delete(*self.tree.get_children()); [self.tree.insert("","end",iid=p["id"],values=("★" if p.get("favorite") else "",p.get("title",""),p.get("category",""))) for p in self.prompts()]
    def selected(self):
        selection=self.tree.selection(); return next((p for p in self.prompts() if p["id"]==selection[0]),None) if selection else None
    def persist(self): self.storage.update_project(self.project["id"],self.project["name"],self.project.get("description",""),self.project.get("status",STATUSES[0]),where_stopped=self.project.get("where_stopped",""),next_step=self.project.get("next_step",""),notes=self.project.get("notes",""),completed_checks=self.project.get("completed_checks",[]),pending_checks=self.project.get("pending_checks",[]),prompts=self.prompts())
    def new_prompt(self):
        dialog=PromptDialog(self); self.wait_window(dialog)
        if dialog.result: self.prompts().append({"id":uuid4().hex,"favorite":False,**dialog.result}); self.persist(); self.refresh()
    def edit_prompt(self):
        prompt=self.selected()
        if not prompt:return
        dialog=PromptDialog(self,prompt); self.wait_window(dialog)
        if dialog.result: prompt.update(dialog.result); self.persist(); self.refresh()
    def duplicate_prompt(self):
        prompt=self.selected()
        if prompt: copy={**prompt,"id":uuid4().hex,"title":prompt["title"]+" (cópia)","favorite":False}; self.prompts().append(copy); self.persist(); self.refresh()
    def toggle_favorite(self):
        prompt=self.selected()
        if prompt: prompt["favorite"]=not prompt.get("favorite",False); self.persist(); self.refresh()
    def copy_prompt(self):
        prompt=self.selected()
        if prompt: self.clipboard_clear(); self.clipboard_append(prompt.get("content","")); messagebox.showinfo("Prompt","Conteúdo copiado.",parent=self)
    def delete_prompt(self):
        prompt=self.selected()
        if prompt and messagebox.askyesno("Excluir prompt",f"Excluir '{prompt['title']}'?",parent=self): self.project["prompts"].remove(prompt); self.persist(); self.refresh()


class MainWindow(tk.Tk):
    def __init__(self, storage):
        super().__init__(); self.storage = storage; self.current = None; self.title("Biblioteca de Projetos QA"); self.geometry("1100x700"); self.minsize(800, 520); self.configure(bg=BG); self._configure_theme(); self._build_layout(); self.refresh_projects()

    def _configure_theme(self):
        style = ttk.Style(self); style.theme_use("clam"); style.configure(".", font=("Segoe UI", 11)); style.configure("TFrame", background=SURFACE); style.configure("TLabel", background=SURFACE, foreground=TEXT); style.configure("Muted.TLabel", background=SURFACE, foreground=MUTED); style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=("Segoe UI", 20, "bold")); style.configure("Section.TLabel", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 14, "bold")); style.configure("TButton", background=SURFACE_RAISED, foreground=TEXT, padding=(12, 8), borderwidth=1, relief="flat", focusthickness=2, focuscolor=FOCUS); style.map("TButton", background=[("active", FOCUS), ("pressed", ACCENT)], foreground=[("active", BG), ("pressed", BG)]); style.configure("Treeview", background=SURFACE, fieldbackground=SURFACE, foreground=TEXT, rowheight=32); style.map("Treeview", background=[("selected", FOCUS)], foreground=[("selected", BG)])

    def _build_layout(self):
        self._build_topbar(); body = ttk.Frame(self, padding=14); body.pack(fill="both", expand=True); body.columnconfigure(1, weight=1); body.rowconfigure(0, weight=1); self._build_sidebar(body); self._build_main_area(body)

    def _build_topbar(self):
        bar = tk.Frame(self, bg=BG, height=64); bar.pack(fill="x"); tk.Label(bar, text="Biblioteca de Projetos QA", bg=BG, fg=ACCENT, font=("Segoe UI", 20, "bold")).pack(side="left", padx=20, pady=14); tk.Label(bar, text="Offline • armazenamento JSON local", bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(side="left", padx=8); tk.Button(bar, text="Restaurar", command=self.restore_backup, bg=SURFACE_RAISED, fg=TEXT, activebackground=ACCENT, activeforeground=BG, relief="flat", padx=10, pady=6).pack(side="right", padx=6); tk.Button(bar, text="Backup", command=self.create_backup, bg=SURFACE_RAISED, fg=TEXT, activebackground=ACCENT, activeforeground=BG, relief="flat", padx=10, pady=6).pack(side="right")

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=SURFACE_RAISED, width=210); sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 14)); sidebar.grid_propagate(False); tk.Label(sidebar, text="NAVEGAÇÃO", bg=SURFACE_RAISED, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(20, 12))
        for label in ("Projetos", "Dashboard", "Configurações"):
            tk.Button(sidebar, text=label, anchor="w", relief="flat", borderwidth=0, bg=SURFACE_RAISED, fg=TEXT, activebackground=ACCENT, activeforeground=BG, padx=18, pady=10, command=lambda item=label: self._select_menu(item)).pack(fill="x", padx=8, pady=2)

    def _build_main_area(self, parent):
        self.main = ttk.Frame(parent, padding=18); self.main.grid(row=0, column=1, sticky="nsew"); self.main.columnconfigure(0, weight=1); self.main.rowconfigure(3, weight=1); self.show_projects()

    def show_projects(self):
        self.view = "projects"
        for child in self.main.winfo_children(): child.destroy()
        main = self.main; main.columnconfigure(0, weight=1); main.rowconfigure(3, weight=1); ttk.Label(main, text="Projetos", style="Section.TLabel").grid(row=0, column=0, sticky="w"); ttk.Label(main, text="Crie, edite, abra e organize seus projetos localmente.", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(5, 10))
        search = ttk.Frame(main); search.grid(row=2, column=0, sticky="ew", pady=(0, 10)); search.columnconfigure(1, weight=1); ttk.Label(search, text="Busca global").grid(row=0, column=0, padx=(0, 8)); self.search_var = tk.StringVar(); entry = ttk.Entry(search, textvariable=self.search_var); entry.grid(row=0, column=1, sticky="ew"); entry.bind("<KeyRelease>", lambda _: self.refresh_projects()); ttk.Button(search, text="Limpar", command=lambda: (self.search_var.set(""), self.refresh_projects())).grid(row=0, column=2, padx=(8, 0))
        content = ttk.Frame(main); content.grid(row=3, column=0, sticky="nsew"); content.columnconfigure(0, weight=1); content.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(content); toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8)); ttk.Button(toolbar, text="＋ Novo Projeto", command=self.new_project).pack(side="left"); ttk.Button(toolbar, text="Abrir", command=self.open_project).pack(side="left", padx=5); ttk.Button(toolbar, text="Editar", command=self.edit_project).pack(side="left"); ttk.Button(toolbar, text="Excluir", command=self.delete_project).pack(side="left", padx=5); self.project_count = ttk.Label(toolbar, text="0 projetos", style="Muted.TLabel"); self.project_count.pack(side="right")
        self.project_tree = ttk.Treeview(content, columns=("name", "status", "match"), show="headings"); self.project_tree.heading("name", text="Nome do projeto"); self.project_tree.heading("status", text="Status"); self.project_tree.heading("match", text="Resultado encontrado em"); self.project_tree.column("name", width=300, anchor="w"); self.project_tree.column("status", width=160, anchor="w"); self.project_tree.column("match", width=300, anchor="w"); self.project_tree.tag_configure("highlight", background="#285e61", foreground=TEXT); self.project_tree.grid(row=1, column=0, sticky="nsew"); self.project_tree.bind("<Double-1>", lambda _: self.open_project()); self.project_tree.bind("<Return>", lambda _: self.open_project()); self.project_tree.bind("<Delete>", lambda _: self.delete_project())

    def show_dashboard(self):
        self.view = "dashboard"
        for child in self.main.winfo_children(): child.destroy()
        self.main.columnconfigure((0, 1), weight=1); self.main.rowconfigure(1, weight=1)
        ttk.Label(self.main, text="Dashboard", style="Section.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18)); ttk.Label(self.main, text="Resumo atualizado automaticamente a partir dos arquivos JSON locais.", style="Muted.TLabel").grid(row=0, column=1, sticky="e", pady=(0, 18))
        self.dashboard_values = {}
        metrics = (("projects", "Total de projetos"), ("active", "Projetos em andamento"), ("finished", "Projetos finalizados"), ("prompts", "Quantidade de prompts"), ("pending", "Pendências abertas"))
        for index, (key, label) in enumerate(metrics):
            card = tk.Frame(self.main, bg=SURFACE_RAISED, padx=20, pady=18); card.grid(row=1 + index // 3, column=index % 3, sticky="nsew", padx=6, pady=6); self.main.columnconfigure(index % 3, weight=1); value = tk.Label(card, text="0", bg=SURFACE_RAISED, fg=ACCENT, font=("Segoe UI", 26, "bold")); value.pack(anchor="w"); tk.Label(card, text=label, bg=SURFACE_RAISED, fg=TEXT, font=("Segoe UI", 11)).pack(anchor="w", pady=(5, 0)); self.dashboard_values[key] = value
        self.update_dashboard()

    def update_dashboard(self):
        if getattr(self, "view", None) != "dashboard": return
        projects = self.storage.list_projects(); self.dashboard_values["projects"].configure(text=len(projects)); self.dashboard_values["active"].configure(text=sum(p.get("status") == "Em andamento" for p in projects)); self.dashboard_values["finished"].configure(text=sum(p.get("status") == "Finalizado" for p in projects)); self.dashboard_values["prompts"].configure(text=sum(len(p.get("prompts", [])) for p in projects)); self.dashboard_values["pending"].configure(text=sum(len(p.get("pending_checks", [])) for p in projects)); self.after(1000, self.update_dashboard)

    def refresh_projects(self):
        query = self.search_var.get().strip().casefold() if hasattr(self, "search_var") else ""
        projects = self.storage.list_projects(); self.project_tree.delete(*self.project_tree.get_children()); shown = 0
        for project in projects:
            fields = [("nome do projeto", project.get("name", "")), ("descrição", project.get("description", "")), ("observações", project.get("notes", "")), ("onde parei", project.get("where_stopped", "")), ("próximo passo", project.get("next_step", "")), ("checklist já rodei", " ".join(project.get("completed_checks", []))), ("checklist falta executar", " ".join(project.get("pending_checks", []))), ("prompts", " ".join(f"{p.get('title', '')} {p.get('category', '')} {p.get('content', '')}" for p in project.get("prompts", [])))]
            matches = [label for label, value in fields if query and query in value.casefold()]
            if query and not matches: continue
            match_text = ", ".join(matches) if query else ""
            self.project_tree.insert("", "end", iid=project["id"], values=(project["name"], project["status"], match_text), tags=("highlight",) if query else ()); shown += 1
        self.project_count.configure(text=f"{shown} resultado(s)" if query else f"{shown} projeto(s)")

    def selected_id(self):
        selection = self.project_tree.selection(); return selection[0] if selection else None

    def new_project(self):
        dialog = ProjectDialog(self); self.wait_window(dialog)
        if dialog.result:
            try:
                project = self.storage.create_project(**dialog.result); self.refresh_projects(); self.project_tree.selection_set(project["id"]); self.open_project()
            except (OSError, ValueError) as exc: messagebox.showerror("Projeto", f"Não foi possível criar o projeto:\n{exc}", parent=self)

    def edit_project(self):
        project_id = self.selected_id()
        if not project_id: messagebox.showinfo("Projeto", "Selecione um projeto para editar.", parent=self); return
        dialog = ProjectDialog(self, self.storage.get_project(project_id)); self.wait_window(dialog)
        if dialog.result:
            try: self.storage.update_project(project_id, **dialog.result); self.refresh_projects(); self.project_tree.selection_set(project_id)
            except (OSError, ValueError) as exc: messagebox.showerror("Projeto", f"Não foi possível salvar o projeto:\n{exc}", parent=self)

    def open_project(self):
        project_id = self.selected_id()
        if not project_id: messagebox.showinfo("Projeto", "Selecione um projeto para abrir.", parent=self); return
        project = self.storage.get_project(project_id); self.current = project
        ProjectWorkspace(self, self.storage, project)

    def delete_project(self):
        project_id = self.selected_id()
        if not project_id: messagebox.showinfo("Projeto", "Selecione um projeto para excluir.", parent=self); return
        project = self.storage.get_project(project_id)
        if messagebox.askyesno("Excluir projeto", f"Excluir permanentemente o projeto '{project['name']}'?", parent=self):
            try: self.storage.delete_project(project_id); self.current = None; self.refresh_projects()
            except OSError as exc: messagebox.showerror("Projeto", f"Não foi possível excluir o projeto:\n{exc}", parent=self)

    def create_backup(self):
        destination = filedialog.asksaveasfilename(parent=self, title="Salvar backup", defaultextension=".zip", filetypes=(("Arquivo ZIP", "*.zip"),))
        if destination and messagebox.askyesno("Backup", "Criar um ZIP com projetos, prompts, anexos e configurações?", parent=self):
            try: self.storage.create_backup(destination); messagebox.showinfo("Backup", "Backup criado com sucesso.", parent=self)
            except OSError as exc: messagebox.showerror("Backup", f"Não foi possível criar o backup:\n{exc}", parent=self)

    def restore_backup(self):
        source = filedialog.askopenfilename(parent=self, title="Selecionar backup", filetypes=(("Arquivo ZIP", "*.zip"),))
        if source and messagebox.askyesno("Restaurar", "A restauração substituirá projetos, anexos, templates e configuração atuais. Continuar?", parent=self):
            try:
                self.storage.restore_backup(source)
                if self.view == "projects": self.refresh_projects()
                else: self.show_projects(); self.refresh_projects()
                messagebox.showinfo("Restaurar", "Backup restaurado com sucesso.", parent=self)
            except (OSError, ValueError) as exc: messagebox.showerror("Restaurar", f"Não foi possível restaurar o backup:\n{exc}", parent=self)

    def _select_menu(self, item):
        if item == "Projetos": self.show_projects(); self.refresh_projects()
        elif item == "Dashboard": self.show_dashboard()
        else: messagebox.showinfo(item, "Esta seção será implementada em uma etapa futura.", parent=self)
