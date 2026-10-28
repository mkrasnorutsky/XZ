// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "XZ", platforms: [.iOS("18.0")],
    products: [.library(name: "LZMA", targets: ["LZMA"])],
    targets: [
        .binaryTarget(name: "CLZMA", path: "dist/LZMA.xcframework"),
        .target(name: "LZMA", dependencies: ["CLZMA"], path: "apple/SPM", publicHeadersPath: "include")
    ])
