import numpy as np
import scipy.interpolate as spi
np.seterr(divide='ignore', invalid='ignore')

# 目标提取
def objectExtractionAnalyse(l): # l表示各样本区目标像素点所占比率的列表
    lis = removeZeroAndMultiply(l)
    if len(lis) == 0:
        return 0, 0, 0, 0, 'C'
    aver = sum(lis) / len(lis)
    cover_score = format(aver * 2)
    x = np.matrix(lis).T
    n = x.shape[0]
    x = np.tile(x, (1, 3))
    x = positivization(x, [0, 3, 2], aver, 0.25, 0.45)
    z = standardization(x)
    res = format(np.sum(z, axis=0) / n * 2)
    scale_score = res[0][0]
    accessible_score = res[0][1]
    matching_score = res[0][2]
    s = np.sum(normailzation(z), axis=0) / n * 2
    s = format(s)
    print(s)
    totality_level = evaluate(s[0][0] * 3)
    return cover_score, scale_score, accessible_score, matching_score, totality_level

# 变化检测
def changeDectionAnalyse(l): # l表示各样本区变化区域像素点所占比率的列表
    lis = removeZero(l)
    if len(lis) == 0:
        return 'C', 'C'
    x = np.matrix(lis).T
    n = x.shape[0]
    x = np.tile(x, (1, 2))
    x = positivization(x, [0, 3], 0, 0.3, 0.6)
    z = standardization(x)
    res = format(np.sum(z, axis=0) / n)
    scope = evaluate(res[0][0] * 2)
    strength = evaluate(res[0][1] * 2)
    print(res)
    return scope, strength

# 目标检测
def objectDectionAnalyse(l): # l表示各样本区目标区域框所占比率的列表
    lis = removeZero(l)
    if len(lis) == 0:
        return 0, 0, 0, 'C'
    x = np.matrix(l).T
    n = x.shape[0]
    x = np.tile(x, (1, 3))
    x = positivization(x, [0, 2, 3], 0.5, 0.1, 0.5)
    z = standardization(x)
    res = format(np.sum(z, axis=0) / n * 2)
    amount_score = res[0][0] * 2
    scope_score = res[0][1] * 2
    density_score = res[0][2] * 2
    s = np.sum(normailzation(z), axis=0) / n * 2
    s = format(s)
    rationality = evaluate(s[0][0] * 4)
    return amount_score, scope_score, density_score, rationality

# 地物分类
def classifictionAnalyse(l1, l2, l3): #l1，l2，l3，分别为建筑、道路、林地覆盖率的列表
    lis1 = removeZero(l1)
    lis2 = removeZero(l2)
    lis3 = removeZero(l3)
    if len(lis1) == 0 or len(lis2) == 0 or len(lis3) == 0:
        return 'C', 'C'
    l1 = np.sum([l1, l2, l3], axis=0)
    x1 = np.matrix(l1).T
    n = x1.shape[0]
    x1 = positivization(x1, [0], 0, 0, 0)
    z1 = standardization(x1)
    res1 = format(np.sum(z1, axis=0) / n)
    avaiabity = evaluate(res1[0][0] * 4)
    l2 = np.sum([l1, l2, l3], axis=1)
    x2 = np.matrix(l2)
    x2 = positivization(x2, [2], 0.33, 0, 0)
    z2 = standardization(x2)
    z2 = np.sum(z2, axis=1) / 3
    res2 = format(np.sum(z2, axis=0) / n)
    rationality = evaluate(res2[0][0])
    return rationality, avaiabity

# 正向化
def positivization(x, l, best, a, b):
    for index, type in enumerate(l):    # type：0表示不用正向化，1表示极小型指标正向化，2表示中间型指标正向化，3表示区间型指标正向化
        if type == 1:
           x[:, index] = minPositivization(x[:, index])
        elif type == 2:
            x[:, index] = midPositivision(x[:, index], best)
        elif type == 3:
            x[:, index] = interPosition(x[:, index], a, b)
    return x

# 标准化
def standardization(x):
    n = x.shape[0]  # 行
    z = np.divide(x, np.tile(np.power(np.sum(np.multiply(x, x), axis=0), 0.5), (n, 1)))
    return z

# 归一化
def normailzation(z):
    n = z.shape[0]  # 行
    z_max = np.max(z, axis=0)   # 列最大值
    z_min = np.min(z, axis=0)   # 列最小值
    d_max = np.power(np.sum(np.power(np.tile(z_max, (n, 1)) - z, 2), axis=1), 0.5)
    d_min = np.power(np.sum(np.power(np.tile(z_min, (n, 1)) - z, 2), axis=1), 0.5)
    s = np.divide(d_min, d_max + d_min)
    s = np.divide(s, np.sum(s, axis=0))
    return s

# 极小型指标正向化
def minPositivization(x):
    posit_x = np.max(x, axis=0) - x
    return posit_x

# 中间型指标正向化
def midPositivision(x, best):
    M = np.max(abs(x - best), axis=0)
    posit_x = 1 - abs(x - best) / M
    return posit_x

# 区间型指标正向化
def interPosition(x, a, b):
    n = x.shape[0]
    m = max((a - np.min(x, axis=0)), (np.max(x, axis=0) - b))
    posit_x = np.zeros((n, 1))
    for i in range(n):
        if (x[i] < a):
            posit_x[i] = 1 - np.divide((a - x[i]), m)
        elif (x[i] > b):
            posit_x[i] = 1 - np.divide((x[i] - b), m)
        else:
            posit_x[i] = 1
    return  posit_x

# 格式化
def format(s):
    s = np.around(s * 10, decimals=3)
    return s

# 评分
def evaluate(score):
    if score < 3:
        return 'C'
    elif 3 <= score and score < 6:
        return 'B'
    else:
        return 'A'

def removeZero(l):
    lis = []
    for i in l:
        if i != 0:
            lis.append(i)
    return lis

def removeZeroAndMultiply(l):
    lis = []
    for i in l:
        if i != 0:
            lis.append(i * 10)
    return lis

# 计算前后变化率，c为变化率
def getBeforeAndAfter(c):
    # 数据
    l = []
    l.append(0)
    l.append(c)
    l.append(1)
    X = np.arange(0, 1.5, 0.5)  # 样本点X
    Y = np.array(l)  # 样本点Y
    new_x = np.arange(0, 1.5, 0.1)  # 插值点
    # 二次样条插值
    ipo2 = spi.splrep(X, Y, k=2)
    iy2 = spi.splev(new_x, ipo2)
    # 前后变化率
    c1 = np.around(iy2[4], decimals=3)
    c2 = np.around(iy2[6], decimals=3)
    return c1, c2