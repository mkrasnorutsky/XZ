// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "XZ", platforms: [.iOS("18.0")],
    products: [.library(name: "LZMA", targets: ["LZMA"])],
    targets: [
        .binaryTarget(name: "CLZMA", url: "https://github.com/mkrasnorutsky/XZ/releases/download/0.1.1/LZMA.xcframework.zip", checksum: "2c337ea870ef8ecd9159144f52a27350a2a3746a35902aff09e81900bc63863f"),
        .target(name: "LZMA", dependencies: ["CLZMA"], path: "apple/SPM", publicHeadersPath: "include")
    ])
