import math
from scipy.optimize import minimize 
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def df_dx(x, y):
    return 8 * x + 16

def df_dy(x, y):
    return 6 * y - 4

def f_x(x, y):
    return 4 * x**2 + 3 * y**2 + 16 * x - 4 * y

def gradient(epsilon, lamda, x, y):

    fun = f_x(x, y)
    vector_stroka = [df_dx(x, y), df_dy(x, y)]
    x = x - lamda * vector_stroka[0]
    y = y - lamda * vector_stroka[1]

    while abs(f_x(x, y) - fun) > epsilon:

        if (f_x(x, y) > fun): 
            lamda /= 2
            
        fun = f_x(x, y)
        vector_stroka = [df_dx(x, y), df_dy(x, y)]
        x = x - lamda * vector_stroka[0]
        y = y - lamda * vector_stroka[1]

    return x, y

def find_minimum(func, initial_guess, method):
    return minimize(func, initial_guess, method=method).x

def steepest_descent(epsilon, x, y):

    abs_grad = math.sqrt(df_dx(x, y)**2 + df_dy(x,y)**2)

    dfdx = df_dx(x, y) / abs_grad
    dfdy = df_dy(x, y) / abs_grad

    points = [x, y]
    point_x, point_y = points[0], points[1]

    (point_x - x * dfdx)
    (point_y - x * dfdy)

    # equation = lambda x: np.exp(-(point_x - x * dfdx)**2 + (point_y - x * dfdy)**2+ 2*(point_x - x * dfdx)*(point_y - x * dfdy) - (point_y - x * dfdy))
    # equation = lambda x: (point_x - x * dfdx)**2 + (point_y - x * dfdy)**2 + 1.5*(point_x - x * dfdx)*(point_y - x * dfdy)

    equation = lambda x: 4*((point_x - x * dfdx))**2 + 3*((point_y - x * dfdy))**2 + 16*((point_x - x * dfdx)) - 4*((point_y - x * dfdy))

    iteration = 10 ** 4
    i = 0

    while (abs_grad > epsilon) and (i < iteration):

        i += 1

        minimized = find_minimum(equation, 0.0, 'BFGS')

        x = points[0] - minimized[0] * dfdx
        y = points[1] - minimized[0] * dfdy

        abs_grad = math.sqrt(df_dx(x, y)**2 +df_dy(x,y)**2)

        dfdx = df_dx(x, y) / abs_grad
        dfdy = df_dy(x, y) / abs_grad

        points = [x, y]
        point_x, point_y = points[0], points[1]

    if (i == iteration) :
        return "No extremum"
    
    return [points[0], points[1]]

epsilon = 0.1
lamda = 0.05
x_0 = 0
y_0 = 0
x, y = gradient(epsilon, lamda, x_0, y_0)
fun = f_x(x, y)

print("\n~~~~~ Нахождение экстремума функции нескольких переменных ~~~~~")
print("\n", "-" * 60, "\n")

print(" Результат полученный с помощью Метода Градиентного Спуска: \n")
print("x = ", x, "\ny = ", y)
print("F = ", fun)
print("\n", "-" * 60, "\n")

x = steepest_descent(epsilon, x_0, y_0)
if (len(x) == 2):
    fun = f_x(x[0], x[1])
    print(" Результат полученный с помощью Метода Наискорейшего Спуска: \n")
    print("x = ", x[0], "\ny = ", x[1])
    print("F = ", fun)
    print("\n", "-" * 60, "\n")
else:
    fun = x
    print(" Результат полученный с помощью Метода Наискорейшего Спуска: \n")
    print("F = ", fun)
    print("\n", "-" * 60, "\n")

