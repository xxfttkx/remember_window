import time
import pygetwindow as gw
from screeninfo import get_monitors
import json

need_move = ['雷电模拟器','Clash Verge','v2rayN','OBS','直播姬','雷神加速器']
need_move_set = set()

# 获取显示器信息
def get_monitor_info():
    monitors = get_monitors()
    monitor_info = []
    for monitor in monitors:
        monitor_info.append({
            "device_name": monitor.name,
            "width": monitor.width,
            "height": monitor.height,
            "x": monitor.x,
            "y": monitor.y
        })
    return monitor_info

def get_window(title):
    windows = gw.getWindowsWithTitle(title)
    if len(windows)==0:
        print("windows.size==0")
        return None
    for w in windows:
        if w.title == title:
            return w
    return windows[0]
    
# 获取窗口位置
def get_window_position(window_title):
    window = get_window(window_title)
    if window == None:
        return None
    return window.left, window.top, window.width, window.height

# 设置窗口位置
def set_window_position(window_title, x, y):
    window = get_window(window_title)
    if window != None:
        window.moveTo(x, y)

def get_window_positions():
    windows = gw.getAllWindows()
    window_positions = []

    # 遍历每个窗口，获取其位置和大小
    for window in windows:
        if window.isVisible():  # 如果窗口是可见的
            window_positions.append({
                "title": window.title,
                "left": window.left,
                "top": window.top,
                "width": window.width,
                "height": window.height
            })
    
    return window_positions

# 将窗口位置数据保存到 JSON 文件
def save_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # 使用缩进使 JSON 更易读
        
def main():
    monitors = get_monitor_info()
    while True:
        windows = gw.getAllTitles()
        for title in need_move:
            if(title in windows):
                if(title not in need_move_set):
                    need_move_set.add(title)
                    set_window_position(title, monitors[1]["x"], monitors[1]["y"])
                    print(title)
        time.sleep(1)  # 每秒
            

if __name__ == "__main__":
    main()

