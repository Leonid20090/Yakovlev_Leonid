import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

# Стартовый набор задач
DEFAULT_TASKS = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Написать отчёт", "type": "работа"},
    {"task": "Решить 5 задач по математике", "type": "учёба"},
    {"task": "Пробежать 3 км", "type": "спорт"},
    {"task": "Ответить на рабочие письма", "type": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("520x650")
        self.root.resizable(False, False)

        self.tasks = list(DEFAULT_TASKS)
        self.history = self.load_history()

        self.setup_ui()
        self.refresh_history()

    def setup_ui(self):
        # --- Фильтр ---
        ttk.Label(self.root, text="Фильтр по типу:").pack(pady=(10, 2))
        self.filter_var = tk.StringVar(value="все")
        self.type_combo = ttk.Combobox(self.root, textvariable=self.filter_var, state="readonly", width=20)
        self.type_combo['values'] = self._get_unique_types()
        self.type_combo.pack(pady=2)

        # --- Кнопка генерации и результат ---
        self.gen_btn = ttk.Button(self.root, text="🎲 Сгенерировать задачу", command=self.generate_task)
        self.gen_btn.pack(pady=10)

        self.result_var = tk.StringVar(value="Нажмите кнопку для генерации")
        ttk.Label(self.root, textvariable=self.result_var, font=("Segoe UI", 12, "bold"), wraplength=480, justify="center").pack(pady=5)

        # --- Добавление своей задачи ---
        ttk.Label(self.root, text="Добавить новую задачу:").pack(pady=(15, 5))
        add_frame = ttk.Frame(self.root)
        add_frame.pack(pady=5)

        self.new_task_entry = ttk.Entry(add_frame, width=25)
        self.new_task_entry.pack(side=tk.LEFT, padx=5)

        self.new_type_var = tk.StringVar(value="работа")
        ttk.Combobox(add_frame, textvariable=self.new_type_var, values=["учёба", "спорт", "работа"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)

        ttk.Button(add_frame, text="➕ Добавить", command=self.add_task).pack(side=tk.LEFT, padx=5)

        # --- История ---
        ttk.Label(self.root, text="📜 История задач:").pack(pady=(15, 5))
        self.history_lb = tk.Listbox(self.root, height=12, width=55, font=("Consolas", 9))
        self.history_lb.pack(padx=10, fill=tk.BOTH, expand=True)

    def _get_unique_types(self):
        types = list({t["type"] for t in self.tasks})
        types.sort()
        return ["все"] + types

    def generate_task(self):
        filt = self.filter_var.get()
        pool = [t for t in self.tasks if filt == "все" or t["type"] == filt]

        if not pool:
            self.result_var.set("⛔ Нет задач для выбранного фильтра.")
            return

        chosen = random.choice(pool)
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.history.insert(0, {"task": chosen["task"], "type": chosen["type"], "time": timestamp})
        
        self.result_var.set(f"✅ {chosen['task']}  (Тип: {chosen['type']})")
        self.refresh_history()
        self.save_history()

    def add_task(self):
        text = self.new_task_entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка ввода", "Задача не может быть пустой!")
            return

        new_type = self.new_type_var.get()
        self.tasks.append({"task": text, "type": new_type})
        self.new_task_entry.delete(0, tk.END)

        # Обновляем выпадающий список фильтров
        self.type_combo['values'] = self._get_unique_types()
        if self.filter_var.get() not in self.type_combo['values']:
            self.filter_var.set("все")

        messagebox.showinfo("Успех", f"Задача «{text}» добавлена в категорию «{new_type}»")

    def refresh_history(self):
        self.history_lb.delete(0, tk.END)
        for h in self.history:
            self.history_lb.insert(tk.END, f"[{h['time']}] {h['task']} ({h['type']})")

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
