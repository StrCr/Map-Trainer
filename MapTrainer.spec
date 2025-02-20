# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'json_utils.py', 'py_maptrainer.py'],
    pathex=[],
    binaries=[],
    datas=[('data/map.sqlite', 'data'), ('data/score.json', 'data'), ('maps', 'maps')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MapTrainer',
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
    icon=['data\\map_icon.ico'],
)
