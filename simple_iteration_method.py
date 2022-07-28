from prettytable import PrettyTable
table_of_results = PrettyTable()
table_of_results1 = PrettyTable()
table_of_results.field_names = ['number_test', 'x_python', 'e', 'x', 'delta', 'k']
table_of_results1.field_names = ['number_test', 'size_matrix', 'E', 'x_python', 'e', 'x', 'delta', 'k']

def matrix_b(arr, m, n):
    '''Вычисление матрицы B'''
    B = []
    for i in range(n):
        B.append([])
        for j in range(n):
            B[i].append((-m) * arr[i][j])
        B[i][i] += 1
    return B

def check_norm(B, n):
    '''Вычисление трёх норм'''
    norm1 = 0
    norm2 = 0
    norm3 = 0
    # первая норма
    max_el1 = []
    for j in range(n):
        sum = 0
        for i in range(n):
                sum += abs(B[i][j])
        max_el1.append(sum)
    norm1 = max(max_el1)
    #норма фрабениуса
    for i in range(n):
        for j in range(n):
            norm2 += B[i][j]*B[i][j]
    norm2 = norm2**(1/2)
    # бесконечная норма
    max_el3 = []
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += abs(B[i][j])
        max_el3.append(sum)
    norm3 = max(max_el3)
    return min([norm1, norm2, norm3])

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

def norm_difference_vector(x1, x2, n):
    '''Считает норму разницы двух векторов'''
    x = []
    norm1 = 0
    norm2 = 0
    norm3 = 0
    for i in range(n):
        x.append(x1[i]-x2[i])
        x[i] = abs(x[i])
        norm1 += x[i]
        norm2 += x[i]*x[i]
    norm2 = norm2**(1/2)
    norm3 = max(x)
    return min([norm1, norm2, norm3])

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

    if min(norm1, norm2, norm3) < e:
        return True
    else:
        return False

def simple_iteration_method(arr, b, n):
    e = 0.01
    m = 1/check_norm(arr, n)      #мю
    utility_matrix_b = matrix_b(arr, m, n)     # вспомонательная матрица В
    if check_norm(utility_matrix_b, n) >= 1:
        '''Если матрица A была не положительно определённой с начала, меняем её на AtA'''
        b1 = []
        arr_t = matrix_transposition(arr, n)
        # считаем новую матрицу А
        A = dot_matrix(arr_t, arr, n)
        m = 1 / check_norm(A, n)
        # cчитаем вектор b с волной
        for i in range(n):
            sum = 0
            for j in range(n):
                sum += arr_t[i][j]*b[j]
            b1.append(sum)
        # считаем вектор c
        c = []
        for i in range(n):
            c.append(m * b1[i])
        # cчитаем матрицу B
        B = matrix_b(A, m, n)
    else:
        b1 = b.copy()
        A = arr.copy()
        B = utility_matrix_b.copy()
        # считаем новый вектор b (c)
        c = []
        for i in range(n):
            c.append(m * b[i])

    x = [c]     # создаём матрицу, которая будет содержать промежуточные результаты
    k = 0       # счетчик
    norm_b = check_norm(B, n)  # норма матрицы B
    while True:
        x0 = []
        for i in range(n):
            sum = 0
            for j in range(n):
                sum += B[i][j] * x[k][j]
            sum += c[i]
            x0.append(round(sum, 6))
        x.append(x0)
        k += 1
        if stopping_criterion(A, x0, b1, n, e):
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
    x = simple_iteration_method(arr[i], b[i], 3)
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
        x = simple_iteration_method(arr_big, b, n)
        norm_x = 0
        norm_x_python = 0
        for j in range(n):
            norm_x += abs(x[0][j])
            norm_x_python += abs(ans1_python[j])
        table_of_results1.add_row([5, n, E, ans1_python, 0.01, x[0], abs(norm_x - norm_x_python), x[1]])

print(table_of_results1)