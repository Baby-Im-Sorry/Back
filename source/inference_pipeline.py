import models
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request_id", type=str, required=True)
    args = parser.parse_args()
    return args


def inference_pipeline(Websocket, request_id):
    args = parse_args()
    # TODO: Implement inference pipeline
    temp_str = f"test_{time.time()}"
    models.save_briefing(briefing=temp_str, request_id=args.request_id)
    Websocket.send_text(temp_str)
    # return temp_str
