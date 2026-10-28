#!/usr/bin/env python3
"""Build static liblzma for arm64 iPhone and arm64/x86_64 iOS Simulator."""
from pathlib import Path
import argparse,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[2]
OPTIONS=['-DBUILD_SHARED_LIBS=OFF','-DBUILD_TESTING=OFF','-DXZ_NLS=OFF','-DXZ_DOC=OFF','-DXZ_DOXYGEN=OFF','-DXZ_TOOL_XZ=OFF','-DXZ_TOOL_XZDEC=OFF','-DXZ_TOOL_LZMADEC=OFF','-DXZ_TOOL_LZMAINFO=OFF','-DXZ_TOOL_SCRIPTS=OFF']
def run(*args):
    print('+',' '.join(map(str,args)),flush=True);return subprocess.run(list(map(str,args)),check=True)
def configure(build,prefix,sdk=None,arch=None,jobs=6,testing=False):
    flags=OPTIONS+['-DCMAKE_BUILD_TYPE=Release','-DCMAKE_INSTALL_PREFIX='+str(prefix)]
    if sdk:flags+=['-DCMAKE_SYSTEM_NAME=iOS','-DCMAKE_OSX_SYSROOT='+sdk,'-DCMAKE_OSX_ARCHITECTURES='+arch,'-DCMAKE_OSX_DEPLOYMENT_TARGET=18.0']
    if testing:flags+=['-DBUILD_TESTING=ON']
    run('cmake','-S',ROOT,'-B',build,*flags)
    run('cmake','--build',build,'--parallel',jobs,*([] if testing else ['--target','liblzma']))
    run('cmake','--install',build)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--jobs',type=int,default=6);a=p.parse_args();built={}
    configurations=[('ios-arm64','iphoneos','arm64'),('simulator-arm64','iphonesimulator','arm64'),('simulator-x86_64','iphonesimulator','x86_64')]
    for label,sdk,arch in configurations:
        build=ROOT/'out/apple'/label;prefix=build/'install';configure(build,prefix,sdk,arch,a.jobs);built[label]=prefix
    out=ROOT/'dist';out.mkdir(exist_ok=True);staging=out/'staging'
    if staging.exists():shutil.rmtree(staging)
    staging.mkdir();universal=staging/'liblzma.a'
    run('lipo','-create',built['simulator-arm64']/'lib/liblzma.a',built['simulator-x86_64']/'lib/liblzma.a','-output',universal)
    headers=staging/'Headers';shutil.copytree(built['ios-arm64']/'include',headers)
    (headers/'module.modulemap').write_text('module CLZMA {\n header "lzma.h"\n export *\n}\n')
    artifact=out/'LZMA.xcframework'
    if artifact.exists():shutil.rmtree(artifact)
    run('xcodebuild','-create-xcframework','-library',built['ios-arm64']/'lib/liblzma.a','-headers',headers,'-library',universal,'-headers',headers,'-output',artifact)
    notices=artifact/'Licenses';notices.mkdir()
    for source in list(ROOT.glob('COPYING*'))+[ROOT/'AUTHORS']:
        if source.is_file():shutil.copy2(source,notices/source.name)
    manifest={'source_revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'upstream_revision':'299eb5c3f597f107fd6019bf156885ac8bfaa5ea','minimum_ios':'18.0','linkage':'static','slices':[x[0] for x in configurations],'cmake_options':OPTIONS}
    (out/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Created',artifact)
if __name__=='__main__':main()
