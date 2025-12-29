import work
import util
import config


# clear()
util.goto_xy(0,0)
while(True):
    # work.inspection(work.try_planting,work.harvest_begins)
    # if (num_items(Items.Hay) < config.Min_Hay
    #     or num_items(Items.Wood) < config.Min_Wood
    #     or num_items(Items.Carrot) < config.Min_Carrot):
    #     work.inspection(work.try_planting_common_crops)
    # elif (num_items(Items.Power) < config.Min_Power):
    #     work.inspection(work.try_planting_sunflower,work.harvest_sunflower_max)
    # elif (num_items(Items.Pumpkin) < config.Min_Pumpkin):
    work.inspection(work.try_planting_pumpkin,work.try_harvest_pumpkin)