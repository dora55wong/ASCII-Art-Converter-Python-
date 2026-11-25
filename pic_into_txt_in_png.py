from PIL import Image, ImageDraw, ImageFont

def image_to_ascii_image(image_path, output_path="ascii_art.png",
                         new_width=120, font_size=10, bg_color=(0, 0, 0),
                         text_color=(255, 255, 255)):
    # 1. 定義 ASCII 字元集（從暗到亮，或從亮到暗）
    # 使用常見的密度漸變字元集
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    
    # 2. 載入圖片並轉為灰階
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"無法開啟圖片: {e}")
        return

    # 計算縮放比例，保持長寬比 (因為終端機字元通常高度是寬度的 2 倍)
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55) # 0.55 是校正係數
    
    img = img.resize((new_width, new_height))
    img = img.convert("L") # 轉為灰階 (L mode)

    # 3. 將像素灰階值映射到 ASCII 字元
    pixels = img.getdata()
    ascii_str = ""
    for pixel in pixels:
        # 將 0-255 的灰階值映射到 0 到 len(ASCII_CHARS)-1 的索引
        # 255 是白色，0 是黑色
        index = pixel * len(ASCII_CHARS) // 256
        ascii_str += ASCII_CHARS[index]
    
    # 將一維字串轉換為二維（帶換行的）字串
    ascii_img_str = ""
    for i in range(0, len(ascii_str), new_width):
        ascii_img_str += ascii_str[i:i+new_width] + "\n"

    # 4. 將 ASCII 文字畫成圖片 (確保輸出成圖片而不是純文字)
    # 尋找等寬字型 (Monospace)
    font_paths = [
        "consola.ttf", # Windows
        "/System/Library/Fonts/Menlo.ttc", # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" # Linux
    ]
    font = None
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except OSError:
            continue
    
    if font is None:
        font = ImageFont.load_default()

    # 計算輸出圖片尺寸
    # 使用 getbbox 獲取字元大小
    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1] + 2 # 加上行距
    
    img_w = new_width * char_width
    img_h = new_height * char_height

    # 建立新的畫布並繪製文字
    out_img = Image.new("RGB", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(out_img)

    y = 0
    for line in ascii_img_str.split("\n"):
        draw.text((0, y), line, font=font, fill=text_color)
        y += char_height

    out_img.save(output_path)
    print(f"已儲存 ASCII 圖片: {output_path}")

# --- 使用範例 ---
# 請將 'your_image.jpg' 替換成你電腦中的圖片路徑
# 建議先找一張背景乾淨、對比度高的照片效果最好
image_to_ascii_image("Snoopy.jpg", "ascii_output.png", 
                     new_width=120, font_size=12)