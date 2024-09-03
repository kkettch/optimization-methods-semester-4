import random

# сгенерировать начальную популяцию
def make_initial_population(traveling_salesman, n):
    numbers = [i for i in range(1, len(traveling_salesman[0]) + 1)]
    initial_population = []
    for _ in range(n):
        random_sequence = random.sample(numbers, len(numbers))
        initial_population.append(random_sequence)
    return initial_population

# сгенерировать границы для двухточечного оператора скрещивания 
def generate_bounds(traveling_salesman):
    n = len(traveling_salesman[0])

    num1 = random.randint(0, n)
    num2 = random.randint(0, n)
    
    while abs(num1 - num2) >= 4 or num1 == num2 or abs(num1 - num2) <= 1:
        num1 = random.randint(0, n)
        num2 = random.randint(0, n)

    # выбор минимальной и максимальной границ
    min_bound = min(num1, num2)
    max_bound = max(num1, num2)
    return min_bound, max_bound

# посчитать значение функции для одного элемента
def calculate_function_value(traveling_salesman, one_element):
    length_of_way = 0
    for i in range(len(one_element) - 1):
        length_of_way += traveling_salesman[one_element[i] - 1][one_element[i+1] - 1]
    length_of_way += traveling_salesman[one_element[len(one_element) - 1] - 1][one_element[0] - 1]
    return length_of_way

# инвертировать вероятности выбора элемента 
def invert_probability(probability_of_choosing_pair):
    number_index_pairs = [(num, idx) for idx, num in enumerate(probability_of_choosing_pair)]
    sorted_pairs = sorted(number_index_pairs, key=lambda x: x[0])
    first_values = [pair[0] for pair in sorted_pairs]
    first_values_reversed = list(reversed(first_values))
    for i, value in enumerate(first_values_reversed):
        sorted_pairs[i] = (value, sorted_pairs[i][1])
    sorted_pairs = sorted(sorted_pairs, key=lambda x: x[1])
    probability = []
    for i in range(len(sorted_pairs)):
        probability.append(sorted_pairs[i][0])
    return probability

# выбрать две пары для итерации, основываясь на вероятности
def choose_pairs(traveling_salesman, population):
    probability_of_choosing_pair = []
    sum_value = 0

    # считается сумму функций элементов
    for one_element in population: 
        function_value = calculate_function_value(traveling_salesman, one_element)
        sum_value += function_value
        probability_of_choosing_pair.append(function_value)
    
    # считается вероятность 
    for i in range(len(probability_of_choosing_pair)):
        probability_of_choosing_pair[i] /= sum_value

    # инвертирования вероятности
    probability = invert_probability(probability_of_choosing_pair)
    numbers = [1, 2, 3, 4]

    # выбор пар
    all_pairs = [(i, j) for i in numbers for j in numbers if i != j]
    all_probabilities = [p for p in probability for _ in range(len(numbers) - 1)]
    chosen_pairs = random.choices(all_pairs, weights=all_probabilities, k=2)
    while (chosen_pairs[0][0] == chosen_pairs[1][0] and chosen_pairs[0][1] == chosen_pairs[1][1]) or (chosen_pairs[0][0] == chosen_pairs[1][1] and chosen_pairs[0][1] == chosen_pairs[1][0]):
        chosen_pairs = random.choices(all_pairs, weights=all_probabilities, k=2)

    return chosen_pairs[0], chosen_pairs[1]

# посчитать потомков (с учетом возможной мутации)
def calculate_descendants(min_bound, max_bound, mutation_probability, population, pair):
    parent_1 = population[pair[0] - 1]
    parent_2 = population[pair[1] - 1]

    descendants_1 = []
    descendants_2 = []

    # нахождение чисел между границами
    min_bound_copy = min_bound
    for i in range(len(parent_1)):
        if (i == min_bound_copy and min_bound_copy < max_bound):
            descendants_1.append(parent_2[min_bound_copy])
            descendants_2.append(parent_1[min_bound_copy])
            min_bound_copy += 1
        else:
            descendants_1.append(0)
            descendants_2.append(0)

    # нахождение остальных чисел
    index = min_bound + 1
    for i in range(len(parent_1)):
        if (parent_1[index] not in descendants_1):
            for j in range(len(descendants_1)):
                if descendants_1[j] == 0:
                    descendants_1[j] = parent_1[index]
                    break
        if (parent_2[index] not in descendants_2):
            for j in range(len(descendants_2)):
                if descendants_2[j] == 0:
                    descendants_2[j] = parent_2[index]
                    break
        index += 1
        if (index > 4):
            index = 0
    
    mutation = random.randint(1, 100)
    if (mutation == (mutation_probability * 100)):
        index1 = random.randint(0, len(descendants_1) - 1)
        index2 = random.randint(0, len(descendants_1) - 1)
        descendants_1[index1], descendants_1[index2] = descendants_1[index2], descendants_1[index1]
    if (mutation == (mutation_probability * 100 + 1)):
        index1 = random.randint(0, len(descendants_2) - 1)
        index2 = random.randint(0, len(descendants_2) - 1)
        descendants_2[index1], descendants_2[index2] = descendants_2[index2], descendants_2[index1]

    return [descendants_1, descendants_2]    

# сделать редукцию
def perform_reduction(traveling_salesman, population, descendants):
    population.extend(descendants)

    # удаляем повторяющиеся значения
    population_tuples = [tuple(subarray) for subarray in population]
    unique_population = {subarray for subarray in population_tuples}
    unique_population_list = [list(subarray) for subarray in unique_population]

    # сортируем и оставляем только первые 4 наименьших пути
    sorted_population = sorted(unique_population_list, key=lambda x: calculate_function_value(traveling_salesman, x))
    return sorted_population[:4]

# данная матрица путей
traveling_salesman = [[0, 1, 7, 2, 8],
                      [2, 0, 10, 3, 1],
                      [7, 10, 0, 2, 6],
                      [2, 3, 2, 0, 4],
                      [8, 1, 6, 4, 0]]

# размер популяции
n = 4

# вероятность мутации
mutation_probability = 0.01

# генерация начальной популяции
population = make_initial_population(traveling_salesman, n)

for i in range(random.randint(2,5)):
    # определить границы оператора скрещивания
    min_bound, max_bound = generate_bounds(traveling_salesman)
    # определить две пары для образования потомков
    pair_1, pair_2 = choose_pairs(traveling_salesman, population)
    # посчитать потомков для 1 пары
    descendants = calculate_descendants(min_bound, max_bound, mutation_probability, population, pair_1)
    # посчитать потомков для 2 пары 
    descendants.extend(calculate_descendants(min_bound, max_bound, mutation_probability, population, pair_2))
    # произвести редукцию
    population = perform_reduction(traveling_salesman, population, descendants)
    print("Популяции на итерации", i+1, ": ")
    for i in range(len(population)):
        print("элемент: ", population[i], "значение функции: ", calculate_function_value(traveling_salesman, population[i]))

# определение минимального значения функции
min_population = min(population, key=lambda x: calculate_function_value(traveling_salesman, x))
print("Полученный путь с минимальной суммой: ", min_population)
print("Нйденная минимальная сумма: ", calculate_function_value(traveling_salesman, min_population))