#Przygotowanie danych do analizy

#Ładowanie pakietów i modułów
import csv
from config import Params as p
from operations import *
#import numpy as np
#import matplotlib.pyplot as plt

#A. Wczytanie daych
# Tworzę puste listy, do których będę wczytywał kolumny danych z pliku csv
sample_id = [] #int
gen_cluster = [] #int
ecozone_name = [] #string
biome_number = [] #int
ecosystem_number = [] #num
mean_annual_temp = [] #float
mean_july_temp = [] #float
mean_january_temp = [] #float
annual_precipitation = [] #int
altitude = [] #int
road_density = [] #float
snow_cover_depth = [] #float
density_of_population = [] #int

# Tworzę uchwyt na plik
df = open(p.data_file, 'rt')
env_data_wolves = csv.reader(df, delimiter=';')

#Opuszczam pierwszą obserwację (nagłówek)
next(env_data_wolves)

# Iteruję po poszczególnych observationch i dołączam do list
for observation in env_data_wolves:
    sample_id.append(observation[0])
    gen_cluster.append(float(observation[1].replace(',', '.')))
    #ecozone_name.append(float(observation[2].replace(',', '.')))
    biome_number.append(float(observation[3].replace(',', '.')))
    ecosystem_number.append(float(observation[4].replace(',', '.')))
    mean_annual_temp.append(float(observation[5].replace(',', '.')))
    mean_july_temp.append(float(observation[6].replace(',', '.')))
    mean_january_temp.append(float(observation[7].replace(',', '.')))
    annual_precipitation.append(float(observation[8].replace(',', '.')))
    altitude.append(float(observation[9].replace(',', '.')))
    road_density.append(float(observation[10].replace(',', '.')))
    snow_cover_depth.append(float(observation[11].replace(',', '.')))
    density_of_population.append(float(observation[12].replace(',', '.')))
#Zamykam uchwyt na plik
df.close()


#B. Podstawowe statystyki
# Tworzę słownik: kluczem jest nazwa zmiennej a wartością - zmienna
variables = {"gen_cluster":gen_cluster, "biome_number":biome_number, "ecosystem_number":ecosystem_number, "mean_annual_temp":mean_annual_temp, "mean_july_temp": mean_july_temp,
             "mean_january_temp":mean_january_temp, "annual_precipitation":annual_precipitation, "altitude":altitude, "road_density":road_density, "snow_cover_depth":snow_cover_depth, "density_of_population":density_of_population}
# Histogram - przedstawienie danych na histogramie
histo(variables)
# Wyświetlanie podstawowych statystyk
corrections(variables)

#C. Czyszczenie danych
#Dla brakujących danych w datasecie przyjęto wartość ....
#Na potrzeby ninejszej analizy, zastąpimy tę wartość medianą.

#Tworzę kopię pomocniczą słownika, którą będę poprawiał
#variables_corr = variables
#corrections(variables_corr)

#Ponieważ w przypadku zmiennej NMHC_GT wartości niepoprawnych jest więcej niż połowa obserwacji - zastąpienie wartości nic nie daje
#W przypadku innych zmiennych zastąpienie błędnej wartości przesuwa wynik w kierunku bardziej zbliżonego do realnego
#Idealnie wartości błędne zostaną zastąpione meedianą liczoną bez wartości błędnej -200.0
#variables_corr_final = {"NMHC_GT":NMHC_GT}
#variables_corr_final = variables
#corrections_final(variables_corr_final)
#histo(variables_corr_final)


#Badanie korelacji
variables_correlation = variables
test_correlation(variables_correlation)

#Wizualizacja mean_annual_temp, mean_january_temp i mean_july_temp na wspólnym wykresie
variable_1 = {"mean_annual_temp":mean_annual_temp}
variable_2 = {"mean_january_temp":mean_january_temp}
variable_3 = {"mean_july_temp":mean_july_temp}
common_visualisation_3_variables(variable_1, variable_2, variable_3)

#Wizualizacja snow_cover_depth a mean_january_temp i mean_annual_temp na wspólnym wykresie
variable_1 = {"snow_cover_depth":snow_cover_depth}
variable_2 = {"mean_january_temp":mean_january_temp}
variable_3 = {"mean_annual_temp":mean_annual_temp}
common_visualisation_3_variables(variable_1, variable_2, variable_3)




# Przeprowadzam regresję liniową tylko dla zmiennych silnie skorelowanych dodatnie
#Silne korelacje dodatnie między:

#1) mean_january_temp a gen_cluster: 0.74 / mean_annual_temp : 0.92
#2) mean_july_temp a mean_annual_temp : 0.83

#Silne korelacje ujemne między:
#3) snow_cover_depth a mean_january_temp : -0.82 / mean_annual_temp : -0.82


#ad.1)
list_pom = []
list_val = ['gen_cluster', 'mean_annual_temp']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'mean_january_temp', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.2)
list_pom = []
list_val = ['mean_annual_temp']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'mean_july_temp', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.3)
list_pom = []
list_val = ['mean_january_temp', 'mean_annual_temp']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'snow_cover_depth', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1
