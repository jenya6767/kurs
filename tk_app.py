"""Вариант 1: процедурное создание виджетов Tkinter и обработчиков callback."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from taskcore import TaskBoard, ValidationError


def main() -> None:
    board = TaskBoard("data/tk_tasks.json")
    root = tk.Tk()
    root.title("Список задач — Tkinter")
    root.geometry("580x440")
    root.configure(bg="#f3f5f8")
    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Управление задачами", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 12))
    line = ttk.Frame(frame)
    line.pack(fill="x")
    entry = ttk.Entry(line)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
    items = tk.Listbox(frame, height=12, font=("Arial", 11), selectmode="browse")
    items.pack(fill="both", expand=True, pady=12)
    counter = ttk.Label(frame, text="")
    counter.pack(anchor="w")

    def refresh() -> None:
        items.delete(0, tk.END)
        for task in board.tasks:
            items.insert(tk.END, f"{'✓' if task.done else '○'}  {task.id}. {task.title}")
        total, done = board.summary()
        counter.configure(text=f"Всего задач: {total}  |  Выполнено: {done}")

    def selected_id() -> int | None:
        idx = items.curselection()
        return board.tasks[idx[0]].id if idx else None

    def add() -> None:
        try:
            board.add(entry.get())
            entry.delete(0, tk.END)
            refresh()
        except ValidationError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def perform(operation: str) -> None:
        item = selected_id()
        if item is None:
            messagebox.showinfo("Выбор", "Выберите задачу в списке")
            return
        try:
            board.toggle(item) if operation == "toggle" else board.remove(item)
            refresh()
        except ValidationError as exc:
            messagebox.showerror("Ошибка", str(exc))

    ttk.Button(line, text="Добавить", command=add).pack(side="left")
    controls = ttk.Frame(frame)
    controls.pack(fill="x", pady=5)
    ttk.Button(controls, text="Выполнена / вернуть", command=lambda: perform("toggle")).pack(side="left", padx=(0, 8))
    ttk.Button(controls, text="Удалить", command=lambda: perform("remove")).pack(side="left")
    entry.bind("<Return>", lambda _event: add())
    refresh()
    root.mainloop()


if __name__ == "__main__":
    main()
