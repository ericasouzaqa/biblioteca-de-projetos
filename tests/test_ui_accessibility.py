import os

import pytest

if not os.environ.get("DISPLAY") and os.name != "nt":
    pytest.skip("Teste de Tkinter requer display", allow_module_level=True)

from storage.local_storage import LocalStorage
from ui.main_window import FOCUS, MainWindow, PromptDialog


def test_main_window_has_keyboard_focus_and_supported_palette(tmp_path):
    app = MainWindow(LocalStorage(tmp_path / "Biblioteca"))
    try:
        assert app.title() == "Biblioteca de Projetos QA"
        assert FOCUS == "#FF4FD8"
    finally:
        app.destroy()


def test_prompt_dialog_binds_enter_and_escape(tmp_path):
    app = MainWindow(LocalStorage(tmp_path / "Biblioteca"))
    dialog = PromptDialog(app)
    try:
        assert dialog.bind("<Return>")
        assert dialog.bind("<Escape>")
    finally:
        dialog.destroy()
        app.destroy()
