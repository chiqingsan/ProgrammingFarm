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
Min_Power = 30000
Min_Pumpkin = 300000
# 最小的水数量
Min_Water = 3000000
# 最小的怪异物质数量
Min_Weird_Substance = 3000000
# 最小的木头数量
Min_Wood = 300000

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
petals_dict = {}
# 定义一个记录坏南瓜的相关字典
bad_pumpkin_list = []
# 定义一个记录坏南瓜的相关字典
bad_pumpkin_dict = {}
# 定义一个记录坏南瓜的相关列表
bad_pumpkin = getFram(None)
# 是否允许收获南瓜
allow_harvest_pumpkin = False
# 是否允许收获仙人掌
allow_harvest_cactus = False
world_size = get_world_size()
