# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis([
                'Main.py',
                'LoadConfig.py',
                'NetworkDiscover.py',
                'Packages.py',
                'PrivateMessage.py',
                'Resources_rc.py',
                'Threadings.py',
                'UI/Dashboard.py',
                'UI/DashboardUI.py',
                'UI/Login.py',
                'UI/LoginUI.py'
             ],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          icon='UI/Resources/logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='Main')
