import util

# 最小的骨头数量
Min_Bone = 3000000
# 最小的仙人掌数量
Min_Cactus = 3000000
# 最小的胡萝卜数量
Min_Carrot = 300000
# 最小的金块数量
Min_Gold = 300000
# 最小的干草数量
Min_Hay = 300000
# 最小的能量数量
Min_Power = 30000
# 最小的南瓜数量
Min_Pumpkin = 300000
# 最小的怪异物质数量
Min_Weird_Substance = 3000000
# 最小的木头数量
Min_Wood = 300000

# 创建一个计划种植的农场地图
plan_farm = util.getFram()
# 定义一个向日葵花瓣的字典, 用来记录最大的花瓣数
petals_dict = {}
# 定义一个记录坏南瓜的相关列表
bad_pumpkin_list = []
# 配置需要施肥的作物
need_fertilize = [Entities.Pumpkin, Entities.Cactus, Entities.Sunflower]

