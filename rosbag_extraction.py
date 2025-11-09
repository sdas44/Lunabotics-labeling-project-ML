import numpy as np
from rosbags.highlevel import AnyReader
import cv2
import os
from pathlib import Path

bag_path = Path("comp2_2025-05-17-10-57-10.bag")

frames_dir = Path("./frames")
frames_dir.mkdir(exist_ok=True)  # Create frames directory if it doesn't exist
topic_name = '/d455_front/camera/color/image_rect_color'

with AnyReader([bag_path]) as reader:
    connections = [c for c in reader.connections if c.topic == topic_name]

    frame_count = 0  # Initialize frame counter

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
                
        # Save the frame as a PNG file with sequential numbering
        frame_path = frames_dir / f"frame_{frame_count:04d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_count += 1

    if out:
        out.release()
        print("✅ Saved video as output.mp4")
    print(f"✅ Saved {frame_count} frames to {frames_dir}")
