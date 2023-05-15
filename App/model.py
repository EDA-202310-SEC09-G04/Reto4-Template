"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
import datetime
import math
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = { "mapa_lobos": None, 
                 "grafo_general": None, 
                 "mapa_seguimiento" :None, 
                 "nodos_encuentro": None,
                 "nodo_seguimiento":None,
                "eventos": None
             }

    data_structs["mapa_lobos"] = mp.newMap()
    data_structs["mapa_seguimiento"] = mp.newMap()
    data_structs["grafo_general"] = gr.newGraph(cmpfunction=cmp1)
    data_structs["nodos_encuentro"] = lt.newList()
    data_structs["hash_puntos"] = mp.newMap()
    data_structs["nodo_seguimiento"] = lt.newList()
    data_structs["eventos"] = lt.newList()
    return data_structs
# Funciones para agregar informacion al modelo

def add_data_wolves(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    
    mapa_lobos = data_structs["mapa_lobos"] # mapa con id e información de lobos
    mp.put(mapa_lobos,data["animal-id"] ,data )

def add_hash_puntos(data_structs, data):
    identificador =  str(round(float(data["location-long"]), 4)).replace(".", "p").replace("-", "m") + "_" +str(round(float( data["location-lat"]),4)).replace(".", "p").replace("-", "m") # filtrar datos lat y long
    id_lobo =  identificador + "_" + str(data["individual-local-identifier"]) # filtrar datos lat y long
    
    contain_gather = mp.contains(data_structs["hash_puntos"],identificador)
    if contain_gather:
        lista = me.getValue(mp.get(data_structs["hash_puntos"], identificador))
        centinela = False
        for i in lt.iterator(lista):
            if i == data["individual-local-identifier"]:
                centinela = True
        if not centinela:
            lt.addLast(lista, data["individual-local-identifier"])
    elif not contain_gather:
        lista = lt.newList()
        lt.addLast(lista, data["individual-local-identifier"])

    contasin_wolf =  mp.contains(data_structs["hash_puntos"], id_lobo)
    if contasin_wolf:
        lista2 = me.getValue(mp.get(data_structs["hash_puntos"], id_lobo))  
        centinela = False
        for i in lt.iterator(lista2):
            # print("bla lista 2!!!!!!!!")
            if i == data["individual-local-identifier"]:
                centinela = True
        if not centinela:
            lt.addLast(lista2, data["individual-local-identifier"])
    elif not contasin_wolf:
        lista2 = lt.newList()
        lt.addLast(lista2, data["individual-local-identifier"])
    # print("wolf node", id_lobo)
    # print("gather node", identificador)
    mp.put(data_structs["hash_puntos"], identificador, lista)
    mp.put(data_structs["hash_puntos"], id_lobo, lista2)
    return data_structs
            
        
def add_data_tracks(data_structs, data): 
    
    lt.addLast(data_structs["eventos"], data)
    
    
    mapa_tracks = data_structs["mapa_seguimiento"] # cramos mapa de seguimiento con los id de los lobos 
    time_stamp = int(datetime.datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M").timestamp()) # tiempo en el que pasó 
    if mp.contains(mapa_tracks,data["individual-local-identifier"]): # si ya tenemos el id
        omap = me.getValue( mp.get(mapa_tracks,data["individual-local-identifier"] )) # extraemos el order map 
        om.put(omap,time_stamp ,data ) # añadimos al order map el la información del id ya ordenada 
    else: 
        omap = om.newMap() # creamos el order map
        om.put(omap,time_stamp ,data ) # añadimos al order map el la información del id ya ordenada 
        mp.put (mapa_tracks, data["individual-local-identifier"], omap ) # añadimos al mapa grande toda la información
    
    v_encuentro = str(round(float(data["location-long"]), 4)).replace(".", "p").replace("-", "m") + "_" +str(round(float( data["location-lat"]),4)).replace(".", "p").replace("-", "m") # filtrar datos lat y long
    v_seguimiento = v_encuentro + "_" + str(data["individual-local-identifier"]) # juntamos todo con el id del animal (cramos representacion nodo)
    # print("id_wolf:", v_seguimiento)
    lista = me.getValue(mp.get(data_structs["hash_puntos"], v_encuentro))
    lista2 = me.getValue(mp.get(data_structs["hash_puntos"], v_seguimiento))
    # print(lista2)
    if lt.size(lista) > 1:
        if not gr.containsVertex(data_structs["grafo_general"], v_encuentro):  # preguntamos si v_encuentro no existe en el grafo porque se puede repetir
            gr.insertVertex(data_structs["grafo_general"],v_encuentro ) # añadimos al grafo 
            lt.addLast(data_structs["nodos_encuentro"], v_encuentro ) # añadir nodos en el orden que aparecen
    if lt.size(lista2) > 0:
        if not gr.containsVertex(data_structs["grafo_general"], v_seguimiento):  # preguntamos si v_encuentro no existe porque puede retornar un lugar
            gr.insertVertex(data_structs["grafo_general"],v_seguimiento ) # añadimos al grafo 
            lt.addLast(data_structs["nodo_seguimiento"], v_seguimiento ) 

        # if gr.getEdge(data_structs["grafo_general"],v_encuentro,v_seguimiento ) == None: 
        #       gr.addEdge(data_structs["grafo_general"],v_encuentro, v_seguimiento)

    return data_structs


def conexiones_tracks (data_structs):  # se van a conectar los tracks por lobo
    mapa_tracks = data_structs["mapa_seguimiento"]
    lobos = lt.iterator(mp.keySet(mapa_tracks)) # se saca la información por lobo
    for lobo_id in lobos: 
        omap = me.getValue( mp.get(mapa_tracks,lobo_id)) # extraemos el order map  
        fechas = om.values(omap, om.minKey(omap), om.maxKey(omap)) # extraemos los valores de todas las fechas organizados retorna lista
        for posicion in range(1,lt.size(fechas)): #recorrer todas las fechas de la lista 
        
            seguimiento1= lt.getElement(fechas,posicion ) # datos del seguimiento de un lobo
            v_encuentro1 = str(round(float(seguimiento1["location-long"]),4)).replace(".", "p").replace("-", "m") + "_" + str(round(float(seguimiento1["location-lat"]),4)).replace(".", "p").replace("-", "m") # filtrar datos lat y long
            v_seguimiento1 = v_encuentro1 + "_" + seguimiento1["individual-local-identifier"] # juntamos todo con el id del animal (cramos representacion nodo)
   
            seguimiento2= lt.getElement(fechas,posicion +1 ) # datos del seguimiento del lobo en un punto diferente
            v_encuentro2 = str(round(float(seguimiento2["location-long"]),4)).replace(".", "p").replace("-", "m") + "_" + str(round(float(seguimiento2["location-lat"]),4)).replace(".", "p").replace("-", "m") # filtrar datos lat y long
            v_seguimiento2 = v_encuentro2+ "_" + seguimiento2["individual-local-identifier"] # juntamos todo con el id del animal (cramos representacion nodo)
            #calculo entre dos puntos 
            # primero extraemos long y lat de los puntos
            long1 = float(seguimiento1["location-long"])
            long2 = float(seguimiento2["location-long"])
            lat1 = float(seguimiento1["location-lat"])
            lat2 = float(seguimiento2["location-lat"])
            # aplicar formula
            paso1_formula = (math.sin(((lat1-lat2)/2)))**2
            paso2_formula = math.cos(lat2)*math.cos(lat1) 
            paso3_formula = paso2_formula * (math.sin(((long1-long2)/2)))**2
            paso4_formula = paso1_formula + paso3_formula
            paso5_formula = math.sqrt(float(paso4_formula))
            distancia = 2 * math.asin(paso5_formula)*6371
            
            # v_seguimiento1 = v_seguimiento1 + "_" + str(lobo_id)
            # v_seguimiento2 = v_seguimiento2 + "_" + str(lobo_id)
            #print(v_encuentro1, v_encuentro2)
            #print(v_seguimiento1, v_seguimiento2)
            # print(gr.numVertices(data_structs["grafo_general"]))
            # print(gr.vertices(data_structs["grafo_general"]))            
            #print(gr.containsVertex(data_structs["grafo_general"], "m111p4828_56p7188_32263B"))
            #print(gr.containsVertex(data_structs["grafo_general"], v_encuentro1))
            #print(gr.containsVertex(data_structs["grafo_general"], v_encuentro2))
            #print(gr.containsVertex(data_structs["grafo_general"], v_seguimiento1))
            #print(gr.containsVertex(data_structs["grafo_general"], v_seguimiento2))
            # print(gr.numVertices(data_structs["grafo_general"]))
            
            gr.addEdge(data_structs["grafo_general"],v_seguimiento1, v_seguimiento2, round(distancia, 4)) #unir los puntos de seguimiento por lobo          
            if gr.containsVertex(data_structs["grafo_general"], v_encuentro1):
                centinela = False
                for i in lt.iterator(gr.adjacents(data_structs["grafo_general"], v_encuentro1)):
                    if i == v_seguimiento1:
                        centinela = True
                if centinela == False:
                     gr.addEdge(data_structs["grafo_general"],v_seguimiento1, v_encuentro1, 0)
            if (posicion== lt.size(fechas)-1):
                if gr.containsVertex(data_structs["grafo_general"], v_encuentro2):
                    centinela = False
                    for i in lt.iterator(gr.adjacents(data_structs["grafo_general"], v_encuentro2)):
                        if i == v_seguimiento2:
                            centinela = True   
                    if centinela == False:                                        
                        gr.addEdge(data_structs["grafo_general"],v_seguimiento2, v_encuentro2, 0)
                
                
           
    return data_structs  
            

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass


def total_lobos_registrados(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista

    return mp.size(data_structs["mapa_lobos"])

def  total_puntos_encuentro(data_structs):
    return lt.size(data_structs["nodos_encuentro"])

def total_de_lobos_presentes (data_structs):
    return 
    

def primeros_ultimos(data_structs): 
    
    mayores =  lt.subList(data_structs["nodos_encuentro"], 1, 5) 
    menores = lt.subList(data_structs["nodos_encuentro"],(lt.size(data_structs["nodos_encuentro"])-4) , 5)
    
    suma = 0 # tercero
    for i in lt.iterator(mp.keySet(data_structs["hash_puntos"])):
        tamanio = lt.size(me.getValue(mp.get(data_structs["hash_puntos"] ,i )))
        if tamanio>1:
            suma+=tamanio
    print(suma)

    tabla_mayores = {}
    tabla_mayores["Identificador_punto_encuentro "] = []
    tabla_mayores["Lat"] = []
    tabla_mayores["long"] = []
    tabla_mayores["numero_encuentros"] = []
    for nodo_mayores in lt.iterator(mayores):
        tabla_mayores["Identificador_punto_encuentro "].append( nodo_mayores)
        lat = float(str(nodo_mayores).split("_")[1].replace("p", ".").replace("m","-"))
        latitud = lat 
        lon = float(str(nodo_mayores).split("_")[0].replace("p", ".").replace("m","-"))
        longitud = lon
        tabla_mayores["Lat"].append(latitud)
        print()
        tabla_mayores["numero_encuentros"].append( lt.size(gr.adjacents(data_structs["grafo_general"],nodo_mayores ))) # nodos adyacentes del nodo
        tabla_mayores["long"].append(longitud)
        
        

    tabla_menores = {}
    tabla_menores["Identificador_punto_encuentro "] = []
    tabla_menores["Lat"] = []
    tabla_menores["long"] = []
    tabla_menores["numero_encuentros"] = []
    for nodo_menores in lt.iterator(menores):
        tabla_menores["Identificador_punto_encuentro "].append(nodo_menores)
        lat = float(str(nodo_menores).split("_")[1].replace("p", ".").replace("m","-"))
        latitud = lat 
        lon = float(str(nodo_menores).split("_")[0].replace("p", ".").replace("m","-"))
        longitud = lon
        tabla_menores["Lat"].append(latitud)
        tabla_menores["numero_encuentros"].append(lt.size(gr.adjacents(data_structs["grafo_general"],nodo_menores ))) # nodos adyacentes del nodo
        tabla_menores["long"].append(longitud)
        
    return tabla_mayores, tabla_menores, data_structs

def cmp1 (node1_id, node2):
    # print(node1_id)
    # print(node2)
    # print(node2["key"])
    if node1_id < node2["key"]:
        return -1
    elif node1_id == node2["key"]:
        return 0
    else:
        return 1