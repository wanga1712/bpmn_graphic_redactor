from graphviz import Digraph
from tkinter import messagebox
from loguru import logger


class Graph:
    """
    Класс, представляющий граф с узлами и связями.

    Этот класс хранит узлы и связи графа, а также определяет направления и типы узлов,
    которые могут быть использованы в графической визуализации.
    """

    def __init__(self):
        """
        Инициализирует новый экземпляр графа.

        Создает пустую структуру для хранения узлов и связей, устанавливает
        направление графа по умолчанию и определяет доступные типы узлов с их формами.
        """
        self.nodes = {}  # Словарь для хранения узлов графа (имя узла: тип узла)
        self.edges = []  # Список для хранения связей графа (откуда, куда, метка)

        # Типы узлов с отображаемыми названиями и формами
        self.node_types = {
            "Прямоугольник": "rectangle",
            "Ромб": "diamond",
            "Эллипс": "ellipse",
            "Круг": "circle",
            "Ящик": "box",
            "Параллелограмм": "parallelogram",
            "Шестиугольник": "hexagon"
        }

    def add_node(self, name, shape):
        """
        Добавляет новый узел в граф.

        Если узел с таким именем уже существует, выводится предупреждение,
        и узел не добавляется.

        Параметры:
        - name (str): Имя узла, которое будет добавлено.
        - shape (str): Форма узла, ассоциируемая с его типом.
        """
        if name in self.nodes:
            logger.warning(f"Узел '{name}' уже существует.")  # Логирование предупреждения
            self.show_error("Ошибка", f"Узел с именем '{name}' уже существует.")  # Сообщение об ошибке
            return

        self.nodes[name] = shape  # Добавление узла в словарь
        logger.info(f"Узел '{name}' добавлен с формой '{shape}'.")  # Логирование успешного добавления

    def add_edge(self, from_node, to_node, direction, label=""):
        """
        Добавляет связь между двумя узлами в графе.

        Проверяет, существуют ли узлы, и если хотя бы один из них не найден,
        выводится сообщение об ошибке. Связь добавляется в список связей
        и устанавливается направление.

        Параметры:
        - from_node (str): Имя узла-источника.
        - to_node (str): Имя узла-назначения.
        - direction (str): Направление связи.
        - label (str, optional): Метка для связи. По умолчанию пустая строка.
        """
        if from_node not in self.nodes or to_node not in self.nodes:
            logger.error(f"Один или оба узла '{from_node}', '{to_node}' не найдены.")
            self.show_error("Ошибка", "Один или оба узла не существуют.")
            return

        self.edges.append((from_node, to_node, label, direction))  # Сохраняем направление
        logger.info(f"Связь добавлена: '{from_node}' -> '{to_node}' с меткой '{label}' и направлением '{direction}'.")

    def delete_last_node(self):
        """
        Удаляет последний узел из графа и все связи, связанные с ним.

        Если узлы отсутствуют, выводится сообщение об ошибке. В противном случае
        удаляется последний добавленный узел и все связи, которые с ним связаны.

        Возвращает:
        None
        """
        if not self.nodes:
            self.show_error("Ошибка", "Нет узлов для удаления.")  # Проверка на наличие узлов
            return

        last_node = list(self.nodes.keys())[-1]  # Получение имени последнего узла
        del self.nodes[last_node]  # Удаление узла из словаря

        # Удаляем также все связи, связанные с этим узлом
        self.edges = [edge for edge in self.edges if edge[0] != last_node and edge[1] != last_node]  # Фильтрация связей

        logger.info(f"Удален последний узел '{last_node}' и связанные с ним связи.")  # Логирование успешного удаления

    def get_node_names(self):
        """
        Получает список имен всех узлов в графе.

        Возвращает:
        list: Список имен узлов, существующих в графе.
        """
        return list(self.nodes.keys())  # Возвращаем список ключей из словаря узлов

    def get_graph_data(self):
        """
        Получает данные о текущем графе, включая узлы и связи.

        Возвращает:
        tuple: Кортеж, содержащий два элемента:
            - list: Список имен узлов в графе.
            - dict: Словарь связей, где ключами являются строки формата "from_node -> to_node",
              а значениями — метки связей.
        """
        nodes = list(self.nodes.keys())  # Получаем список имен узлов
        edges = {f"{from_node} -> {to_node}": (label, direction) for from_node, to_node, label, direction in
                 self.edges}  # Создаем словарь связей
        return nodes, edges  # Возвращаем список узлов и словарь связей

    def render_graph(self):
        """
        Отрисовывает граф с использованием библиотеки Graphviz и сохраняет его в файл.
        """
        try:
            # Вывод содержимого узлов и связей перед отрисовкой
            logger.debug(f"Содержимое узлов: {self.nodes}")
            logger.debug(f"Содержимое связей: {self.edges}")

            dot = Digraph(format='png')  # Создаем новый объект графа формата PNG

            # Добавляем узлы в граф
            for name, shape in self.nodes.items():
                dot.node(name, shape=shape)  # Добавляем узел с заданной формой
                logger.debug(f"Добавлен узел '{name}' с формой '{shape}'.")

            # Добавляем связи в граф, указывая направление для каждой связи
            for from_node, to_node, label, direction in self.edges:
                dot.edge(from_node, to_node, label=label if label else "", dir=direction)  # Указываем направление
                logger.debug(
                    f"Добавлена связь '{from_node}' -> '{to_node}' с меткой '{label}' и направлением '{direction}'.")

            dot.render("graph_output", view=True)  # Сохраняем граф в файл и открываем его
            logger.info("Граф успешно отрисован.")

        except Exception as e:
            logger.exception("Ошибка при отрисовке графа")  # Логируем ошибку
            self.show_error("Ошибка отрисовки",
                            f"Произошла ошибка при отрисовке: {e}")  # Показываем сообщение об ошибке

    @staticmethod
    def show_error(title, message):
        logger.error(f"{title}: {message}")
        messagebox.showerror(title, message)
