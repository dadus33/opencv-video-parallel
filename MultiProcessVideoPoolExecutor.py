import itertools

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
        process_m = self.processing_factory()
        cap = cv2.VideoCapture(self.video_path)
        temp_list = []
        print(f"start processing interval: {interval}")
        current_frame = interval[0]
        while current_frame <= interval[1]:
            success, frame = cap.read()
            current_frame += 1
            result = process_m.process(frame)
            temp_list.append(result)
        print(f"end processing interval: {interval}")
        return temp_list

    def start_processes(self):
        pool = Pool(self.number_of_processes)
        results = pool.map(self._process, self.intervals)
        return list(itertools.chain(*results))
