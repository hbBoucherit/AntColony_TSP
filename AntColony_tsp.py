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
        # liste des villes que la fourmi peut visiter, ce sont toutes les villes au tout début
        self.possible_cities = deepcopy(_CITIES)
        self.distance_traveled = 0
        self.alpha = alpha
        self.beta = beta
        self.rho = rho #evaporation
        self.const = const  # constante Q de dépôt de phéromones
        self.visited_cities = []  # dans l'ordre de visite
        self.tour_complete = False  # true quand le tour est terminé

    def run(self):
        while self.possible_cities:
            next_city = self.find_next_city(self.location)
            self.traverse(self.location, next_city)
        self.tour_complete = True
        self.get_distance_traveled()
        self.add_pheromones()

    def find_next_city(self, actual_city):
        # on suppose que la ville suivante est la première de la liste
        next_city = self.possible_cities[0]
        visibility0 = float(1/distance(actual_city[1], next_city[1]))  # inverse de la distance
        attractiveness0 = ((visibility0**self.alpha) * (pheromone_map[_CITIES.index(actual_city)][_CITIES.index(next_city)]**self.beta))

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
        self.distance_traveled += float(distance(start[1], end[1]))

    def get_visited_cities(self):
        if self.tour_complete:
            return self.visited_cities
        return None

    def get_distance_traveled(self):
        if self.tour_complete:
            print("distance traveled :" + str(self.distance_traveled))
            return self.distance_traveled
        else:
            return None

    def add_pheromones(self):
        for i in range (0,len(self.visited_cities)-1) :
            #on récupère l'indice de deux villes successives 
            index_city1 = _CITIES.index(self.visited_cities[i])
            index_city2 = _CITIES.index(self.visited_cities[i+1])
        
            #on prend on compte l'évaporation aussi 
            pheromone_map[index_city1][index_city2] = (1-self.rho)*pheromone_map[index_city1][index_city2] + float(self.const/self.distance_traveled)

# matrice des pheromones
pheromone_map = [[0.1] * len(_CITIES) for i in range(len(_CITIES))]

from random import randint
colony = [] #on initialise une colonie de fourmis
for i in range(20) : 
    #ville choisie au hasard
    city = _CITIES[randint(0,len(_CITIES)-1)]
    colony.append(ant(city, 0.1, 0.3, 0.2, 1))

for i in range(len(colony)) :
    colony[i].update_visited_cities(colony[i].location)
    colony[i].run() 
    print(str(i) + " -------------------------------------------- ")
    print(colony[i].visited_cities)

#taille de la fenêtre
height = 600 
width = 600

#liste de villes avec des coordonnées assez séparées pour pouvoir bien les représenter sur la map 
#à modifier ! 
cities = [
    ["Bordeaux", [44.833333, -0.566667]],
    ["Paris", [48.8566969, 2.3514616]],
    ["Nice", [43.7009358, 7.2683912]],
    ["Lyon", [45.7578137, 4.8320114]],
    ["Nantes", [47.2186371, -1.5541362]],
    ["Brest", [48.4, -4.483333]],
    ["Lille", [50.633333, 3.066667]],
    ["Clermont-Ferrand", [45.783333, 3.083333]],
    ["Strasbourg", [48.583333, 7.75]],
    ["Poitiers", [46.583333, 0.333333]],
    ["Angers", [47.466667, -0.55]],
    ["Montpellier", [43.6, 3.883333]],
    ["Caen", [49.183333, -0.35]],
    ["Rennes", [48.083333, -1.683333]],
    ["Pau", [43.3, -0.366667]],
] 

blank_image = np.zeros((height,width,3), np.uint8)
blank_image[:,0:width] = (255,255,255)
for i in range(len(cities)):
    cv2.circle(blank_image,(int(cities[i][1][0]),int(cities[i][1][1])), 3, (0,0,255), -1)
cv2.imshow("Ant colony best path",blank_image)
cv2.waitKey(0)