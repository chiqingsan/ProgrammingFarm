def getDictValue(dict):
    value = []
    for key in dict:
        value.append(dict[key])
    return value


# 世界坐标 (x,y) -> grid 下标 (row,col)
# 你的世界：y 向上
# grid 存储：row 0 在最上面
def world_to_grid_index(n, x, y):
    row = n - 1 - y
    col = x
    return row, col


# 计算二维前缀和（按“世界坐标”来建表）
# ps 的尺寸是 (n+1) x (n+1)
# ps[y+1][x+1] = 世界坐标从 (0,0) 到 (x,y) 这个矩形内 “其他点” 的数量
def build_prefix_occupied(grid, landing):
    n = len(grid)
    lx = landing[0]  # 世界坐标 x
    ly = landing[1]  # 世界坐标 y

    # 创建 (n+1) x (n+1) 的 0 表
    ps = []
    i = 0
    while i < n + 1:
        row = []
        j = 0
        while j < n + 1:
            row.append(0)
            j = j + 1
        ps.append(row)
        i = i + 1

    # 填充前缀和
    # 注意：这里 i 表示世界坐标 y（从下到上 0..n-1）
    y = 0
    while y < n:
        row_sum = 0
        x = 0
        while x < n:
            # 取出世界坐标 (x,y) 对应的 grid 单元
            row_idx, col_idx = world_to_grid_index(n, x, y)
            cell = grid[row_idx][col_idx]

            # 其他点：不是 None 且不是落点
            is_other = False
            if cell != None:
                if not (x == lx and y == ly):
                    is_other = True

            if is_other:
                row_sum = row_sum + 1

            # ps 是按 [y+1][x+1] 组织的
            ps[y + 1][x + 1] = ps[y][x + 1] + row_sum

            x = x + 1
        y = y + 1

    return ps


# 查询正方形区域内 “其他点”的数量
# 区域是世界坐标下：
# x ∈ [start_x, start_x + size)
# y ∈ [start_y, start_y + size)
def rect_sum(ps, start_x, start_y, size):
    bottom = start_y
    top = start_y + size
    left = start_x
    right = start_x + size

    return ps[top][right] - ps[bottom][right] - ps[top][left] + ps[bottom][left]


# 从大到小找一个包含 landing 的合法 k*k 区域
# 返回 (start_x, start_y, size)（世界坐标：区域左下角 + 边长）
# 找不到返回 None
def find_square_region(grid, landing, max_size=6):
    n = len(grid)
    x = landing[0]  # 世界坐标 x
    y = landing[1]  # 世界坐标 y

    ps = build_prefix_occupied(grid, landing)

    k = max_size
    if k > n:
        k = n

    while k >= 1:
        # 区域左下角 (start_x,start_y) 必须保证 landing 在区域内：
        # start_x <= x <= start_x + k - 1
        # start_y <= y <= start_y + k - 1

        start_x_min = x - k + 1
        if start_x_min < 0:
            start_x_min = 0
        start_x_max = x
        if start_x_max > n - k:
            start_x_max = n - k

        start_y_min = y - k + 1
        if start_y_min < 0:
            start_y_min = 0
        start_y_max = y
        if start_y_max > n - k:
            start_y_max = n - k

        candidates = []

        start_y = start_y_min
        while start_y <= start_y_max:
            start_x = start_x_min
            while start_x <= start_x_max:
                # 区域内没有“其他点”才算合法
                if rect_sum(ps, start_x, start_y, k) == 0:
                    candidates.append((start_x, start_y, k))
                start_x = start_x + 1
            start_y = start_y + 1

        if len(candidates) > 0:
            return random_elem(candidates)

        k = k - 1

    return None


def random_elem(lst):
    index = random() * len(lst) // 1
    return lst[index]


def _always_true():
    return True


def fill_plan_farm_with_pumpkin(plan_farm, region):
    # region 是 find_square_region 的返回值
    # 形式：(start_x, start_y, size)
    if region == None:
        return False

    start_x = region[0]
    start_y = region[1]
    size = region[2]

    y = start_y
    while y < start_y + size:
        x = start_x
        while x < start_x + size:
            plan_farm[y][x] = Entities.Pumpkin
            x = x + 1
        y = y + 1

    return True


# def getFram(n=10):
#     farm = []
#     world_size = get_world_size()
#     for i in range(n):  # 循环创建每一行
#         row = []  # 2. 为每一行创建一个空的列表
#         for j in range(n):  # 循环填充这一行的每一列
#             if random() < 0.3:
#                 row.append(Entities.Grass)
#             else:
#                 row.append(None)  # 3. 把元素添加到行列表的末尾
#         farm.append(row)  # 4. 把填充好的行添加到 farm 列表的末尾
#     return farm

# print(find_square_region(getFram(), (3,3), 6))
