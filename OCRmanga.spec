# manga_ocr.spec
block_cipher = None

a = Analysis(
    ['OCRmanga.py'],
    pathex=[],
    binaries=[(r'C:\Program Files\Tesseract-OCR', 'Tesseract-OCR')],
    datas=[
        ('/usr/share/tesseract-ocr/5/tessdata/jpn.traineddata', 'tessdata'),
        ('/usr/share/tesseract-ocr/5/tessdata/jpn_vert.traineddata', 'tessdata')
    ],
    hiddenimports=[
        'pytesseract',
        'cv2',
        'PIL',
        'numpy'
    ],
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
    name='OCRmanga',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, 
    icon='icono.ico'  
)