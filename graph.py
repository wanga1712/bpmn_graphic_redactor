import networkx as nx
import webbrowser
import os
from loguru import logger
from pyvis.network import Network

class GraphRenderer:
    def __init__(self):
        """
        Инициализирует граф как ориентированный с использованием NetworkX.
        """
        # Добавляем новый логгер для хранения сообщений о добавлении узлов и связей
        self.graph_logger = logger.bind(source="graph_logger")
        self.graph_logs = []  # Список для хранения логов графа

        # Настройка логирования в список
        self.graph_logger.add(lambda msg: self.graph_logs.append(msg), level="INFO")

        self.graph = nx.DiGraph()  # Ориентированный граф
        self.nodes = {}  # Словарь для хранения узлов с их атрибутами
        self.edges = []  # Список для хранения связей и меток
        self.node_shapes = {  # Сопоставление названий форм с параметрами matplotlib
            "Прямоугольник": "s",
            "Ромб": "D",
            "Эллипс": "o",
            "Круг": "o",
            "Ящик": "s",
            "Параллелограмм": "p",
            "Шестиугольник": "h"
        }

    def wrap_text(self, text, max_length=25):
        """
        Переносит строки текста на новую строку, если строка превышает заданное количество символов.
        """
        return "\n".join([text[i:i+max_length] for i in range(0, len(text), max_length)])

    def add_node(self, name, shape, color="#000000"):
        """
        Добавляет узел в граф с указанной формой и цветом.
        """
        if name in self.nodes:
            logger.warning(f"Узел '{name}' уже существует.")
            return
        if shape not in self.node_shapes:
            logger.error(f"Форма '{shape}' не поддерживается.")
            return

        # Добавление узла в граф и запись его формы и цвета
        self.graph.add_node(name, shape=self.node_shapes[shape], color=color)
        self.nodes[name] = {"shape": shape, "color": color}
        logger.info(f"Узел '{name}' добавлен с формой '{shape}' и цветом '{color}'.")
        self.graph_logger.info(f"Узел '{name}' добавлен с формой '{shape}' и цветом '{color}'.")

    def add_edge(self, from_node, to_node, label=None):
        """
        Добавляет связь между двумя узлами с опциональной меткой.
        """
        if from_node not in self.nodes or to_node not in self.nodes:
            logger.error(f"Один или оба узла '{from_node}', '{to_node}' не найдены.")
            return

        label = self.wrap_text(label) if label else label  # Применяем перенос текста
        self.edges.append((from_node, to_node, label))  # Убираем направление
        logger.info(f"Связь добавлена: '{from_node}' -> '{to_node}' с меткой '{label}'.")
        self.graph_logger.info(f"Связь добавлена: '{from_node}' -> '{to_node}' с меткой '{label}'.")

    def delete_last_node(self):
        """
        Удаляет последний добавленный узел.
        """
        if not self.nodes:
            logger.error("Нет узлов для удаления.")
            return

        last_node = list(self.nodes.keys())[-1]
        self.graph.remove_node(last_node)
        del self.nodes[last_node]
        self.edges = [edge for edge in self.edges if last_node not in edge[:2]]
        logger.info(f"Удален узел '{last_node}' и все связанные с ним связи.")

    def render_graph(self):
        """
        Создает интерактивный HTML-файл с графом и открывает его в браузере.
        """
        try:
            # Создаем интерактивную сеть с помощью pyvis
            net = Network(directed=True)

            # Добавляем узлы с кастомизацией
            for node, attributes in self.nodes.items():
                shape = attributes["shape"]
                color = attributes["color"]
                label = self.wrap_text(node)
                net.add_node(
                    node,
                    label=label,
                    shape="ellipse" if shape == "Круг" else "box",
                    color=color,
                    size=25 if shape == "Круг" else 20  # Размер по типу узла
                )

            # Добавляем связи с кастомизацией и метками
            for from_node, to_node, label in self.edges:
                net.add_edge(
                    from_node,
                    to_node,
                    label=label,
                    color="gray",  # Цвет связей
                    width=2,  # Толщина связи
                    arrowStrikethrough=False
                )

            # Настройка физики для компактного отображения
            net.set_options("""
            var options = {
              "nodes": {
                "font": {"size": 16},
                "borderWidth": 2
              },
              "edges": {
                "smooth": {"type": "cubicBezier"},
                "color": {"inherit": true},
                "font": {"size": 12, "align": "middle"}
              },
              "physics": {
                "enabled": true,
                "stabilization": {"enabled": true},
                "barnesHut": {
                  "gravitationalConstant": -2000,
                  "centralGravity": 0.1,
                  "springLength": 150,
                  "springConstant": 0.05,
                  "damping": 0.09
                }
              }
            }
            """)

            # Сохраняем граф в HTML-файл и открываем его
            output_path = "business_process_visualization.html"
            net.show(output_path, notebook=False)
            webbrowser.open("file://" + os.path.abspath(output_path))
            logger.info("Граф бизнес-процесса успешно сохранен и открыт в браузере.")

        except Exception as e:
            logger.exception("Ошибка при отрисовке графа.")


    def show_error(self, title, message):
        """
        Показывает сообщение об ошибке.
        """
        logger.error(f"{title}: {message}")
