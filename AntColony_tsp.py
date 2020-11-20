from copy import deepcopy
import cv2
import numpy as np

_CITIES = [
    ("Bordeaux", (44.833333, -0.566667)),
    ("Paris", (48.8566969, 2.3514616)),
    ("Nice", (43.7009358, 7.2683912)),
    ("Lyon", (45.7578137, 4.8320114)),
    ("Nantes", (47.2186371, -1.5541362)),
    ("Brest", (48.4, -4.483333)),
    ("Lille", (50.633333, 3.066667)),
    ("Clermont-Ferrand", (45.783333, 3.083333)),
    ("Strasbourg", (48.583333, 7.75)),
    ("Poitiers", (46.583333, 0.333333)),
    ("Angers", (47.466667, -0.55)),
    ("Montpellier", (43.6, 3.883333)),
    ("Caen", (49.183333, -0.35)),
    ("Rennes", (48.083333, -1.683333)),
    ("Pau", (43.3, -0.366667)),
]

import numpy as np
def distance(a, b):
    (x1, y1), (x2, y2) = (a, b)
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class ant:
    def __init__(self, initial_city, alpha, beta, rho, const):
        self.location = initial_city
        self.start = initial_city
        # liste des villes que la fourmi peut visiter, ce sont toutes les villes au tout début
        self.possible_cities = deepcopy(_CITIES)
        self.distance_traveled = 0
        self.alpha = alpha
        self.beta = beta
        self.rho = rho # coef d'évaporation
        self.const = const  # constante Q de dépôt de phéromones
        self.visited_cities = []  # dans l'ordre de visite
        self.tour_complete = False  # true quand le tour est terminé

    def run(self):
        while self.possible_cities:
            next_city = self.find_next_city(self.location)
            self.traverse(self.location, next_city)
        self.tour_complete = True
        self.update_distance_traveled(self.start, self.location)
        self.get_distance_traveled()
        self.add_pheromones()

    def find_next_city(self, actual_city):
        # on suppose que la ville suivante est la première de la liste
        next_city = self.possible_cities[0]
        visibility0 = float(1/distance(actual_city[1], next_city[1]))  # inverse de la distance
        attractiveness0 = ((visibility0**self.alpha) * (pheromone_map[_CITIES.index(actual_city)][_CITIES.index(next_city)]**self.beta))

        # on parcourt la liste et vérifie si il y a une ville qui a une plus grande 'attractiveness' 
        for i in range(len(self.possible_cities)):
            visibility = float(1/distance(actual_city[1], self.possible_cities[i][1]))
            attractiveness = ((visibility**self.alpha) * (pheromone_map[_CITIES.index(actual_city)][_CITIES.index(self.possible_cities[i])]**self.beta))
            if (attractiveness > attractiveness0):
                next_city = self.possible_cities[i]
        return next_city

    def traverse(self, start, end):
        self.update_visited_cities(end)
        self.update_distance_traveled(start, end)
        self.location = end

    def update_visited_cities(self, new_city):
        if new_city not in self.visited_cities :
            self.visited_cities.append(new_city)
        if new_city in self.possible_cities:
            self.possible_cities.remove(new_city)

    def update_distance_traveled(self, start, end):
        if self.tour_complete == True : 
            self.distance_traveled += float(distance(self.start[1], end[1]))
        else :
            self.distance_traveled += float(distance(start[1], end[1]))

    def get_visited_cities(self):
        if self.tour_complete:
            self.visited_cities.append(self.start)
            return self.visited_cities
        return None

    def get_distance_traveled(self):
            return self.distance_traveled

    def add_pheromones(self):
        for i in range (0,len(self.visited_cities)-1) :
            # on récupère l'indice de deux villes successives 
            index_city1 = _CITIES.index(self.visited_cities[i])
            index_city2 = _CITIES.index(self.visited_cities[i+1])
        
            # on prend on compte l'évaporation aussi 
            pheromone_map[index_city1][index_city2] = (1-self.rho)*pheromone_map[index_city1][index_city2] + float(self.const/self.distance_traveled)

# on initialise matrice des pheromones avec des 0.1 partout
pheromone_map = [[0.1] * len(_CITIES) for i in range(len(_CITIES))]

from random import randint
colony = [] # on initialise une colonie de fourmis
for i in range(100) : 
    # ville initiale choisie au hasard
    city = _CITIES[randint(0,len(_CITIES)-1)]
    colony.append(ant(city, 0.3, 0.3, 0.05, 1))

# on suppose que la distance la plus courte est celle de la première fourmi 
ant = 0 # indice de la fourmi ayant fait le chemin le plus court (sera utile pour afficher la distance cumulée)
colony[0].update_visited_cities(colony[0].location)
colony[0].run() 
shortest_distance = colony[0].get_distance_traveled() #distance numérique
shortest_route = colony[0].get_visited_cities() #chemin correspondant à la distance la plus courte 

# les fourmis commencent leurs tours, on parcourt la liste et vérifie s'il existe une distance plus courte que celle qu'on a supposé
for i in range(1,len(colony)) :
    colony[i].update_visited_cities(colony[i].location)
    colony[i].run() 
    if colony[i].get_distance_traveled() < shortest_distance :
        ant = i
        shortest_distance = colony[i].get_distance_traveled()
        shortest_route = colony[i].get_visited_cities()

# on affiche la distance la plus courte ainsi que le chemin correspondant
print("Shortest distance : " + str(shortest_distance))

#liste de villes avec des coordonnées assez séparées pour pouvoir bien les représenter sur la map 
dict_cities = {
    "Bordeaux" : [230, 460],
    "Paris" : [370, 200],
    "Nice" : [570, 550],
    "Lyon" : [470, 410],
    "Nantes" : [190, 300],
    "Brest" : [70, 210],
    "Lille" : [400, 110],
    "Clermont-Ferrand" : [390, 380],
    "Strasbourg" : [590, 250],
    "Poitiers" : [300, 340],
    "Angers":  [250, 290],
    "Montpellier" : [420, 550],
    "Caen" : [260, 190],
    "Rennes" : [190, 240],
    "Pau" : [230, 560],
}

#il faut modifier les coordonnées dans shortest_route pour pouvoir bien afficher chaque ville sur la map 
updated_shortest_route = [[0]*2 for i in range(len(shortest_route))]
for i in range(len(shortest_route)):
    updated_shortest_route[i][0] = str(shortest_route[i][0])
    updated_shortest_route[i][1] = dict_cities[str(shortest_route[i][0])]
print('Shortest route : ' + str(updated_shortest_route))
print(pheromone_map)

#image de la carte de france
france_map = cv2.imread('france_map.png')
cumulative_distance = 0 
for i in range(len(updated_shortest_route)) :
    # on affiche le titre + les villes avec les fonctions d'OpenCV putText et circle
    cv2.putText(france_map, "Shortest distance traveled : " + str(round(shortest_distance,2)), (180, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1)
    cv2.putText(france_map, updated_shortest_route[i][0], (int(updated_shortest_route[i][1][0]-10),int(updated_shortest_route[i][1][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.circle(france_map,(int(updated_shortest_route[i][1][0]),int(updated_shortest_route[i][1][1])), 3, (0,0,255), -1)
for i in range(len(updated_shortest_route)-1) :
    # on affiche la distance cumulée
    cumulative_distance += float(distance(colony[ant].visited_cities[i][1], colony[ant].visited_cities[i+1][1]))
    cv2.putText(france_map, "Cumulative distance : " + str(round(cumulative_distance,2)), (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    # on trace le chemin pris 
    cv2.arrowedLine(france_map, (int(updated_shortest_route[i][1][0]),int(updated_shortest_route[i][1][1])), (int(updated_shortest_route[i+1][1][0]),int(updated_shortest_route[i+1][1][1])), (0,180,0), 1)
    cv2.imshow("Ant colony best path", france_map)
    # tant que le tour n'est pas fini, on attend 0.5s avant de tracer le chemin vers la ville suivante choisie 
    cv2.waitKey(500)
    cv2.putText(france_map, "Cumulative distance : " + str(round(cumulative_distance,2)), (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
# si le tour est fini, on laisse la fenêtre ouverte
cv2.waitKey(0)