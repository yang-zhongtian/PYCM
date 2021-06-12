from PyQt5.QtCore import QObject
import subprocess
import time
import re


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, ffmpeg_path, ffmpeg_packet_size=1316):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.ffmpeg_path = ffmpeg_path
        self.ffmpeg_device_config = ['-f', 'gdigrab',
                                     '-framerate', '24',
                                     '-probesize', '60M',
                                     '-i', 'desktop']
        self.ffmpeg_args = ['-preset', 'ultrafast',
                            '-vcodec', 'libx264',
                            '-tune', 'zerolatency',
                            '-b:v', '900k',
                            '-f', 'h264']
        self.ffmpeg_uri = f'udp://{self.current_ip}@{self.socket_ip}:{self.socket_port}?pkt_size={ffmpeg_packet_size}'
        self.ffmpeg_command = [self.ffmpeg_path] + self.ffmpeg_device_config + self.ffmpeg_args + [self.ffmpeg_uri]
        self.ffmpeg_object = None
        self.ffmpeg_log_pattern = r'frame= *(?P<frame>\S+) *fps= *(?P<fps>\S+) *q=.*size= *(?P<size>\S+) *time= *(' \
                                  r'?P<time>\S+) *bitrate= *(?P<bitrate>\S+) *speed= *(?P<speed>\S+) *'
        self.working = True

    def start(self):
        # print(" ".join(self.ffmpeg_command)) # Enable this for debug
        self.ffmpeg_object = subprocess.Popen(self.ffmpeg_command, shell=True, stdin=subprocess.PIPE, bufsize=64,
                                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        while self.working:
            line = self.ffmpeg_object.stdout.readline().strip()
            if line[:5] == 'frame':
                line = re.match(self.ffmpeg_log_pattern, line)
        self.ffmpeg_object.stdin.write('q')
        self.ffmpeg_object.communicate()
        self.ffmpeg_object.wait()
