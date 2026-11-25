from PIL import Image

def image_to_ascii_text(image_path, new_width=100):
    
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

    img = Image.open(image_path)

    
    width, height = img.size
    new_height = int((height / width) * new_width * 0.5)
    img = img.resize((new_width, new_height)).convert("L")

    
    pixels = img.getdata()
    ascii_str = "".join(
        ASCII_CHARS[p * len(ASCII_CHARS) // 256] for p in pixels
    )

    # Break into lines
    lines = [ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)]
    return "\n".join(lines)


# --- Usage ---
art = image_to_ascii_text("images.jpg", new_width=100)
print(art)

# Save as a .txt file instead of an image (optional)
with open("ascii_art.txt", "w", encoding="utf-8") as f:
    f.write(art)