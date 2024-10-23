import graphviz
import webbrowser
import os
from tkinter import messagebox
from loguru import logger

# Настройка логирования
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

class Graph:
    def __init__(self):
        try:
            self.nodes = []
            self.edges = []
            self.dot = graphviz.Digraph()
            self.node_types = self.get_node_types()  # Получаем типы узлов
            logger.info("Граф успешно инициализирован.")
        except Exception as e:
            logger.exception(f"Ошибка при инициализации графа: {e}")
            self.show_error("Ошибка инициализации", str(e))

    @staticmethod
    def get_node_types():
        try:
            node_types = {
                "Прямоугольник": "rectangle",
                "Ромб": "diamond",
                "Эллипс": "ellipse",
                "Круг": "circle",
                "Ящик": "box",
                "Параллелограмм": "parallelogram",
                "Шестиугольник": "hexagon"
            }
            logger.info("Типы узлов успешно получены.")
            return node_types
        except Exception as e:
            logger.exception(f"Ошибка при получении типов узлов: {e}")
            return {}

    def add_node(self, node_name, node_type):
        try:
            if node_name not in [n[0] for n in self.nodes]:
                self.nodes.append((node_name, node_type))
                self.dot.node(node_name, shape=node_type, label=node_name, width='1.5', height='0.5',
                              fontsize='10', fixedsize='true')
                logger.info(f"Узел '{node_name}' типа '{node_type}' успешно добавлен.")
                self.show_info("Узел добавлен", f"Узел '{node_name}' типа '{node_type}' добавлен.")
                self.show_graph()
            else:
                logger.error(f"Узел '{node_name}' уже существует.")
                self.show_error("Ошибка", f"Узел '{node_name}' уже существует.")
        except Exception as e:
            logger.exception(f"Ошибка при добавлении узла '{node_name}': {e}")
            self.show_error("Ошибка добавления узла", str(e))

    def add_edge(self, edge_from, edge_to, edge_label=None):
        try:
            if (edge_from, edge_to, edge_label) not in self.edges:
                self.edges.append((edge_from, edge_to, edge_label))
                if edge_label:
                    self.dot.edge(edge_from, edge_to, label=edge_label)
                else:
                    self.dot.edge(edge_from, edge_to)
                logger.info(f"Связь '{edge_from}' -> '{edge_to}' успешно добавлена.")
                self.show_info("Связь добавлена", f"Связь '{edge_from}' -> '{edge_to}' добавлена.")
                self.show_graph()
            else:
                logger.error(f"Связь '{edge_from}' -> '{edge_to}' уже существует.")
                self.show_error("Ошибка", f"Связь '{edge_from}' -> '{edge_to}' уже существует.")
        except Exception as e:
            logger.exception(f"Ошибка при добавлении связи '{edge_from}' -> '{edge_to}': {e}")
            self.show_error("Ошибка добавления связи", str(e))

    def get_node_names(self):
        try:
            node_names = [name for name, _ in self.nodes]
            logger.info("Имена узлов успешно получены.")
            return node_names
        except Exception as e:
            logger.exception(f"Ошибка при получении имен узлов: {e}")
            self.show_error("Ошибка получения имен узлов", str(e))
            return []

    def show_graph(self):
        try:
            output_file = 'graph.html'
            self.dot.attr(rankdir='LR')  # Устанавливаем направление справа налево
            self.dot.render(filename='graph', format='svg', cleanup=True)

            with open(output_file, 'w') as f:
                f.write(f'<html><body><img src="graph.svg" style="width:100%; height:auto;"></body></html>')

            logger.info("Граф успешно отрисован и сохранен.")
            webbrowser.open('file://' + os.path.realpath(output_file))
        except Exception as e:
            logger.exception(f"Ошибка при отображении графа: {e}")
            self.show_error("Ошибка отображения графа", str(e))

    @staticmethod
    def show_info(title, message):
        try:
            messagebox.showinfo(title, message)
            logger.info(f"Сообщение: {title} - {message}")
        except Exception as e:
            logger.exception(f"Ошибка при отображении информационного сообщения: {e}")

    @staticmethod
    def show_error(title, message):
        try:
            messagebox.showerror(title, message)
            logger.error(f"Ошибка: {title} - {message}")
        except Exception as e:
            logger.exception(f"Ошибка при отображении сообщения об ошибке: {e}")
