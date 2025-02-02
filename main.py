import os
import time
import pygetwindow as gw
from screeninfo import get_monitors
import json
import win32gui
import win32con

blacklist = ['Google Chrome', 'Visual Studio Code']
whitelist = ['Clash Verge']
class Window:
    def __init__(self, title, left, top, width, height):
        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def toJson(self):
        return {
            "title": self.title,
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height
        }

    @staticmethod
    def fromJson(data):
        return Window(data['title'], data['left'], data['top'], data['width'], data['height'])

    def __str__(self):
        return f"Window(title={self.title})"
    
    def __eq__(self, other):
        # 判断两个对象是否属于同一类，并且它们的 `value` 是否相等
        if isinstance(other, Window):
            return self.title == other.title and self.left == other.left and self.top == other.top and self.width == other.width and self.height == other.height
        return False

def get_window(title):
    windows = gw.getWindowsWithTitle(title)
    if len(windows)==0:
        print("windows.size==0")
        return None
    for w in windows:
        if w.title == title:
            return w
    return windows[0]
    

# 设置窗口位置
def set_window_position(window_title, window):
    w = get_window(window_title)
    if w != None:
        w.resizeTo(window.width, window.height)
        w.moveTo(window.left, window.top)

def saveJson():
    filename = 'window_positions.json'
    data = []
    for w in curr_windows:
        data.append(w.toJson())
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Save Successd!")

def loadJson():
    filename = 'window_positions.json'
    if not os.path.exists(filename):  # 判断文件是否存在
        print(f"File '{filename}' does not exist.")
        return []  # 如果文件不存在，返回一个空列表
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)  # 读取并解析 JSON 数据
    windows = []
    for window_data in data:
        windows.append(Window.fromJson(window_data))  # 转换回 Window 对象
    print("Load Successd!")
    return windows

def tryUpdateJson(title):
    found = False
    for index, w in enumerate(curr_windows):
        if w.title==title:
            curr = getWindowFromTitle(title)
            if curr!=w:
                curr_windows[index] = curr
                print(curr)
                return True
            return False
    if not found:
        w = getWindowFromTitle(title)
        curr_windows.append(w)
        print(w)
        return True

def getWindowFromTitle(title):
    window = get_window(title)
    return Window(window.title, window.box.left, window.box.top, window.box.width, window.box.height)

def is_alt_tab_window(hwnd):
    """判断窗口是否是 Alt + Tab 可见的窗口"""

    title = win32gui.GetWindowText(hwnd)
    if title:  # 只添加有标题的窗口
        for white in whitelist:
            if white in title:
                return True
        for black in blacklist:
            if black in title:
                return False
    if not win32gui.IsWindowVisible(hwnd):
        return False  # 如果窗口不可见，排除
    placement = win32gui.GetWindowPlacement(hwnd)
    # can del  --- showCmd 
    if placement[1] == win32con.SW_HIDE:
        return False  # 如果窗口最小化，排除
    if placement[2] == (-1,-1):
        return False  # 如果窗口最小化，排除
    return True

def get_alt_tab_windows():
    """获取所有 Alt + Tab 可见的窗口"""
    visible_windows = []

    def enum_window_callback(hwnd, lParam):
        """回调函数，用于遍历窗口"""
        if is_alt_tab_window(hwnd):
            title = win32gui.GetWindowText(hwnd)
            visible_windows.append(title)
    
    # 遍历所有窗口
    win32gui.EnumWindows(enum_window_callback, None)
    return visible_windows

curr_windows = []

def main():
    global curr_windows
    curr_windows = loadJson()
    move_set = set()
    while True:
        alt_tab_windows = get_alt_tab_windows()
        needSave = False
        for title in alt_tab_windows:
            if(title not in move_set):
                move_set.add(title)
                for index, w in enumerate(curr_windows):
                    if w.title==title:
                        set_window_position(title, w)
                        break
            needSave = tryUpdateJson(title) or needSave
        if needSave:
            saveJson()      
        time.sleep(1)  # 每秒
            

if __name__ == "__main__":
    main()