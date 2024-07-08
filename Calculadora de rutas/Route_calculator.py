import heapq  #proporciona implementaciones eficientes de estructuras de datos de colas de prioridad
                #son útiles en algoritmos como A* para manejar la lista de nodos abiertos de manera eficiente

# Colores para la visualización en la consola
class Colores: #investigar porque clase o variables
    CEL = '\033[94m'  # Celeste
    ROJ = '\033[91m'  # Rojo
    VER = '\033[92m'  # Verde
    FIN = '\033[0m'   # Fin del color
#Codigo ANSI: secuencias de escape que permiten controlar aspectos de la salida de texto
# en terminales y consolas, como el color del texto.

# Función para generar el mapa
def generar_mapa(filas, columnas):
    return [['0' for _ in range(columnas)] for _ in range(filas)] #investigar como hacer o porque una lista de listas
#representado con una lista de listas donde cada celda inicialmente contiene el carácter '0'.

# Función para agregar obstáculos al mapa
def agregar_obstaculo(mapa, x, y, tipo_obstaculo):
    if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]): # calcula cuantas filas - calcula cuantas columnas 
        mapa[x][y] = tipo_obstaculo
    else:
        print("Coordenadas inválidas")
#Longitud

# Función para ingresar coordenadas
def ingresar_coordenadas(mensaje, filas, columnas, mapa): #parametros
    while True:
        try:
            x, y = map(int, input(mensaje).split()) #se utiliza para dividir la entrada del usuario en coordenadas x e y
            if 0 <= x < filas and 0 <= y < columnas and mapa[x][y] == '0':
                return x, y
            else:
                print("Coordenadas fuera del rango del mapa o en un obstáculo. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar dos números enteros separados por un espacio.")

# Función heurística para A*
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) #Valor absoluto, para que arroje valores positivos
#estima la distancia desde el punto a hasta el punto b
#se utiliza la distancia de Manhattan, que es la suma de las diferencias absolutas de las coordenadas x y y.
#Mide la distancia de los puntos para determinar cual es el mejor 

# Algoritmo A*
def a_star(mapa, inicio, fin):
    filas, columnas = len(mapa), len(mapa[0]) # como se llama esta expresión y que representa el len mapa 0
    abiertos = [(0, inicio)]
    heapq.heapify(abiertos) #Es una función de heapq que reorganiza los elementos de la lista
                            #para cumplir con las propiedades de un heap
    costos = {inicio: 0}
    padres = {inicio: None}
    
    while abiertos: # Mientras haya nodos en la lista de abiertos (nodos por explorar)
        _, actual = heapq.heappop(abiertos) #Extraer el nodo con la prioridad más baja de la cola de prioridad
        #la informacion no relevante pasa de largo, 
        #porque heapq es una cola de prioridades
        
        if actual == fin: # Si el nodo actual es igual al nodo de destino
            ruta = [] # Crear una lista vacía para almacenar la ruta
            while actual: # Mientras el nodo actual no sea None
                ruta.append(actual) # Agregar el nodo actual a la ruta
                actual = padres[actual] # Actualizar el nodo actual al nodo padre del nodo actual
            ruta.reverse() # Revertir la ruta para obtener el camino desde el inicio hasta el fin
            return ruta # Devolver la ruta encontrada
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Para cada desplazamiento (dx, dy) en las cuatro direcciones
            vecino = (actual[0] + dx, actual[1] + dy) # Calcular las coordenadas del nodo vecino
            
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas and mapa[vecino[0]][vecino[1]] == '0':
                        # Si el vecino está dentro de los límites del mapa y no es un obstáculo

                nuevo_costo = costos[actual] + 1 # Calcular el nuevo costo para llegar al vecino
                if vecino not in costos or nuevo_costo < costos[vecino]: 
                # Si el vecino no tiene un costo registrado o el nuevo costo es menor que el costo registrado
                    costos[vecino] = nuevo_costo # Actualizar el costo para llegar al vecino
                    prioridad = nuevo_costo + heuristica(fin, vecino) # Calcular la prioridad del vecino
                    heapq.heappush(abiertos, (prioridad, vecino)) 
                    #Metodo que hace que la informacion quede como maxima prioridad
                    # bucando siempre el camino más optimo
                    padres[vecino] = actual
    
    return None  # No hay ruta

# Función para visualizar el mapa y la ruta
def visualizar_mapa(mapa, ruta=None, inicio=None, fin=None):
    for x, fila in enumerate(mapa): # Iterar sobre cada fila en el mapa, con `x` como índice de la fila y `fila` como el contenido de la fila
        for y, celda in enumerate(fila): # Iterar sobre cada celda en la fila, con `y` como índice y `celda` como valor de la celda
            if (x, y) == inicio: # Si las coordenadas actuales son las del punto de inicio
                print(Colores.VER + 'I' + Colores.FIN, end=' ') # Imprimir 'I' en color verde
            elif (x, y) == fin: # Si las coordenadas actuales son las del punto final
                print(Colores.ROJ + 'F' + Colores.FIN, end=' ')# Imprimir 'F' en color rojo
            elif ruta and (x, y) in ruta: # Si hay una ruta y la celda actual está en la ruta
                print('.', end=' ') # Imprimir un punto (.) para representar la ruta
            else: # Si ninguna de las condiciones anteriores se cumple
                print(celda, end=' ') # Imprimir el contenido original de la celda
        print() # Imprimir una nueva línea después de cada fila

# Crear el mapa
filas, columnas = 10, 10
mapa = generar_mapa(filas, columnas)

# Función para permitir al usuario agregar obstáculos
def agregar_obstaculos_usuario(mapa, filas, columnas):
    tipos_obstaculos = {
        '1': ('█', "Edificio (█)"),
        '2': (Colores.CEL + '|' + Colores.FIN, "Agua (" + Colores.CEL + "|" + Colores.FIN + ")"),
        '3': ('#', "Construcción (#)")
    }
    
    while True: # Bucle infinito
        print("\nSeleccione el tipo de obstáculo:") # Imprimir mensaje para seleccionar tipo de obstáculo
        for key, value in tipos_obstaculos.items(): # Iterar sobre los ítems del diccionario `tipos_obstaculos`
            print(f"{key}: {value[1]}") #Imprimir la clave y la descripción del tipo de obstáculo
        print("0: Terminar de agregar obstáculos") #Opción para terminar de agregar obstáculos
        
        tipo = input("Seleccione el tipo de obstáculo (0-3): ")
        # Leer la entrada del usuario para seleccionar el tipo de obstáculo
        if tipo == '0': # Si el usuario selecciona '0'
            break  #Romper el bucle y terminar de agregar obstáculos
        elif tipo in tipos_obstaculos: # Si el tipo seleccionado está en `tipos_obstaculos`
            while True: # Bucle infinito para ingresar coordenadas hasta que se ingresen correctamente
                try: # Intentar ejecutar el bloque de código que sigue
                    x, y = map(int, input("Ingrese las coordenadas del obstáculo (x y): ").split())
                    # Leer y convertir las coordenadas ingresadas a enteros
                    if 0 <= x < filas and 0 <= y < columnas and mapa[x][y] == '0':
                        # Verificar si las coordenadas están dentro del rango y si la celda está vacía
                        agregar_obstaculo(mapa, x, y, tipos_obstaculos[tipo][0])
                        # Agregar el obstáculo al mapa en las coordenadas dadas
                        break # Romper el bucle de coordenadas
                    else:
                        print("Coordenadas fuera del rango del mapa o en un obstáculo. Inténtalo de nuevo.")
                except ValueError:
                    print("Entrada inválida. Asegúrate de ingresar dos números enteros separados por un espacio.")
        else:
            print("Selección inválida. Inténtalo de nuevo.")

# Agregar obstáculos
agregar_obstaculos_usuario(mapa, filas, columnas)

# Visualizar el mapa después de agregar los obstáculos
print("Mapa con obstáculos:")
visualizar_mapa(mapa)

# Ingresar puntos de inicio y fin
inicio = ingresar_coordenadas("Ingrese las coordenadas del punto de inicio (x y): ", filas, columnas, mapa)
fin = ingresar_coordenadas("Ingrese las coordenadas del punto de fin (x y): ", filas, columnas, mapa)

# Encontrar la ruta
ruta = a_star(mapa, inicio, fin)

# Visualizar el mapa y la ruta
print("Mapa con la ruta:")
visualizar_mapa(mapa, ruta, inicio, fin)