import os
from conans import ConanFile, CMake
from conans.tools import download, unzip, patch

class LibgeotiffConan(ConanFile):
    name = "libgeotiff"
    version = "1.4.1"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    requires = "libtiff/4.0.6@bilke/stable", "proj/4.9.2@bilke/stable"
    exports = ["CMakeLists.txt", "FindLibGeoTiff.cmake"]
    url="http://github.com/bilke/conan-geotiff"
    license="http://trac.osgeo.org/geotiff/"

    ZIP_FOLDER_NAME = "libgeotiff-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://opengeosys.s3.amazonaws.com/ogs6-lib-sources/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        patch_content = '''--- libxtiff/CMakeLists.txt	2014-09-29 15:30:34.000000000 +0200
+++ libxtiff/CMakeLists.txt	2016-04-25 16:58:07.000000000 +0200
@@ -8,2 +8,11 @@

-ADD_LIBRARY(xtiff STATIC xtiff.c)
+ADD_LIBRARY(xtiff xtiff.c)
+IF(WIN32)
+	SET_TARGET_PROPERTIES(xtiff PROPERTIES DEBUG_POSTFIX _d)
+ENDIF()
+
+INSTALL( TARGETS xtiff
+	 EXPORT depends
+	 RUNTIME DESTINATION bin
+	 LIBRARY DESTINATION lib
+	 ARCHIVE DESTINATION lib )
'''
        patch(patch_string=patch_content, base_path=self.ZIP_FOLDER_NAME)
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line))
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
