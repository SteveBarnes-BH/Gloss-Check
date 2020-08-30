# -*- mode: python -*-

block_cipher = None


a = Analysis(['gloss_check.py'],
             pathex=['D:\\Users\\212303160\\GitWorking\\Gloss-Check'],
             binaries=[],
             datas=[('C:\\Python35-32\\Lib\\site-packages\\enchant\\tokenize', 'enchant\\tokenize')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gloss_check',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gloss_check')
