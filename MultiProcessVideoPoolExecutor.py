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

    def _process(self, input_parameter):
        interval_start, interval_stop, process_index, metadata = input_parameter
        cap = None
        try:
            cap = cv2.VideoCapture(self.video_path)
            process_m = self.processing_factory(process_index, metadata)

            cap.set(cv2.CAP_PROP_POS_FRAMES, interval_start)
            temp_list = []
            print(f"start processing interval: {(interval_start, interval_stop)}")
            current_frame = interval_start
            while current_frame <= interval_stop:
                success, frame = cap.read()
                result = process_m.process(frame, current_frame)
                temp_list.append(result)
                current_frame += 1
            print(f"end processing interval: {(interval_start, interval_stop)}")
            return temp_list
        except Exception:
            traceback.print_exc()
            exit(1)
        finally:
            if cap is not None:
                cap.release()

    def start_processes(self, metadata):
        pool = Pool(self.number_of_processes)
        self.intervals.sort(key=lambda x: x[0])
        self.intervals = [(interval[0], interval[1], idx, metadata) for idx, interval in enumerate(self.intervals)]
        self.intervals.sort(key=lambda x: x[1] - x[0])
        results = pool.map(self._process, self.intervals)
        return list(itertools.chain(*results))
