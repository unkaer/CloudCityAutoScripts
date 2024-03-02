import pygame
import sys
import math
import time
import win32gui
import win32ui
import win32con
import win32print
from win32.win32api import GetSystemMetrics
from PIL import Image
import struct

def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h

def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h

def capture_window(hwnd, output_filename="screenshot.bmp"):
    """截取指定窗口的屏幕截图"""
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)

    # 获取窗口大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = int((right - left) * screen_scale_rate)
    height = int((bot - top) * screen_scale_rate)

    # 获取窗口设备环境
    hWndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    # 将截图保存到 saveBitMap 中
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    # 保存 bitmap 到文件
    saveBitMap.SaveBitmapFile(saveDC, output_filename)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)

# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Map")

 # 指定窗口标题
window_title = "alt:V Multiplayer"
# 获取窗口句柄
hwnd = win32gui.FindWindow(None, window_title)

if hwnd != 0:
    # 指定保存文件名
    output_filename = "screenshot_winapi.bmp"
    # 截取窗口截图
    capture_window(hwnd, output_filename)
    print(f"截图已保存为 {output_filename}")
else:
    print(f"未找到标题为 '{window_title}' 的窗口")


background_image = pygame.image.load(output_filename)
# 获取原始图片的大小
original_image_size = background_image.get_size()

# 计算缩放比例，保持横纵比例
aspect_ratio = original_image_size[0] / original_image_size[1]
scaled_width = int(height * aspect_ratio)
background_image = pygame.transform.scale(background_image, (scaled_width, height))


# 存储两个坐标和实际距离的列表
points = []
real_distance = None

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 存储所有点和半径的列表
circles = []

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(points) < 2:
                # 玩家点击两个坐标
                point = pygame.mouse.get_pos()
                print("Point:", point)
                points.append(point)
                
                if len(points) == 2:
                    # 输入实际距离
                    real_distance = float(input("Enter the real distance between the points (in km): "))
                    # 计算比例因子
                    pixel_to_distance_ratio = real_distance / math.dist(points[0], points[1])
                    print("Pixel to Distance Ratio:", pixel_to_distance_ratio)
            else:
                # 玩家输入距离进行绘制圆圈
                if real_distance is not None:
                    # 获取鼠标点击位置作为点A
                    point_a = pygame.mouse.get_pos()
                    print("Point A:", point_a)
                    # 输入目的地距离（实际距离）
                    distance = float(input("Enter destination distance (in km): "))
                    # 计算对应的像素距离
                    pixel_distance = distance / pixel_to_distance_ratio
                    # 将点A和半径添加到列表
                    circles.append((point_a, pixel_distance))
    
    # 清除屏幕
    screen.fill(white)
    
    # 绘制缩放后的背景图片
    screen.blit(background_image, (0, 0))
    
    # 画两个点击点
    for point in points:
        pygame.draw.circle(screen, black, point, 5)  # 以点为中心画小圆点
    
    # 画所有的圆圈
    for circle in circles:
        pygame.draw.circle(screen, black, circle[0], 5)  # 以点A为中心画小圆点
        pygame.draw.circle(screen, red, circle[0], int(circle[1]), 2)  # 以点A为中心画圆圈
    
    # 更新屏幕
    pygame.display.flip()
    time.sleep(0.2)  # 添加适当的延迟，避免频繁截图
