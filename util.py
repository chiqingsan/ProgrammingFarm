def getDictValue(dict):
    value = []
    for key in dict:
        value.append(dict[key])
    return value



def random_elem(lst):
    index = random() * len(lst) // 1
    return lst[index]

def _always_true():
    return True


# 移动到世界坐标 (x,y)
def goto_xy(x,y):
    now_x, now_y = get_pos_x(), get_pos_y()
    world_size = get_world_size()
    half = world_size // 2

    # ---------- X 轴 ----------
    dx = x - now_x

    # 映射到最短环形距离
    if dx > half:
        dx = dx - world_size
    elif dx < -half:
        dx = dx + world_size

    # 按方向移动
    if dx > 0:
        i = 0
        while i < dx:
            move(East)
            i = i + 1
    elif dx < 0:
        i = 0
        while i < -dx:
            move(West)
            i = i + 1

    # ---------- Y 轴 ----------
    dy = y - now_y

    if dy > half:
        dy = dy - world_size
    elif dy < -half:
        dy = dy + world_size

    if dy > 0:
        i = 0
        while i < dy:
            move(North)
            i = i + 1
    elif dy < 0:
        i = 0
        while i < -dy:
            move(South)
            i = i + 1
