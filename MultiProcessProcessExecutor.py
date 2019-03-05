import cv2
import multiprocessing


class MultiProcessProcessExecutor:
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

    def _process(self, video_path, intervals, return_list):
        process_m = self.processing_factory()
        cap = cv2.VideoCapture(video_path)
        temp_list = []
        for interval in intervals:
            print(f"start processing interval: {interval}")
            current_frame = interval[0]
            while current_frame <= interval[1]:
                success, frame = cap.read()
                current_frame += 1
                result = process_m.process(frame)
                temp_list.append(result)
            print(f"end processing interval: {interval}")
        return_list.extend(temp_list)

    def start_processes(self):
        interval_lengths = [((start, stop), stop - start) for (start, stop) in self.intervals]
        interval_lengths = sorted(interval_lengths, key=lambda a: a[1])

        process_intervals = [[] for _ in range(self.number_of_processes)]
        added_intervals = 0
        while added_intervals <= len(interval_lengths):
            for i in range(min(self.number_of_processes, len(interval_lengths)-added_intervals+1)):
                process_intervals[i].append(interval_lengths[added_intervals - 1][0])
                added_intervals += 1
            if added_intervals == len(interval_lengths):
                break
            for i in range(min(self.number_of_processes, len(interval_lengths)-added_intervals+1)):
                process_intervals[self.number_of_processes - 1 - i].append(interval_lengths[added_intervals - 1][0])
                added_intervals += 1

        jobs = []
        return_list = multiprocessing.Manager().list()
        for i in range(self.number_of_processes):
            p = multiprocessing.Process(target=self._process,
                                        args=(self.video_path, process_intervals[i], return_list))
            p.start()
            jobs.append(p)

        for proc in jobs:
            proc.join()

        return return_list
