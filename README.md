# opencv-video-parallel
```python
optimal_processor = VideoOptimalMultiProcess(video_path)
lst = optimal_processor.start_processes(Signature_p)

class Signature_p:
    def __init__(self):
        self.signature = ImageSignature()

    def process(self, frame):
        return self.signature.generate_signature(frame)
```
