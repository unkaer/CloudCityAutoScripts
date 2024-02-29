import pyautogui
from PIL import ImageGrab
import time
import keyboard

# 在GTAV窗口的左下角区域的坐标
left, top, width, height = 10, 540, 300, 40

# 目标字符串，当左下角出现该字符串时，发送按键e
target_string = "your_target_string"

def capture_screen():
    # 截取屏幕指定区域的图像
    screenshot = ImageGrab.grab(bbox=(left, top, left+width, top+height))
    return screenshot

def main():
    print("程序已启动，按Esc键退出...")
    
    while True:
        try:
            # 获取屏幕截图
            screen = capture_screen()

            # 转换为灰度图像，方便识别
            grayscale_screen = screen.convert('L')

            # 获取图像中的文字
            text = pyautogui.image_to_string(grayscale_screen)

            # 输出识别到的文字
            print("识别到的文字:", text)

            # 如果目标字符串出现在屏幕截图中，发送按键e
            if target_string in text:
                keyboard.press_and_release('e')
                print(f"目标字符串 '{target_string}' 出现，按键e已发送.")

            # 暂停一段时间，避免频繁截图
            time.sleep(1)

        except KeyboardInterrupt:
            print("程序已终止.")
            break

if __name__ == "__main__":
    main()
