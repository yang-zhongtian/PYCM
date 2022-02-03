# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C) 2021 Richard Yang  <zhongtian.yang@qq.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import subprocess
import os
import glob
import argparse

SEARCH_DIRS = ['../UI', '../Module']


def generate(file, target='zh_CN'):
    if type(file) == list:
        file = ' '.join(file)
    command = f'pylupdate5 {file} -ts Translation/{target}.ts -noobsolete -verbose'
    try:
        result = subprocess.getoutput(command)
        print(result)
    except OSError as e:
        print(e)


def auto_generate(args):
    translate_files = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for path in SEARCH_DIRS:
        translate_files.extend(list(map(os.path.abspath, glob.glob(f'{os.path.join(base_dir, path)}/[!__]*.py'))))
    generate(translate_files, args.lang)


parser = argparse.ArgumentParser(description='PYCM Translation File Generator')
parser.add_argument('--lang', type=str, default='zh_CN', help='The target language for translation')
parser.set_defaults(func=auto_generate)

args = parser.parse_args()
args.func(args)
