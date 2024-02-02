import time
import json
from bson import ObjectId

# 데이터 리스트
briefings = [
    "손님이 늦은 오후에 따뜻한 라떼를 주문하며 창밖을 바라보고 있다.",
    "바리스타가 손님의 주문을 받고 친절하게 인사를 나누고 있다.",
    "카페 안에는 채팅하는 소리와 커피 머신의 소음이 어우러져 있고, 새로운 손님이 들어오고 있다.",
    "젊은 커플이 카페의 아늑한 모퉁이 자리에 앉아 서로의 손을 잡고 있다.",
    "카페에서 진행하는 이벤트에 여러 손님이 참여하고 있으며, 분위기가 활기차다.",
    "한 손님이 카운터에서 직원과 메뉴에 대해 상담하고 있다.",
    "카페의 벽에는 현지 아티스트의 그림이 전시되어 있고, 손님들이 관심을 보이고 있다.",
    "학생 그룹이 카페에서 스터디 모임을 하고 있으며, 커피와 간식을 곁들이고 있다.",
    "손님이 조용한 구석 자리를 찾아 노트북을 펴고 작업을 시작하고 있다.",
    "카페 직원이 신선한 커피콩을 갈고 있으며, 커피의 향이 공간을 채우고 있다.",
    "주말 오후, 가족 단위의 손님이 느긋하게 차를 마시며 대화를 나누고 있다.",
    "카페에서 샌드위치와 샐러드 메뉴를 새로 출시했으며, 손님들이 관심을 보이고 있다.",
    "손님이 장시간 독서를 하며 가끔 커피를 마시고 있다.",
    "카페의 작은 무대에서 로컬 밴드가 공연을 하고 있으며, 관객들이 즐거워하고 있다.",
    "오후에 커피를 마시며 휴식을 취하는 사람들로 카페가 붐비고 있다.",
    "바리스타가 손님에게 시즌 한정 음료를 추천하고 있다.",
    "어린이를 동반한 손님이 아이에게 핫 초코를 주문하며 책을 읽어주고 있다.",
    "카페의 테라스에서 사람들이 햇볕을 즐기며 차를 마시고 있다.",
    "바리스타가 손님과 이야기를 나누며 친근하게 커피를 내리고 있다.",
    "카페 직원이 마감 시간에 맞춰 청소를 하고 소등 준비를 하고 있다.",
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
    request_id = "65bc7b763d76950d3c62aca2"
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
