import math

def find_nearest_right(sorted_x_values, x):
    for value in sorted_x_values:
        if value > x:
            return value
    return None

def find_nearest_left(sorted_x_values, x):
    reversed_sorted_x_values = list(reversed(sorted_x_values))
    for value in reversed_sorted_x_values:
        if value < x:
            return value
    return None

def y(x):
    return (1/x) + math.exp(x)

def quadratic_optimization(epsilon_1, epsilon_2, delta, a, b):

    # Шаг 1
    x_1 = a
    
    # Шаг 2
    x_2 = x_1 + delta

    # Шаг 3
    y_1 = y(x_1)
    y_2 = y(x_2)

    # Шаг 4
    if (y_1 > y_2):
        x_3 = x_1 + 2 * delta
    else:
        x_3 = x_1 - delta
    
    # Шаг 5
    y_3 = y(x_3)

    # Шаг 6
    x_values = [x_1, x_2, x_3]
    y_values = [y_1, y_2, y_3]
    y_min = min(y_values)
    min_y_index = y_values.index(y_min)
    x_min = x_values[min_y_index]

    # Шаг 7
    x_waved = 0.5 * ((x_2**2 - x_3**2) * y_1 + (x_3**2 - x_1**2) * y_2 + (x_1**2 - x_2**2) * y_3) / ((x_2 - x_3) * y_1 + (x_3 - x_1) * y_2 + (x_1 - x_2) * y_3)
    y_waved = y(x_waved)

    # Циклим весь этот кошмар 
    while (abs((y_min - y_waved) / y_waved) >= epsilon_1) and (abs((x_min - x_waved) / x_waved) >= epsilon_2):

        if (min(x_1, x_2, x_3) <= x_waved <= max(x_1, x_2, x_3)): 

            # Шаг 8 (б)
            sorted_x_values = sorted([x_1, x_2, x_3, max(x_min, x_waved)])
            x_2 = min(x_min, x_waved)

            x_1 = find_nearest_right(sorted_x_values, x_2)   
            x_3 = find_nearest_left(sorted_x_values, x_2)

            # Шаг 6
            y_1 = y(x_1)
            y_2 = y(x_2)
            y_3 = y(x_3)

            x_values = [x_1, x_2, x_3]
            y_values = [y_1, y_2, y_3]
            y_min = min(y_values)
            min_y_index = y_values.index(y_min)
            x_min = x_values[min_y_index]

            # Шаг 7
            x_waved = 0.5 * ((x_2**2 - x_3**2) * y_1 + (x_3**2 - x_1**2) * y_2 + (x_1**2 - x_2**2) * y_3) / ((x_2 - x_3) * y_1 + (x_3 - x_1) * y_2 + (x_1 - x_2) * y_3)
            y_waved = y(x_waved)
        
        else:
            # Шаг 8(в)
            x_1 = x_waved
            
            # Шаг 2
            x_2 = x_1 + delta

            # Шаг 3
            y_1 = y(x_1)
            y_2 = y(x_2)

            # Шаг 4
            if (y_1 > y_2):
                x_3 = x_1 + 2 * delta
            else:
                x_3 = x_1 - delta
            
            # Шаг 5
            y_3 = y(x_3)

            # Шаг 6
            x_values = [x_1, x_2, x_3]
            y_values = [y_1, y_2, y_3]
            y_min = min(y_values)
            min_y_index = y_values.index(y_min)
            x_min = x_values[min_y_index]

            # Шаг 7
            x_waved = 0.5 * ((x_2**2 - x_3**2) * y_1 + (x_3**2 - x_1**2) * y_2 + (x_1**2 - x_2**2) * y_3) / ((x_2 - x_3) * y_1 + (x_3 - x_1) * y_2 + (x_1 - x_2) * y_3)
            y_waved = y(x_waved)

    x_result = x_waved
    y_result = y(x_result)
    return x_result, y_result


epsilon_1 = 0.0001
epsilon_2 = 0.0001
delta = 0.01
a = 0.5
b = 1.5
x_extremum, y_extremum = quadratic_optimization(epsilon_1, epsilon_2, delta, a, b)

print("\n~~~~~ Нахождение экстремума функции ~~~~~")
print("\n", "-" * 60, "\n")

print(" Результат полученный с помощью Метода Квадратичной Апроксимации: \n")
print("x = ", x_extremum, "\ny = ", y_extremum)
print("\n", "-" * 60, "\n")
