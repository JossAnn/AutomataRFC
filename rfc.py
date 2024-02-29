import re
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define la regular expression para las primeras cuatro letras de RFC
rfc_first_four_pattern = re.compile(r'^[NnAaOo]{1,4}')

# Variable global para almacenar el canvas actual
current_canvas = None

# Función que crea y muestra el autómata


def show_automaton(rfc_start):
    global current_canvas

    # Crea un grafo dirigido para el autómata
    Graff = nx.DiGraph()

    # Añade los nodos y aristas al grafo
    for i, letter in enumerate(rfc_start):
        Graff.add_edge(f'q{i}', f'q{i+1}', label=letter)

    # Crea la figura de Matplotlib
    fig, ax = plt.subplots()

    # Dibuja el autómata
    pos = nx.spring_layout(Graff)  
    # Posiciona los nodos
    nx.draw(Graff, pos, ax=ax, with_labels=True, node_size=3000,
            node_color="lightblue", linewidths=2, font_size=18)

    # Destaca el estado inicial y final
    nx.draw_networkx_nodes(Graff, pos, nodelist=['q0'], node_color="blue")
    nx.draw_networkx_nodes(
        Graff, pos, nodelist=[f'q{len(rfc_start)}'], node_color="red")

    # Dibuja las etiquetas de las aristas
    edge_labels = {(u, v): d['label'] for u, v, d in Graff.edges(data=True)}
    nx.draw_networkx_edge_labels(
        Graff, pos, edge_labels=edge_labels, font_color='red')

    # Elimina el canvas anterior si existe
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Muestra el autómata en la ventana de Tkinter
    current_canvas = FigureCanvasTkAgg(fig, master=window)
    current_canvas.draw()
    current_canvas.get_tk_widget().pack()

# Función que se llama cuando el usuario presiona el botón para ingresar su RFC


def on_submit():
    # Solicita al usuario que ingrese el RFC mediante un diálogo
    rfc_input = simpledialog.askstring(
        "Input", "Ingresa tu RFC:", parent=window)

    # Valida y extrae las primeras cuatro letras del RFC ingresado
    if rfc_input:  # Asegúrate de que el usuario no haya cancelado el diálogo
        match = rfc_first_four_pattern.match(rfc_input)
        if match:
            rfc_start = match.group(0).upper()
            show_automaton(rfc_start)
        else:
            messagebox.showerror(
                "Error", "RFC Invalido. Por favor ingresa como minimo los primeros 4 digitos.")
    else:
        messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")


# Crea la ventana principal de Tkinter
window = tk.Tk()
window.title("Generador de Autómata RFC")

# Añade un botón para ingresar el RFC
submit_button = tk.Button(window, text="Ingresar RFC", command=on_submit)
submit_button.pack()

# Inicia el bucle de eventos de Tkinter
window.mainloop()
