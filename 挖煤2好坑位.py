import ctypes
import time
import win32api, win32print
import win32con
import win32gui
import pyautogui
import pydirectinput

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h

# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def run_for_milliseconds(key_code, duration_ms):
    start_time = time.time()
    while (time.time() - start_time) * 1000 < duration_ms:
        PressKey(key_code)
        time.sleep(0.01)  # 控制循环速度，可根据需要调整
    ReleaseKey(key_code)

def move_mouse(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx, dy, 0, 0x0001 | 0x8000, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def simulate_key_press(hWnd, key_code, Sleep_time=112):
    # 模拟按下指定键
    win32api.PostMessage(hWnd, win32con.WM_KEYDOWN, key_code, 0)
    # 等待一些时间，可以根据需要调整
    win32api.Sleep(Sleep_time)
    # 模拟释放指定键
    win32api.PostMessage(hWnd, win32con.WM_KEYUP, key_code, 0)


# Mapping of keys to their respective virtual key codes
key_mapping = {
    'W': 0x11,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20
}

# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("grcWindow", "alt:V Multiplayer") 
print(hWnd)

# 获取窗口位置和大小
rect = win32gui.GetWindowRect(hWnd)

# 计算窗口中心坐标
center_x = (rect[0] + rect[2]) // 2
center_y = (rect[1] + rect[3]) // 2

# 将鼠标移动到窗口中心
win32api.SetCursorPos((center_x, center_y))
print(center_x, center_y)

# 切换到前台
win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hWnd)

wight,hight = get_real_resolution()
# 转屏幕宽度=180度

# 模拟鼠标点击
# pydirectinput.click()
time.sleep(1)

# 鼠标左移动200像素
# move_mouse(200, 0)
kuang =2 


if kuang==2:
    # 示例用法，运行按键 W 操作2秒钟
    run_for_milliseconds(key_mapping['W'], 2000)
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['A'], 2800)
    time.sleep(0.5)
    simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['D'], 2500)
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['S'], 2400)

if kuang==3:
    # 示例用法，运行按键 W 操作2秒钟
    run_for_milliseconds(key_mapping['W'], 2500)
    time.sleep(0.5)
    # 向左转
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -(int(wight/2)+150), 0)
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['W'], 2800)
    time.sleep(0.5)

    simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键

    # 向后转
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, wight+150, 0)
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['W'], 2800)
    time.sleep(0.5)
    # 向右转
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(wight/2)+150, 0)
    time.sleep(0.5)
    run_for_milliseconds(key_mapping['W'], 2800)
    time.sleep(0.5)

    # 向后转
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, wight+150, 0)
    time.sleep(0.5)
