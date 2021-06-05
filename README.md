# Python Class Management System
[![Github Build](https://github.com/yangzhongtian001/PYCM/workflows/PYCM-Build/badge.svg)](https://github.com/yangzhongtian001/PYCM/releases) [![GitHub issues](https://img.shields.io/github/issues/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/issues) [![GitHub forks](https://img.shields.io/github/forks/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/network) [![GitHub stars](https://img.shields.io/github/stars/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/stargazers) [![GitHub license](https://img.shields.io/github/license/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/yangzhongtian001/PYCM)

## Mirror Repository
* [Github(Master)](https://github.com/yangzhongtian001/PYCM)
* [Gitee(Mirror)](https://gitee.com/yangzhongtian/PYCM)
* [Gitlab(Mirror)](https://gitlab.com/yangzhongtian/PYCM)
* [Coding(Mirror)](https://yangzhongtian.coding.net/public/PYCM/PYCM/git/files)

## Introduction
This program is a e-classroom management system written by python. It contains both client(student side) and console(teacher size). GUI written by PyQt5, supporting all platforms.

## Features
* [x] Auto LAN discover
* [x] Console screen broadcasting
* [ ] Cient screen remote control by Console
* [ ] Console side file handout
* [ ] Screen locking
* [x] Client side file submitting
* [x] Console side message sending. Supporting both private & public messages.
* [ ] Client notify
* [x] Nuitka packaging

## Structure
```
|-Client: Used for muti users, ex: students, visitors.
|-Console: Used for one host user, ex: teacher, host.
|-Public: [DEPRECATED] Some files and algorithms for use.
```

## Config file
### Admin.json@console
This file is used for console login authentication
```json
{
  "username": "username for logging in Console",
  "password": "MD5 of password for logging in Console"
}
```

### Client.json@console
This file is used to store all client configurations.
```json
{
  "FileUploadPath": "The directory for storing client uploaded files",
  "ClientLabel": {
    "A client mac address": "the label to show in console dashboard",
    "Another client mac address": "the label to show in console dashboard"
  },
  "AvailableRemoteCommands": {
    "A command display name": "command",
    "Another command display name": "command"
  }
}
```

### Network.json@console&client
This file is used to store network configurations for both console and client.
**The settings bellow "NetworkDiscover" is not adviced to be modified.**
```json
{
  "Local": {
    "Device": "The name of default network device"
  },
  "NetworkDiscover": {
    "IP": "224.50.50.50",
    "Port": 4088,
    "Interval": 5
  },
  "ClassBroadcast": {
    "IP": "225.2.2.19",
    "Port": 4089,
    "Buffer": 65500
  },
  "PrivateMessage": {
    "Port": 4091,
    "Buffer": 32768
  },
  "ScreenBroadcast": {
    "IP": "225.2.2.21",
    "Port": 4092,
    "FFMpegPath": "ffmpeg",
    "FFMpegQuality": 6
  }
}
```

## Release Install Guide
* Download release version [here](https://github.com/yangzhongtian001/PYCM/releases).
* Install `ffmpeg` and add to environment variable
* Create `*.json` files according to `*.json.example` and the description above.
* Run `Main.exe` or `Main`

## Dev Install Guide
* Clone repository.
* Run `pip install -r requirements.txt` to install required libraries.
* Install `ffmpeg` and add to environment variable
* Edit `*.json.example` file for configuration & remove the .example extention.
* Run `python Main.py` to start application.

## Contact
* Author: Richard Yang
* Email: zhongtian.yang@qq.com
* School: China Beijing National Day School
* Club: HCC Computer Community