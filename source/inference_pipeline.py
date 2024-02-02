from datetime import datetime
import os
from dotenv import load_dotenv
import pytz
import models
import time
import pyrealsense2 as rs
import numpy as np
import cv2
import yolo_basic


class Realsense:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()


def inference_pipeline(username, request_id):
    cam = Realsense()
    start = time.time()
    res = []
    while True:
        _, _, img = cam.get_frame()
        try:
            caption = yolo_basic.main(username, img)
            res.append(caption)
        except:
            print("error")
        if time.time() - start > 1:
            break  # 10초가 지나면 while 루프 종료
    # timestamp = time.time()
    # seoul_timezone = pytz.timezone("Asia/Seoul")
    # date_time_seoul = datetime.fromtimestamp(timestamp, seoul_timezone)
    # formatted_time = date_time_seoul.strftime("%Y-%m-%d %H:%M:%S")
    # temp_str = f"test_{formatted_time}"

    models.save_briefing(request_id,briefing=res[-1])
    #models.save_briefing(request_id, temp_str)

