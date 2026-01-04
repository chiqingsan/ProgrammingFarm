import work
import util
import config

def _do_work():

    def work_func(type):
        if type == Items.Hay or type == Items.Wood or type == Items.Carrot:
            work.inspection(work.try_planting_common_crops)
        elif type == Items.Power:
            work.inspection(work.try_planting_sunflower,work.harvest_sunflower_max)
        elif type == Items.Pumpkin:
            work.inspection(work.try_planting_pumpkin,work.try_harvest_pumpkin)
        elif type == Items.Cactus:
            work.inspection(work.try_planting_cactus, work.try_sort_and_harvest_cactus)
        elif type == Items.Gold:
            work.try_finding_treasure()
        elif type == Items.Bone:
            work.try_feed_dinosaur()

        if not type:
            print("error: 没有工作类型!")

    def drones_work_func(type):
        if type == Items.Hay or type == Items.Wood or type == Items.Carrot:
            work.inspection(work.try_planting_common_crops)
        elif type == Items.Power:
            work.drones_plant_sunflower()
        elif type == Items.Pumpkin:
            work.inspection(work.try_planting_pumpkin, work.try_harvest_pumpkin)
        elif type == Items.Cactus:
            work.drones_plant_cactus()
        elif type == Items.Gold:
            work.try_finding_treasure()
        elif type == Items.Bone:
            work.try_feed_dinosaur()

        if not type:
            print("error: 没有工作类型!")

    if num_unlocked(Unlocks.Megafarm):
        return drones_work_func
    else:
        return work_func

def main():
    clear()
    # work.drones_plant_sunflower()
    # work.drones_plant_cactus()
    do_work = _do_work()
    util.goto_xy(0,0)
    # 草, 木头, 胡萝卜为混合种植, 工作类型都为Items.Hay
    work_list = [Items.Hay, Items.Power, Items.Pumpkin, Items.Cactus, Items.Gold, Items.Bone]
    work_type = Items.Hay
    while(True):
        if (num_items(Items.Hay) < config.Min_Hay
            or num_items(Items.Wood) < config.Min_Wood
            or num_items(Items.Carrot) < config.Min_Carrot):
            work_type = Items.Hay
        elif (num_items(Items.Power) < config.Min_Power):
            work_type = Items.Power
        elif (num_items(Items.Pumpkin) < config.Min_Pumpkin):
            work_type = Items.Pumpkin
        elif (num_items(Items.Cactus) < config.Min_Cactus):
            work_type = Items.Cactus
        elif num_items(Items.Gold) < config.Min_Gold:
            work_type = Items.Gold
        else:
            # 都不缺了就随便来一个
            work_type = util.random_elem(work_list)
        # 开始工作
        do_work(work_type)


main()
