from prettytable import PrettyTable
table_of_results = PrettyTable()
table_of_results1 = PrettyTable()
table_of_results.field_names = ['number_test', 'x_python', 'e', 'x', 'delta', 'k']
table_of_results1.field_names = ['number_test', 'size_matrix', 'E', 'x_python', 'e', 'x', 'delta', 'k']

def check_diagonal_dominance(arr, n):
    '''Проверяет матрицу на диагональное преобладание'''
    flag = True
    for i in range(n):
       sum = 0
       for j in range(n):
           if i != j:
               sum += abs(arr[i][j])
       if abs(arr[i][i]) - sum <= 0:             # выбрал диагональное преобладание величины 1
           flag = False
    return flag

def matrix_transposition(a, n):
    '''Транспонирование матрицы'''
    arr = []
    for i in range(n):
        arr.append([])
        for j in range(n):
            arr[i].append(a[j][i])
    return arr

def dot_matrix(a, b, n):
    '''Умножение матриц'''
    c = []
    for i in range(n):
        c.append([])
        for j in range(n):
            sum = 0
            for k in range(n):
                sum += a[i][k] * b[k][j]
            c[i].append(sum)
    return c

def stopping_criterion(A, x0, b, n, e):
    '''Проверяет критерий остановки'''
    a = []
    norm1, norm2, norm3 = 0, 0, 0
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += A[i][j]*x0[j]
        sum -= b[i]
        a.append(abs(sum))
    for i in range(n):
        norm1 += a[i]
        norm2 += a[i]*a[i]
    norm2 = norm2**(1/2)
    norm3 = max(a)

    if min(norm1, norm2, norm3) <= e:
        return True
    else:
        return False

def seidel_method(arr, b0, n, e):
    # проверка на диагональное преобладание
    if check_diagonal_dominance(arr, n):
        A = arr.copy()
        b = b0.copy()
    else:
        arr_t = matrix_transposition(arr, n)
        A = dot_matrix(arr_t, arr, n)
        b = []
        for i in range(n):
            sum = 0
            for j in range(n):
                sum += arr_t[i][j]*b0[j]
            b.append(sum)

    C = []      # построение матрицы С
    for i in range(n):
        C.append([])
        for j in range(n):
            if i!=j:
                C[i].append(-A[i][j]/A[i][i])
            else:
                C[i].append(0)

    d = []      # построение свободного вектора d
    for i in range(n):
        d.append(b[i]/A[i][i])

    x = [d]
    k = 0
    while True:
        x0 = []
        for i in range(n):
            sum = 0
            for j in range(n):
                if len(x0)<j+1:
                    sum += C[i][j]*x[k][j]
                else:
                    sum += C[i][j]*x0[j]
            sum += d[i]
            x0.append(round(sum,6))

        x.append(x0)
        k+=1

        if stopping_criterion(A, x0, b, n, e):
            break

    return (x[k], k)

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
    x = seidel_method(arr[i], b[i], 3, 0.001)
    norm_x = 0
    norm_x_python = 0
    for j in range(3):
        norm_x += abs(x[0][j])
        norm_x_python += abs(ans_python[i][j])
    table_of_results.add_row([i, ans_python[i], 0.01, x[0], abs(norm_x - norm_x_python), x[1]])

print(table_of_results)

for i in range(3):
    for j in range(2):
        n = i + 4
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
        b = [-1 for _ in range(n - 1)]
        b.append(1)
        # вычисление плохо обусловленной матрицы для размерности n x n
        for i1 in range(n):
            arr_big.append([])
            for j1 in range(n):
                if i1 == j1:
                    arr_big[i1].append(1 + 11 * E)
                elif i1 > j1:
                    arr_big[i1].append(11 * E)
                else:
                    arr_big[i1].append(-1 - 11 * E)
        x = seidel_method(arr_big, b, n, 0.00001)
        norm_x = 0
        norm_x_python = 0
        for j in range(n):
            norm_x += abs(x[0][j])
            norm_x_python += abs(ans1_python[j])
        table_of_results1.add_row([5, n, E, ans1_python, 0.01, x[0], abs(norm_x - norm_x_python), x[1]])

print(table_of_results1)