from PyQt5.QtCore import QObject
import os
import platform
import subprocess
import time
import re
import logging


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, ffmpeg_quality=6):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        system = platform.system().lower()
        ffmpeg_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Utils'))
        if system == 'windows':
            self.ffmpeg_path = os.path.join(ffmpeg_basedir, 'Win/ffmpeg.exe')
            self.ffmpeg_device_config = ['-f', 'gdigrab',
                                         '-framerate', '24',
                                         '-probesize', '60M',
                                         '-i', 'desktop']
        elif system == 'darwin':
            self.ffmpeg_path = os.path.join(ffmpeg_basedir, 'Mac/ffmpeg')
            self.ffmpeg_device_config = ['-f', 'avfoundation',
                                         '-r', '24',
                                         '-pix_fmt', 'yuv420p',
                                         '-i', '1']
        else:
            self.ffmpeg_path = ''
            self.ffmpeg_device_config = []
        self.ffmpeg_path = os.path.abspath(self.ffmpeg_path)
        self.ffmpeg_quality = ffmpeg_quality
        self.ffmpeg_args = ['-vcodec', 'mpeg4',
                            '-q', str(self.ffmpeg_quality),
                            '-f', 'mpegts']
        self.ffmpeg_uri = f'udp://{self.current_ip}@{self.socket_ip}:{self.socket_port}?pkt_size=1316'
        self.ffmpeg_command = [self.ffmpeg_path] + self.ffmpeg_device_config + self.ffmpeg_args + [self.ffmpeg_uri]
        self.ffmpeg_object = None
        self.ffmpeg_log_pattern = r'frame= *(?P<frame>\S+) *fps= *(?P<fps>\S+) *q=.*size= *(?P<size>\S+) *time= *(' \
                                  r'?P<time>\S+) *bitrate= *(?P<bitrate>\S+) *speed= *(?P<speed>\S+) *'
        self.working = False

    def start(self):
        logging.debug(f'FFMpeg command: {" ".join(self.ffmpeg_command)}')
        if not self.ffmpeg_path:
            logging.critical(f'FFMpeg error: this system({platform.system()}) is currently not supported.')
            return
        self.ffmpeg_object = subprocess.Popen(self.ffmpeg_command, shell=True, stdin=subprocess.PIPE, bufsize=64,
                                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        while self.working:
            line = self.ffmpeg_object.stdout.readline().strip()
            if line[:5] == 'frame':
                line = re.match(self.ffmpeg_log_pattern, line)
                if line:
                    logging.debug(f'FFMpeg streaming log: {line.groupdict()}')
        self.ffmpeg_object.stdin.write('q')
        self.ffmpeg_object.communicate()
        self.ffmpeg_object.wait()
