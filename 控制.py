import win32api
import win32con
import win32gui

# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("grcWindow", "alt:V Multiplayer") 
print(hWnd)

# 切换到前台
win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hWnd)

win32api.SendMessage