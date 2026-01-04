def get_dict_value(dict):
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
        for _ in range(dx):
            move(East)
    elif dx < 0:
        for _ in range(-dx):
            move(West)

    # ---------- Y 轴 ----------
    dy = y - now_y

    if dy > half:
        dy = dy - world_size
    elif dy < -half:
        dy = dy + world_size

    if dy > 0:
        for _ in range(dy):
            move(North)
    elif dy < 0:
        for _ in range(-dy):
            move(South)

# 等待所有无人机工作完成
def wait_drones_done():
    while num_drones() != 1:
        do_a_flip()


# 朝着一个方向释放无人机执行任务
def do_spawn_drone(work_func, direction=North, start_xy=(0, 0)):
    _max_drones = num_drones()
    world_size = get_world_size()
    goto_xy(start_xy[0], start_xy[1])
    handle_list = []
    for _ in range(world_size):
        if num_drones() < _max_drones:
            # 无人机没有满, 尝试 spawn 一个
            handle_list.append(spawn_drone(work_func))
        elif _ == (world_size - 1):
            handle_list.append(work_func())
        else:
            handle = spawn_drone(work_func)
            while not handle:
                do_a_flip()
                handle = spawn_drone(work_func)
            handle_list.append(handle)
        move(direction)
    return handle_list

# 解析句柄里结果
def get_drone_handle_result(handle_list):
    result = []
    # 解析句柄里结果
    for i in handle_list:
        if i != None and ("<drone " in str(i)):
            result.append(wait_for(i))
        else:
            result.append(i)
    return result
