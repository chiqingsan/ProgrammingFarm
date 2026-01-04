import work
import util
import config

def _do_work():

    def work_func(type):
        if type in (Items.Hay, Items.Wood, Items.Carrot):
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
        else:
            print("error: 未知工作类型!  " + str(type))

    def drones_work_func(type):
        if type in (Items.Hay, Items.Wood, Items.Carrot):
            work.drones_plant_common_crops()
        elif type == Items.Power:
            work.drones_plant_sunflower()
        elif type == Items.Pumpkin:
            work.drones_plant_pumpkin()
        elif type == Items.Cactus:
            work.drones_plant_cactus()
        elif type == Items.Gold:
            work.drones_try_finding_treasure()
        elif type == Items.Bone:
            work.try_feed_dinosaur()
        else:
            print("error: 未知工作类型!  " + str(type))


    if num_unlocked(Unlocks.Megafarm):
        return drones_work_func
    else:
        return work_func
    

def choose_work_type():
    # 草、木头、胡萝卜为混合种植，逻辑上都归为 Items.Hay 类型
    if (num_items(Items.Hay) < config.Min_Hay
        or num_items(Items.Wood) < config.Min_Wood
        or num_items(Items.Carrot) < config.Min_Carrot):
        return Items.Hay

    if num_items(Items.Power) < config.Min_Power:
        return Items.Power

    if num_items(Items.Pumpkin) < config.Min_Pumpkin:
        return Items.Pumpkin

    if num_items(Items.Cactus) < config.Min_Cactus:
        return Items.Cactus

    if num_items(Items.Gold) < config.Min_Gold:
        return Items.Gold

    # 都不缺了就随便来一个
    work_list = [Items.Hay, Items.Power, Items.Pumpkin, Items.Cactus, Items.Gold, Items.Bone]
    return util.random_elem(work_list)

def main():
    clear()
    do_work = _do_work()
    set_world_size(12)

    while True:
        # work.inspection(work.try_planting_common_crops)
        work.inspection(work.try_planting_cactus, work.try_sort_and_harvest_cactus)
        # work_type = choose_work_type()
        # do_work(work_type)


main()
