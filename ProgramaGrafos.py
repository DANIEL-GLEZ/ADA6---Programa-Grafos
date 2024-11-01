import networkx as nx
import matplotlib.pyplot as plt

estados = {
    "Aguascalientes": [("Zacatecas", 120), ("Jalisco", 150)],
    "Zacatecas": [("Aguascalientes", 120), ("San Luis Potosi", 200), ("Durango", 220)],
    "Jalisco": [("Aguascalientes", 150), ("Michoacan", 180), ("Colima", 130)],
    "San Luis Potosi": [("Zacatecas", 200), ("Nuevo Leon", 300)],
    "Durango": [("Zacatecas", 220), ("Chihuahua", 400)],
    "Michoacan": [("Jalisco", 180)],
    "Nuevo Leon": [("San Luis Potosi", 300), ("Chihuahua", 250)],
    "Chihuahua": [("Durango", 400), ("Nuevo Leon", 250)],
}

G = nx.Graph()
for estado, conexiones in estados.items():
    for destino, costo in conexiones:
        G.add_edge(estado, destino, weight=costo)

def calcular_costo(ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        try:
            costo_total += G[ruta[i]][ruta[i + 1]]['weight']
        except KeyError:
            print(f"Error: No hay conexión directa entre {ruta[i]} y {ruta[i + 1]}")
            return None
    return costo_total

def recorrer_sin_repetir(estado_inicial):
    ruta = list(nx.dfs_preorder_nodes(G, estado_inicial))
    return ruta, calcular_costo(ruta)

def recorrer_con_repeticion(estado_inicial):
    ruta = list(nx.dfs_preorder_nodes(G, estado_inicial))
    ruta.append(ruta[0]) 
    return ruta, calcular_costo(ruta)

estado_inicial = "Aguascalientes"
ruta_sin_repetir, costo_sin_repetir = recorrer_sin_repetir(estado_inicial)
ruta_con_repeticion, costo_con_repeticion = recorrer_con_repeticion(estado_inicial)

if costo_sin_repetir is not None:
    print("Recorrido sin repetir estados:", ruta_sin_repetir)
    print("Costo total (sin repetir):", costo_sin_repetir)
else:
    print("No se pudo calcular el costo sin repetir debido a una conexión faltante.")

if costo_con_repeticion is not None:
    print("\nRecorrido con repetición de un estado:", ruta_con_repeticion)
    print("Costo total (con repetición):", costo_con_repeticion)
else:
    print("No se pudo calcular el costo con repetición debido a una conexión faltante.")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.title("Mapa de conexiones y costos de los estados")
plt.show()
