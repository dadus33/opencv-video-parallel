import multiprocessing

import cv2

from VideoParallelProcessing.MultiProcessVideoPoolExecutor import MultiProcessVideoPoolExecutor


class VideoOptimalMultiProcess:

    def __init__(self, video_path, process_count=None, intervals_per_process=4):
        self.intervals_per_process = intervals_per_process
        self.video_path = video_path
        cap = cv2.VideoCapture(video_path)
        self.frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        cap.release()

        if process_count is None:
            self.process_count = multiprocessing.cpu_count()
        else:
            self.process_count = process_count

    def get_frame(self, seconds):
        return int(seconds*self.fps)

    def start_processes(self, processing_factory, start_frame=0, end_frame=None):
        if end_frame is None:
            end_frame = self.frame_count

        total_frames = end_frame-start_frame
        intervals_len = (self.process_count * self.intervals_per_process)
        frames_per_interval = int(total_frames/intervals_len)
        extra_frames_last_interval = int(total_frames % intervals_len)
        intervals_start = [start_frame + (frames_per_interval * interval_idx) for interval_idx in range(intervals_len)]
        intervals = [(start, start + frames_per_interval - 1) for start in intervals_start]
        intervals[-1] = (intervals[-1][0], intervals[-1][1] + extra_frames_last_interval)

        print(f"start processing intervals:{intervals}, on {self.process_count} cpu's")
        multi_process_runner = MultiProcessVideoPoolExecutor(self.video_path, processing_factory, intervals, self.process_count)
        return multi_process_runner.start_processes()
