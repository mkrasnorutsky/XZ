// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "XZ", platforms: [.iOS("18.0")],
    products: [.library(name: "LZMA", targets: ["LZMA"])],
    targets: [
        .binaryTarget(name: "CLZMA", url: "https://github.com/mkrasnorutsky/XZ/releases/download/0.1.0/LZMA.xcframework.zip", checksum: "f1977bfd02efe8ace94ac41e87ddf51dc33b73247f35fd60ddb01e3dacb827ac"),
        .target(name: "LZMA", dependencies: ["CLZMA"], path: "apple/SPM", publicHeadersPath: "include")
    ])
