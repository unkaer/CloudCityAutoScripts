
import win32gui, win32ui, win32con, win32print
from win32.win32api import GetSystemMetrics

def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h

real_resolution = get_real_resolution()
screen_size = get_screen_size()
print(real_resolution)
print(screen_size)

screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
print(screen_scale_rate)


# 获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("grcWindow", "alt:V Multiplayer") 
print(hWnd)
# 获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
width = int(width*screen_scale_rate)

height = bot - top
height = int(height*screen_scale_rate)
print(width)
print(height)

# 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
# 创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
# 创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()
# 创建位图对象准备保存图片
saveBitMap = win32ui.CreateBitmap()
# 为 bitmap 开辟存储空间
saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
# 将截图保存到 saveBitMap 中
saveDC.SelectObject(saveBitMap)
# 保存 bitmap 到内存设备描述表
saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

# 保存 bitmap 到文件
saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")

# 内存释放
win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hWnd, hWndDC)
