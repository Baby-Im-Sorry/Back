from datetime import datetime
import pytz
import models
import time


def inference_pipeline(request_id):
    # TODO: Implement inference pipeline
    timestamp = time.time()
    seoul_timezone = pytz.timezone("Asia/Seoul")
    date_time_seoul = datetime.fromtimestamp(timestamp, seoul_timezone)
    formatted_time = date_time_seoul.strftime("%Y-%m-%d %H:%M:%S")
    temp_str = f"test_{formatted_time}"
    models.save_briefing(briefing=temp_str, request_id=request_id)
