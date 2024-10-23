import tkinter as tk
from tkinter import ttk
from graph import Graph


class GraphInputApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphviz Diagram Creator")
        self.geometry("400x400")

        self.graph = Graph()  # Создаем экземпляр графа

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода для узлов
        self.node_name_label = tk.Label(self, text="Название узла:")
        self.node_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.node_name_entry = self.create_entry()
        self.node_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.node_type_label = tk.Label(self, text="Тип узла:")
        self.node_type_label.grid(row=1, column=0, padx=5, pady=5)
        self.node_type_var = tk.StringVar(value="Прямоугольник")
        self.node_type_menu = ttk.Combobox(self, textvariable=self.node_type_var)
        self.node_type_menu['values'] = list(self.graph.node_types.keys())  # Получаем типы узлов
        self.node_type_menu.grid(row=1, column=1, padx=5, pady=5)

        self.add_node_button = tk.Button(self, text="Добавить узел", command=self.add_node)
        self.add_node_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Поля ввода для связей
        self.create_edge_widgets()

        # Отображение графа
        self.show_graph_button = tk.Button(self, text="Показать граф", command=self.graph.show_graph)
        self.show_graph_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def create_edge_widgets(self):
        # Создание полей для связей
        self.edge_from_label = tk.Label(self, text="Из узла:")
        self.edge_from_label.grid(row=3, column=0, padx=5, pady=5)
        self.edge_from_menu = ttk.Combobox(self)
        self.edge_from_menu.grid(row=3, column=1, padx=5, pady=5)

        self.edge_to_label = tk.Label(self, text="В узел:")
        self.edge_to_label.grid(row=4, column=0, padx=5, pady=5)
        self.edge_to_menu = ttk.Combobox(self)
        self.edge_to_menu.grid(row=4, column=1, padx=5, pady=5)

        self.edge_label_question = tk.Label(self, text="Добавить метку перехода?")
        self.edge_label_question.grid(row=5, column=0, padx=5, pady=5)

        self.edge_label_var = tk.StringVar(value="нет")
        self.yes_button = tk.Radiobutton(self, text="Да", variable=self.edge_label_var, value="да")
        self.yes_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.no_button = tk.Radiobutton(self, text="Нет", variable=self.edge_label_var, value="нет")
        self.no_button.grid(row=5, column=1, padx=5, pady=5)

        self.edge_label_entry = self.create_entry()
        self.edge_label_entry.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.add_edge_button = tk.Button(self, text="Добавить связь", command=self.add_edge)
        self.add_edge_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def create_entry(self):
        entry = tk.Entry(self)
        entry.bind("<Control-v>", self.paste_text)
        return entry

    def paste_text(self, event):
        entry = event.widget
        try:
            entry.delete(0, tk.END)
            entry.insert(0, self.clipboard_get())
        except tk.TclError:
            self.graph.show_error("Ошибка вставки", "Не удалось вставить текст из буфера обмена.")

    def add_edge(self):
        edge_from = self.edge_from_menu.get()
        edge_to = self.edge_to_menu.get()
        edge_label = self.edge_label_entry.get()

        if edge_label == "":
            if self.edge_label_var.get() == "да":
                self.graph.show_error("Ошибка", "Если выбрано 'Да', необходимо ввести метку.")
                return
            edge_label = None  # Если "Нет", то метка пустая

        self.graph.add_edge(edge_from, edge_to, edge_label)  # Добавляем связь в граф
        self.update_edge_menus()  # Обновляем меню выбора узлов

    def add_node(self):
        node_name = self.node_name_entry.get()
        node_type = self.graph.node_types[self.node_type_var.get()]  # Получаем значение для типа узла

        if node_name:
            self.graph.add_node(node_name, node_type)  # Добавляем узел в граф
            self.update_edge_menus()  # Обновляем меню связей
            self.node_name_entry.delete(0, tk.END)  # Очищаем поле ввода
        else:
            self.graph.show_error("Ошибка", "Название узла не может быть пустым.")

    def update_edge_menus(self):
        self.edge_from_menu['values'] = self.graph.get_node_names()
        self.edge_to_menu['values'] = self.graph.get_node_names()


if __name__ == "__main__":
    app = GraphInputApp()
    app.mainloop()
