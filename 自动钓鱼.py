import win32gui, win32ui, win32con, win32print, win32api
from win32.win32api import GetSystemMetrics
from PPOCR_api import GetOcrApi
from PIL import Image
import re
import io
import time
import pygame
import datetime

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
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def simulate_key_press(hWnd, key_code, Sleep_time=112):
    # 模拟按下指定键
    win32api.PostMessage(hWnd, win32con.WM_KEYDOWN, key_code, 0)
    # 等待一些时间，可以根据需要调整
    win32api.Sleep(Sleep_time)
    # 模拟释放指定键
    win32api.PostMessage(hWnd, win32con.WM_KEYUP, key_code, 0)

def play_mp3(file_path):
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the loaded MP3 file
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.quit()

# 函数用于向文件中写入钓鱼获得物品的信息
def write_to_file(item_name):
    # 定义文件名
    file_name = 'guaji_log.txt'
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 打开文件，以追加模式写入，指定编码为UTF-8
    with open(file_name, 'a', encoding='utf-8') as file:
        # 写入时间和物品信息
        file.write(f'{current_time} - 获得物品：{item_name}\n')

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
width = int(width * screen_scale_rate)

height = bot - top
height = int(height * screen_scale_rate)
print(width)
print(height)

# 初始化识别器对象，传入 PaddleOCR_json.exe 的路径
ocr = GetOcrApi("PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe")
argument = {"config_path": "models/config_chinese.txt"}  # 指定使用简体中文识别库

while True:  # 无限循环
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

    # 截取图片并保存到内存中
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    # 截取左下角1/4 x 和 1/3 y 的部分
    left = 0
    bottom = int(height * (2/3))
    right = int(width * 0.25)
    top = height

    # 截取图片
    cropped_image = img.crop((left, bottom, right, top))

    # 将 PIL Image 转为字节流
    image_byte_array = io.BytesIO()
    cropped_image.save(image_byte_array, format='PNG')
    image_bytes = image_byte_array.getvalue()

    # 记录开始时间
    start_time = time.time()

    # 识别截取后的图片字节流
    getObj = ocr.runBytes(image_bytes)

    # 记录结束时间
    end_time = time.time()

    # 计算运行耗时
    elapsed_time = end_time - start_time

    # 提取文本信息
    if 'data' in getObj and isinstance(getObj['data'], list):
        text_results = [result['text'] for result in getObj['data']]
        text_string = " ".join(text_results)
        # 打印文本信息
        # print(f'OCR识别文本：\n{text_string}\n')
    else:
        text_string=""
        # print('OCR未成功识别文字')

    # 打印运行耗时
    # print(f'运行耗时：{elapsed_time} 秒')

    # 判断是否包含 "背包" 字符
    if any("背包" in text for text in text_results):
        # 使用正则表达式提取未加工的物品名称
        match = re.search(r"未加工的(\S+)", text_string)
        # 输出提取的物品名称
        if match:
            unprocessed_item_name = match.group(1).strip()
            print(f'获得物品：{unprocessed_item_name}')
        else:
            match = re.search(r"背包增加了1个(\S+)", text_string)
            if match:
                unprocessed_item_name = match.group(1).strip()
                print(f'获得物品：{unprocessed_item_name}')
            else:
                unprocessed_item_name=""
                print(f'等待字体消失')
        write_to_file(unprocessed_item_name)
        if any("最大" in text for text in text_results):
            print("最大")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            play_mp3(r'music\钓满10条鱼了.mp3')
        time.sleep(5) # 等待字体消失
    else:
        if any("收杆" in text for text in text_results):
            print("收杆")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            time.sleep(0.8)
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
        if any("采集" in text for text in text_results):
            print("采集")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            time.sleep(0.8)
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
        if any("开始钓鱼" in text for text in text_results):
            print("开始钓鱼")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            play_mp3(r'music\开始钓鱼.mp3')
            time.sleep(5)
        if any("开始挖矿" in text for text in text_results):
            print("开始挖矿")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            play_mp3(r'music\开始挖矿.mp3')
            time.sleep(5)
        if any("没有鱼饵" in text for text in text_results):
            print("没有鱼饵了")
            play_mp3(r'music\没有鱼饵了.mp3')
            time.sleep(5)
        if any("物品加工" in text for text in text_results):
            print("物品加工")
            simulate_key_press(hWnd, 0x45, Sleep_time=112)  # E 键
            play_mp3(r'music\加工完成.mp3')
        if any("今天钓鱼太多次了" in text for text in text_results):
            print("今天钓鱼太多次了")
            play_mp3(r'music\今日钓鱼已达上限.mp3')
            time.sleep(999)

    time.sleep(1)  # 添加适当的延迟，避免频繁截图