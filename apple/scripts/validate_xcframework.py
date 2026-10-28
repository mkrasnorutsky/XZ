#!/usr/bin/env python3
"""Link each iOS slice, then run a native compression/decompression test."""
from pathlib import Path
import plistlib,subprocess,tempfile
from build_xcframework import ROOT,configure
artifact=ROOT/'dist/LZMA.xcframework';info=plistlib.loads((artifact/'Info.plist').read_bytes());assert len(info['AvailableLibraries'])==2
for entry in info['AvailableLibraries']:
    sim=entry.get('SupportedPlatformVariant')=='simulator'
    assert entry['SupportedPlatform']=='ios'
    assert set(entry['SupportedArchitectures'])==({'arm64','x86_64'} if sim else {'arm64'})
    folder=artifact/entry['LibraryIdentifier'];archive=folder/entry['LibraryPath'];headers=folder/entry['HeadersPath']
    subprocess.run(['lipo',str(archive),'-verify_arch',*entry['SupportedArchitectures']],check=True)
    sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator' if sim else 'iphoneos','--show-sdk-path'],text=True).strip()
    for arch in entry['SupportedArchitectures']:
        triple=arch+'-apple-ios18.0'+('-simulator' if sim else '')
        with tempfile.TemporaryDirectory(prefix='lzma-client-') as directory:
            subprocess.run(['xcrun','clang','-target',triple,'-isysroot',sdk,'-fmodules','-fmodules-cache-path='+directory+'/modules','-I'+str(headers),str(ROOT/'apple/scripts/roundtrip.c'),str(archive),'-o',directory+'/client'],check=True)
print('PASS: API links for arm64 device and arm64/x86_64 Simulator',flush=True)
build=ROOT/'out/native-validation';prefix=build/'install';configure(build,prefix,jobs=6)
subprocess.run(['xcrun','clang','-I'+str(prefix/'include'),str(ROOT/'apple/scripts/roundtrip.c'),str(prefix/'lib/liblzma.a'),'-o',str(build/'roundtrip')],check=True)
subprocess.run([str(build/'roundtrip')],check=True)
