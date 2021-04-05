import os

from conans import ConanFile, CMake, tools


class KaitaiStructCppStlRuntimeConan(ConanFile):
    name = "kaitai_struct_cpp_stl_runtime"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://kaitai.io/"
    description = "kaitai struct c++ runtime library"
    topics = ("parsers", "streams", "dsl")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    options = {
        "shared": [True],
        "fPIC": [True, False],
        "with_zlib": [True, False],
        "with_iconv": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_zlib": False,
        "with_iconv": False
    }

    _cmake = None

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11")
        if self.options.with_iconv:
            self.requires("libiconv/1.16")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        if self.options.with_iconv:
            self._cmake.definitions["STRING_ENCODING_TYPE"] = "ICONV"
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
