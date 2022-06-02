from tools import *

x_list = [0.2, 0.6, 1, 1.4, 1.8]
func_list = [-2.3026, -0.69315, -0.10536, 0.26236, 0.53063]
h = 0.4
X = 8

qs = calculate_q(func_list, h)
splines = spline(x_list, func_list, qs, h)
print("q: ", *qs)

node2 = x_list[1]
for i in range(2):
    lst = check(node2, splines[i])
    print(str(i+1) + ": S(x) = " + str(lst[0]) + " S'(x) = " + str(lst[1]) + " S''(x) = " + str(lst[2]))
print(f"f(x*) = {splines[3](X)}")
