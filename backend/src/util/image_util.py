import io
import base64
import random
from PIL import Image, ImageDraw

def text_to_image_base64(text):
    img = Image.new("RGB", (60, 60), color="white")
    d = ImageDraw.Draw(img)

    d.text((25, 20), text, fill="black")

    for _ in range(15):
        x = random.randint(0, 60)
        y = random.randint(0, 60)
        d.point((x, y), fill="gray")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"