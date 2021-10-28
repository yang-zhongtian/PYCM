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
subparsers = parser.add_subparsers(help='Generator')
automode = subparsers.add_parser('auto', help='Generate translation file by auto')
automode.add_argument('--lang', type=str, default='zh_CN', help='The target language for translation')
automode.set_defaults(func=auto_generate)

args = parser.parse_args()
args.func(args)
