from pathlib import Path

from storage.local_storage import LocalStorage
from ui.main_window import MainWindow


def main():
    data_dir = Path.home() / "Biblioteca"
    storage = LocalStorage(data_dir)
    app = MainWindow(storage)
    app.mainloop()


if __name__ == "__main__":
    main()
