import math

def y(x):
    return (1/x) + math.exp(x)

def half_interval_method(a, b, epsilon):
    while (b - a > 2 * epsilon):
        x_1 = (a + b - epsilon) / 2
        x_2 = (a + b + epsilon) / 2
        if (y(x_1) > y(x_2)):
            a = x_1
        else:
            b = x_2
    x_m = (a + b) / 2
    y_m = y(x_m)
    return x_m, y_m

def golden_ratio_method(a, b, epsilon):
    golden_ratio = (3 - math.sqrt(5)) / 2 
    x_1 = a + golden_ratio * (b - a)
    x_2 = a + (1 - golden_ratio) * (b - a)
    while (b - a > epsilon):
        y_1, y_2 = y(x_1), y(x_2)
        if (y_1 <= y_2):
            b, x_2 = x_2, x_1
            x_1 = a + golden_ratio * (b - a)
        else:
            a, x_1= x_1, x_2
            x_2 = a + (1 - golden_ratio) * (b - a)
    x_m = (a + b) / 2
    y_m = y(x_m)
    return x_m, y_m
    
def calculate_x_with_wave(a, b, y_a, y_b):
    return a - (y_a / (y_a - y_b)) * (a - b) 

def derivative(x, n = 1):
    return (((-1)**n * math.factorial(n)) / x**(n + 1)) + math.exp(x)
    
def chord_method(a, b, epsilon):
    f_a_derivative = derivative(a)
    f_b_derivative = derivative(b)
    x_waved = calculate_x_with_wave(a, b, f_a_derivative, f_b_derivative)
    y_waved_derivative = derivative(x_waved)
    while (abs(y_waved_derivative) > epsilon):
        if (y_waved_derivative > 0):
            b = x_waved
            f_b_derivative = y_waved_derivative
        else:
            a = x_waved
            f_a_derivative = y_waved_derivative
        x_waved = calculate_x_with_wave(a, b, f_a_derivative, f_b_derivative)
        y_waved_derivative = derivative(x_waved)
    x_m = x_waved
    y_m = y(x_waved)
    return x_m, y_m

def newtons_method(a, b, epsilon):

    x_0 = (a + b) / 2
    while (abs(derivative(x_0)) > epsilon):
        x_0 = x_0 - (derivative(x_0, 1) / derivative(x_0, 2))

    x_m = x_0
    y_m = y(x_m)
    return x_m, y_m

print("\n~~~~~ Нахождения точки минимума функции ~~~~~")
print("\n", "-" * 60, "\n")

a = 0.5
b = 1.5
epsilon = 0.001

x_extremum, y_extremum = half_interval_method(a, b, epsilon)

print(" 1. Результат полученный с помощью Метода Половинного Деления: ")
print("x = ", x_extremum, "\ny = ", y_extremum)
print("\n", "-" * 60, "\n")

x_extremum, y_extremum = golden_ratio_method(a, b, epsilon)

print(" 2. Результат полученный с помощью Метода Золотого Сечения: ")
print("x = ", x_extremum, "\ny = ", y_extremum)
print("\n", "-" * 60, "\n")

x_extremum, y_extremum = chord_method(a, b, epsilon)

print(" 3. Результат полученный с помощью Метода Хорд: ")
print("x = ", x_extremum, "\ny = ", y_extremum)
print("\n", "-" * 60, "\n")

x_extremum, y_extremum = newtons_method(a, b, epsilon)

print(" 4. Результат полученный с помощью Метода Ньютона: ")
print("x = ", x_extremum, "\ny = ", y_extremum)
print("\n", "-" * 60, "\n")
