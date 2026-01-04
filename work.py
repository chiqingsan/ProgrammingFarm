import util
import config


# 尝试种一个胡萝卜, 返回种植结果True/False
def plant_carrot():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Carrot)


# 尝试种一个干草, 返回种植结果True/False
def plant_hay():
    if get_ground_type() == Grounds.Soil:
        till()
    return True


# 尝试种一个灌木, 返回种植结果True/False
def plant_wood():
    if get_ground_type() == Grounds.Soil:
        till()
    return plant(Entities.Bush)


# 尝试种一棵树, 如果位置不符合要求则种灌木, 返回种植结果True/False
def plant_tree():
    x, y = get_pos_x(), get_pos_y()
    if ((x + y) % 2) == 0:
        return plant(Entities.Tree)
    else:
        if get_ground_type() == Grounds.Soil:
            till()
        return plant(Entities.Bush)


# 尝试种一个向日葵, 返回种植结果True/False
def plant_sunflower():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Sunflower)


# 尝试种一个南瓜, 返回种植结果True/False
def plant_pumpkin():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Pumpkin)


# 尝试种一个仙人掌, 返回种植结果True/False
def plant_cactus():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Cactus)

# 根据输入参数来种植对应的植物, 返回种植结果True/False
def plant_entities(entity_type):
    if entity_type == Entities.Bush:
        return plant_wood()
    elif entity_type == Entities.Tree:
        return plant_tree()
    elif entity_type == Entities.Carrot:
        return plant_carrot()
    elif entity_type == Entities.Sunflower:
        return plant_sunflower()
    elif entity_type == Entities.Pumpkin:
        return plant_pumpkin()
    elif entity_type == Entities.Cactus:
        return plant_cactus()
    else:
        return plant_hay()


# 浇水
def water_plant():
    if get_water() < 0.6 and num_items(Items.Water):
        use_item(Items.Water)
        water_plant()

# 施肥
def fertilize_plant():
    if num_items(Items.Fertilizer):
        use_item(Items.Fertilizer)

# 根据配置, 决定是否需要施肥
def try_fertilize_plant():
    if get_entity_type() in config.need_fertilize:
        fertilize_plant()


# 尝试种植常规作物
def try_planting_common_crops():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        try_harvest()

    # 查看当前位置是否已经有计划种植的植物
    if config.plan_farm[x][y] != None:
        if plant_entities(config.plan_farm[x][y]):
            # 混合种植之后, 删掉当前位置的种植计划
            config.plan_farm[x][y] = None
    else:
        if num_items(Items.Hay) < config.Min_Hay:
            plant_hay()
        # 木头不够种树
        elif num_items(Items.Wood) < config.Min_Wood:
            plant_tree()
        # 胡萝卜不够了种胡萝卜
        elif num_items(Items.Carrot) < config.Min_Carrot:
            plant_carrot()
        else:
            # 都够了就随机种一个
            util.random_elem([plant_hay, plant_tree, plant_carrot])()

    # 尝试进行混合种植
    companion = get_companion()
    if companion != None:
        plant_type, (x, y) = companion
        config.plan_farm[x][y] = plant_type

# 多无人机混合种植
def drones_plant_common_crops():
    wrold_size = get_world_size()

    # 种植任务
    def _plant_common_crops():
        plan_farm = dict()
        # 尝试收获
        if get_entity_type() != None:
            try_harvest()

        for i in range(wrold_size):
            if num_items(Items.Hay) < config.Min_Hay:
                plant_hay()
            # 木头不够种树
            elif num_items(Items.Wood) < config.Min_Wood:
                plant_tree()
            # 胡萝卜不够了种胡萝卜
            elif num_items(Items.Carrot) < config.Min_Carrot:
                plant_carrot()
            else:
                # 都够了就随机种一个
                util.random_elem([plant_hay, plant_tree, plant_carrot])()
            
            # 记录偏好作物和位置
            companion = get_companion()
            if companion != None:
                plant_type, (x, y) = companion
                plan_farm[(x,y)] = plant_type
            
            move(East)
        
        for pos in plan_farm:
            util.goto_xy(pos[0], pos[1])
            if get_entity_type() != None:
                try_harvest()
            plant_entities(plan_farm[pos])

    util.do_spawn_drone(_plant_common_crops)




# 尝试种植向日葵
def try_planting_sunflower():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        try_harvest()

    if plant_sunflower():
            config.petals_dict[(x, y)] = measure()
            # 查询是否需要施肥
            try_fertilize_plant()
        


# 种植完向日葵之后尝试以最大收益收获向日葵
def harvest_sunflower_max():
    tmp_petals = dict()  # {花瓣数: [坐标列表]}

    # pos -> petals  转  petals -> [pos...]
    for pos in config.petals_dict:
        petals = config.petals_dict[pos]

        if petals in tmp_petals:
            tmp_petals[petals].append(pos)
        else:
            tmp_petals[petals] = [pos]

    # 15 到 7 倒序遍历
    p = 15
    while p >= 7:
        if p in tmp_petals:
            for pos in tmp_petals[p]:
                util.goto_xy(pos[0], pos[1])
                while not try_harvest():
                    do_a_flip()
        p -= 1

    config.petals_dict = dict()
    util.goto_xy(0, 0)

# 多无人机种植向日葵
def drones_plant_sunflower():
    wrold_size = get_world_size()
    # 种植向日葵任务
    def _plant_sunflower():
        petals_dict = dict()
        for _ in range(wrold_size):
            x, y = get_pos_x(), get_pos_y()
            try_harvest()
            if plant_sunflower():
                petals_dict[(x, y)] = measure()
                # 查询是否需要施肥
                try_fertilize_plant()
            move(East)
        return petals_dict

    # 收获向日葵任务
    def harvest_sunflower(x, y):
        def _harvest_sunflower():
            util.goto_xy(x, y)
            while not try_harvest():
                do_a_flip()

        return _harvest_sunflower

    # 拿到无人机任务执行的句柄
    petals_list = util.get_drone_handle_result(util.do_spawn_drone(_plant_sunflower))
    util.wait_drones_done()

    # 解析句柄里结果
    for i in petals_list:
        for k in i:
            config.petals_dict[k] = i[k]

    tmp_petals = dict()  # {花瓣数: [坐标列表]}

    # pos -> petals  转  petals -> [pos...]
    for pos in config.petals_dict:
        petals = config.petals_dict[pos]

        if petals in tmp_petals:
            tmp_petals[petals].append(pos)
        else:
            tmp_petals[petals] = [pos]

    # 15 到 7 倒序遍历
    p = 15
    while p >= 7:
        if p in tmp_petals:
            for pos in tmp_petals[p]:
                while not spawn_drone(harvest_sunflower(pos[0], pos[1])):
                    do_a_flip()
        util.wait_drones_done()
        p -= 1


# 尝试种植南瓜
def try_planting_pumpkin():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        try_harvest()

    my = y % (6 + 1)
    mx = x % (6 + 1)
    if my == 6 or mx == 6:
        plant_carrot()
    else:
        plant_pumpkin()
        # 查询是否需要施肥
        try_fertilize_plant()


# 尝试收获南瓜, 补种坏掉的南瓜, 直到完好后收获
def try_harvest_pumpkin():
    is_all_good = False
    config.bad_pumpkin_list = []
    util.goto_xy(0, 0)

    # 全图查找一遍坏南瓜
    def tmp_func():
        x, y = get_pos_x(), get_pos_y()
        entity_type = get_entity_type()

        if entity_type == Entities.Dead_Pumpkin or entity_type == None:
            config.bad_pumpkin_list.append((x, y))
            plant_pumpkin()
        elif entity_type == Entities.Pumpkin and not can_harvest():
            # 如果是南瓜, 但是不可以收获, 则说明还没有成熟, 记录下来
            config.bad_pumpkin_list.append((x, y))

    inspection(tmp_func)

    while not is_all_good:
        new_bad_pumpkin_list = []
        for pos in config.bad_pumpkin_list:
            util.goto_xy(pos[0], pos[1])
            entity_type = get_entity_type()
            if entity_type == Entities.Dead_Pumpkin or entity_type == None:
                plant_pumpkin()
                new_bad_pumpkin_list.append(pos)
            elif entity_type == Entities.Pumpkin and not can_harvest():
                new_bad_pumpkin_list.append(pos)

        config.bad_pumpkin_list = new_bad_pumpkin_list
        is_all_good = len(new_bad_pumpkin_list) == 0

    util.goto_xy(0, 0)


# 多无人机种植收获南瓜
def drones_plant_pumpkin():
    world_size = get_world_size()

    # 播种任务, 尝试种植南瓜
    def plant_pumpkin_task():
        for i in range(world_size):
            try_planting_pumpkin()
            move(East)

    # 南瓜补种任务, 补种坏掉的南瓜
    def replant_pumpkin_task():
        replant_list = []
        for i in range(world_size):
            x, y = get_pos_x(), get_pos_y()
            entity_type = get_entity_type()
            if entity_type == Entities.Dead_Pumpkin or entity_type == None:
                replant_list.append((x, y))
                plant_pumpkin()
                # 查询是否需要施肥
                try_fertilize_plant()
            elif entity_type == Entities.Pumpkin and not can_harvest():
                replant_list.append((x, y))
            move(East)
        
        while len(replant_list):
            new_replant_list = []
            for pos in replant_list:
                util.goto_xy(pos[0], pos[1])
                entity_type = get_entity_type()
                if entity_type == Entities.Dead_Pumpkin or entity_type == None:
                    plant_pumpkin()
                    # 查询是否需要施肥
                    try_fertilize_plant()
                    new_replant_list.append(pos)
                elif entity_type == Entities.Pumpkin and not can_harvest():
                    new_replant_list.append(pos)
            replant_list = new_replant_list

    # 先种植南瓜
    util.do_spawn_drone(plant_pumpkin_task)
    # 补种南瓜
    util.do_spawn_drone(replant_pumpkin_task)
    # 等待全部补种完成
    util.wait_drones_done()



# 尝试寻找迷宫中的宝藏
def try_finding_treasure():
    # 不在迷宫里就生成新迷宫
    entity_type = get_entity_type()
    treasure_size = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    if entity_type != Entities.Treasure and entity_type != Entities.Hedge:
        plant(Entities.Bush)
        use_item(Items.Weird_Substance, treasure_size)

    treasure_x, treasure_y = measure()

    directions = [North, East, South, West]
    index = 0

    # 贴墙走到宝藏
    while (get_pos_x(), get_pos_y()) != (treasure_x, treasure_y):
        right = (index + 1) % 4
        if can_move(directions[right]):
            index = right
            move(directions[index])
            continue

        if can_move(directions[index]):
            move(directions[index])
            continue

        left = (index - 1) % 4
        if can_move(directions[left]):
            index = left
            move(directions[index])
            continue

        back = (index + 2) % 4
        index = back
        move(directions[index])

    # 到宝藏 → 收获 → 这一局迷宫结束
    try_harvest()


# 多无人机寻找宝藏(单次迷宫版)
def drones_try_finding_treasure():
    # 不在迷宫里就生成新迷宫
    entity_type = get_entity_type()
    treasure_size = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    if entity_type != Entities.Treasure and entity_type != Entities.Hedge:
        plant(Entities.Bush)
        use_item(Items.Weird_Substance, treasure_size)

    # 检查是否还在迷宫里
    def check_in_maze():
        entity_type = get_entity_type()
        return entity_type == Entities.Treasure or entity_type == Entities.Hedge

    def treasure_finding_task(initial_dir = 0):
        def _treasure_finding_task():
            directions = [North, East, South, West]
            index = initial_dir  # 当前朝向

            # 分支探索
            def spawn_branch(dir_index):
                move(directions[dir_index])
                while not spawn_drone(treasure_finding_task(dir_index)):
                    do_a_flip()
                back = (dir_index + 2) % 4
                move(directions[back])


            while True:
                if not check_in_maze():
                    break

                right = (index + 1) % 4
                left = (index - 1) % 4
                front = index

                move_path = []

                if can_move(directions[right]):
                    move_path.append(right)
                if can_move(directions[front]):
                    move_path.append(front)
                if can_move(directions[left]):
                    spawn_branch(left)

                if len(move_path) == 1:
                    move(directions[move_path[0]])
                    index = move_path[0]
                elif len(move_path) > 1:
                    for i in range(1,len(move_path)):
                        spawn_branch(move_path[i])
                    move(directions[move_path[0]])
                    index = move_path[0]
                elif len(move_path) == 0:
                    break

            if get_entity_type() == Entities.Treasure:
                try_harvest()


        return _treasure_finding_task

    spawn_drone(treasure_finding_task())
    util.wait_drones_done()

    

# 蛇形循环整个农场
def inspection(handle=util._always_true, harvest_begins=util._always_true):
    if (get_pos_x() !=0 or get_pos_y() != 0):
        util.goto_xy(0, 0)

    world_size = get_world_size()
    direction_x = East  # 当前行的横向方向（初始向右）
    direction_y = North  # 竖直方向，向上

    for i in range(world_size):  # 遍历每一行
        # 当前行横向移动 world_size - 1 步
        for j in range(world_size - 1):
            handle()  # 处理当前格子
            move(direction_x)  # 向当前行方向移动一格

        handle()  # 这一行最后一个格子

        # 最后一行处理完就不用再往上走了
        if i < world_size - 1:
            move(direction_y)  # 上移到下一行

            # 下一行把横向方向反过来，实现“蛇形”
            if direction_x == East:
                direction_x = West
            else:
                direction_x = East

    harvest_begins()


# 尝试种植仙人掌
def try_planting_cactus():
    # 尝试收获
    if get_entity_type() != None:
        try_harvest()

    plant_cactus()
    # 查询是否需要施肥
    try_fertilize_plant()


# 对仙人掌进行排序, 并且收获仙人掌
def try_sort_and_harvest_cactus():
    n = get_world_size()

    # ① 逐行冒泡：每行从左到右升序
    for h in range(n):
        for i in range(n):
            util.goto_xy(0, h)
            swapped = False
            for j in range(0, n - i - 1):
                if measure() > measure(East):
                    swap(East)
                    swapped = True
                move(East)
            if not swapped:
                break  # 这一行已经有序，提前结束

    # ② 逐列冒泡：每列从下到上升序
    for w in range(n):
        for i in range(n):
            util.goto_xy(w, 0)
            swapped = False
            for j in range(0, n - i - 1):
                if measure() > measure(North):
                    swap(North)
                    swapped = True
                move(North)
            if not swapped:
                break  # 这一列已经有序，提前结束

    # ③ 回到原点开始连锁收割
    util.goto_xy(0, 0)
    try_harvest()


# 多无人机种植仙人掌
def drones_plant_cactus():
    world_size = get_world_size()

    # 播种任务, 尝试种植仙人掌
    def plant_cactus_task():
        for i in range(world_size):
            try_planting_cactus()
            move(East)

    # 排序任务, 尝试对种植的仙人掌进行排序
    def sort_cactus_task(dir):
        def task():   
            n = get_world_size()
            x, y = get_pos_x(), get_pos_y()
            for i in range(n):
                util.goto_xy(x, y)
                swapped = False
                for j in range(0, n - i - 1):
                    dir_size = measure(dir)
                    if measure() > dir_size:
                        swap(dir)
                        swapped = True
                    move(dir)
                if not swapped:
                    break  # 这一行已经有序，提前结束
        return task

    # 先种植仙人掌
    util.do_spawn_drone(plant_cactus_task)
    # 对横向的仙人掌进行排序
    util.do_spawn_drone(sort_cactus_task(East))
    # 等待横向的仙人掌排序完毕
    util.wait_drones_done()
    # 对纵向的仙人掌进行排序
    util.do_spawn_drone(sort_cactus_task(North), East)
    # 等待纵向的仙人掌排序完毕
    util.wait_drones_done()
    # 尝试收获
    util.goto_xy(0, 0)
    try_harvest()


# 尝试养恐龙来收获骨头
def try_feed_dinosaur():
    if get_entity_type() != None:
        clear()
    
    start_time = get_time()
    def log_fun(start, apple_num):
        # 计算吃一个苹果所需要的平均时间
        time = get_time() - start
        quick_print("本轮贪吃蛇已结束, 所耗时间为(单位: s)：" + str(time))
        quick_print("本轮贪吃蛇已结束, 吃掉的苹果数量为：" + str(apple_num))
        quick_print("本轮贪吃蛇已结束, 吃一个苹果所需的平均时间为(单位: s)：" + str(time/apple_num))
        quick_print("本轮贪吃蛇已结束, 骨头生产效率为(单位: /s)：" + str(apple_num**2 / time))
        quick_print("-------------------------------------------------------------------")

    # 先保证世界的大小为偶数
    world_size = get_world_size()
    if world_size % 2 != 0:
        world_size -= 1
        set_world_size(world_size)

    # 选择一个新的方向进行移动；若四个方向都走不动，返回 None
    def try_safe_step():
        path = []

        if can_move(West):
            path.append(West)
        if can_move(North):
            path.append(North)
        if can_move(East):
            path.append(East)
        if can_move(South):
            path.append(South)

        if len(path) == 1:
            return move(path[0])
        elif len(path) > 1:
            if (get_pos_x() + get_pos_y()) < world_size:
                if North in path:
                    return move(North)
                elif East in path:
                    return move(East)
                else:
                    return move(path[0])
            else:
                if South in path:
                    return move(South)
                elif West in path:
                    return move(West)
                else:
                    return move(path[0])
        # 四个方向都走不动，说明被包住了
        return None

    # 贪心朝 (tx, ty) 走，返回 True=成功到达，False=中途撞墙/尾巴
    def move_to_target(tx, ty):
        while True:
            x = get_pos_x()
            y = get_pos_y()

            if x == tx and y == ty:
                return True  # 已到目标

            if x < tx:
                if not move(East):
                    return False
            elif x > tx:
                if not move(West):
                    return False
            elif y < ty:
                if not move(North):
                    return False
            elif y > ty:
                if not move(South):
                    return False

    # 蛇形循环, 直到身体铺满整个农场
    def snake_loop(world_size):
        while True:

            direction_x = East  # 水平移动方向
            direction_y = North  # 换行方向（向上）

            # 蛇形遍历每一行，并在最后一行做一段“回到底边”的闭环
            for i in range(world_size):
                # ── 横向移动部分 ──
                if i == 0:
                    # 第一行：水平走 world_size - 1 步
                    j = 0
                    while j < world_size - 1:
                        if not move(direction_x):
                            # 蛇形阶段：一旦走不动，直接收割
                            change_hat(Hats.Green_Hat)
                            return
                        j = j + 1
                else:
                    # 中间行 & 最后一行：先走 world_size - 2 步
                    j = 0
                    while j < world_size - 2:
                        if not move(direction_x):
                            change_hat(Hats.Green_Hat)
                            return

                        # 在最后一行的特定位置额外处理一次：
                        # 再多走一格 + 整列向下，形成闭环
                        if i == world_size - 1 and j == world_size - 3:
                            # 再向当前横向方向多走 1 步
                            if not move(direction_x):
                                change_hat(Hats.Green_Hat)
                                return

                            # 再向下走 world_size - 1 步，回到底行
                            k = 0
                            while k < world_size - 1:
                                if not move(South):
                                    change_hat(Hats.Green_Hat)
                                    return
                                k = k + 1

                        j = j + 1

                # ── 换行部分（从当前行移动到下一行）──
                if i < world_size - 1:
                    if not move(direction_y):
                        change_hat(Hats.Green_Hat)
                        return

                    # 换行后水平方向反转，实现蛇形
                    if direction_x == East:
                        direction_x = West
                    else:
                        direction_x = East

    # 吃苹果的阈值, 大于该阈值之后, 转换策略, 改为蛇形循环
    APPLE_LIMIT = world_size * 2

    # 已经吃掉的苹果数
    apples = 0
    next_x = 0
    next_y = 0

    # 准备完毕, 开始养恐龙
    change_hat(Hats.Dinosaur_Hat)

    while apples < APPLE_LIMIT:
        if get_entity_type() == Entities.Apple:
            apples = apples + 1
            next_x, next_y = measure()
            
            # 先判断是在上半还是下半
            x, y = get_pos_x(), get_pos_y()
            dis = []
            if (x + y) < world_size:
                dis = [North, East]
                if not can_move(dis[0]):
                    dis[0], dis[1] = dis[1], dis[0]
            else:
                dis = [South, West]
                if not can_move(dis[0]):
                    dis[0], dis[1] = dis[1], dis[0]
            for i in range(apples):
                if not move(dis[0]):
                    break
                if get_entity_type() == Entities.Apple:
                    apples = apples + 1
                    next_x, next_y = measure()
            for j in range(apples):
                if not move(dis[1]):
                    break
                if get_entity_type() == Entities.Apple:
                    apples = apples + 1
                    next_x, next_y = measure()

        # 无论现在是不是在苹果上，都尝试朝目标走
        if not move_to_target(next_x, next_y):
            move_result = try_safe_step()
            if move_result == None:
                change_hat(Hats.Green_Hat)
                # 计算吃一个苹果所需要的平均时间
                log_fun(start_time, apples)
                return

    # 前期结束 → 进入 snake_loop(world_size)
    # 先回到坐标0, 0
    while not move_to_target(0, 0):
        move_result = try_safe_step()
        if move_result == None:
            change_hat(Hats.Green_Hat)
            # 计算吃一个苹果所需要的平均时间
            log_fun(start_time, apples)
            return

    snake_loop(world_size)
    # 计算吃一个苹果所需要的平均时间
    log_fun(start_time, world_size**2)



# 尝试收获当前格子的植物
def try_harvest(fun=util._always_true):
    if fun() and can_harvest():
        return harvest()
    elif get_entity_type() == Entities.Dead_Pumpkin:
        harvest()
    return False
