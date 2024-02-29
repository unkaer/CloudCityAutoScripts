from PPOCR_api import GetOcrApi
from PIL import Image
import time

# 初始化识别器对象，传入 PaddleOCR_json.exe 的路径
ocr = GetOcrApi("PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe")

# 图片路径
image_path = r'img_Winapi.bmp'

# 打开图片
original_image = Image.open(image_path)

# 获取图片宽度和高度
width, height = original_image.size

# 截取左下角1/4 x 和 1/3 y 的部分
left = 0
bottom = int(height * (2/3))
right = int(width * 0.25)
top = height

# 截取图片
cropped_image = original_image.crop((left, bottom, right, top))

# 保存截取后的图片
cropped_image.save(r'D:\github\GTA5-云城\cropped_image.bmp')

# 记录开始时间
start_time = time.time()

# 识别截取后的图片
getObj = ocr.run(r'D:\github\GTA5-云城\cropped_image.bmp')

# 记录结束时间
end_time = time.time()

# 计算运行耗时
elapsed_time = end_time - start_time

# 提取文本信息
text_results = [result['text'] for result in getObj['data']]

# 打印文本信息
print(f'OCR识别文本：\n{" ".join(text_results)}\n')

# 打印运行耗时
print(f'运行耗时：{elapsed_time} 秒')

# 判断是否包含 "按E收杆" 字符
if any("按E收杆" in text for text in text_results):
    print("识别结果中包含\"按E收杆\"字符")
else:
    print("识别结果中不包含\"按E收杆\"字符")
