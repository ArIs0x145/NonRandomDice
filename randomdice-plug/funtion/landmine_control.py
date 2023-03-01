from mouse_control import keyboard_press


def landmine_ctrl(hwndTool, wave, action, boss_hit, target_first=None):
    if wave == -1 and target_first:
        # roll landmine
        if action == '準備排雷':
            keyboard_press(hwndTool, 'A')
            print('排雷中')
            return '排雷中'
        # put landmine
        if action == '排雷中':
            if target_first >= 290:
                keyboard_press(hwndTool, 'A')
                print('已排好')
                return '已排好'

    if wave == 1:
        # roll landmine to hit
        if action == '已排好' and boss_hit:
            keyboard_press(hwndTool, 'A')
            print('等雷清光')
            return '等雷清光'

        # Release landmine
        if action == '等雷清光':
            keyboard_press(hwndTool, 'A')
            print('準備排雷')
            return '準備排雷'


def main():
    pass


if __name__ == '__main__':
    pass


