from ultralytics import YOLO
from openai import OpenAI
from dotenv import load_dotenv
import os
from models import get_custom

Yolo_classes = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    4: "airplane",
    5: "bus",
    6: "train",
    7: "truck",
    8: "boat",
    9: "traffic light",
    10: "fire hydrant",
    11: "stop sign",
    12: "parking meter",
    13: "bench",
    14: "bird",
    15: "cat",
    16: "dog",
    17: "horse",
    18: "sheep",
    19: "cow",
    20: "elephant",
    21: "bear",
    22: "zebra",
    23: "giraffe",
    24: "backpack",
    25: "umbrella",
    26: "handbag",
    27: "tie",
    28: "suitcase",
    29: "frisbee",
    30: "skis",
    31: "snowboard",
    32: "sports ball",
    33: "kite",
    34: "baseball bat",
    35: "baseball glove",
    36: "skateboard",
    37: "surfboard",
    38: "tennis racket",
    39: "bottle",
    40: "wine glass",
    41: "cup",
    42: "fork",
    43: "knife",
    44: "spoon",
    45: "bowl",
    46: "banana",
    47: "apple",
    48: "sandwich",
    49: "orange",
    50: "broccoli",
    51: "carrot",
    52: "hot dog",
    53: "pizza",
    54: "donut",
    55: "cake",
    56: "chair",
    57: "couch",
    58: "potted plant",
    59: "bed",
    60: "dining table",
    61: "toilet",
    62: "tv",
    63: "laptop",
    64: "mouse",
    65: "remote",
    66: "keyboard",
    67: "cell phone",
    68: "microwave",
    69: "oven",
    70: "toaster",
    71: "sink",
    72: "refrigerator",
    73: "book",
    74: "clock",
    75: "vase",
    76: "scissors",
    77: "teddy bear",
    78: "hair drier",
    79: "toothbrush",
}

dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), ".env.production"
)
load_dotenv(dotenv_path)


def get_yolo_inference(img):
    model = YOLO("yolov8n.pt")
    result = model(img)
    result_tensor = result[0].boxes.cls
    result_class = result_tensor.tolist()
    for i, j in enumerate(result_class):
        temp = Yolo_classes.__getitem__(j)
        result_class[i] = temp

    count_class = {}
    for i in result_class:
        try:
            count_class[i] += 1
        except:
            count_class[i] = 1
    return count_class


def format_class_counts(count_class):
    try:
        formatted_string = ""
        for j, k in count_class.items():
            formatted_string += f"{j}는 {str(k)}개 "

        return formatted_string
    except:
        formatted_string = "없음"

        return formatted_string


def get_caption(formatted_string, user_custom):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    print(user_custom)

    promt = f"""
    아래 제공된 데이터는 현재 매장 내부에 있는 Class들인데, 지금 매장 내부의 상황을 '최대한 간결하게' 설명해줘. 객체가 없다면 없다고 해줘.
    출력 형식은 {user_custom} 의 값들을 참고해줘.
    만약 user_custom이 빈 리스트라면 클래스만 참고해서 캡션을 만들어 줘.
    --------------------------------
    {formatted_string}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{promt}",
            }
        ],
        model="gpt-4-0125-preview",
    )

    return chat_completion.choices[0].message.content


def main(username, img):
    count_class = get_yolo_inference(img)
    formatted_string = format_class_counts(count_class)
    user_custom = get_custom(username)
    caption = get_caption(formatted_string, user_custom)
    return caption
