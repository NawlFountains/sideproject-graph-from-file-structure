
import time
import networkx as nx
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json

graph=nx.Graph()
current_folder = input("Enter filepath to generate graph: ")
target_ending = (".txt",".pdf")


def make_graph_tree(tree):
    for node in tree.children:
        graph.add_node(node.data , color='blue')
        graph.add_edge(tree.data,node.data)
        make_graph_tree(node)

def save_graph_tree():
    plt.figure(figsize=(40, 40))
    plt.title("File structure")
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.savefig("graph_output.png",bbox_inches='tight',dpi=100)  

class Tree:
    def __init__(self,data):
        self.children = []
        self.data = data
    def add_child(self,node):
        self.children.append(node)

root_node = Tree("agent")

def recursive_trace (file_path, parent_node):
    for filename in os.listdir(file_path):
        child_node = Tree(filename)
        if os.path.isdir(file_path+'/'+filename):
            parent_node.add_child(child_node)
            recursive_trace(file_path+'/'+filename, child_node)
        elif filename.endswith(target_ending):
            parent_node.add_child(child_node)

def create_graph():
    recursive_trace(current_folder, root_node)
    make_graph_tree(root_node)
    save_graph_tree()

create_graph()
# class MyHandler(FileSystemEventHandler):
#     def on_modified(self,event):
#         recursive_trace(current_folder, root_node)
#         print("FInishing event")
#         make_graph_tree(root_node)
#         save_graph_tree()



# event_handler= MyHandler()
# observer= Observer()
# observer.schedule(event_handler,current_folder,recursive=True)
# observer.start()

# try:
#     while True:
#         time.sleep(10)
#         print("Sleep finished")
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()