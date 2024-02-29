import win32api
import win32con
import win32gui

# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("grcWindow", "alt:V Multiplayer") 
print(hWnd)

# 模拟按下E键
win32api.PostMessage(hWnd, win32con.WM_KEYDOWN, 0x45, 0)
# 等待一些时间，可以根据需要调整
win32api.Sleep(100)
# 模拟释放E键
win32api.PostMessage(hWnd, win32con.WM_KEYUP, 0x45, 0)

