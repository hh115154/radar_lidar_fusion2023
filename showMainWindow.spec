# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(
    ['showMainWindow.py', 'testMainWindow_Ui.py', 'mySocket.py', 'protocol.py', 'threadMngt.py', 'myControls.py', 'presentationLayer.py', 'procAsamMdf.py', 'CppApi.py', 'logFileMngt.py'],
    pathex=['C:\\CodeProjects\\4D_Radar'],
    binaries=[],
    datas=[('images\\*', 'images'),('cppdll\\*.dll','cppdll')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='bhap_4D_Radar_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='C:\\CodeProjects\\4D_Radar\\logo.ico'

)
