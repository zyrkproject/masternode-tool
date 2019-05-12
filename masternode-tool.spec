# -*- mode: python -*-
# vim: ft=python
import sys
import os
import os.path
import platform
import hashlib

block_cipher = None

os_type = sys.platform
no_bits = platform.architecture()[0].replace('bit','')
version_str = ''
base_dir = os.path.dirname(os.path.realpath('__file__'))

os.system('git rev-parse --short HEAD > git-rev.txt')
# look for version string
with open(os.path.join(base_dir, 'version.txt')) as fptr:
    for line in fptr:
        parts = [elem.strip() for elem in line.split('=')]
        if len(parts) == 2 and parts[0].lower() == 'version_str':
            version_str = parts[1].strip("'")
            break

add_files = [
 ('img/masternode-tool.png','/img'),
 ('img/masternode-tool.ico','/img'),
 ('img/arrow-right.ico','/img'),
 ('img/hw-disconnect.png','/img'),
 ('img/hw-test.png','/img'),
 ('img/check.png','/img'),
 ('img/link-check.png','/img'),
 ('img/money-transfer-1.png','/img'),
 ('img/money-transfer-2.png','/img'),
 ('img/gear.png','/img'),
 ('img/hw.png','/img'),
 ('img/info.png','/img'),
 ('img/money-bag.png','/img'),
 ('img/sign.png','/img'),
 ('img/uncheck.png','/img'),
 ('img/wallet.png','/img'),
 ('img/save.png','/img'),
 ('img/thumbs-up-down.png','/img'),
 ('img/recover.png','/img'),
 ('version.txt', ''),
 ('git-rev.txt', '')
]

lib_path = next(p for p in sys.path if 'site-packages' in p)
#if os_type == 'win32':
#
#    qt5_path = os.path.join(lib_path, 'PyQt5\\Qt\\bin')
#    sys.path.append(qt5_path)
#
#    # add file vcruntime140.dll manually, due to not including by pyinstaller
#    found = False
#    for p in os.environ["PATH"].split(os.pathsep):
#        file_name = os.path.join(p, "vcruntime140.dll")
#        if os.path.exists(file_name):
#            found = True
#            add_files.append((file_name, ''))
#            print('Adding file ' + file_name)
#            break
#    if not found:
#        raise Exception('File vcruntime140.dll not found in the system path.')

# add bitcoin library data file
add_files.append( (os.path.join(lib_path, 'bitcoin/english.txt'),'/bitcoin') )
add_files.append( (os.path.join(lib_path, 'mnemonic/wordlist/english.txt'),'/mnemonic/wordlist') )

a = Analysis(['src/masternode_tool.py'],
             pathex=[base_dir],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# Workaround for Ubuntu 16.04 and newer
# https://github.com/fman-users/fman/issues/119
a.binaries = a.binaries - [('libdrm.so.2', None, None)]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MasternodeTool',
          debug=False,
          strip=False,
          upx=False,
          console=False,
		  icon=os.path.join('img',('masternode-tool.%s' % ('icns' if os_type=='darwin' else 'ico'))))

if os_type == 'darwin':
    app = BUNDLE(exe,
                 name='MasternodeTool.app',
                 icon='img/masternode-tool.icns',
                 bundle_identifier=None,
                     info_plist={
                        'NSHighResolutionCapable': 'True'
                     }
                 )

dist_path = os.path.join(base_dir, DISTPATH)
all_bin_dir = os.path.join(dist_path, '..', 'all')
if not os.path.exists(all_bin_dir):
    os.makedirs(all_bin_dir)

# zip archives
print(dist_path)
print(all_bin_dir)
os.chdir(dist_path)

if os_type == 'win32':
    print('Compressing Windows executable')
    filename = os.path.join(all_bin_dir, 'MasternodeTool_' + version_str + '.win' + no_bits + '.zip')
    os.system('"7z.exe" a %s %s -mx0' % (filename,  'MasternodeTool.exe'))
elif os_type == 'darwin':
    print('Compressing Mac executable')
    filename = os.path.join(all_bin_dir, 'MasternodeTool_' + version_str + '.mac.zip')
    os.system('zip -r "%s" "%s"' % (filename,  'MasternodeTool.app'))
elif os_type == 'linux':
    print('Compressing Linux executable')
    filename = os.path.join(all_bin_dir, 'MasternodeTool_' + version_str + '.linux.tar.gz')
    os.system('tar -zcvf %s %s' % (filename,  'MasternodeTool'))

print('SHA-256 of %s:' % filename)
sha256_hash = hashlib.sha256()
with open(filename, "rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    print(sha256_hash.hexdigest())
