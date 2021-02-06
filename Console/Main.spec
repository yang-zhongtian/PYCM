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
                'UI/LoginUI.py',
				'qt_material/resources/generate.py',
				'qt_material/resources/logos_pyqt5_rc.py',
				'qt_material/resources/resource_pyqt5_rc.py'
             ],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('*.json.example', '.'), ('qt_material/fonts', 'qt_material/fonts'), ('qt_material/themes', 'qt_material/themes'), ('qt_material/dock_theme.ui', 'qt_material/dock_theme.ui'), ('qt_material/material.css.template', 'qt_material/material.css.template')],
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
