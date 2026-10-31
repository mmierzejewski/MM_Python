# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for a single-file macOS command-line executable.
# Build: python3 -m PyInstaller --clean clear_caches.spec

import os

a = Analysis(
    [os.path.join(SPECPATH, "clear_caches.py")],
    pathex=[SPECPATH],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "unittest", "pydoc", "test"],
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
    name="clear_caches",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX-compressed binaries break macOS code signing.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
