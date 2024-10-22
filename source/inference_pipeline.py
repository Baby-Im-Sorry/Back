from .models import save_briefing
import time
import datetime
import pytz
# import numpy as np
# from .yolo_basic import main
# import pyrealsense2 as rs


def inference_pipeline(username, request_id):
    timestamp = time.time()
    seoul_timezone = pytz.timezone("Asia/Seoul")
    date_time_seoul = datetime.fromtimestamp(timestamp, seoul_timezone)
    formatted_time = date_time_seoul.strftime("%Y-%m-%d %H:%M:%S")
    temp_str = f"현재시각: {formatted_time}"
    save_briefing(request_id, temp_str)


# realsense 관련 코드
# class Realsense:
#     def __init__(self):
#         self.pipeline = rs.pipeline()
#         config = rs.config()
#         config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
#         self.pipeline.start(config)

#     def get_frame(self):
#         frames = self.pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()
#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#         if not depth_frame or not color_frame:
#             return False, None, None
#         return True, depth_image, color_image

#     def release(self):
#         self.pipeline.stop()


# def inference_pipeline(username, request_id):
    # cam = Realsense()
    # start = time.time()
    # res = []
    # while True:
    #     _, _, img = cam.get_frame()
    #     try:
    #         caption = main(username, img)
    #         res.append(caption)
    #     except:
    #         print("error")
    #     if time.time() - start > 1:
    #         break
    # save_briefing(request_id, briefing=res[-1])