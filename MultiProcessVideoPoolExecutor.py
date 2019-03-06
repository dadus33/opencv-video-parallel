import itertools
import traceback

import cv2
import multiprocessing
from multiprocessing import Pool


class MultiProcessVideoPoolExecutor:
    def __init__(self, video_path, processing_factory, intervals, number_of_processes=None):
        self.processing_factory = processing_factory
        self.video_path = video_path
        self.intervals = intervals

        if number_of_processes is None:
            number_of_processes = multiprocessing.cpu_count()

        if len(self.intervals) < number_of_processes:
            self.number_of_processes = len(self.intervals)
        else:
            self.number_of_processes = number_of_processes

    def _process(self, interval):
        try:
            process_m = self.processing_factory(interval[2])
            cap = cv2.VideoCapture(self.video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, interval[0])
            temp_list = []
            print(f"start processing interval: {interval}")
            current_frame = interval[0]
            while current_frame <= interval[1]:
                success, frame = cap.read()
                result = process_m.process(frame, current_frame)
                temp_list.append(result)
                current_frame += 1
            print(f"end processing interval: {interval}")
            return temp_list
        except Exception:
            traceback.print_exc()
            exit(1)

    def start_processes(self):
        pool = Pool(self.number_of_processes)
        self.intervals.sort(key=lambda x: x[0])
        self.intervals = [(interval[0], interval[1], idx) for idx, interval in enumerate(self.intervals)]
        self.intervals.sort(key=lambda x: x[1] - x[0])
        results = pool.map(self._process, self.intervals)
        return list(itertools.chain(*results))
