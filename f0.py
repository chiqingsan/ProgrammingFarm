import util

# 最小的骨头数量
Min_Bone = 3000000
# 最小的仙人掌数量
Min_Cactus = 3000000
# 最小的胡萝卜数量
Min_Carrot = 300000
# 最小的化肥数量
Min_Fertilizer = 3000000
Min_Gold = 3000000
# 最小的干草数量
Min_Hay = 300000
Min_Piggy = 3000000
# 最小的能量数量
Min_Power = 3000000
# 最小的南瓜数量
Min_Pumpkin = 3000000
# 最小的水数量
Min_Water = 3000000
# 最小的怪异物质数量
Min_Weird_Substance = 3000000
# 最小的木头数量
Min_Wood = 300000
# 最大的向日葵数量
Max_Sunflower = 50


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
    has_tree_up = (y > 0) and (farm[x][y - 1] == Entities.Tree)
    has_tree_down = (y < world_size - 1) and (farm[x][y + 1] == Entities.Tree)
    has_tree_left = (x > 0) and (farm[x - 1][y] == Entities.Tree)
    has_tree_right = (x < world_size - 1) and (farm[x + 1][y] == Entities.Tree)

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
    else:
        return plant_hay()


# 浇水
def water_plant():
    if get_water() < 0.6 and num_items(Items.Water) :
        use_item(Items.Water)
        water_plant()

# 施肥
def fertilize_plant():
    if num_items(Items.Fertilizer):
        use_item(Items.Fertilizer)


def getFram(entities=Entities.Grass):
    farm = []
    world_size = get_world_size()
    for i in range(world_size):  # 循环创建每一行
        row = []  # 2. 为每一行创建一个空的列表
        for j in range(world_size):  # 循环填充这一行的每一列
            row.append(entities)  # 3. 把元素添加到行列表的末尾
        farm.append(row)  # 4. 把填充好的行添加到 farm 列表的末尾
    return farm


farm = getFram()
# 创建一个计划种植的农场地图
plan_farm = getFram(None)
# print(farm)
# 定义一个向日葵花瓣的字典, 用来记录最大的花瓣数
petals_list = {}
world_size = get_world_size()


def planting_extra():
    if get_entity_type() == Entities.Sunflower:
        x, y = get_pos_x(), get_pos_y()
        petal_num = measure()
        values = util.getDictValue(petals_list)
        if len(values) < Max_Sunflower or petal_num < max(values):
            return False
        petals_list.pop((x, y))
    return True


def try_planting():
    x, y = get_pos_x(), get_pos_y()

    # 尝试收获
    if get_entity_type() != None:
        if not try_harvest(planting_extra):
            is_bad_pumpkin()
            return

    # 查看当前位置是否已经有计划种植的植物
    if plan_farm[x][y] != None:
        if plant_entities(plan_farm[x][y]):
            # 混合种植之后, 删掉当前位置的种植计划
            plan_farm[x][y] = None
            farm[x][y] = get_entity_type()
            return
    # 根据资源情况决定种植什么植物
    # 优先种向日葵
    val = util.getDictValue(petals_list)
    if (
        num_items(Items.Power) < Min_Power
        and len(val) < Max_Sunflower
        and num_items(Items.Carrot)
    ):
        if plant_sunflower():
            petals_list[(x, y)] = measure()
    # 草不够了就种草
    elif num_items(Items.Hay) < Min_Hay:
        plant_hay()
    # 木头不够种树
    elif num_items(Items.Wood) < Min_Wood:
        plant_tree(farm)
    # 胡萝卜不够了种胡萝卜
    elif num_items(Items.Carrot) < Min_Carrot:
        plant_carrot()
    # 南瓜不够了种南瓜
    elif num_items(Items.Pumpkin) < Min_Pumpkin:
        plant_pumpkin()
        # if plant_pumpkin():
        #     range_xy = util.find_square_region(plan_farm, (x, y), 6)
        #     util.fill_plan_farm_with_pumpkin(plan_farm, range_xy)

    # fertilize_plant()
    farm[x][y] = get_entity_type()

    # 尝试进行混合种植, 同时只允许胡萝卜和树可以混合种植
    if farm[x][y] == Entities.Carrot or farm[x][y] == Entities.Tree:
        companion = get_companion()
        if companion != None:
            plant_type, (x, y) = companion
            plan_farm[x][y] = plant_type

def inspection(fun=util._always_true):
    world_size = get_world_size()
    direction_x = East
    direction_y = North

    # 遍历整个网格世界，按行进行蛇形移动
    for i in range(world_size):
        # 在当前行中横向移动并执行函数
        for j in range(world_size - 1):
            x = get_pos_x()
            # 检查是否到达右边界，如果是则改变移动方向为向左
            if x == world_size - 1:
                direction_x = West
            # 检查是否到达左边界，如果是则改变移动方向为向右
            if x == 0:
                direction_x = East
            # pass
            fun()
            move(direction_x)
        # 完成一行的遍历后，执行函数并向上移动到下一行
        fun()
        move(direction_y)


def try_harvest(fun=util._always_true):
    if can_harvest() and fun():
        return harvest()
    return False
