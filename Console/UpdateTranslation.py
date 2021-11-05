# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C)2021 Richard Yang <zhongtian.yang@qq.com>

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

import os
import glob
import argparse

SEARCH_DIRS = ['UI', 'Module']


def generate(file, target='zh_CN'):
    if type(file) == list:
        file = ' '.join(file)
    os.system(f'pylupdate5 {file} -ts Translation/{target}.ts')


def auto_generate(args):
    translate_files = []
    for path in SEARCH_DIRS:
        translate_files.extend(glob.glob(f'{path}/[!__]*.py'))
    generate(translate_files, args.lang)


parser = argparse.ArgumentParser(description='PYCM Translation File Generator')
parser.add_argument('--lang', type=str, default='zh_CN', help='The target language for translation')
parser.set_defaults(func=auto_generate)

args = parser.parse_args()
args.func(args)
