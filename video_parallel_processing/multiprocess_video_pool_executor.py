import itertools
import traceback

import cv2
import multiprocessing
from multiprocessing import Pool


class MultiprocessVideoPoolExecutor:
    def __init__(self, video_path, processor_factory, intervals, number_of_processes=None):
        self._processor_factory = processor_factory
        self._video_path = video_path
        self._intervals = intervals

        if number_of_processes is None:
            number_of_processes = multiprocessing.cpu_count()

        if len(self._intervals) < number_of_processes:
            self._number_of_processes = len(self._intervals)
        else:
            self._number_of_processes = number_of_processes

    def _process(self, input_parameter):
        interval_start, interval_stop, process_index, metadata = input_parameter
        cap = None
        try:
            cap = cv2.VideoCapture(self._video_path)
            with self._processor_factory(process_index, metadata) as processor:
                cap.set(cv2.CAP_PROP_POS_FRAMES, interval_start)
                results = []
                print(f"start processing interval: {(interval_start, interval_stop)}")
                current_frame = interval_start
                while current_frame <= interval_stop:
                    success, frame = cap.read()
                    result = processor.process(frame, current_frame)
                    results.append(result)
                    current_frame += 1
                print(f"end processing interval: {(interval_start, interval_stop)}")
                return results
        except Exception:
            traceback.print_exc()
            exit(1)
        finally:
            if cap is not None:
                cap.release()

    def start_processes(self, metadata):
        pool = Pool(self._number_of_processes)
        self._intervals.sort(key=lambda x: x[0])
        self._intervals = [(interval[0], interval[1], idx, metadata) for idx, interval in enumerate(self._intervals)]
        self._intervals.sort(key=lambda x: x[1] - x[0])
        results = pool.map(self._process, self._intervals)
        return list(itertools.chain(*results))
