from logging import getLogger
from pathlib import Path
from typing import Callable, Dict
from natsucord.plugin import reloadPlugin
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent, FileModifiedEvent
from time import time_ns

LOGGER = getLogger(__name__)

class g:
    times: Dict[str, int] = {}
    check_changed: bool = True

class WatchDog(PatternMatchingEventHandler):

    def __init__(self, callback: Callable) -> None:
        super(WatchDog, self).__init__(patterns=['*.py'],
                                       ignore_patterns=['*.pyc'])
        self.callback: Callable = callback

    def on_moved(self, event: FileSystemEvent):
        self._run_command(event.src_path)

    def on_created(self, event: FileSystemEvent):
        self._run_command(event.src_path)

    def on_deleted(self, event: FileSystemEvent):
        self._run_command(event.src_path)

    def on_modified(self, event: FileModifiedEvent):
        self.callback(event.src_path)


def start(path: str):

    def on_changed(path: str) -> None:
        if g.check_changed:
            if path not in g.times or time_ns() - g.times[path] > 1000:
                reloadPlugin(Path(path))
            g.times[path] = time_ns()

    handler = WatchDog(on_changed)
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()