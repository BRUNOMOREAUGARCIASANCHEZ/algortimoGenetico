import math
import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import simpledialog


# Definir los límites del espacio de búsqueda
plt.ion()  # Activa el modo interactivo de Matplotlib
x_min, x_max = -4, 4
y_min, y_max = -4, 4
tam_poblacion_inicial = 10
tasa_mutacion = 0.05


def ejecutar_algoritmo(pob_in):
    n_generaciones = simpledialog.askinteger("Número de Generaciones", "Ingrese el número de generaciones:")
    sig_generacion = pob_in

    # configurar los valores de la poblacion 0 en un plot
    plt.figure()
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Generación 0')
    plt.grid(True)
    x_values = [individual[0] for individual in sig_generacion]
    y_values = [individual[1] for individual in sig_generacion]
    plt.scatter(x_values, y_values, c='gray')

    # Aplicar elitismo a los dos mejores individuos de la generación actual
    sig_generacion.sort(key=funcion_aptitud)                # minimizar el valor

    #los primeros dos mejores, son los dos valores más pequeños
    best_solution = sig_generacion[0]
    second_best_solution = sig_generacion[1]

    print("\nPoblación inicial (generacion 0):\n") # imprimimos la poblacion 0 por consola....
    for i, individual in enumerate(sig_generacion, 1):
        print(f"Individuo {i}: (x={individual[0]}, y={individual[1]}) ___________ apt = {funcion_aptitud(individual)}")
    print("\n")

    print(f"\n\nMejor individuo:........... {best_solution} ___________ apt = {funcion_aptitud(best_solution)}")
    print(f"Segundo mejor individuo:... {second_best_solution} ___________ apt = {funcion_aptitud(second_best_solution)}")

    # Mostrar el gráfico de la generación 0
    plt.show()

    # configuraciones para las siguentes generaciones....
    best_solution = None
    colors = plt.cm.viridis([gen_cont / n_generaciones for gen_cont in range(n_generaciones)])

    # el algoritmo se repite, n_generaciones veces
    for gen_cont in range(n_generaciones):
        # Crear un plot para cada generación....
        plt.figure()
        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title(f'Generación {gen_cont+1}')
        plt.grid(True)

        #reproducción, uso de la ruleta....
        print(f"\nProceso de reproducción de la generacion {gen_cont}:")
        # cada pareja va a tener dos hijos, por eso el numero de parejas
        # (numero de reproducciones), es la mitad de la población total
        for i in range(int(tam_poblacion_inicial/2)):
            #giramos la ruleta una vez aquí, (por cada vez, se seleccionan a dos padres)
            padres_seleccionados = seleccion_por_ruleta(sig_generacion)
            print(f"\n    Pareja {i}: P1={padres_seleccionados[0]}    X    P2={padres_seleccionados[1]}")
            # mandamos a escoger el método de cruce, de manera aleatoria en la funcion "elegir_cruza()"
            nuevos_2_hijos = elegir_cruza(padres_seleccionados[0], padres_seleccionados[1])
            print(f"   Sus hijos: H1:{nuevos_2_hijos[0]}    &    H2:{nuevos_2_hijos[1]}")

            # agregamos los dos hijos obtenidos a la siguiente generacion (en el mismo espacio en el que se encuentra la vieja)
            # (la población vieja se elimina automáticamente al terminar este 'for')
            sig_generacion.append(nuevos_2_hijos[0])
            sig_generacion.append(nuevos_2_hijos[1])

        #eliminamos a la generación anterior (conservando únicamente a la generación nueva)
        sig_generacion = sig_generacion[tam_poblacion_inicial:]

        # configuramos los datos del plot para la generación actual
        x_values = [individual[0] for individual in sig_generacion]
        y_values = [individual[1] for individual in sig_generacion]
        plt.scatter(x_values, y_values, c=[colors[gen_cont]] * len(x_values))

        # hacer mutaciones, con una tasa del 5% de probabilidad
        for i in range(len(sig_generacion)):
            if random.random() < tasa_mutacion: # probabilidad
                print(f"\n\n(Mutando al individuo: {sig_generacion[i]})", end="")
                sig_generacion[i] = mutacion(sig_generacion[i])
                print(f" ----> {sig_generacion[i]}")

        # Aplicar elitismo a los dos mejores individuos de la generación actual
        # ordenamos de menor a mayor, y tomamos los dos primeros elementos de la lista ya ordenada (cuando el objetivo es minimizar)
        # si el objetivo en cambio es maximizar, entonces tomamos los dos ultimos elementos
        sig_generacion.sort(key=funcion_aptitud)

        #minimizar (tomar los valores mas chicos)
        best_solution = sig_generacion[0]
        second_best_solution = sig_generacion[1]

        #maximizar (tomar los valores mas grandes)
        #best_solution = sig_generacion[tam_poblacion_inicial-1]
        #second_best_solution = sig_generacion[tam_poblacion_inicial-2]


        #imprimimos los datos de la generacion actual por consola....
        print(f"\n\nMejor individuo:........... {best_solution} ___________ apt = {funcion_aptitud(best_solution)}")
        print(f"Segundo mejor individuo:... {second_best_solution} ___________ apt = {funcion_aptitud(second_best_solution)}")

        print(f"\n\n ################################### GENERACION {gen_cont+1}  ################################### \n")
        j = 0
        for i in sig_generacion:
            print(f"Individuo {j}: {i}  ___________ apt = {funcion_aptitud(i)}")
            j = j + 1

        # Mostramos el gráfico de la generación actual....
        plt.show()
        plt.pause(1)

    # al salir del for, ya solo queda imprimir al mejor individuo de la ultima generacion....


    # configurar datos de la ultima ventana....
    plt.figure()
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title(f'Mejor Individuo de la Última Generación')
    plt.grid(True)

    # Pintar a la población completa de otro color
    x_values = [individual[0] for individual in sig_generacion]
    y_values = [individual[1] for individual in sig_generacion]
    plt.scatter(x_values, y_values, c='blue', label='Población')

    # !!!! Pintar al mejor individuo de rojo
    plt.scatter(best_solution[0], best_solution[1], c='red', label='Mejor Solución')

    # imprimir el plot
    plt.legend(loc='best')
    plt.show()


def limitar_valor(valor):
    # no permite que el valor sea mayor a 4 ni menor a -4
    val = np.random.uniform(0.01,0.5)
    valor = max(-4, min(4, valor))
    if valor == 4:
        valor = valor - val
    if valor == -4:
        valor = valor + val

    return valor


def cruza_interpolada(p1, p2):
    t = 0.5
    x1, y1 = p1
    x2, y2 = p2

    # interpolamos las coordenadas de los padres
    x_interpolado = x1 + (x2 - x1) * t
    y_interpolado = y1 + (y2 - y1) * t

    #las guardamos en el hijo 1
    h1 = (x_interpolado,y_interpolado)

    # e intercambiamos la coordenada x por la coordenada y (y viceversa) para el segundo hijo
    h2 = (y_interpolado,x_interpolado)

    return (h1, h2)


def cruza_hiperbolica(p1, p2):
    alpha = np.random.uniform(0, 1)  # Factor de ponderación aleatorio entre 0 y 1

    # Aplicar funciones hiperbólicas para combinar los valores de los padres
    x1, y1 = np.sinh(p1[0]), np.cosh(p1[1])
    x2, y2 = np.sinh(p2[0]), np.cosh(p2[1])

    # Combinar los valores ajustados para crear los hijos
    # Realiza una cruza hiperbólica ponderada entre dos padres para generar dos hijos.
    # La ponderación es controlada por 'alpha', con coordenadas ajustadas usando funciones hiperbólicas 'sinh' y 'cosh'.
    # Los hijos 'h1' y 'h2' se calculan a partir de las coordenadas de los padres 'p1' y 'p2' de acuerdo a la ponderación 'alpha'.
    h1 = (limitar_valor(alpha * x1 + (1 - alpha) * x2), limitar_valor(alpha * y1 + (1 - alpha) * y2))
    h2 = (limitar_valor((1 - alpha) * x1 + alpha * x2), limitar_valor((1 - alpha) * y1 + alpha * y2))

    return h1, h2


def cruza_sinusoidal(p1, p2):
    alpha = np.random.uniform(0, 1)  # Factor de ponderación aleatorio entre 0 y 1

    # Combinar los valores de los padres utilizando seno y coseno
    x1, y1 = np.sin(p1[0]), np.cos(p1[1])
    x2, y2 = np.sin(p2[0]), np.cos(p2[1])

    # Combinar los valores ajustados para crear los hijos
    #funciona igual que la hiperbolica pero usa seno y coseno normales en lugar de hiperbolicos
    h1 = (limitar_valor(alpha * x1 + (1 - alpha) * x2), limitar_valor(alpha * y1 + (1 - alpha) * y2))
    h2 = (limitar_valor((1 - alpha) * x1 + alpha * x2), limitar_valor((1 - alpha) * y1 + alpha * y2))

    return h1, h2


def mutacion(individuo):
    # Generar valores aleatorios para la mutación
    mutacion_x = np.random.uniform(-2, 2)
    mutacion_y = np.random.uniform(-2, 2)

    # sumar la mutación en 'x' e 'y'
    mutado_x = limitar_valor(individuo[0] + mutacion_x)
    mutado_y = limitar_valor(individuo[1] + mutacion_y)

    return (mutado_x, mutado_y)


def funcion_aptitud(suj):
    x = suj[0]
    y = suj[1]
    # implementamos la función Z
    Z = math.exp(-(y + 1) ** 2 - x ** 2) * (x - 1) ** 2 - (math.exp(-(x + 1) ** 2) / 3) + math.exp(-x ** 2 - y ** 2) * (10 * x ** 3 - 10 + 10 * y ** 3)
    return Z


def seleccion_por_ruleta(poblacion):
    padres_seleccionados = []

    # Calcular la suma total de aptitudes en la población y las probabilidades acumulativas (CDF)
    suma_aptitudes = sum(funcion_aptitud(individuo) for individuo in poblacion)
    probabilidades_acumulativas = [sum(funcion_aptitud(individuo) for individuo in poblacion[:i+1]) / suma_aptitudes for i in range(len(poblacion))]

    # Selección de individuos mediante una búsqueda lineal basada en probabilidades acumulativas.
    # Se encuentra el primer individuo cuya probabilidad acumulativa es mayor o igual al número aleatorio.
    numero_aleatorio1 = random.random()
    numero_aleatorio2 = random.random()
    padre1 = next(individuo for individuo, prob in zip(poblacion, probabilidades_acumulativas) if prob >= numero_aleatorio1)
    padre2 = next(individuo for individuo, prob in zip(poblacion, probabilidades_acumulativas) if prob >= numero_aleatorio2)
    padres_seleccionados.append(padre1)
    padres_seleccionados.append(padre2)

    return padres_seleccionados


def elegir_cruza(padre1, padre2):
    # Elige un operador de cruza basado en algún criterio
    selected_crossover = random.choice(["adaptiva", "hiperbolica", "sinusoidal"])

    if selected_crossover == "adaptiva":
        hijo1, hijo2 = cruza_interpolada(padre1, padre2)
    elif selected_crossover == "hiperbolica":
        hijo1, hijo2 = cruza_hiperbolica(padre1, padre2)
    elif selected_crossover == "sinusoidal":
        hijo1, hijo2 = cruza_sinusoidal(padre1, padre2)
    else:
        print("Ha habido un error, vuelve a inentar....")
        pass

    return hijo1, hijo2


# Generar una población aleatoria...
population = []
for idx in range(tam_poblacion_inicial):
    x = np.random.uniform(x_min, x_max)
    y = np.random.uniform(y_min, y_max)
    individual = (x, y)
    population.append(individual)

ejecutar_algoritmo(population)

