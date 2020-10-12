import fractions
frac = fractions.Fraction

def solve_matrix(matrix):
    #number of rows
    n = len(matrix)
    #number of columns (including b column)
    m = len(matrix[0])
    
    def subtract_rows(matrix, n1, n2, nproduct, pivot):
        N = pivot[0]
        M = pivot[1]
        C = matrix[N][M] / matrix[N - 1][M]
        for i in range(m):
            matrix[nproduct][i] = matrix[n1][i] * C - matrix[n2][i]
        return matrix
    
    def reduce_leading_entries(matrix, n):
        M = 0
        while matrix[n][M] == 0:
            if M == m - 2:
                return matrix
            M += 1
        divisor = matrix[n][M]
        for y in range(m):
            matrix[n][y] = matrix[n][y] / divisor
        return matrix
    
    def find_leading_entries(matrix):
        def find_pivot(row):
            for i in range(len(row)):
                if row[i] == 1:
                    return i
            return None
        columns = set([])
        pivots = set([])
        for i in range(len(matrix)):
            pivot = find_pivot(matrix[i])
            if pivot != None:
                columns.add(pivot)
                pivots.add((i, pivot))
        return (columns, pivots)


    def compare(row1, row2):
        i = 0
        while i != m - 1:
            if row1[i] == 0 and row2[i] == 1:
                return False
            elif row2[i] == 0 and row1[i] == 1:
                return True
            i += 1
        if row1[0] == row2[0]:
            return True
        elif row2[0] == 0:
            return False
        elif row1[0] == 0:
            return True
        else:
            raise AssertionError('bro')
    
    def sort_rows(matrix):
        i = 0
        while i != n - 1:
            if compare(matrix[i], matrix[i + 1]):
                i += 1
            else:
                temp = matrix[i]
                matrix[i] = matrix[i + 1]
                matrix[i + 1] = temp
                i = 0
        return matrix
    
    '''I was tired of coding so I used a bad solution where
    h reduces matrix to echelon form, and h2 reduces it to
    reduced echelon form. Very inefficient.'''
    def h(matrix, N, M):
        element1 = matrix[N][M]
        if N != n - 1:
            element2 = matrix[N + 1][M]
        else:
            element2 = False
        if N == n - 1 and M == m - 2:
            #done
            return matrix
        elif element1 == 1 and element2 == 1:
            #row operation
            if compare(matrix[N], matrix[N + 1]):
                earlier = N + 1
                later = N
                matrix = subtract_rows(matrix, later, earlier, N, (N + 1, M))
                matrix = reduce_leading_entries(matrix, N + 1)
                matrix = reduce_leading_entries(matrix, N)
                matrix = sort_rows(matrix)
            else:
                earlier = N
                later = N + 1
                matrix = subtract_rows(matrix, later, earlier, N + 1, (N + 1, M))
                matrix = reduce_leading_entries(matrix, N + 1)
                matrix = reduce_leading_entries(matrix, N)
                matrix = sort_rows(matrix)
            return h(matrix, 0, 0)
        elif M == m - 2:
            #move down
            return h(matrix, N + 1, 0)
        else:
            #move right
            if M == m - 2:
                return h(matrix, N + 1, 0)
            else: return h(matrix, N, M + 1)

    def h2(matrix, N, M):
        stuff = find_leading_entries(matrix)
        pivots = stuff[1]
        columns = stuff[0]
        element1 = matrix[N][M]
        if N == n - 1 and M == m - 2:
            #done
            return matrix
        elif {M}.issubset(columns) and element1 != 0 and not {(N, M)}.issubset(pivots):
            #row operation
            if compare(matrix[N], matrix[N + 1]):
                earlier = N + 1
                later = N
                matrix = subtract_rows(matrix, later, earlier, N, (N + 1, M))
                matrix = reduce_leading_entries(matrix, N + 1)
                matrix = reduce_leading_entries(matrix, N)
                matrix = sort_rows(matrix)
            else:
                earlier = N
                later = N + 1
                matrix = subtract_rows(matrix, later, earlier, N + 1, (N + 1, M))
                matrix = reduce_leading_entries(matrix, N + 1)
                matrix = reduce_leading_entries(matrix, N)
                matrix = sort_rows(matrix)
            return h2(matrix, 0, 0)
        elif M == m - 2:
            #move down
            return h2(matrix, N + 1, 0)
        else:
            #move right
            if M == m - 2:
                return h2(matrix, N + 1, 0)
            else: return h2(matrix, N, M + 1)
    
    for i in range(len(matrix)):
        matrix = reduce_leading_entries(matrix, i)
    matrix = sort_rows(matrix)
    return h2(h(matrix, 0, 0), 0, 0)


def ask_for_row(number):
    row_string = input('input row ' + str(number) + ' seperated w spaces, if no more rows input "N": ')
    if row_string != 'N':
        row_list = row_string.split(' ')
        for i in range(len(row_list)):
            if row_list[i][0] == '-':
                row_list[i] = -1 * frac(int(row_list[i][1:len(row_list[i])]))
            elif row_list[i] == '0':
                row_list[i] = 0
            else:
                row_list[i] = frac(int(row_list[i]))
        return row_list
    else: return row_string


def make_floats(matrix):
    for i in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix[i][y] = str(matrix[i][y].numerator) + '/' + str(matrix[i][y].denominator)
    return matrix


matrix = []
row = None
count = 1
while row != 'N':
    row = ask_for_row(count)
    count += 1
    matrix.append(row)
matrix.pop()

print('Solving...')
matrix = solve_matrix(matrix)
matrix = make_floats(matrix)
print('reduced echelon form (all values are fractions):')
for i in matrix:
    print(i)
