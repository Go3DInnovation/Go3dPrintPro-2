from .diagnostic import Diagnostic


class Meshes:
    def __init__(self, file, settings):
        self._settings = settings
        self._file = file
        self._max_file_size = self._settings.get("diagnostic-mesh-file-size", 1e6)

    def check(self):
        if self._settings["checks"].get("diagnostic-mesh-file-extension", False):
            for check in self.checkFileFormat():
                yield check

        if self._settings["checks"].get("diagnostic-mesh-file-size", False):
            for check in self.checkFileSize():
                yield check

        yield

    def checkFileFormat(self):
        if self._file.suffix.lower() not in (".3mf", ".obj", ".stl"):
            yield Diagnostic("diagnostic-mesh-file-extension",
                             f"Extension **{self._file.suffix}** not supported, use **3mf**, **obj** or **stl**",
                             self._file)
        yield

    def checkFileSize(self):

        if self._file.stat().st_size > self._max_file_size:
            yield Diagnostic("diagnostic-mesh-file-size",
                             f"Mesh file with a size **{self._file.stat().st_size}** is bigger then allowed maximum of **{self._max_file_size}**",
                             self._file)
        yield