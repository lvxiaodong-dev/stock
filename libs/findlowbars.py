import numpy as np

# N周期前的M周期内的第T个最小值到当前周期的周期数.
# 用法:FINDLOWBARS(VAR,N,M,T):VAR在N日前的M天内第T个最低价到当前周期的周期数.
def FINDLOWBARS(var, n, m, t):
    # 获取n天前到m天前的数据
    temp = var[-n:-n+m]

    # 排序
    temp = sorted(temp)

    # 获取第t小的值
    if t <= len(temp):
        value = temp[t-1]

        # 倒着查找value在原序列中的位置
        for i in range(len(var)-1, -1, -1):
            if var[i] == value:
                return len(var) - i

    # 如果没找到返回-1
    return -1