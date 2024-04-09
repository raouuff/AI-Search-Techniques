import time
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import networkx as nx

#rom phase1.Uniformed import Uniformed_canvas
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
        Informed_canvas.itemconfig(self.id, fill=new_color)
    def SetH(self,h):
        self.h=h
    def display_attributes(self):
        print(self.x, self.y, self.text, self.color)

store = {'x': 0, 'y': 0, 'x2': 0, 'y2': 0}
global is_adding_node, is_editing_node, deleteNode, move_node_button
is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, False, False

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
    elif move_node_button and clicked_node:
        # The same code as in on_drag
        new_x, new_y = event.x, event.y
        Informed_canvas.coords(clicked_node.id, new_x, new_y, new_x + 45, new_y + 45)
        center_x = (new_x + new_x + 45) / 2
        center_y = (new_y + new_y + 45) / 2
        Informed_canvas.coords(f"text_{clicked_node.id}", center_x, center_y)
        for edge in g.edges(clicked_node):
            other_node = edge[1] if edge[0] == clicked_node else edge[0]
            Informed_canvas.delete(f"edge_{clicked_node.id}_{other_node.id}")
            Informed_canvas.create_line(new_x, new_y, other_node.x, other_node.y, fill="white", arrow=tk.LAST, tags=f"edge_{clicked_node.id}_{other_node.id}")


def draw_temporary_line():
    Informed_canvas.delete("temp_line")  # Remove previous temporary line
    Informed_canvas.create_line(store['x'], store['y'], store['x2'], store['y2'], tags="temp_line", fill="white", arrow=tk.LAST)

def draw():
    Informed_canvas.delete("temp_line")  # Remove the temporary line
    Informed_canvas.create_line(store['x'], store['y'], store['x2'], store['y2'], fill="white", arrow=tk.LAST)
    mid_x = (store['x'] + store['x2']) / 2
    mid_y = (store['y'] + store['y2']) / 2
    # Add text above the line
    Informed_canvas.create_text(mid_x, mid_y - 10, text=f"Path Cost={path_cost}", fill="white")


def find_node(x, y):
    for node in g.nodes():
        if node.x-10 <= x <= node.x + 45 and node.y -10<= y <= node.y + 45:
            return node
    return None
ctNode = 0
def create_node(x, y):
    global ctNode
    oval_id = Informed_canvas.create_oval(x, y, x + 45, y + 45, fill="brown", outline="white", width=2)
    center_x = (x + x + 45) / 2
    center_y = (y + y + 45) / 2
    node_instance = Node(x, y, "red",f"N{ctNode}", oval_id)
    Informed_canvas.create_text(center_x, center_y, text=node_instance.text , fill="white", tags=f"text_{node_instance.id}")
    ctNode += 1
    Informed_canvas.create_text(center_x, y - 10, text=f'H={node_instance.h}', fill="white", tags=[f"text_{node_instance.id}", f"h_text_{node_instance.id}"])
    g.add_node(node_instance)
    node_instance.display_attributes()

def find_node_by_text(node_text):
        for node in g.nodes():
            if node.text == node_text:
                return node
        return None
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
def edit_node(x, y):
    global g
    for node in g.nodes():
        if node.x - 10 <= x <= node.x + 45 and node.y - 10 <= y <= node.y + 45:
            h = simpledialog.askfloat("H", "Enter the H")
            if h==-1:
                return
            while h is None :
                h = simpledialog.askfloat("H", "Enter the H")

            node.h = h
            # Update the node in the graph
            g.nodes[node]['h'] = h

            # Redraw the oval with updated attributes
            redraw_oval(node)

            Informed_canvas.update()
            print(f"Node edited: {node.text}, new H={node.h}")
            return
    return None

def redraw_oval(node):
    # Remove existing oval and text
    Informed_canvas.delete(node.id)
    Informed_canvas.delete(f"h_text_{node.id}")

    # Redraw oval with updated attributes
    oval_id = Informed_canvas.create_oval(node.x, node.y, node.x + 45, node.y + 45, fill="brown", outline="white", width=2)
    node.id = oval_id

    # Recreate text with updated value
    center_x = (node.x + node.x + 45) / 2
    center_y = (node.y + node.y + 45) / 2
    Informed_canvas.create_text(center_x, center_y, text=node.text, fill="white", tags=f"text_{node.id}")
    Informed_canvas.create_text(center_x, node.y - 10, text=f'H={node.h}', fill="white", tags=[f"text_{node.id}", f"h_text_{node.id}"])


 

def activate_delete_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, True, True
    print(f"delete node has been activated: is_delete_node={deleteNode}")

def RRRemove(x,y):
    Node=find_node(x,y)
    if Node:
        # Get the edges connected to the node
        edges = list(g.edges(Node))
        # Remove the lines representing the edges from the canvas
        for edge in edges:
            Informed_canvas.delete(f"line_{edge[0].id}_{edge[1].id}")
            Informed_canvas.delete(f"line_{edge[1].id}_{edge[0].id}")
        # Remove the node from the graph
        g.remove_node(Node)
        # Remove the node from the canvas
        Informed_canvas.delete(Node.id)
        Informed_canvas.delete(f"text_{Node.id}")
        Informed_canvas.delete(f"h_text_{Node.id}")
        print(f"Node {Node.text} has been deleted.")
        Informed_canvas.update()
def Reset():
    global ctNode
    g.clear()
    Informed_canvas.delete("all")
    ctNode = 0
    print(f" ctNode->{ctNode}")
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, False, False
    print(is_adding_node, is_editing_node, deleteNode, move_node_button)
    print("All have been reset")

def create_buttons():
    add_node_button = ttk.Button(Informed_window, text="ADD NODE", command=activate_adding_node)
    add_node_button.place(x=100, y=470)
    edit_node_button = ttk.Button(Informed_window, text="EDIT NODE", command= activate_editing_node)
    edit_node_button.place(x=200, y=470)
    move_node_button = ttk.Button(Informed_window, text="MOVE NODE", command=activate_move_node)
    move_node_button.place(x=300, y=470)
    delete_node_button = ttk.Button(Informed_window, text="DELETE NODE", command=activate_delete_node)
    delete_node_button.place(x=400, y=470)
    RunGREEDY_button = ttk.Button(Informed_window, text="RUN GREEDY", command=run_greedy)
    RunGREEDY_button.place(x=500, y=470)
    RunA_STAR_button = ttk.Button(Informed_window, text="RUN A_STAR", command=run_astar)
    RunA_STAR_button.place(x=600, y=470)
    reset_button = ttk.Button(Informed_window, text="RESET", command=Reset)
    reset_button.place(x=800, y=470)
    back_button = ttk.Button(Informed_window, text="BACK", command=Informed_window.destroy)
    back_button.place(x=900, y=470)
def activate_delete_node():
    global is_adding_node, is_editing_node, deleteNode, move_node_button
    is_adding_node, is_editing_node, deleteNode, move_node_button = False, False, True, False
    print(f"delete node has been activated: is_delete_node={deleteNode}")
def print_graph():
    print("Nodes:")
    for node in g.nodes():
        print(node.display_attributes())
    print("\nEdges:")
    for edge in g.edges():
        node1, node2 = edge
        print(f"{node1.text} -- {node2.text}")
def AStarSearch(start_node_name):
    
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

    queue.append((start_node.h, start_node, [start_node.text], 0))  # Add start_node with heuristic, path, and cost to the queue

    while queue:
        queue.sort(key=lambda x: x[0] + x[3])  # Sort the queue based on the sum of heuristic and cost
        _, current_node, path, cost = queue.pop(0)
        Visited.append(current_node.text)  # Add the visited node to the Visited array
        Fringe.append([node.text for _, node, _, _ in queue])  # Add the nodes in the fringe to the Fringe array
        visited.add(current_node)
        current_node.Color("gray")  # Change color of the current node to yellow (visited)
        Informed_canvas.update()  # Update the canvas to visualize the change
        time.sleep(0.5)
        FPath.append(current_node)  # Add the path to the final path

        visited.add(current_node)
        if current_node.h == 0:
            print(f"Goal Node found: {current_node.text}")
            print(f"Final Correct Path from Start to Goal: {' -> '.join(path)}")
            print(f"Visited Nodes: {Visited}")
            print(f"Fringe Nodes: {Fringe}")
            print(f"Final Path: {FPath}")
            for node in path:
                find_node_by_text(node).Color("green")  # Change color only for nodes in the final path
                Informed_canvas.update()
                time.sleep(0.5)
            return  # Terminates A* Search if goal node with heuristic value 0 is found

        neighbors = sorted(list(g.neighbors(current_node)), key=lambda x: x.text)  # Sort neighbors alphabetically
        for neighbor in neighbors:
            if neighbor not in visited:
                edge_weight = g[current_node][neighbor]["weight"]
                queue.append((neighbor.h, neighbor, path + [neighbor.text], cost + edge_weight))
                neighbor.Color("orange")  # Change color of the neighbor to orange (fringe)
                Informed_canvas.update()  # Update the canvas to visualize the change
                time.sleep(1.5)  # Add neighbor to queue along with updated heuristic, path, and cost
def run_astar():
    # Start A* search from node named 'n0' or alphabetically if 'n0' doesn't exist
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
    AStarSearch(start_node_name)
def Greedy(start_node_name):
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
    for node in g.nodes():
        node.Color("red")
    ctH=0
    for node in g.nodes():
        if node.h==0:
            ctH+=1
    if ctH==0:
        messagebox.showinfo("Error","There is no goal")
        return    


    if start_node is None:
        print(f"Node '{start_node_name}' not found in the graph. Starting traversal alphabetically.")
        start_node = sorted(list(g.nodes()), key=lambda x: x.text)[0]  # Start with the first node alphabetically

    queue.append((start_node.h, start_node, [start_node.text]))  # Add start_node with heuristic and path to the queue

    while queue:
        queue.sort(key=lambda x: x[0])  # Sort the queue based on heuristic
        _, current_node, path = queue.pop(0)
        Visited.append(current_node.text)  # Add the visited node to the Visited array
        Fringe.append([node.text for _, node, _ in queue])  # Add the nodes in the fringe to the Fringe array
        visited.add(current_node)
        current_node.Color("gray")  # Change color of the current node to yellow (visited)
        Informed_canvas.update()  # Update the canvas to visualize the change
        time.sleep(0.5)
        FPath.append(current_node)  # Add the path to the final path

        visited.add(current_node)
        if current_node.h == 0:
            print(f"Goal Node found: {current_node.text}")
            print(f"Final Correct Path from Start to Goal: {' -> '.join(path)}")
            print(f"Visited Nodes: {Visited}")
            print(f"Fringe Nodes: {Fringe}")
            print(f"Final Path: {FPath}")
            for node in path:
                find_node_by_text(node).Color("green")  # Change color only for nodes in the final path
                Informed_canvas.update()
                time.sleep(0.5)
            return  # Terminates Greedy Search if goal node with heuristic value 0 is found

        neighbors = sorted(list(g.neighbors(current_node)), key=lambda x: x.text)  # Sort neighbors alphabetically
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor.h, neighbor, path + [neighbor.text]))
                neighbor.Color("orange")  # Change color of the neighbor to orange (fringe)
                Informed_canvas.update()  # Update the canvas to visualize the change
                time.sleep(1.5)  # Add neighbor to queue along with updated heuristic and path

    print("No goal found after exploring all possible routes.")
def find_node_by_text(node_text):
    for node in g.nodes():
        if node.text == node_text:
            return node
    return None


def run_greedy():
    # Start Greedy search from node named 'n0' or alphabetically if 'n0' doesn't exist
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
    Greedy(start_node_name)

def CreatInformed():
    global Informed_window,Informed_canvas
    Informed_window = tk.Tk()
    Informed_window.title("Graph Editor")
    Informed_window.geometry("1000x500")
    Informed_canvas = tk.Canvas(Informed_window, width=1000, height=450, bg="black")
    Informed_canvas.pack(padx=20)
    Informed_canvas.bind("<Button-1>", left_click)
    Informed_canvas.bind("<Button-3>", on_right_click)
    Informed_canvas.bind("<B3-Motion>", on_drag)
    Informed_canvas.bind("<ButtonRelease-3>", on_release)
    create_buttons()
g = nx.DiGraph()
