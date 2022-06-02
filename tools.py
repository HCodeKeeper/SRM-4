from scipy.misc import derivative



def SLARkoefs(f_list, i, h):
    lst = [h/6, 2 * h / 3, h / 6,
           (f_list[i+1] - f_list[i]) / h - (f_list[i] - f_list[i-1]) / h
           ]
    if i == 1 or i == 3:
        lst[i-1] = 0
    return lst


def q_koefs(f_list, i, h):
    lst = []
    part = SLARkoefs(f_list, i, h)
    if i == 1:
        lst.append( (-part[2]) / part[1] )
        lst.append( part[3] /  part[1] )
        return lst
    recursive_part = q_koefs(f_list, i - 1, h)
    lst.append(
        (-part[2]) / (part[1] + part[0] * recursive_part[0])
    )
    lst.append(
        (part[3] - part[0] * recursive_part[1]) / (part[1] + part[0] * recursive_part[0])
    )
    return lst


def calculate_q(f_list, h):
    q_list = [0 for _ in f_list]
    for i in range(len(q_list)-2, 0, -1): #qn = q0= 0
        part = q_koefs(f_list, i, h)
        q_list[i] = q_list[i+1] * part[0] + part[1]
    return q_list


def spline(x_list, f_list, q_list, h):
    s_list = [0, 0, 0, 0]
    for i in range(len(x_list) - 1):
        _part1 = lambda x: q_list[i] * ( x_list[i+1] - x) ** 3
        _part2 = lambda x: q_list[i+1] * (x - x_list[i]) ** 3
        half1 = lambda x: _part1(x) / (h * 6) + _part2(x) / (h * 6)

        part1 = lambda x: (f_list[i] / h - (q_list[i] * h / 6)) * (x_list[i+1] - x)
        part2 = lambda x: (f_list[i+1] / h - (q_list[i+1] * h / 6)) * (x - x_list[i])
        half2 = lambda x: part1(x) + part2(x)

        s_list[i] = lambda x: half1(x) + half2(x)
        #print(f"({q_list[i]} * ( {x_list[i+1]} - x) ** 3) /{h*6} + ({q_list[i+1]} * (x - {x_list[i]}) ** 3) / {h*6}      + ({(f_list[i] / h - (q_list[i] * h / 6))} * ({x_list[i+1]} - x) + {(f_list[i + 1] / h - (q_list[i + 1] * h / 6))} * (x - {x_list[i]}))")

    return s_list


def check(x, func):
    results = []
    results.append(func(x))
    results.append(derivative(func, x))
    results.append(derivative(func, x, n=2))
    return results
