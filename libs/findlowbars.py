import numpy as np



# N周期前的M周期内的第T个最小值到当前周期的周期数.
# 用法:FINDLOWBARS(VAR,N,M,T):VAR在N日前的M天内第T个最低价到当前周期的周期数.

#https://raw.githubusercontent.com/jones2000/HQChart/c0d7f75a85e91380d6e396e72ba9bff15776fadc/wechathqchart/umychart.complier.wechat.js
def FINDLOWBARS(data, n, m, t):
    count = len(data)
    result = [10000] * count
    values = [None] * count
    for i in range(count - 1, -1, -1):
        aryValue = []
        for j in range(n, m):
            index = i - j
            if index < 0:
                break
            item = data[index]
            aryValue.append({"Value": item, "Period": j})
        if aryValue:
            aryValue.sort(key=lambda x: x["Value"])
            index = t - 1 if t > 0 else 0
            index = min(index, len(aryValue) - 1)
            result[i] = aryValue[index]["Period"]
            values[i] = aryValue[index]["Value"]
    return result, values

# def FINDLOWBARS(var, n, m, t):
#     # 获取n天前到m天前的数据
#     temp = var[-n-m:-n]

#     # 排序
#     temp2 = sorted(temp)

#     # 获取第t小的值
#     if t <= len(temp2):
#         value = temp2[t-1]

#         # 倒着查找value在原序列中的位置
#         for i in range(len(temp)-1, -1, -1):
#             if temp[i] == value:
#                 m = len(temp) - i + n
#                 return m

#     # 如果没找到返回-1
#     return -1


