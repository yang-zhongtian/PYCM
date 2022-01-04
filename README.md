# Python Class Management System

[![GitHub issues](https://img.shields.io/github/issues/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/issues)
[![GitHub forks](https://img.shields.io/github/forks/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/network)
[![GitHub stars](https://img.shields.io/github/stars/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM/stargazers)
[![GitHub license](https://img.shields.io/github/license/yangzhongtian001/PYCM)](https://github.com/yangzhongtian001/PYCM)
[![Code Factor](https://www.codefactor.io/repository/github/yangzhongtian001/pycm/badge/master)](https://www.codefactor.io/repository/github/yangzhongtian001/pycm/overview/master)
![Build windows](https://github.com/yangzhongtian001/PYCM/actions/workflows/build-windows.yml/badge.svg)

[English](README.md) [简体中文](README.zh-CN.md)

## Mirror Repository

* [Github(Master)](https://github.com/yangzhongtian001/PYCM)
* [Gitee(Mirror)](https://gitee.com/yangzhongtian/PYCM)

## Introduction

This program is an e-classroom management system written by python.
It contains both `client(student side)` and `console(teacher side)`. GUI written by `PyQt5`, supporting all platforms.

## Features

* [x] Auto LAN discover
* [x] Console screen broadcasting
* [x] Cient screen spyby Console
* [X] Console side file share
* [x] Client side file submitting
* [x] Console side message sending
* [x] Client side message sending
* [x] `PyInstaller` packaging

## Programs

* **Client:** Used for muti users, ex: students, visitors.
* **Console:** Used for one host user, ex: teacher, host.

## Release Install Guide

* Download release version [here](https://github.com/yangzhongtian001/PYCM/releases).
* Run `ConsoleMain` or `ClientMain`

## Dev Install Guide

* Clone repository.
* Run `pip install -r requirements.txt` to install required libraries.
* Run `python ConsoleMain.py` or `python ClientMain.py` to start application.

## Screenshot

### Console

![Dashboard](Images/Console/Dashboard.png)

![Message send](Images/Console/MessageSend.png)

![Remote command](Images/Console/RemoteCommand.png)

### Client

![Main](Images/Client/Main.png)

![File transfer](Images/Client/FileTransfer.png)

## Known Issues
1. Due to some compiling issues, currently only Windows version of binary file is available. If you want to use it on macOS or Linux, consider following the [Dev Guide](#Dev Install Guide).
2. The screen capturing module can have some problem under low screen resolution.

## Contact

* Author: Richard Yang
* School: China Beijing National Day School
* Club: HCC Computer Community

---

![GPLv3 or later](Images/Logo/GPLv3OrLater.png) 
![HCC Computer Community](Images/Logo/HCC.png)
![BNDSE](Images/Logo/BNDSE.png)