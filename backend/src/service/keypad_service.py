import random
import uuid

from util.image_util import text_to_image_base64
from util.hash_util import make_hash

EMPTY_TOKEN = "empty"

def generate_keypad():
    session_id = str(uuid.uuid4())

    nums = [str(i) for i in range(10)] + [" ", " "]
    random.shuffle(nums)

    keypad_data = []
    for num in nums:
        if num == " ":
            img_data = text_to_image_base64(" ")
            hash_value = EMPTY_TOKEN
        else:
            img_data = text_to_image_base64(num)
            hash_value = make_hash(session_id, num)

        keypad_data.append({
            "image": img_data,
            "hash": hash_value
        })

    return {"session_id": session_id, "layout": keypad_data}