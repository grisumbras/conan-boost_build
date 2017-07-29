"""Conan.io recipe for Boost.Build
"""
from conans import ConanFile, tools, os

class BoostBuildConan(ConanFile):
    """Checkout Boost.Build, build and create package
    """
    name = "Boost.Build"
    version = "1.64.0"
    generators = "txt"
    url = "https://github.com/boostorg/build"
    description = "Boost.Build makes it easy to build C++ projects, everywhere"
    license = "www.boost.org/users/license.html"
    folder_name = "boost_{0}".format(version.replace(".", "_"))
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone --depth=50 --branch=boost-{0} {1}.git {2}"
                 .format(self.version, self.url, self.folder_name))

    def build(self):
        command = "bootstrap" if self.settings.os == "Windows" else "./bootstrap.sh"

        build_path_full = os.path.join(self._conanfile_directory, self.folder_name)
        vscmd_path_full = os.path.join(build_path_full, "src", "engine")
        with tools.environment_append({"VSCMD_START_DIR": vscmd_path_full}):
            try:
                self.run(command, cwd=build_path_full)
            except:
                if self.settings.os == "Windows":
                    read_cmd = "type"
                else:
                    read_cmd = "cat"
                self.run("{0} bootstrap.log".format(read_cmd))
                raise

        command = "b2" if self.settings.os == "Windows" else "./b2"
        full_command = "{0} --abbreviate-paths".format(command)
        self.output.warn(full_command)
        self.run(full_command, cwd=self.folder_name)

    def package(self):
        release_dir = path.join(self.folder_name, "Release")
