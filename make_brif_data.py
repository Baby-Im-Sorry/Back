import time
import json
from bson import ObjectId

# 데이터 리스트
briefings = [
    "현재 매장에는 한 명의 남자가 있습니다.",
    "현재 매장 내부에는 3명의 남자가 있습니다.",
    "현재 매장 내부에는 3명의 여자가 있습니다.",
    "현재 매장 내부에는 1명의 남자와 2명의 여자가 있습니다.",
    "매장 내부에는 현재 한명의 남자와 3명의 여자가 있습니다.",
    "매장 내부에는 1명의 남자와 2명의 여자가 있습니다.",
    "현재 매장 내부에는 1명의 남자가 있습니다.",
    "현재 매장 내부에는 2명의 여자가 있습니다",
    "현재 매장 내부에는 4명의 남자와 2명의 여자가 있습니다.",
    "현재 매장 내부에는 15명의 남자가 있습니다.",
    "현재 매장 내부에는 3명의 여자가 있습니다.",
    "현재 매장 내부에는 10명의 남자가 있습니다.",
    "현재 매장 내부에는 5명의 남자가 있습니다.",
    "현재 매장 내부에는 3명의 남자가 있습니다.",
    "현재 매장 내부에는 15명의 남자가 있습니다.",
    "현재 매장 내부에는 13명의 남자가 있습니다.",
    "현재 매장 내부에는 2명의 남자가 있습니다.",
    "현재 매장 내부에는 3명의 남자가 있습니다.",
    "현재 매장 내부에는 1명의 남자가 있습니다.",
    "현재 매장 내부에는 2명의 여자가 있습니다.",
]

data_objects = []

# briefing id 생성자
def generate_custom_objectid(counter):
    timestamp = int(time.time())
    random_bytes = ObjectId().binary[4:9]
    counter_bytes = counter.to_bytes(3, byteorder='big')
    return ObjectId(bytes([timestamp >> 24 & 0xFF, timestamp >> 16 & 0xFF, timestamp >> 8 & 0xFF, timestamp & 0xFF]) + random_bytes + counter_bytes)

counter = 0
data_objects = []
for briefing in briefings:
    request_id = "65bc7b763d76950d3c62aca5"
    briefing_id = generate_custom_objectid(counter)
    
    data_objects.append({
        "_id": {"$oid": briefing_id},
        "request_id": {"$oid": ObjectId(request_id)},
        "briefing": briefing
    })
    counter += 1

# 파일에 데이터 객체들을 JSON 형식으로 쓰기
with open('sample_brif_data.json', 'w', encoding='utf-8') as file:
    file.write("[\n")
    for index, obj in enumerate(data_objects):
        obj['_id'] = str(obj['_id']['$oid'])
        obj['request_id'] = str(obj['request_id']['$oid'])
        # 마지막 객체인 경우 쉼표를 추가하지 않음
        if index == len(data_objects) - 1:
            file.write(json.dumps(obj, ensure_ascii=False) + "\n")
        else:
            file.write(json.dumps(obj, ensure_ascii=False) + ",\n")
    file.write("]")
