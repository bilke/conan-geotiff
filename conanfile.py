import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class LibgeotiffConan(ConanFile):
    name = "libgeotiff"
    description = """Libgeotiff is a library for reading, and writing GeoTIFF
                     information tags."""

    version = "1.4.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "utilities": [True, False]}
    default_options = "shared=False", "utilities=False"
    requires = "libtiff/4.0.6@bilke/stable", "proj/4.9.2@bilke/stable"
    exports = ["CMakeLists.txt", "FindLibGeoTiff.cmake"]
    url="http://github.com/bilke/conan-geotiff"
    license="http://trac.osgeo.org/geotiff/"

    def config(self):
        del self.settings.compiler.libcxx

    def source(self):
        zip_name = "%s.zip" % self.version
        download("https://github.com/ufz/geotiff/archive/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_ZLIB"] = "ON"
        if self.settings.os == "Linux":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        if self.options.shared == True:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        if self.options.utilities == False:
            cmake.definitions["WITH_UTILITIES"] = "OFF"
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["geotiff_d", "xtiff_d"]
        else:
            self.cpp_info.libs = ["geotiff", "xtiff"]
