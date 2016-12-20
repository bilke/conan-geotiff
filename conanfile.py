import os
from conans import ConanFile, CMake
from conans.tools import download, unzip, patch, replace_in_file

class LibgeotiffConan(ConanFile):
    name = "libgeotiff"
    version = "1.4.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "utilities": [True, False]}
    default_options = "shared=False", "utilities=True"
    requires = "libtiff/4.0.6@bilke/stable", "proj/4.9.2@bilke/stable"
    exports = ["CMakeLists.txt", "FindLibGeoTiff.cmake"]
    url="http://github.com/bilke/conan-geotiff"
    license="http://trac.osgeo.org/geotiff/"

    INSTALL_DIR = "_install"

    def source(self):
        zip_name = "%s.zip" % self.version
        download("https://github.com/ufz/geotiff/archive/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        CMAKE_OPTIONALS = "-DWITH_ZLIB=ON "
        if self.settings.os == "Linux":
            CMAKE_OPTIONALS += "-DCMAKE_POSITION_INDEPENDENT_CODE=ON "
        if self.options.shared == True:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=ON "
        if self.options.utilities == False:
            CMAKE_OPTIONALS += "-DWITH_UTILITIES=OFF "
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line, CMAKE_OPTIONALS))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindLibGeoTiff.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["geotiff_d", "xtiff_d"]
        else:
            self.cpp_info.libs = ["geotiff", "xtiff"]
