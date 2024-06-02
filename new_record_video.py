import cv2
from collections import deque
import threading
import time
import os
from datetime import datetime

BUFFER_SIZE_MULT = 3


class Recorder:
    def __init__(self, resolution=(640, 480), frame_rate=30):
        self.seconds = 0
        self.resolution = resolution
        self.frame_rate = frame_rate
        self.start_recording = False
        self.time_diff = 0  # sec
        self.running = True
        #self.camera_thread = None

    def start(self, seconds):
        self.seconds = seconds
        self.buffer_size = int(
            self.frame_rate * self.seconds * 2 * BUFFER_SIZE_MULT
        )  # 2*5s * buffer num
        self.frame_buffer = deque(maxlen=self.buffer_size)

        # Try different backends and device indices
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2, cv2.CAP_AVFOUNDATION, cv2.CAP_ANY]
        device_indices = range(5)  # Try first 5 indices

        self.cap = None
        for backend_index, backend in enumerate(backends):
            for device_index in device_indices:
                cap = cv2.VideoCapture(device_index, backend)
                if cap.isOpened():
                    self.cap = cap
                    print(f"Camera opened with backend index {backend_index} ({backend}) and device index {device_index}")
                    break
            if self.cap is not None:
                break

        if self.cap is None or not self.cap.isOpened():
            print("Error: Camera not opened")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Frame", -10000, -10000)

        self.camera_thread = threading.Thread(target=self.__record_video)
        self.camera_thread.start()
    
    def close(self):
        if hasattr(self, "camera_thread") and self.camera_thread.is_alive():
            self.running = False
            self.camera_thread.join()
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Resources have been released and windows destroyed.")

    def record(self, moment):
        now = time.time()
        self.time_diff = int(now - moment)
        self.start_recording = True

    def __record_video(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            self.frame_buffer.append(frame)

            if self.start_recording:
                frames_needed = (
                    self.seconds * self.frame_rate - self.time_diff * self.frame_rate
                )
                if frames_needed > 0:
                    for _ in range(frames_needed):
                        ret, frame = self.cap.read()
                        if not ret:
                            print("Error: Failed to capture frame")
                            continue
                        self.frame_buffer.append(frame)
                    self.time_diff += int(frames_needed / self.frame_rate)
                break

    def save_the_file(self, bluff_category, player_id):
        os.makedirs('videos', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = ".mp4"

        size = len(self.frame_buffer)
        frame_diff = int(self.time_diff * self.frame_rate)
        if size / self.frame_rate < self.seconds + self.time_diff:
            print(
                f"Buffer size in seconds: {size / self.frame_rate}; Required: {self.seconds + self.time_diff}"
            )
            return

        filename = f"videos/{timestamp}_{bluff_category}_{player_id}{extension}"

        fourcc = cv2.VideoWriter_fourcc(*"MP4v")
        out = cv2.VideoWriter(filename, fourcc, self.frame_rate, self.resolution)

        i = 0
        for frame in self.frame_buffer:
            if i > (size - frame_diff - self.seconds * self.frame_rate) and i < (
                size - frame_diff + self.seconds * self.frame_rate
            ):
                out.write(frame)
            i += 1

        self.cap.release()
        out.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recorder = Recorder()
    recorder.start(3)
    for i in range(8):
        time.sleep(1)
        print(i)
    recorder.record(time.time())
    recorder.camera_thread.join()
    recorder.save_the_file("BCB", 2)
    recorder.start_recording = False


