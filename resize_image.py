from PIL import Image

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        resized_img = img.resize(size, Image.LANCZOS)
        resized_img.save(output_path)

# 調整圖片尺寸為 2500x1686 像素
resize_image(r"D:\程式設計3\linebot_finalproject\new_richmenu.png", r"D:\程式設計3\linebot_finalproject\new_richmenu_resized.png", (2500, 1686))