import graphviz
import webbrowser
import os
from tkinter import messagebox

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.dot = graphviz.Digraph()

        self.node_types = {
            "Прямоугольник": "rectangle",
            "Ромб": "diamond",
            "Эллипс": "ellipse",
            "Круг": "circle",
            "Ящик": "box",
            "Параллелограмм": "parallelogram",
            "Шестиугольник": "hexagon"
        }

    def get_node_types(self):
        return list(self.node_types.keys())

    def add_node(self, node_name, node_type):
        if node_name not in [n[0] for n in self.nodes]:
            self.nodes.append((node_name, node_type))
            self.dot.node(node_name, shape=node_type, label=node_name, width='1.5', height='0.5',
                          fontsize='10', fixedsize='true')
            messagebox.showinfo("Узел добавлен", f"Узел '{node_name}' типа '{node_type}' добавлен.")
            self.show_graph()  # Обновляем граф после добавления узла
        else:
            messagebox.showerror("Ошибка", f"Узел '{node_name}' уже существует.")

    def add_edge(self, edge_from, edge_to, edge_label):
        if (edge_from, edge_to, edge_label) not in self.edges:
            self.edges.append((edge_from, edge_to, edge_label))
            if edge_label:
                self.dot.edge(edge_from, edge_to, label=edge_label)
            else:
                self.dot.edge(edge_from, edge_to)
            messagebox.showinfo("Связь добавлена", f"Связь '{edge_from}' -> '{edge_to}' добавлена.")
            self.show_graph()  # Обновляем граф после добавления рёбер
        else:
            messagebox.showerror("Ошибка", f"Связь '{edge_from}' -> '{edge_to}' уже существует.")

    def get_node_names(self):
        return [name for name, _ in self.nodes]

    def show_graph(self):
        output_file = 'graph.html'
        self.dot.render(filename='graph', format='svg', cleanup=True)  # Сохраняем граф в формате SVG

        with open(output_file, 'w') as f:
            f.write(f'<html><body><img src="graph.svg" style="width:100%; height:auto;"></body></html>')

        webbrowser.open('file://' + os.path.realpath(output_file))

