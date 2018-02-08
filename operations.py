import numpy as np
import matplotlib.pyplot as plt
from config import Params as p

def basic_stats(name, param):
    print()
    print("Podstawowa statystyka dla:", name)
    print("MIN:", min(param))
    print("MAX:", max(param))
    print("ŚREDNIA:", np.mean(param))
    print("MEDIANA:", np.median(param))
    print("ODCH. STD:", np.std(param))
    print("WARIANCJA:", np.var(param))
    print("HISTOGRAM:", np.histogram(param))
    print()

def corrections(variables):
    print("Wstępne poprawianie danych:")
    for name, variable in variables.items():
        basic_stats(name, variable)
        #for index, value in enumerate(variable):
            #if (value == p.missing_value):
            #    #konsola
            #    print ("Zmienna:", name, "indeks:", index, "anomalia o wartości:", value)
            #    median = np.median(variable)
            #    print("Naprawiam. Stara wartość:", variable[index], ", nowa wartość:", median)
            #    variable[index] = median
            #wyliczamy podstawowe statystyki
        #basic_stats(name, variable)

def histo(variables):
    i = 0; j = 0
    # Tworzę wykres 4*4, tak by zmieściły się wszystkie histogramy
    f, axarr = plt.subplots(4, 4)
    # Maksymalizacja okna wykresu
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    # Czcionka
    plt.rc('font', family='Arial', size=15)
    # Iterujemy po słowniku, wyświetlając statystyki dla poszczególnych zmiennych
    for name, variable in variables.items():
        # basic_stats(name, variable)
        axarr[i, j].hist(variable, 100)
        # Nadaję tytuły histogramom takie, jak nazwa zmiennej, którą wizualizują
        axarr[i, j].set_title(name)
        j += 1
        if (j % 4 == 0):
            i += 1
        j = j % 4
    # Wyświetlam wykres
    plt.show()

def ncorrelate(param_a, param_b):
    result_a = (param_a -np.mean(param_a)) / (np.std(param_a) * len(param_a))
    result_b = (param_b - np.mean(param_b)) / (np.std(param_b))
    return np.correlate(result_a, result_b)[0]

def test_correlation(variables):
    # Badamy korelacje między wszystkimi zmiennymi
    print("\nSprawdzenie korelacji:")
    for name1, variable1 in variables.items():
        for name2, variable2 in variables.items():
            if name1 != name2:
                if (ncorrelate(variable1,variable2) > p.correlation_ratio_pos):
                    print ("Silna dodatnia korelacja między", name1,"a", name2,":", ncorrelate(variable1,variable2))
                if (ncorrelate(variable1,variable2) < p.correlation_ratio_neg):
                    print("Silna ujemna korelacja między", name1, "a", name2, ":", ncorrelate(variable1, variable2))

def dict_to_list(variables):
    list = []
    for name, variable in variables.items():
        x = name
        for index, value in enumerate(variable):
            list.append(variable[index])
    return list, x

def common_visualisation_3_variables(variables_1, variables_2, variables_3):
    list1, name1 = dict_to_list(variables_1)
    list2, name2 = dict_to_list(variables_2)
    list3, name3 = dict_to_list(variables_3)
    #Maksymalizacja okna
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    #Dane do wizualizacji 1 charakterysytki
    x1 = range(len(list1)); y1 = list1
    plt.plot(x1,y1, 'r--')
    # Dane do wizualizacji 2 charakterysytki
    x2 = range(len(list2)); y2 = list2
    plt.plot(x2,y2, 'b--')
    # Dane do wizualizacji 3 charakterysytki
    x3 = range(len(list3));
    y3 = list3
    plt.plot(x3, y3, 'g--')

    #Opis osi wykresu i tytuł
    plt.title("Wykres zależności: %s" %(name1) + " , %s" %(name2) + " i %s" %(name3))
    plt.xlabel('Numer obserwacji')
    plt.ylabel('Wartości obserwacji')
    plt.show()

def common_visualisation_2_variables(variables_1, variables_2):
    list1, name1 = dict_to_list(variables_1)
    list2, name2 = dict_to_list(variables_2)
    #Maksymalizacja okna
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    #Dane do wizualizacji 1 charakterysytki
    x1 = range(len(list1)); y1 = list1
    plt.plot(x1,y1, 'r--')
    # Dane do wizualizacji 2 charakterysytki
    x2 = range(len(list2)); y2 = list2
    plt.plot(x2,y2, 'b--')

    #Opis osi wykresu i tytuł
    plt.title("Wykres zależności: %s" %(name1) + " , %s" %(name2))
    plt.xlabel('Numer obserwacji')
    plt.ylabel('Wartości obserwacji')
    plt.show()



def gather_data(variables, ref, eval):
    list1 = []
    list2 = []
    for name1, variable in variables.items():
        for index, value in enumerate(variable):
            if name1 == ref:
                list1.append(variable[index])

    for name2, variable in variables.items():
        for index, value in enumerate(variable):
            if name2 == eval:
                list2.append(variable[index])
    return list1, ref, list2, eval


def linear_regression_simple(list1, name1, list2, name2):
    #Maksymalizacja okna
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    # Regresja liniowa dla zmiennych z dużą korelacją dodatnią
    a, b = np.polyfit(list1, list2, 1)  # Wielomian 1 rzędu - prosta
    yreg = [a * i + b for i in list1]
    #Wykresy
    plt.plot(list1, list2, ".")
    plt.plot(list1, yreg)
    plt.title("Regresja liniowa")
    plt.xlabel("%s" %(name1))
    plt.ylabel("%s" %(name2))
    plt.show()