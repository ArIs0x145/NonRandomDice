import time
import math

from landmine_control import landmine_ctrl


def handle_data(obj_data, f_start, hwndTool):
    # def value
    unlock = True
    wave_time = time.time() - 10
    wave = -1
    landmine_action = '準備排雷'
    action = landmine_action
    while True:
        # detect button input
        if not f_start.empty():
            if f_start.get() == 1:
                unlock = not unlock

                # restart
                if unlock:
                    print('腳本雷: 開啟')
                    # re def value
                    wave_time = time.time() - 9
                    wave = -1
                    landmine_action = '準備排雷'
                    action = landmine_action
                else:
                    print('腳本雷: 關閉')
        # unlock script
        if unlock:
            # def value
            boss = False
            target_first = None
            distance_min = None

            # per_img_data
            while True:
                if not obj_data.empty():
                    obj_list = obj_data.get()
                    # end number
                    if obj_list == 777:
                        break
                    # boss
                    elif obj_list[0] == 0:
                        boss = True

                    # landmine
                    elif obj_list[0] == 1:
                        # find first landmine
                        distance = round(math.sqrt(((obj_list[1][0] - 0) ** 2) + ((obj_list[1][1] - 640) ** 2)), 2)
                        if not distance_min or distance < distance_min:
                            distance_min = distance
                            target_first = obj_list[1][1]

                    # wave
                    elif obj_list[0] == 2:
                        wave_time_delay = time.time() - wave_time
                        wave_time = time.time()
                        # convert wave
                        if wave_time_delay > 10:
                            wave = wave * (-1)
                            # Show wave
                            if wave == -1:
                                print('小怪關')
                            else:
                                print('王關')

            # use data to ctrl landmine
            if landmine_action == '等雷清光':
                time.sleep(4)
                action = landmine_ctrl(
                    hwndTool, wave=wave, action=landmine_action, boss_hit=boss, target_first=target_first
                )
            else:
                action = landmine_ctrl(
                    hwndTool, wave=wave, action=landmine_action, boss_hit=boss, target_first=target_first
                )

                # covert action
            if action:
                landmine_action = action
        else:
            pass


if __name__ == "__main__":
    pass

