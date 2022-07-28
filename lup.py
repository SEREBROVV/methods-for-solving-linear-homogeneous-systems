from prettytable import PrettyTable
table_of_results = PrettyTable()
table_of_results1 = PrettyTable()
table_of_results.field_names = ['number_test', 'x_python', 'e', 'x', 'delta']
table_of_results1.field_names = ['number_test', 'size_matrix', 'E', 'x_python', 'e', 'x', 'delta']

def answer_lup(b, l, u, p, n):
    b_new = [0 for i in range(n)]

    for i in range(n):
        '''Преобразовываем b с помощью матрицы перестановок'''
        sum = 0
        for j in range(n):
            sum += p[i][j]*b[j]
        b_new[i] = sum

    y = []
    for i in range(n):
        '''Считаем y'''
        sum = 0
        for j in range(i):
            sum += l[i][j]*y[j]
        y.append((b_new[i] - sum)/l[i][i])        # обязательно ли делить?

    x = [0 for i in range(n)]

    for i in range(n-1,-1,-1):
        '''Считаем вектор-ответ'''
        sum = 0
        for j in range(i, n):
            sum += u[i][j]*x[j]
        x[i] = round(((y[i] - sum)/u[i][i]), 6)

    return x

def lup(arr, b, n):
    p = []
    for i in range(n):
        p.append([])
        for j in range(n):
            p[i].append(0)
        p[i][i] = 1
    for i in range(n):

        a_i_max = abs(arr[i][i])
        h = i

        for j in range(i, n):
            '''Находим ведущий элемент'''
            if abs(arr[j][i]) > a_i_max:
                a_i_max = abs(arr[j][i])
                h = j
        '''Переставляем i-ю строку со сторой, к которой нашли ведущий элемент'''
        arr[i], arr[h] = arr[h], arr[i]
        p[i], p[h] = p[h], p[i]

        for j in range(i+1, n):
            '''Преобразовываем матрицу'''
            arr[j][i] = arr[j][i]/arr[i][i]
            for k in range(i+1, n):
                arr[j][k] -= arr[j][i]*arr[i][k]

    for i in range(n):
        '''Находим L + U'''
        arr[i][i] += 1

    l = []
    u = []
    for i in range(n):
        l.append([])
        u.append([])
        for j in range(n):
            l[i].append(0)
            u[i].append(0)

    for i in range(n):
        '''Находим L'''
        l[i][i] = 1
        for j in range(i):
            l[i][j] = arr[i][j]
    for i in range(n):
        '''Находим U'''
        for j in range(n):
            u[i][j] = arr[i][j] - l[i][j]

    return answer_lup(b, l, u, p, n)

arr = [[[0,2,3], [1,2,4], [4,5,6]],
       [[13,1,1],[1,15,1],[1,1,17]],
       [[-13,1,1],[1,-15,1],[1,1,-17]],
       [[-13,14,15],[16,-15,12],[15,16,-17]],
       [[13,12,12],[12,15,12],[12,12,17]]]
b = [[13,17,32],
     [15,17,19],
     [-15,-17,-19],
     [15,17,19],
     [15,17,19]]
ans_python = [[1.0,2.0,3.0],
              [1.0,1.0,1.0],
              [1.352509,1.308445,1.274173],
              [1.299748,1.118830,1.082206],
              [-0.134020,0.621993,0.773195]]
for i in range(5):
    x = lup(arr[i], b[i], 3)
    norm_x = 0
    norm_x_python = 0
    for j in range(3):
        norm_x += abs(x[j])
        norm_x_python += abs(ans_python[i][j])
    table_of_results.add_row([i, ans_python[i], 0.01, x, abs(norm_x-norm_x_python)])

print(table_of_results)

for i in range(3):
    for j in range(2):
        n = i+4
        # вычисление E и ответа
        if j == 0:
            E = 0.001
            ans1_python = [0 for _ in range(n - 1)]
            ans1_python.append(round((1000 / 1011), 6))
        else:
            E = 0.000001
            ans1_python = [0 for _ in range(n - 1)]
            ans1_python.append(round((1000000 / 1000011), 6))
        arr_big = []
        b = [-1 for _ in range(n-1)]
        b.append(1)
        # вычисление плохо обусловленной матрицы для размерности n x n
        for i1 in range(n):
            arr_big.append([])
            for j1 in range(n):
                if i1 == j1:
                    arr_big[i1].append(1+11*E)
                elif i1 > j1:
                    arr_big[i1].append(11*E)
                else:
                    arr_big[i1].append(-1-11*E)
        x = lup(arr_big, b, n)
        norm_x = 0
        norm_x_python = 0
        for j in range(n):
            norm_x += abs(x[j])
            norm_x_python += abs(ans1_python[j])
        table_of_results1.add_row([5, n, E, ans1_python, 0.01, x, abs(norm_x - norm_x_python)])

print(table_of_results1)