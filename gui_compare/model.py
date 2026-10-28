"""Модель задач и валидация независимо от технологии GUI."""
from __future__ import annotations
from dataclasses import dataclass, replace
import json
from pathlib import Path

class ValidationError(ValueError):
    """Некорректное действие пользователя."""

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool = False

class TaskBoard:
    """Хранилище задач; виджеты не должны изменять данные напрямую."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else None
        self.tasks: list[Task] = []
        if self.path and self.path.exists():
            self.load()

    def add(self, title: str) -> Task:
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Введите название задачи")
        if len(title.strip()) > 80:
            raise ValidationError("Название должно содержать не более 80 символов")
        task = Task(max((x.id for x in self.tasks), default=0) + 1, title.strip())
        self.tasks.append(task)
        self.save()
        return task

    def toggle(self, task_id: int) -> Task:
        for idx, task in enumerate(self.tasks):
            if task.id == task_id:
                changed = replace(task, done=not task.done)
                self.tasks[idx] = changed
                self.save()
                return changed
        raise ValidationError("Задача не найдена")

    def remove(self, task_id: int) -> None:
        if not any(x.id == task_id for x in self.tasks):
            raise ValidationError("Задача не найдена")
        self.tasks = [x for x in self.tasks if x.id != task_id]
        self.save()

    def summary(self) -> tuple[int, int]:
        return len(self.tasks), sum(x.done for x in self.tasks)

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([x.__dict__ for x in self.tasks], ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.path:
            raise ValidationError("Файл хранения не выбран")
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValidationError("Неверный формат файла")
        loaded = [Task(int(row["id"]), str(row["title"]), bool(row["done"])) for row in raw]
        if any(not x.title.strip() or x.id < 1 for x in loaded) or len({x.id for x in loaded}) != len(loaded):
            raise ValidationError("Неверные данные задач")
        self.tasks = loaded
