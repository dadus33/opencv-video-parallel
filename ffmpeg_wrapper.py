import os
import re
import subprocess


class FfmpegWrapper:
    length_frames_regex = r"frame *\= *(?P<frames>[\d\.]+).*"

    def __init__(self, ffmpeg_path):
        self.ffmpeg_path = ffmpeg_path

    @staticmethod
    def _read_lines(process):
        while True:
            process.stderr.flush()
            lines = process.stderr.readline().decode('utf-8').splitlines()
            if process.poll() is not None:
                if len(lines) == 0:
                    break
            for line in lines:
                yield line
        process.poll()

    @classmethod
    def _parse_frame_count(cls, lines):
        lines = list(lines)
        for line in reversed(list(lines)):
            frames_match = re.match(cls.length_frames_regex, line)
            if frames_match:
                frames_match = frames_match.groupdict()
                return int(frames_match["frames"])

    @staticmethod
    def _run_bash(command):
        exit_code = os.system(command)
        if exit_code != 0:
            raise Exception(f"ffmpeg exit code:{exit_code}")

    @staticmethod
    def _get_absolute_path(paths):
        if type(paths) is list:
            return [os.path.abspath(path) for path in paths]
        return os.path.abspath(paths)

    def get_length_frames(self, video_path):
        video_path = self._get_absolute_path(video_path)
        ffmpeg_cmd = f"{self.ffmpeg_path} -i {video_path} -map 0:v:0 -c copy -f null -"
        process = subprocess.Popen(ffmpeg_cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return self._parse_frame_count(self._read_lines(process))
