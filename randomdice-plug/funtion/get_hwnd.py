import win32gui, win32ui, win32con, win32api


def main():
    hwnd_title = dict()
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            print(h, t)


def get_hwnd(filename):
    hwnd = win32gui.FindWindow(None, filename)

    hwndTool = []
    def find_hwndTool(hwnd, param):
        if win32gui.GetWindowText(hwnd) == 'toolbar_nox':
            hwndTool.append(hwnd)
            return False

    win32gui.EnumChildWindows(hwnd, find_hwndTool, None)

    if hwnd:
        if hwndTool:
            return hwnd, hwndTool[0]
        else:
            print('未取得工具句炳')
    else:
        print('未取得遊戲句炳')

if __name__ == '__main__':
    hwnd, hwndTool = get_hwnd('夜神模擬器')
    print(hwnd, hwndTool)