"""Вариант 2: объектная композиция Qt Widgets и механизм сигналов/слотов."""
from __future__ import annotations
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox)
from taskcore import TaskBoard, ValidationError

class TaskWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.board = TaskBoard("data/qt_tasks.json")
        self.setWindowTitle("Список задач — PySide6")
        self.resize(580, 440)
        layout = QVBoxLayout(self)
        title = QLabel("Управление задачами")
        title.setStyleSheet("font-size: 20px; font-weight: 600;")
        layout.addWidget(title)
        row = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Введите название задачи")
        row.addWidget(self.entry)
        btn_add = QPushButton("Добавить")
        row.addWidget(btn_add)
        layout.addLayout(row)
        self.items = QListWidget()
        layout.addWidget(self.items)
        row2 = QHBoxLayout()
        btn_toggle = QPushButton("Выполнена / вернуть")
        btn_delete = QPushButton("Удалить")
        row2.addWidget(btn_toggle)
        row2.addWidget(btn_delete)
        layout.addLayout(row2)
        self.counter = QLabel()
        layout.addWidget(self.counter)
        btn_add.clicked.connect(self.add_task)
        self.entry.returnPressed.connect(self.add_task)
        btn_toggle.clicked.connect(self.toggle_task)
        btn_delete.clicked.connect(self.remove_task)
        self.refresh()

    def refresh(self) -> None:
        self.items.clear()
        for task in self.board.tasks:
            self.items.addItem(f"{'✓' if task.done else '○'}  {task.id}. {task.title}")
        total, done = self.board.summary()
        self.counter.setText(f"Всего задач: {total}  |  Выполнено: {done}")

    def selected_id(self) -> int | None:
        idx = self.items.currentRow()
        return self.board.tasks[idx].id if idx >= 0 else None

    def add_task(self) -> None:
        try:
            self.board.add(self.entry.text())
            self.entry.clear()
            self.refresh()
        except ValidationError as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))

    def toggle_task(self) -> None:
        task_id = self.selected_id()
        if task_id is None:
            QMessageBox.information(self, "Выбор", "Выберите задачу")
            return
        self.board.toggle(task_id)
        self.refresh()

    def remove_task(self) -> None:
        task_id = self.selected_id()
        if task_id is None:
            QMessageBox.information(self, "Выбор", "Выберите задачу")
            return
        self.board.remove(task_id)
        self.refresh()


def main() -> None:
    app = QApplication(sys.argv)
    w = TaskWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
