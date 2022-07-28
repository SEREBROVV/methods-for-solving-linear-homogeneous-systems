from prettytable import PrettyTable
table_of_results = PrettyTable()
table_of_results1 = PrettyTable()
table_of_results.field_names = ['number_test', 'x_python', 'e', 'x', 'delta']
table_of_results1.field_names = ['number_test', 'size_matrix', 'E', 'x_python', 'e', 'x', 'delta']

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

def w_count(y, z, k):
    '''Считает w'''
    alpha = 0
    for i in range(k):
        alpha += y[i] * y[i]
    alpha = (alpha) ** (1 / 2)

    # считаем p1
    p = 0
    for i in range(k):
        p += (y[i] - alpha * z[i]) * (y[i] - alpha * z[i])
    p = (p) ** (1 / 2)

    # считаем w1
    w = []
    for i in range(k):
        w.append((y[i] - alpha * z[i]) / p)

    return w

def w_wT(w, k):
    '''Считаем выражение -2*w*wT'''
    w_wt = []
    for i in range(k):
        w_wt.append([])
        for j in range(k):
            w_wt[i].append((-2) * w[i] * w[j])
    return w_wt

def q_count(w, k):
    '''Считает Q'''
    E = []
    w_wt = w_wT(w, k)
    for i in range(k):
        E.append([])
        for j in range(k):
            E[i].append(0)
        E[i][i] = 1

    Q = []
    for i in range(k):
        Q.append([])
        for j in range(k):
            Q[i].append(E[i][j] + w_wt[i][j])

    return Q

def get_answer(q, r, b, n):
    y = []
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += q[j][i] * b[j]
        y.append(sum)
    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        '''Считаем вектор-ответ'''
        sum = 0
        for j in range(i, n):
            sum += r[i][j] * x[j]
        x[i] = round(((y[i] - sum) / r[i][i]),6)

    return x

def qr(arr,b,n):
    q = []
    r = [arr]
    q0 = []
    for i in range(n):
        q0.append([])
        for j in range(n):
            q0[i].append(0)
        q0[i][i] = 1
    q.append(q0)

    for iter_num in range(n-1):
        y = []
        k = n-iter_num
        if iter_num == 0:
            for i in range(k):
                y.append(r[iter_num][i][0])
        else:
            for i in range(1, k+1):
                y.append(r[iter_num][i][1])
        z = [1]
        for i in range(n-iter_num-1):
            z.append(0)

        w = w_count(y, z, n-iter_num)
        q_iter_num = q_count(w, k)
        q_help = []
        r_help = []
        if iter_num == 0:
            r_help = r[iter_num]
            q_help = q_iter_num.copy()
        else:
            for i in range(n):
                q_help.append([])
                for j in range(n):
                    if i < n - len(q_iter_num[0]) or j < n - len(q_iter_num[0]):
                        if i != j:
                            q_help[i].append(0)
                        else:
                            q_help[i].append(1)
                    else:
                        q_help[i].append(q_iter_num[n - i - k][n - j - k])
            for i in range(1, k+1):
                r_help.append([])
                for j in range(1,k+1):
                    r_help[i-1].append(r[iter_num][i][j])

        r_iter_num = dot_matrix(q_iter_num, r_help, n-iter_num)
        q.append(q_help)
        r.append(r_iter_num)

    for i in range(len(q)-2):
        q[i+1] = dot_matrix(q[i], q[i+1], n)

    q_ans = dot_matrix(q[len(q)-2], q[len(q)-1], n)

    r_ans = []
    for i in range(n):
        r_ans.append([])
        for j in range(n):
            r_ans[i].append(-1000)

    for k in range(1, n):
        for i in range(len(r[k][0])):
            for j in range(len(r[k][0])):
                r_ans[i+k-1][j+k-1] = r[k][i][j]

    x = get_answer(q_ans, r_ans, b, n)
    return x

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
    x = qr(arr[i], b[i], 3)
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
        x = qr(arr_big, b, n)
        norm_x = 0
        norm_x_python = 0
        for j in range(n):
            norm_x += abs(x[j])
            norm_x_python += abs(ans1_python[j])
        table_of_results1.add_row([5, n, E, ans1_python, 0.01, x, abs(norm_x - norm_x_python)])

print(table_of_results1)