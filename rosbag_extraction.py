import numpy as np
from rosbags.highlevel import AnyReader
import cv2
from pathlib import Path

bag_path = Path("./comp4_2025-05-20-16-33-03.bag")
topic_name = '/d455_front/camera/color/image_rect_color'

with AnyReader([bag_path]) as reader:
    connections = [c for c in reader.connections if c.topic == topic_name]

    out = None

    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = reader.deserialize(rawdata, connection.msgtype)

        # Check if this is a compressed image
        if hasattr(msg, "format"):  # sensor_msgs/CompressedImage
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
        else:  # sensor_msgs/Image (raw)
            # Convert raw bytes to a numpy array
            dtype = np.uint8  # usually uint8, check msg.encoding
            # reshape: height x width x channels
            if 'rgb8' in msg.encoding or 'bgr8' in msg.encoding:
                channels = 3
            elif 'mono8' in msg.encoding:
                channels = 1
            else:
                raise ValueError(f"Unsupported encoding: {msg.encoding}")

            frame = np.frombuffer(msg.data, dtype=dtype).reshape(msg.height, msg.width, channels)

            # If mono, convert to BGR for VideoWriter
            if channels == 1:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Initialize video writer dynamically
        if out is None:
            height, width = frame.shape[:2]
            out = cv2.VideoWriter('output.mp4',
                                  cv2.VideoWriter_fourcc(*'mp4v'),
                                  30,
                                  (width, height))

        out.write(frame)

    if out:
        out.release()
        print("✅ Saved video as output.mp4")
