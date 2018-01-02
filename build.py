from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(remotes="https://ogs.jfrog.io/ogs/api/conan/conan")
    builder.add_common_builds()
    builder.run()
