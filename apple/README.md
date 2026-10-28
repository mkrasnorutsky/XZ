# XZ / liblzma for iOS and Swift Package Manager

Full tracked XZ sources and upstream history are preserved at the project's pinned revision `299eb5c3f597f107fd6019bf156885ac8bfaa5ea`. This package supplies liblzma headers and compiled code together for SimGear's compressed-data support, rather than mixing locally installed headers with an SDK library.

## Use the published package

Add `https://github.com/mkrasnorutsky/XZ.git` in Xcode, select version **0.1.0** or later, and add the **LZMA** product. It integrates a checksum-verified static XCFramework for **arm64 iPhone, arm64 Simulator and x86_64 Simulator**, minimum iOS **18.0**. The binary module is **CLZMA**; public headers retain the standard `#include <lzma.h>` interface. The wrapper header is `LZMASPM.h`.

[Release 0.1.0](https://github.com/mkrasnorutsky/XZ/releases/tag/0.1.0) contains the XCFramework ZIP, SHA-256 checksum and build manifest. This is binary-backed SPM integration: consumers do not need CMake, and SPM does not compile XZ sources during resolution.

## Build

Requirements: macOS, Xcode with iPhoneOS and iPhoneSimulator SDKs, CMake, Python 3 and Git. No additional library downloads or signing identity are required.

```sh
git clone https://github.com/mkrasnorutsky/XZ.git
cd XZ
python3 apple/scripts/build_xcframework.py --jobs 6
python3 apple/scripts/validate_xcframework.py
```

CMake builds liblzma independently for all three architectures. Lipo combines only the two Simulator archives, and Xcode packages them alongside the device archive as `dist/LZMA.xcframework`. Public headers, Clang module metadata and license files are included. Command-line tools, translated messages, documentation generation and iOS test executables are disabled; the library's encoder/decoder capabilities and threading defaults remain enabled.

Validation checks the XCFramework architecture metadata, links an encoder/decoder client for every iOS target, then compiles a separate native macOS library and runs a compression/decompression round-trip and header/library version check. Native execution validates the source build, not execution of an iOS binary on the Mac.

A manual GitHub Actions workflow runs the same build and validation steps. For local rebuilt artifacts, copy `apple/Package.local.swift` to the root `Package.swift` before adding this folder as a local package.

## Release packaging

```sh
python3 apple/scripts/package_release.py --tag 0.2.0
```

Upload the generated archive and checksum to that GitHub release. Commit the generated `dist/Package.swift` as the root manifest at the release revision. Published ZIP bytes/checksums remain immutable; the local template stays in `apple/Package.local.swift`.

The library is distributed under the upstream 0BSD terms described in `COPYING` and `COPYING.0BSD`. Other parts of the full source repository have their own licensing terms; original notices and COPYING files are preserved and bundled. The package builds liblzma only, not the shell scripts or command-line tools.
