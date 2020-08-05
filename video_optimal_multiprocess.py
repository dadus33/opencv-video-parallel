import multiprocessing

import cv2

from multiprocess_video_pool_executor import MultiprocessVideoPoolExecutor
from ffmpeg_wrapper import FfmpegWrapper
from processor import Processor


class VideoOptimalMultiprocess:

    def __init__(self, video_path, ffmpeg_path, process_count=None, intervals_per_process=4):
        self._intervals_per_process = intervals_per_process
        self._video_path = video_path
        self._ffmpeg_wrapper = FfmpegWrapper(ffmpeg_path)

        self._frame_count = self._ffmpeg_wrapper.get_length_frames(video_path)
        cap = cv2.VideoCapture(video_path)
        self._fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        if process_count is None:
            self._process_count = multiprocessing.cpu_count()
        else:
            self._process_count = process_count

    def get_frame(self, seconds):
        return int(seconds * self._fps)

    def start_processes(self, processor_factory: Processor, start_frame=0, end_frame=None, metadata=None):
        if end_frame is None:
            end_frame = self._frame_count

        total_frames = end_frame - start_frame + 1  # both ends included
        intervals_len = self._process_count * self._intervals_per_process
        frames_per_interval = int(total_frames / intervals_len)
        extra_frames_last_interval = int(total_frames % intervals_len)
        intervals_start = [start_frame + (frames_per_interval * interval_idx) for interval_idx in range(intervals_len)]
        intervals = [(start, start + frames_per_interval - 1) for start in intervals_start]
        intervals[-1] = (intervals[-1][0], intervals[-1][1] + extra_frames_last_interval)

        print(f"start processing intervals: {intervals}, on {self._process_count} cpu's")
        multi_process_runner = MultiprocessVideoPoolExecutor(self._video_path, processor_factory, intervals, self._process_count)
        return multi_process_runner.start_processes(metadata)
