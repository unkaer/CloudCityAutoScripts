import win32api
import win32con
import win32gui

def move_mouse(x, y):
    # 移动鼠标
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("grcWindow", "alt:V Multiplayer") 
print(hWnd)

# 设置鼠标相对移动的距离，这里示例为向右移动200个像素
move_distance = 200

# 移动鼠标
move_mouse(move_distance, 0)
