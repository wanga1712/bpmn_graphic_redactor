import tkinter as tk
from tkinter import ttk
from graph import Graph
from loguru import logger


class GraphInputApp(tk.Tk):
    """
    Основное окно приложения для создания диаграмм Graphviz.

    Этот класс наследуется от `tk.Tk`, инициализирует интерфейс пользователя и
    управляет компонентами для добавления узлов и связей в граф.
    """

    def __init__(self):
        """
        Инициализирует главное окно приложения.

        Устанавливает заголовок, размер окна и настраивает систему логирования.
        Создает экземпляр класса Graph для хранения структуры графа и вызывает
        метод для создания пользовательского интерфейса.
        """
        super().__init__()
        self.title("Graphviz Diagram Creator")  # Заголовок окна приложения
        self.geometry("470x550")  # Размер окна приложения

        # Создаем экземпляр графа
        self.graph = Graph()

        # Создаем виджеты пользовательского интерфейса
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Создает основные виджеты интерфейса приложения для работы с узлами графа и
        инициализирует структуру интерфейса.
        """
        try:
            # Метка и поле ввода для имени узла
            self.node_name_label = tk.Label(self, text="Название узла:")
            self.node_name_label.grid(row=0, column=0, padx=5, pady=5)
            self.node_name_entry = self.create_entry()
            self.node_name_entry.grid(row=0, column=1, padx=5, pady=5)

            # Метка и выпадающее меню для выбора типа узла
            self.node_type_label = tk.Label(self, text="Тип узла:")
            self.node_type_label.grid(row=1, column=0, padx=5, pady=5)
            self.node_type_var = tk.StringVar(value="Прямоугольник")
            self.node_type_menu = ttk.Combobox(self, textvariable=self.node_type_var)
            self.node_type_menu['values'] = list(self.graph.node_types.keys())
            self.node_type_menu.grid(row=1, column=1, padx=5, pady=5)

            # Кнопка для добавления узла
            self.add_node_button = tk.Button(self, text="Добавить узел", command=self.insert_node)
            self.add_node_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

            # Вызов функции для создания виджетов, связанных с добавлением связи между узлами
            self.create_edge_widgets()

            # Поле для отображения списка узлов и связей
            self.info_display = tk.Text(self, height=10, width=50)
            self.info_display.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

            # Кнопка для удаления последнего добавленного узла
            self.delete_last_node_button = tk.Button(self, text="Удалить последний узел", command=self.delete_last_node)
            self.delete_last_node_button.grid(row=7, column=1, columnspan=2, padx=5, pady=5)

        except Exception as e:
            # Логирование и отображение ошибки при создании виджетов
            logger.exception("Ошибка при создании виджетов")
            self.graph.show_error("Ошибка", f"Ошибка при создании интерфейса: {e}")

    def create_edge_widgets(self) -> None:
        """
        Создает виджеты для интерфейса управления связями между узлами,
        включая выбор узлов, задание метки перехода и настройку направления графа.
        """
        try:
            # Метка и выпадающее меню для выбора начального узла
            self.edge_from_label = tk.Label(self, text="Из узла:")
            self.edge_from_label.grid(row=3, column=0, padx=5, pady=5)
            self.edge_from_menu = ttk.Combobox(self)
            self.edge_from_menu.grid(row=3, column=1, padx=5, pady=5)

            # Метка и выпадающее меню для выбора конечного узла
            self.edge_to_label = tk.Label(self, text="В узел:")
            self.edge_to_label.grid(row=4, column=0, padx=5, pady=5)
            self.edge_to_menu = ttk.Combobox(self)
            self.edge_to_menu.grid(row=4, column=1, padx=5, pady=5)

            # Поле для запроса на добавление метки перехода
            self.edge_label_question = tk.Label(self, text="Добавить метку перехода?")
            self.edge_label_question.grid(row=5, column=0, padx=5, pady=5)

            # Переключатели для добавления или исключения метки
            self.edge_label_var = tk.StringVar(value="нет")
            self.yes_button = tk.Radiobutton(self, text="Да", variable=self.edge_label_var, value="да")
            self.yes_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")
            self.no_button = tk.Radiobutton(self, text="Нет", variable=self.edge_label_var, value="нет")
            self.no_button.grid(row=5, column=1, padx=5, pady=5)

            # Поле ввода для метки, отображается только если выбран вариант "Да"
            self.edge_label_entry = self.create_entry()
            self.edge_label_entry.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

            # Кнопка добавления связи
            self.add_edge_button = tk.Button(self, text="Добавить связь", command=self.insert_edge)
            self.add_edge_button.grid(row=7, column=0, columnspan=1, padx=5, pady=5)

            # Поля для выбора направления отрисовки графа
            self.direction_var = tk.StringVar(value="LR")
            direction_label = tk.Label(self, text="Направление отрисовки:")
            direction_label.grid(row=8, column=0, padx=5, pady=5)

            # Кнопка отображения графа
            self.show_graph_button = tk.Button(self, text="Показать граф", command=self.graph.render_graph)
            self.show_graph_button.grid(row=8, column=1, columnspan=2, padx=5, pady=10)

            # Переключатели для выбора направления графа: слева направо, сверху вниз и т.д.
            self.lr_button = tk.Radiobutton(self, text="Слева направо (LR)", variable=self.direction_var, value="LR")
            self.lr_button.grid(row=9, column=0, padx=5, pady=5, sticky="w")
            self.tb_button = tk.Radiobutton(self, text="Сверху вниз (TB)", variable=self.direction_var, value="TB")
            self.tb_button.grid(row=9, column=1, padx=5, pady=5, sticky="w")
            self.rl_button = tk.Radiobutton(self, text="Справа налево (RL)", variable=self.direction_var, value="RL")
            self.rl_button.grid(row=10, column=0, padx=5, pady=5, sticky="w")
            self.bt_button = tk.Radiobutton(self, text="Снизу вверх (BT)", variable=self.direction_var, value="BT")
            self.bt_button.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        except Exception as e:
            # Логирование и отображение ошибки при создании виджетов для связей
            logger.exception("Ошибка при создании полей для связей")
            self.graph.show_error("Ошибка", f"Ошибка при создании полей для связей: {e}")

    def create_entry(self):
        """
        Создает виджет ввода текста (Entry) с привязанным обработчиком для вставки текста
        из буфера обмена по комбинации клавиш Ctrl+V.

        Returns:
            tk.Entry: Созданный виджет ввода текста.
        """
        entry = tk.Entry(self)  # Создаем виджет ввода текста
        entry.bind("<Control-v>", self.paste_text)  # Привязываем обработчик вставки текста
        return entry  # Возвращаем созданный виджет

    def paste_text(self, event):
        """
        Обработчик вставки текста из буфера обмена в виджет ввода текста (Entry).

        Параметры:
            event (tk.Event): Событие, связанное с виджетом, из которого выполняется вставка.
        """
        entry = event.widget  # Получаем виджет, вызвавший событие
        try:
            entry.delete(0, tk.END)  # Удаляем текущий текст из виджета
            entry.insert(0, self.clipboard_get())  # Вставляем текст из буфера обмена
        except tk.TclError as e:
            logger.error("Ошибка вставки текста из буфера обмена")  # Логируем ошибку вставки
            self.graph.show_error("Ошибка вставки", f"Не удалось вставить текст: {e}")  # Показываем сообщение об ошибке

    def insert_edge(self):
        """
        Обработчик для добавления связи (ребра) между узлами графа.

        Эта функция получает значения из интерфейса для определения
        узлов, между которыми добавляется связь, а также метки и
        направления этой связи. При возникновении ошибок выводится сообщение.
        """
        try:
            edge_from = self.edge_from_menu.get()  # Получаем исходный узел из выпадающего меню
            edge_to = self.edge_to_menu.get()  # Получаем целевой узел из выпадающего меню
            edge_label = self.edge_label_entry.get()  # Получаем метку связи из поля ввода

            # Проверяем, если выбрана метка, но она не введена
            if edge_label == "" and self.edge_label_var.get() == "да":
                self.graph.show_error("Ошибка", "Если выбрано 'Да', необходимо ввести метку.")
                return  # Завершаем выполнение функции, если метка не введена

            direction = self.direction_var.get()  # Получаем направление отрисовки из радиокнопок
            self.graph.add_edge(edge_from, edge_to, direction, edge_label)  # Добавляем связь в граф
            self.update_display()  # Обновляем отображение графа
        except Exception as e:
            logger.exception("Ошибка при добавлении связи")  # Логируем ошибку добавления
            self.graph.show_error("Ошибка", f"Ошибка при добавлении связи: {e}")  # Показываем сообщение об ошибке

    def insert_node(self):
        """
        Обработчик для добавления нового узла в граф.

        Эта функция получает название и тип узла из интерфейса и добавляет его в граф.
        Если название узла пустое, выводится сообщение об ошибке.
        """
        try:
            node_name = self.node_name_entry.get()  # Получаем название узла из поля ввода
            node_type = self.graph.node_types[self.node_type_var.get()]  # Получаем тип узла из выпадающего меню

            if node_name:  # Проверяем, что название узла не пустое
                self.graph.add_node(node_name, node_type)  # Добавляем узел в граф
                self.update_edge_menus()  # Обновляем меню для связей, если узлы изменились
                self.node_name_entry.delete(0, tk.END)  # Очищаем поле ввода названия узла
                self.update_display()  # Обновляем отображение графа
            else:
                self.graph.show_error("Ошибка",
                                      "Название узла не может быть пустым.")  # Показываем сообщение об ошибке, если название пустое
        except Exception as e:
            logger.exception("Ошибка при добавлении узла")  # Логируем ошибку добавления
            self.graph.show_error("Ошибка", f"Ошибка при добавлении узла: {e}")  # Показываем сообщение об ошибке

    def delete_last_node(self):
        """
        Обработчик для удаления последнего узла из графа.

        Эта функция вызывает метод удаления последнего узла, обновляет меню связей
        и отображение графа после удаления узла.
        """
        try:
            self.graph.delete_last_node()  # Удаляем последний узел из графа
            self.update_edge_menus()  # Обновляем меню для связей, чтобы отразить изменения
            self.update_display()  # Обновляем отображение графа
        except Exception as e:
            logger.exception("Ошибка при удалении последнего узла")  # Логируем ошибку удаления
            self.graph.show_error("Ошибка", f"Ошибка при удалении узла: {e}")  # Показываем сообщение об ошибке

    def update_edge_menus(self):
        """
        Обновляет меню выбора узлов для создания связей.

        Эта функция получает имена всех узлов из графа и обновляет выпадающие меню
        для выбора узлов, из которых и в которые будет добавлена связь.
        """
        try:
            node_names = self.graph.get_node_names()  # Получаем список имен узлов из графа
            self.edge_from_menu['values'] = node_names  # Обновляем меню "Из узла" с новыми именами узлов
            self.edge_to_menu['values'] = node_names  # Обновляем меню "В узел" с новыми именами узлов
        except Exception as e:
            logger.error("Ошибка при обновлении меню выбора узлов")  # Логируем ошибку обновления
            self.graph.show_error("Ошибка", f"Ошибка при обновлении меню: {e}")  # Показываем сообщение об ошибке

    def update_display(self):
        """
        Обновляет текстовое поле для отображения текущих узлов и связей в графе.

        Эта функция получает данные о текущих узлах и связях из графа, очищает текстовое поле,
        а затем заново заполняет его списком узлов и связей с указанием направления.
        """
        try:
            nodes, edges = self.graph.get_graph_data()  # Получаем данные графа: узлы и связи
            self.info_display.delete(1.0, tk.END)  # Очищаем поле отображения
            self.info_display.insert(tk.END, "Узлы:\n")  # Заголовок для списка узлов

            # Заполняем поле списком узлов
            for node in nodes:
                self.info_display.insert(tk.END, f" - {node}\n")

            self.info_display.insert(tk.END, "\nСвязи:\n")  # Заголовок для списка связей

            # Заполняем поле списком связей с указанием направлений
            for edge, (label, direction) in edges.items():  # Обновлено для извлечения метки и направления
                self.info_display.insert(tk.END, f" - {edge}: метка '{label}', направление {direction}\n")

        except Exception as e:
            logger.error("Ошибка при обновлении поля отображения узлов и связей")  # Логируем ошибку
            self.graph.show_error("Ошибка", f"Ошибка при обновлении отображения: {e}")  # Показываем сообщение об ошибке


if __name__ == "__main__":
    try:
        app = GraphInputApp()
        app.mainloop()
    except Exception as e:
        logger.critical("Критическая ошибка в приложении", exc_info=e)
