# Python Class Management System
[![Github Build](https://github.com/yangzhongtian001/PYCM/workflows/PYCM-Build/badge.svg)](https://github.com/yangzhongtian001/PYCM/releases) [![GitHub issues](https://img.shields.io/github/issues/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/issues) [![GitHub forks](https://img.shields.io/github/forks/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/network) [![GitHub stars](https://img.shields.io/github/stars/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/stargazers) [![GitHub license](https://img.shields.io/github/license/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/yangzhongtian001/PYCM)


## Structure
```
|-Client: Used for muti users, ex: students, visitors.
|-Console: Used for one host user, ex: teacher, host.
|-Public: [DEPRECATED] Some files and algorithms for use.
```

## Screenshots
![console-login.png](https://i.loli.net/2021/02/05/nb6k57NJuWDxyAz.png)

![console-main.png](https://i.loli.net/2021/02/05/fFt1iTxroBL3hJl.png)

![client-main.png](https://i.loli.net/2021/02/05/HzofFCdVR2cK8qX.png)

![client-file-send.png](https://i.loli.net/2021/02/05/CsAuZKvIcgXVBok.png)

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
  "FileUploadPath": "The directory for storing client uploaded files"
}
```

### Network.json@console&client
This file is used to store network configurations for both console and client.
```json
{
  "Local": {
    "IP": "Current IP address",
    "MAC": "Current MAC address"
  },
  /* The settings bellow is not adviced to be modified. */
  "NetworkDiscover": {
    "IP": "224.50.50.50",
    "Port": 4088,
    "Interval": 5
  },
  "ClassBroadcast": {
    "IP": "225.2.2.19",
    "Port": 4089
  },
  "PrivateMessage": {
    "Port": 4091,
    "Buffer": 32768
  }
}
```


## Download
See all downloads at [Github Release](https://github.com/yangzhongtian001/PYCM/releases). Please notice that all pre-releases are not tested fully and may contain unknown problems.

## Install Guide
* Download zipped file from RELEASE page & extract.
* Edit *.json.example file for configuration & remove the .example extention.
* Enjoy

## Contact
* Author: Richard Yang
* Email: zhongtian.yang@qq.com
* School: China Beijing National Day School
* Club: HCC Computer Community