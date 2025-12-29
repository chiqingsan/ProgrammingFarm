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
def plant_tree(farm_map=[]):
    if len(farm_map) == 0:
        return plant(Entities.Tree)
    world_size = get_world_size()
    x = get_pos_x()
    y = get_pos_y()
    # 1. 检查四个方向，并将结果存入变量
    has_tree_up = (y > 0) and (config.farm[x][y - 1] == Entities.Tree)
    has_tree_down = (y < world_size - 1) and (config.farm[x][y + 1] == Entities.Tree)
    has_tree_left = (x > 0) and (config.farm[x - 1][y] == Entities.Tree)
    has_tree_right = (x < world_size - 1) and (config.farm[x + 1][y] == Entities.Tree)

    # 2. 用 or 连接所有变量
    if has_tree_up or has_tree_down or has_tree_left or has_tree_right:
        return plant_wood()
    else:
        return plant(Entities.Tree)


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
        plant_tree(config.farm)
    # 胡萝卜不够了种胡萝卜
    elif num_items(Items.Carrot) < config.Min_Carrot:
        plant_carrot()
    else:
        # 都够了就种草来兜底
        plant_hay()

    # 尝试进行混合种植, 同时只允许胡萝卜和树可以混合种植
    if config.farm[x][y] == Entities.Carrot or config.farm[x][y] == Entities.Tree:
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
    # list = util.get_dict_value(config.petals_dict)

    # if not list:
    #     util.goto_xy(0, 0)
    #     return

    # max_petal = max(list)
    # del_key = []
    # for pos in config.petals_dict:
    #     if config.petals_dict[pos] == max_petal:
    #         util.goto_xy(pos[0], pos[1])
    #         if try_harvest():
    #             del_key.append(pos)

    # if del_key:
    #     for key in del_key:
    #         config.petals_dict.pop(key)

    # harvest_sunflower_max()
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
