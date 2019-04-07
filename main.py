import random
import math
import matplotlib.pyplot as plt


"""
START
Generate the initial population
Compute fitness
REPEAT
    Selection
    Crossover
    Mutation
    Compute fitness
UNTIL population has converged
STOP
"""


class TSP(object):
    def __init__(self, filename, start_city, pop_size):
        self.filename = filename
        self.start_city = start_city
        self.pop_size = pop_size
        self.popultn = []
        self.dist_list = []

    solution_path = []

    def generate_initial_population(self):

        population = []

        with open(self.filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        size = len(content)

        for i in range(self.pop_size):
            numbers = list(range(1, (size + 1)))

            temp = numbers.index(self.start_city)
            numbers.pop(temp)

            aa = [
                numbers.pop(random.randint(0,
                                           len(numbers) - 1))
                for i in range((size - 1))
            ]
            population.append(list(aa))

        self.popultn = population
        self.individuals_length = len(self.popultn[0])

        return self.popultn

    def eval_function(self, population):

        with open(self.filename) as f:
            content = f.readlines()
        content = [[x.strip('\n')] for x in content]

        starting_city = content[self.start_city - 1][0].split()[0]

        starting_city_xcord = float(content[self.start_city - 1][0].split()[1])
        starting_city_ycord = float(content[self.start_city - 1][0].split()[2])

        distance_array = []

        for i in range(len(population)):
            dist = 0
            starting_city_xcord = float(
                content[self.start_city - 1][0].split()[1])
            starting_city_ycord = float(
                content[self.start_city - 1][0].split()[2])
            for j in range(len(population[i])):
                temp = int(population[i][j])

                dest_x = float(content[temp - 1][0].split()[1])
                dest_y = float(content[temp - 1][0].split()[2])

                dist += math.sqrt(
                    math.pow((starting_city_xcord - dest_x), 2) +
                    math.pow((starting_city_ycord - dest_y), 2))

                starting_city_xcord = dest_x
                starting_city_ycord = dest_y

            distance_array.append(dist)

        self.dist_list = distance_array

        return distance_array

    def do_selection(self, dist_array, n_element):

        tmp = []
        selected_indices = []
        cpy_dist_array = dist_array[:]
        dist_array.sort()

        for i in range(n_element):
            tmp.append(dist_array[i])

        for i in range(n_element):
            xyz = cpy_dist_array.index(tmp[i])
            selected_indices.append(xyz)
            cpy_dist_array[xyz] = 0

        return selected_indices

    def crossover_operation(self, mummy, daddy):
        def correct_repeatation(pre_kid1, pre_kid2):
            count1 = 0
            for gen1 in pre_kid1[:index_point]:

                repeat = pre_kid1.count(gen1)
                if repeat > 1:
                    count2 = 0
                    for gen2 in mummy[index_point:]:
                        if gen2 not in pre_kid1:
                            kid1[count1] = mummy[index_point:][count2]
                        count2 += 1
                count1 += 1

            count1 = 0
            for gen1 in pre_kid2[:index_point]:
                repeat = pre_kid2.count(gen1)
                if repeat > 1:
                    count2 = 0
                    for gen2 in daddy[index_point:]:
                        if gen2 not in pre_kid2:
                            kid2[count1] = daddy[index_point:][count2]
                        count2 += 1
                count1 += 1

            return [kid1, kid2]

        index_point = random.randrange(1, self.individuals_length - 1)
        kid1 = mummy[:index_point] + daddy[index_point:]
        kid2 = daddy[:index_point] + mummy[index_point:]

        return correct_repeatation(kid1, kid2)

    def do_crossover(self, selected_indices):

        matrix = [[] for i in range(len(self.popultn))]
        tmp_lst = []

        for i in range(0, len(selected_indices), 2):
            xc = self.crossover_operation(
                self.popultn[selected_indices[i]],
                self.popultn[selected_indices[i + 1]])
            matrix[i] = xc[0]
            matrix[i + 1] = xc[1]
        rt = []
        for i in range(len(self.popultn)):
            if i not in selected_indices:
                rt.append(i)
        for i in range(len(matrix) - len(selected_indices)):
            matrix[i +
                   len(selected_indices)] = self.popultn[selected_indices[i]]

        self.popultn = matrix
        return self.popultn

    def do_mutation(self, population):

        first_no = random.randint(0, len(x.popultn[0]) - 1)
        second_no = random.randint(0, len(x.popultn[0]) - 1)

        for i in range(len(population) // 10 * 8):
            tmp_num = population[i][second_no]
            population[i][second_no] = population[i][first_no]
            population[i][first_no] = tmp_num

        first_no = random.randint(0, len(x.popultn[0]) - 1)
        second_no = random.randint(0, len(x.popultn[0]) - 1)
        for i in range(len(population) // 10 * 8):
            tmp_num = population[i][second_no]
            population[i][second_no] = population[i][first_no]
            population[i][first_no] = tmp_num

        self.popultn = population
        return population


print('\nEnter file name:')
#print('For example: djibouti.txt')
file_name = input()

pop_sizee = 100

starting_city_index = print('\nEnter starting city:')
starting_city_index = int(input())

print("\nCalculating Shortest Path... ")
# x = TSP('djibouti.txt', 3, 40)

x = TSP(file_name, starting_city_index, pop_sizee)

population = x.generate_initial_population()

result_distances = []
result_population = []

for i in range(100):
    distances = x.eval_function(x.popultn)

    print(min(distances))
    result_population.append(x.popultn[distances.index(min(distances))])
    result_distances.append(min(distances))
    dd = x.do_selection(distances, pop_sizee // 10 * 8)
    aa = x.do_crossover(dd)

    x.popultn = x.do_mutation(x.popultn)

print("\nShortest distances is : ")
print((min(result_distances)))
print("\nResult Path is : ")
print(result_population[result_distances.index(min(result_distances))])

plt.plot(result_distances)
plt.title('Length of the shortest path for {} , Population Size = 100'.format(x.filename))
plt.xlabel('Number of generations')
plt.show()
#plt.savefig('Djibouti.png')

