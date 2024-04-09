import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import networkx as nx
from collections import deque
from tkinter import messagebox

import time
class Node:
    def __init__(self, x, y, color, text="N", id=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.h = 1
        self.id = id
    def Color(self, new_color):
        self.color = new_color
        Uniformed_canvas.itemconfig(self.id, fill=new_color)
    def SetH(self,h):
        self.h=h
    def display_attributes(self):
        print(self.x, self.y, self.text, self.color)
store = {'x': 0, 'y': 0, 'x2': 0, 'y2': 0}
global is_adding_node, is_editing_node, deleteNode, move_node_button
is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, False, False
def draw_temporary_line():
    Uniformed_canvas.delete("temp_line")
    Uniformed_canvas.create_line(store['x'], store['y'], store['x2'], store['y2'], tags="temp_line", fill="white", arrow=tk.LAST)
def draw():
    Uniformed_canvas.delete("temp_line")
    Uniformed_canvas.create_line(store['x'], store['y'], store['x2'], store['y2'], fill="white", arrow=tk.LAST)
    mid_x = (store['x'] + store['x2']) / 2
    mid_y = (store['y'] + store['y2']) / 2
    Uniformed_canvas.create_text(mid_x, mid_y - 10, text=f"Path Cost={path_cost}", fill="white")
ctNode = 0
# #In both the create_node and redraw_oval functions, we're creating a text item on the canvas to display the 'H' value of a node. This text item is created with the create_text method of the Uniformed_canvas object.
# In the original code, when you redraw the oval in the redraw_oval function, you're creating a new text item for the 'H' value but not deleting the old one. This results in two 'H' values being displayed.
# To fix this, I added a unique tag to the 'H' text item when it's created. This tag is h_text_{node.id} for the redraw_oval function and h_text_{node_instance.id} for the create_node function. The {node.id} and {node_instance.id} parts are replaced with the actual ID of the node, so each node's 'H' text item has a unique tag.
# Then, before creating a new 'H' text item, I delete all items with that tag. This is done with the delete method of the Uniformed_canvas object, which deletes all items with a given tag. This ensures that the old 'H' text item is removed before the new one is created, preventing multiple 'H' values from being displayed for the same node.
def create_node(x, y):
    global ctNode
    oval_id = Uniformed_canvas.create_oval(x, y, x + 45, y + 45, fill="brown", outline="white", width=2)
    center_x = (x + x + 45) / 2
    center_y = (y + y + 45) / 2
    node_instance = Node(x, y, "red",f"N{ctNode}", oval_id)
    Uniformed_canvas.create_text(center_x, center_y, text=node_instance.text , fill="white", tags=f"text_{node_instance.id}")
    ctNode += 1
    Uniformed_canvas.create_text(center_x, y - 10, text=f'H={node_instance.h}', fill="white", tags=[f"text_{node_instance.id}", f"h_text_{node_instance.id}"])
    g.add_node(node_instance)
    node_instance.display_attributes()
def find_node(x, y):
    for node in g.nodes():
        if node.x - 10 <= x <= node.x + 45 and node.y - 10 <= y <= node.y + 45:
            return node
    return None
def find_node_by_text(node_text):
    for node in g.nodes():
        if node.text == node_text:
            return node
    return None
def redraw_oval(node):
    # Remove existing oval and text
    Uniformed_canvas.delete(node.id)
    Uniformed_canvas.delete(f"h_text_{node.id}")
    # Redraw oval with updated attributes
    oval_id = Uniformed_canvas.create_oval(node.x, node.y, node.x + 45, node.y + 45, fill="brown", outline="white", width=2)
    node.id = oval_id
    # Recreate text with updated value
    center_x = (node.x + node.x + 45) / 2
    center_y = (node.y + node.y + 45) / 2
    Uniformed_canvas.create_text(center_x, center_y, text=node.text, fill="white", tags=f"text_{node.id}")
    Uniformed_canvas.create_text(center_x, node.y - 10, text=f'H={node.h}', fill="white", tags=[f"text_{node.id}", f"h_text_{node.id}"])
#####################MOUSE EVENTS###############################
def left_click(event):
    x, y = event.x, event.y
    if is_adding_node:
        create_node(x, y)
    if is_editing_node:
        edit_node(x, y)
    if deleteNode:
        RRRemove(x,y)
def on_right_click(event):
    global clicked_node
    x, y = event.x, event.y
    clicked_node = find_node(x, y)
    if clicked_node:
        clicked_node.Color("green")
        store['x'] = event.x
        store['y'] = event.y


def on_drag(event):
    global clicked_node
    if is_adding_node:
        store['x2'] = event.x
        store['y2'] = event.y
        draw_temporary_line()

def on_release(event):
    global path_cost
    if is_adding_node:
        second_node = find_node(event.x, event.y)
        if second_node and clicked_node:
            store["x2"] = event.x
            store["y2"] = event.y
            path_cost = simpledialog.askinteger("Cost", "Enter Path Cost")
            g.add_edge(clicked_node, second_node, weight=path_cost)
            edge_data = g.get_edge_data(clicked_node, second_node)
            if edge_data:
                edge_weight = edge_data.get('weight', 'N/A')
                print(f'The edge has been added between {clicked_node.text} and {second_node.text} with a path cost of {edge_weight}')
                draw()
#####################MOUSE EVENTS###############################
#####################BUTTON FUNCTIONS###############################
def activate_adding_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = True, False, False, False
    print(f"Adding node has been activated: is_adding_node={is_adding_node}")

def activate_editing_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, True, False, False
    print(f"Adding node has been activated: is_editing_node={is_editing_node}")
def activate_move_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, False, True
    print(f"Moving node has been activated: is_Move_node={move_node_button}")
def activate_delete_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, True, False
    print(f"delete node has been activated: is_delete_node={deleteNode}")
def edit_node(x, y):
    global g
    for node in g.nodes():
        if node.x - 10 <= x <= node.x + 45 and node.y - 10 <= y <= node.y + 45:
            h = simpledialog.askfloat("H", "Enter the H")
            if h==-1:
                return
            while h is None :
                if h==-1:
                    return
                h = simpledialog.askfloat("H", "Enter the H")
            node.h = h
            # Update the node in the graph
            g.nodes[node]['h'] = h
            # Redraw the oval with updated attributes
            redraw_oval(node)
            Uniformed_canvas.update()
            print(f"Node edited: {node.text}, new H={node.h}")
            return
    return None
def Reset():
    #btmsa7 kol haga
    global ctNode
    g.clear()
    Uniformed_canvas.delete("all")
    ctNode = 0
    print(f" ctNode->{ctNode}")
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, False, False
    print(is_adding_node, is_editing_node, deleteNode, move_node_button)
    print("All have been reset")
def RRRemove(x,y):
    Node=find_node(x,y)
    if Node:
#Get the edges connected to the node
        edges = list(g.edges(Node))
        # Remove the lines representing the edges from the canvas
        for edge in edges:
            Uniformed_canvas.delete(f"line_{edge[0].id}_{edge[1].id}")
            Uniformed_canvas.delete(f"line_{edge[1].id}_{edge[0].id}")
        #Remove the node from the graph
        g.remove_node(Node)
        # Remove the node from the canvas
        Uniformed_canvas.delete(Node.id)
        Uniformed_canvas.delete(f"text_{Node.id}")
        Uniformed_canvas.delete(f"h_text_{Node.id}")
        print(f"Node {Node.text} has been deleted.")
        Uniformed_canvas.update()
#####################BUTTON FUNCTIONS###############################
def create_status_texts():
    #text 3adi 3han ashrah el anitmation
    Uniformed_canvas.create_text(10, 10, text="Green -> Final Path", fill="green", anchor=tk.W)
    Uniformed_canvas.create_text(10, 30, text="Gray -> Visited", fill="gray", anchor=tk.W)
    Uniformed_canvas.create_text(10, 50, text="Orange -> Fringe", fill="orange", anchor=tk.W)
#####################SEARCH STRATGYES###############################
from collections import deque

def BFS(start_node_name):
    create_status_texts()
    Visited = []  # Array to store visited nodes
    Fringe = []  # Array to store nodes in the fringe
    FPath = []   # Array to store the final path

    visited = set() 
    queue = deque()  # Initialize a deque as the queue for BFS

    # Find the start_node by its name
    start_node = None
    for node in g.nodes():
        if node.text == start_node_name:
            start_node = node
            break

    if start_node is None:
        print(f"Node '{start_node_name}' not found in the graph. Starting traversal alphabetically.")
        start_node = sorted(list(g.nodes()), key=lambda x: x.text)[0]  # Start with the first node alphabetically

    queue.append((start_node, [start_node.text]))  # Add start_node and its path to the queue

    while queue:
        current_node, path = queue.popleft()  # Dequeue the node and its path
        Visited.append(current_node.text)  # Add the visited node to the Visited array
        Fringe.append([node.text for node, _ in queue])  # Add the nodes in the fringe to the Fringe array
        visited.add(current_node)
        current_node.Color("gray")  # Change color of the current node to gray (visited)
        Uniformed_canvas.update()  # Update the canvas to visualize the change
        time.sleep(0.5)
        FPath.append(current_node)  # Add the current node to the final path

        visited.add(current_node)
        if current_node.h == 0:
            print(f"Goal Node found: {current_node.text}")
            print(f"Final Correct Path from Start to Goal: {' -> '.join(path)}")
            print(f"Visited Nodes: {Visited}")
            print(f"Fringe Nodes: {Fringe}")
            print(f"Final Path: {FPath}")
            for node in path:
                find_node_by_text(node).Color("green")  # Change color only for nodes in the final path
                Uniformed_canvas.update()
                time.sleep(0.5)
            return

        neighbors = sorted(list(g.neighbors(current_node)), key=lambda x: x.text)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor.text]))
                neighbor.Color("orange")  # Change color of the neighbor to orange (fringe)
                Uniformed_canvas.update()
                time.sleep(1.5)

    print("No goal found after exploring all possible routes.")




def run_BFS():
    # Start DFS from node named 'N0' or alphabetically if 'N0' doesn't exist
    ct=-1
    start_node_name = 'N0'
    for node in g.nodes():
        node.Color("brown")
    for node in g.nodes():
        if node.h==0:
            ct+=1
            break
    if ct==-1:
        messagebox.showinfo("error","please edit the goal node!!!!")
        return
    BFS(start_node_name)

def DepthFirstSearch(start_node_name):

    create_status_texts()
    Visited = []  # Array to store visited nodes
    Fringe = []  # Array to store nodes in the fringe
    FPath = []   # Array to store the final path

    visited = set()
    stack = []  # Initialize a stack for DFS traversal

    # Find the start_node by its name
    start_node = None
    for node in g.nodes():
        if node.text == start_node_name:
            start_node = node
            break

    if start_node is None:
        print(f"Node '{start_node_name}' not found in the graph. Starting traversal alphabetically.")
        start_node = sorted(list(g.nodes()), key=lambda x: x.text)[0]  # Start with the first node alphabetically

    stack.append((start_node, [start_node.text]))  # Add start_node and its path to the stack

    while stack:
        current_node, path = stack.pop()  # Pop the node and its path from the stack
        Visited.append(current_node.text)  # Add the visited node to the Visited array
        Fringe.append([node.text for node, _ in stack])  # Add the nodes in the fringe to the Fringe array
        visited.add(current_node)
        current_node.Color("gray")  # Change color of the current node to gray (visited)
        Uniformed_canvas.update()  # Update the canvas to visualize the change
        time.sleep(0.5)
        FPath.append(current_node)  # Add the path to the final path

        visited.add(current_node)
        if current_node.h == 0:
            print(f"Goal Node found: {current_node.text}")
            print(f"Final Correct Path from Start to Goal: {' -> '.join(path)}")
            print(f"Visited Nodes: {Visited}")
            print(f"Fringe Nodes: {Fringe}")
            # print(f"Final Path: {FPath}")
            for node in path:
                find_node_by_text(node).Color("green")  # Change color only for nodes in the final path
                Uniformed_canvas.update()
                time.sleep(0.5)
            return  # Terminates Depth-First Search if goal node with heuristic value 0 is found

        neighbors = sorted(list(g.neighbors(current_node)), key=lambda x: x.text, reverse=True)  # Sort neighbors alphabetically in reverse for DFS
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor.text]))
                neighbor.Color("orange")  # Change color of the neighbor to orange (fringe)
                Uniformed_canvas.update()  # Update the canvas to visualize the change
                time.sleep(1.5)  # Push neighbor along with its path to the stack

    print("No goal found after exploring all possible routes.")

def create_status_texts():
    # Create text objects for status indication
    Uniformed_canvas.create_text(10, 10, text="Green -> Final Path", fill="green", anchor=tk.W)
    Uniformed_canvas.create_text(10, 30, text="Gray -> Visited", fill="gray", anchor=tk.W)
    Uniformed_canvas.create_text(10, 50, text="Orange -> Fringe", fill="orange", anchor=tk.W)

def find_node_by_text(text):
    for node in g.nodes():
        if node.text == text:
            return node
    return None

def UniformCostSearch(start_node_name):
    create_status_texts()
    Visited = []  # Array to store visited nodes
    Fringe = []  # Array to store nodes in the fringe
    FPath = []   # Array to store the final path

    visited = set()
    queue = []  # Initialize an empty priority queue

    # Find the start_node by its name
    start_node = None
    for node in g.nodes():
        if node.text == start_node_name:
            start_node = node
            break

    if start_node is None:
        print(f"Node '{start_node_name}' not found in the graph. Starting traversal alphabetically.")
        start_node = sorted(list(g.nodes()), key=lambda x: x.text)[0]  # Start with the first node alphabetically

    queue.append((0, start_node, [start_node.text], 0))  # Add start_node with cost and path to the queue

    while queue:
        queue.sort(key=lambda x: x[3])  # Sort the queue based on the cost
        _, current_node, path, cost = queue.pop(0)
        Visited.append(current_node.text)  # Add the visited node to the Visited array
        Fringe.append([node.text for _, node, _, _ in queue])  # Add the nodes in the fringe to the Fringe array
        visited.add(current_node)
        current_node.Color("gray")  # Change color of the current node to gray (visited)
        Uniformed_canvas.update()  # Update the canvas to visualize the change
        time.sleep(0.5)
        FPath.append(current_node)  # Add the path to the final path

        visited.add(current_node)
        if current_node.h == 0:
            print(f"Goal Node found: {current_node.text}")
            print(f"Final Correct Path from Start to Goal: {' -> '.join(path)}")
            print(f"Visited Nodes: {Visited}")
            print(f"Fringe Nodes: {Fringe}")
            print(f"Final Path: {FPath}")
            print(f"Final Path Cost: {cost}")  # Print the total cost of the final path

            for node in path:
                find_node_by_text(node).Color("green")  # Change color only for nodes in the final path
                Uniformed_canvas.update()
                time.sleep(0.5)
            return  # Terminates Uniform Cost Search if goal node with heuristic value 0 is found

        neighbors = sorted(list(g.neighbors(current_node)), key=lambda x: x.text)  # Sort neighbors alphabetically
        for neighbor in neighbors:
            if neighbor not in visited:
                edge_weight = g[current_node][neighbor]["weight"]
                queue.append((0, neighbor, path + [neighbor.text], cost + edge_weight))
                neighbor.Color("orange")  # Change color of the neighbor to orange (fringe)
                Uniformed_canvas.update()  # Update the canvas to visualize the change
                time.sleep(1.5) # Add neighbor to queue along with updated cost and path

    print("No goal found after exploring all possible routes.")

def run_ucs():
    # Start UCS from node named 'N0' or alphabetically if 'N0' doesn't exist
    start_node_name = 'N0'
    ct=-1
    for node in g.nodes():
        node.Color("brown")
    for node in g.nodes():
        if node.h==0:
            ct+=1
            break
    if ct==-1:
        messagebox.showinfo("error","please edit the goal node!!!!")
        return
    UniformCostSearch(start_node_name)

def run_dfs():
    # Start UCS from node named 'N0' or alphabetically if 'N0' doesn't exist
    start_node_name = 'N0'
    for node in g.nodes():
        node.Color("brown")
    ct=-1
    for node in g.nodes():
        if node.h==0:
            ct+=1
            break
    if ct==-1:
        messagebox.showinfo("error","please edit the goal node!!!!")
        return
    DepthFirstSearch(start_node_name)
#####################SEARCH STRATGYES###############################
    
####################MAIN WINDOW STRUCHTER###########################
def create_Uniformed_window():
    global Uniformed_window, Uniformed_canvas
    Uniformed_window = tk.Tk()
    Uniformed_window.title("Graph Editor")
    Uniformed_window.geometry("1000x500")
    Uniformed_canvas = tk.Canvas(Uniformed_window, width=1000, height=450, bg="black")
    Uniformed_canvas.pack(padx=20)
    Uniformed_canvas.bind("<Button-1>", left_click)
    Uniformed_canvas.bind("<Button-3>", on_right_click)
    Uniformed_canvas.bind("<B3-Motion>", on_drag)
    Uniformed_canvas.bind("<ButtonRelease-3>", on_release)
    create_buttons()
def create_buttons():
    add_node_button = ttk.Button(Uniformed_window, text="ADD NODE", command=activate_adding_node)
    add_node_button.place(x=100, y=470)
    edit_node_button = ttk.Button(Uniformed_window, text="EDIT NODE", command= activate_editing_node)
    edit_node_button.place(x=200, y=470)
    move_node_button = ttk.Button(Uniformed_window, text="MOVE NODE", command=activate_move_node)
    move_node_button.place(x=300, y=470)
    delete_node_button = ttk.Button(Uniformed_window, text="DELETE NODE", command=activate_delete_node)
    delete_node_button.place(x=400, y=470)
    RunUniformed_button = ttk.Button(Uniformed_window, text="RUN BFS", command=run_BFS)
    RunUniformed_button.place(x=500, y=470)
    RunDFS_button = ttk.Button(Uniformed_window, text="RUN DFS", command=run_dfs)
    RunDFS_button.place(x=600, y=470)
    RunUni_button = ttk.Button(Uniformed_window, text="RUN UNI", command=run_ucs)
    RunUni_button.place(x=700, y=470)
    reset_button = ttk.Button(Uniformed_window, text="RESET", command=Reset)
    reset_button.place(x=800, y=470)
    back_button = ttk.Button(Uniformed_window, text="BACK", command=Uniformed_window.destroy)
    back_button.place(x=900, y=470)
############################MAIN WINDOW#############################################################
g = nx.DiGraph()
