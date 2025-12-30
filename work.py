import util
import config


# 尝试种一个胡萝卜
def plant_carrot():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Carrot)


# 尝试种一个干草
def plant_hay():
    if get_ground_type() == Grounds.Soil:
        till()
    return True


# 尝试种一个灌木
def plant_wood():
    if get_ground_type() == Grounds.Soil:
        till()
    return plant(Entities.Bush)


# @param farm_map: 二维列表, 代表农场的地图
# 尝试种一棵树, 如果周围有树则种灌木.
# 如果 farm_map 为空则直接种树.
def plant_tree():
    # if len(farm_map) == 0:
    #     return plant(Entities.Tree)
    # world_size = get_world_size()
    # x = get_pos_x()
    # y = get_pos_y()
    # # 1. 检查四个方向，并将结果存入变量
    # has_tree_up = (y > 0) and (config.farm[x][y - 1] == Entities.Tree)
    # has_tree_down = (y < world_size - 1) and (config.farm[x][y + 1] == Entities.Tree)
    # has_tree_left = (x > 0) and (config.farm[x - 1][y] == Entities.Tree)
    # has_tree_right = (x < world_size - 1) and (config.farm[x + 1][y] == Entities.Tree)

    # # 2. 用 or 连接所有变量
    # if has_tree_up or has_tree_down or has_tree_left or has_tree_right:
    #     return plant_wood()
    # else:
    #     return plant(Entities.Tree)
    x,y = get_pos_x(), get_pos_y()
    if ((x+y) % 2) == 0 :
        plant(Entities.Tree)
    else:
        if get_ground_type() == Grounds.Soil:
            till()
        plant(Entities.Bush)


# 尝试种一个向日葵
def plant_sunflower():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Sunflower)


# 尝试种一个南瓜
def plant_pumpkin():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Pumpkin)


# 尝试种一个仙人掌
def plant_cactus():
    if get_ground_type() != Grounds.Soil:
        till()
    return plant(Entities.Cactus)


# 判断是不是坏南瓜
def is_bad_pumpkin():
    if get_entity_type() == Entities.Dead_Pumpkin:
        plant_pumpkin()


# 根据输入参数来种植对应的植物
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


def planting_extra():
    entity_type = get_entity_type()
    x, y = get_pos_x(), get_pos_y()
    if entity_type == Entities.Sunflower:
        petal_num = measure()
        values = util.get_dict_value(config.petals_dict)
        if petal_num < 14:
            pass
        elif len(values) < config.Max_Sunflower or petal_num < max(values):
            return False
        config.petals_dict.pop((x, y))
    elif entity_type == Entities.Dead_Pumpkin:
        config.bad_pumpkin[x][y] = False
        plant_pumpkin()
    elif entity_type == Entities.Pumpkin:
        config.bad_pumpkin[x][y] = None
        return allow_harvest_pumpkin
    return True


def harvest_begins():
    # 控制南瓜的收获
    global allow_harvest_pumpkin
    global allow_harvest_cactus
    if allow_harvest_pumpkin:
        allow_harvest_pumpkin = False
    else:
        for y in range(config.world_size):
            for x in range(config.world_size):
                if config.bad_pumpkin[x][y] == False:
                    return
        allow_harvest_pumpkin = True

    # 控制仙人掌的收获
    # 查找当前地图中的成团的仙人掌
    for y in range(config.world_size):
        for x in range(config.world_size):
            if (
                config.farm[x][y] == Entities.Cactus
                and (x > 0 and config.farm[x - 1][y] != Entities.Cactus)
                and (y > 0 and config.farm[x][y - 1] != Entities.Cactus)
            ):
                pass


def try_planting():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        if not try_harvest(planting_extra):
            return

    # 查看当前位置是否已经有计划种植的植物
    if config.plan_farm[x][y] != None:
        if plant_entities(config.plan_farm[x][y]):
            # 混合种植之后, 删掉当前位置的种植计划
            config.plan_farm[x][y] = None
            config.farm[x][y] = get_entity_type()
            return
    # 根据资源情况决定种植什么植物
    # 优先种向日葵
    val = util.get_dict_value(config.petals_dict)
    if (
        num_items(Items.Power) < config.Min_Power
        and len(val) < config.Max_Sunflower
        and num_items(Items.Carrot)
    ):
        if plant_sunflower():
            config.petals_dict[(x, y)] = measure()
    # 草不够了就种草
    elif num_items(Items.Hay) < config.Min_Hay:
        plant_hay()
    # 木头不够种树
    elif num_items(Items.Wood) < config.Min_Wood:
        plant_tree(config.farm)
    # 胡萝卜不够了种胡萝卜
    elif num_items(Items.Carrot) < config.Min_Carrot:
        plant_carrot()
    # 南瓜不够了种南瓜
    elif num_items(Items.Pumpkin) < config.Min_Pumpkin:
        my = y % (6 + 1)
        mx = x % (6 + 1)
        if my == 6 or mx == 6:
            plant_carrot()
        else:
            plant_pumpkin()
            fertilize_plant()
    # 仙人掌不够了种仙人掌
    elif num_items(Items.Cactus) < config.Min_Cactus:
        # if plant_cactus():
        # try_fill_cactus(x, y, plan_farm)
        plant_cactus()

    # fertilize_plant()
    config.farm[x][y] = get_entity_type()

    # 尝试进行混合种植, 同时只允许胡萝卜和树可以混合种植
    if config.farm[x][y] == Entities.Carrot or config.farm[x][y] == Entities.Tree:
        companion = get_companion()
        if companion != None:
            plant_type, (x, y) = companion
            config.plan_farm[x][y] = plant_type


# 尝试种植常规作物
def try_planting_common_crops():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        if not try_harvest():
            return

    # 查看当前位置是否已经有计划种植的植物
    if config.plan_farm[x][y] != None:
        if plant_entities(config.plan_farm[x][y]):
            # 混合种植之后, 删掉当前位置的种植计划
            config.plan_farm[x][y] = None
            config.farm[x][y] = get_entity_type()
            return

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

    # 尝试进行混合种植, 同时只允许胡萝卜和树可以混合种植
    # if config.farm[x][y] == Entities.Carrot or config.farm[x][y] == Entities.Tree:
    companion = get_companion()
    if companion != None:
        plant_type, (x, y) = companion
        config.plan_farm[x][y] = plant_type


# 尝试种植向日葵
def try_planting_sunflower():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        if not try_harvest():
            return

    if num_items(Items.Power) < config.Min_Power and num_items(Items.Carrot):
        if plant_sunflower():
            config.petals_dict[(x, y)] = measure()


# 种植完向日葵之后尝试以最大收益收获向日葵
def harvest_sunflower_max():
    tmp_petals = dict()   # {花瓣数: [坐标列表]}

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
                try_harvest()
        p -= 1

    config.petals_dict = dict()
    util.goto_xy(0, 0)


# 尝试种植南瓜
def try_planting_pumpkin():
    x, y = get_pos_x(), get_pos_y()


    # 尝试收获
    if get_entity_type() != None:
        if not try_harvest():
            return
        
    my = y % (6 + 1)
    mx = x % (6 + 1)
    if my == 6 or mx == 6:
        plant_carrot()
    else:
        plant_pumpkin()
        fertilize_plant()

# 尝试收获南瓜, 补种坏掉的南瓜, 直到完好后收获
def try_harvest_pumpkin():
    is_all_good = False
    config.bad_pumpkin_list = []
    util.goto_xy(0, 0)
    # 全图查找一遍坏南瓜
    def tmp_func():
        x,y = get_pos_x(), get_pos_y()
        entity_type = get_entity_type()

        if entity_type == Entities.Dead_Pumpkin or entity_type == None:
            config.bad_pumpkin_list.append((x,y))
            plant_pumpkin()
        elif entity_type == Entities.Pumpkin and not can_harvest():
            # 如果是南瓜, 但是不可以收获, 则说明还没有成熟, 记录下来
            config.bad_pumpkin_list.append((x,y))

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


# 尝试寻找迷宫中的宝藏
def try_finding_treasure(treasure_size=None):
    # 不在迷宫里就生成新迷宫
    entity_type = get_entity_type()
    if entity_type != Entities.Treasure and entity_type != Entities.Hedge:
        plant(Entities.Bush)
        if treasure_size == None:
            treasure_size = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
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


def inspection(handle=util._always_true, harvest_begins=util._always_true):
    world_size = get_world_size()
    direction_x = East      # 当前行的横向方向（初始向右）
    direction_y = North     # 竖直方向，向上

    for i in range(world_size):           # 遍历每一行
        # 当前行横向移动 world_size - 1 步
        for j in range(world_size - 1):
            handle()                      # 处理当前格子
            move(direction_x)             # 向当前行方向移动一格

        handle()                          # 这一行最后一个格子

        # 最后一行处理完就不用再往上走了
        if i < world_size - 1:
            move(direction_y)             # 上移到下一行

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



# 尝试养恐龙来收获骨头
def try_feed_dinosaur_123():
    set_world_size(12)
    world_size = get_world_size()

    # 确保世界大小为偶数（当前逻辑依赖偶数尺寸）
    if world_size % 2 != 0:
        world_size -= 1
        set_world_size(world_size)
        

    # 换上恐龙帽，开始养恐龙
    change_hat(Hats.Dinosaur_Hat)

    # 无限循环沿着预设路径移动，直到某一步 move() 失败
    while True:
        direction_x = East   # 水平移动方向（当前行）
        direction_y = North  # 垂直移动方向（换行时）

        # 蛇形遍历每一行，并在最后一行做一段“回到底边”的闭环
        for i in range(world_size):
            # ── 横向移动部分 ──
            if i == 0:
                # 第一行：水平走 world_size - 1 步
                for j in range(world_size - 1):
                    if not move(direction_x):
                        # 撞墙或尾巴，收尾巴结束
                        change_hat(Hats.Green_Hat)
                        return
            else:
                # 中间行 & 最后一行：先走 world_size - 2 步
                for j in range(world_size - 2):
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
                        for k in range(world_size - 1):
                            if not move(South):
                                change_hat(Hats.Green_Hat)
                                return

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

# ================== 辅助函数：简单朝目标走（贪心直线） ==================

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


# ================== 辅助函数：前期乱逛一步（避免太快撞死） ==================

def walk_simple(direction):
    # direction：当前前进方向
    # 返回：新的方向；若四面都走不动，返回 None

    def turn_left(dir):
        if dir == North:
            return West
        if dir == West:
            return South
        if dir == South:
            return East
        return North  # East

    def turn_right(dir):
        if dir == North:
            return East
        if dir == East:
            return South
        if dir == South:
            return West
        return North  # West

    def turn_back(dir):
        if dir == North:
            return South
        if dir == South:
            return North
        if dir == East:
            return West
        return East  # West

    # 1️⃣ 先尝试原方向
    if move(direction):
        return direction

    # 2️⃣ 左转
    left_dir = turn_left(direction)
    if move(left_dir):
        return left_dir

    # 3️⃣ 右转
    right_dir = turn_right(direction)
    if move(right_dir):
        return right_dir

    # 四个方向都走不动，说明被包住了
    return None


# ================== 辅助函数：蛇形大循环（你原来的逻辑，稍微包了一层） ==================

def snake_loop(world_size):
    while True:
        # 先滑到左边界，再滑到底边，尽量从左下角开始蛇形
        while move(West):
            pass
        while move(South):
            pass

        direction_x = East   # 水平移动方向
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


# ================== 主函数：前期吃苹果 + 后期蛇形 ==================

def try_feed_dinosaur():
    # 地图大小：按需要调整
    set_world_size(12)
    world_size = get_world_size()

    # 逻辑依赖偶数尺寸，保证为偶数
    if world_size % 2 != 0:
        world_size = world_size - 1
        set_world_size(world_size)

    # 戴上恐龙帽
    change_hat(Hats.Dinosaur_Hat)

    apples = 0
    APPLE_LIMIT = 15  # 吃到这个数量后切换蛇形（可调）

    direction_walk = East  # 前期乱逛的初始方向
    next_x = 0
    next_y = 0

    # ========= 前期：主动吃苹果阶段 =========
    while apples < APPLE_LIMIT:
        if get_entity_type() == Entities.Apple:
            apples = apples + 1

            # 在苹果上时，measure() 返回下一颗苹果的位置
            next_x, next_y = measure()

            # 贪心朝下一颗苹果走
            if not move_to_target(next_x, next_y):
                # ❗ 这里不再立刻收割：
                #    撞到了，就尝试用 walk_simple 换个方向继续挣扎
                new_dir = walk_simple(direction_walk)
                if new_dir == None:
                    # 四个方向都走不动，才真正收割
                    change_hat(Hats.Green_Hat)
                    return
                direction_walk = new_dir
        else:
            # 没踩在苹果上，就用简单规则在场地里乱逛
            move(direction_walk)
            if not move_to_target(next_x, next_y):
                # ❗ 这里不再立刻收割：
                #    撞到了，就尝试用 walk_simple 换个方向继续挣扎
                new_dir = walk_simple(direction_walk)
                if new_dir == None:
                    # 四个方向都走不动，才真正收割
                    change_hat(Hats.Green_Hat)
                    return
                direction_walk = new_dir
            # new_dir = walk_simple(direction_walk)
            # if new_dir == None:
            #     # 四个方向都走不动，被完全包住了，收割
            #     change_hat(Hats.Green_Hat)
            #     return
            # direction_walk = new_dir

    # ========= 后期：蛇形大循环阶段 =========
    snake_loop(world_size)



# 尝试收获当前格子的植物
def try_harvest(fun=util._always_true):
    if fun() and can_harvest():
        return harvest()
    return False


# 尝试填写计划种植的仙人掌
def try_fill_cactus(x, y, plan_farm):
    world_size = get_world_size()
    extra = 1
    row = []
    col = []
    not_entities = True

    plan_farm[x][y] = Entities.Cactus

    while not_entities and x + extra < world_size and y + extra < world_size:
        if not_entities:
            for i in range(extra):
                if plan_farm[x + extra][y + i] == None:
                    row.append((x + extra, y + i))
                else:
                    not_entities = False
                    break
            row.append((x + extra, y + extra))

        if not_entities:
            for j in range(extra):
                if plan_farm[x + j][y + extra] == None:
                    col.append((x + j, y + extra))
                else:
                    not_entities = False
                    break

        if not_entities:
            for i in range(len(row)):
                plan_farm[row[i][0]][row[i][1]] = Entities.Cactus
            for j in range(len(col)):
                plan_farm[col[j][0]][col[j][1]] = Entities.Cactus

            row = []
            col = []
            extra = extra + 1
