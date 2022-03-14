# -*- coding=UTF-8 -*-
# pyright: strict
"""Simple plugin system, user can do what they want in install method.  """

import importlib.util
import logging
import os
import traceback
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Dict

import cast_unknown as cast

from natsucord.command import Command

LOGGER = logging.getLogger(__name__)

class g:
    plugins: Dict[str, Command] = {}
    path: str = os.path.join(os.getcwd(), 'plugins')

def register(name: str, cmd: Command) -> None:
    if name in g.plugins:
        LOGGER.warning("plugin.register: %s Replaced by %s" % (g.plugins[name].name, name))
    g.plugins[name] = cmd


def reload():
    g.plugins.clear()
    if not os.path.exists(g.path):
        os.makedirs(g.path)
    for i in Path(g.path).glob("*.py"):
        try:
            spec = importlib.util.spec_from_file_location(i.stem, i)
            assert spec
            module = importlib.util.module_from_spec(spec)
            loader = cast.instance(spec.loader, SourceFileLoader)
            loader.exec_module(module)
        except:
            traceback.print_exc()
            LOGGER.error('load failed %s' % i.absolute())
    LOGGER.info("loaded: %s", ", ".join(g.plugins.keys()))


def reloadPlugin(path: Path) -> None:
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec
        module = importlib.util.module_from_spec(spec)
        loader = cast.instance(spec.loader, SourceFileLoader)
        loader.exec_module(module)
        LOGGER.info("reloaded: %s", path)
    except:
        traceback.print_exc()
        LOGGER.error('load failed %s' % path.absolute())