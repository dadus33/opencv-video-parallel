# opencv-video-parallel
```python
from video_parallel_processing.video_optimal_multiprocess import VideoOptimalMultiprocess
from video_parallel_processing.processor import Processor

optimal_processor = VideoOptimalMultiprocess(video_path, ffmpeg_path)
results = optimal_processor.start_processes(Processor)

class FrameProcessor(Processor):
    def __init__(self, process_index, metadata):
        super().__init__(process_index, metadata)

    def process(self, frame, frame_number):
        # process the frame
        return result  # will be saved in results list
```
