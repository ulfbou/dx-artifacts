"""Load the packaged command runtime under a registered module identity."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

_MODULE_NAME = "dx_artifacts._packaged_runtime"


def load_main() -> Callable[..., int]:
    """Load and return the packaged runtime entry point."""
    source = Path(__file__).with_name("_runtime.py")
    spec = importlib.util.spec_from_file_location(
        _MODULE_NAME,
        source,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"cannot create runtime module specification: {source}"
        )

    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(_MODULE_NAME)
    sys.modules[_MODULE_NAME] = module

    try:
        spec.loader.exec_module(module)
    except BaseException:
        if previous is None:
            sys.modules.pop(_MODULE_NAME, None)
        else:
            sys.modules[_MODULE_NAME] = previous
        raise

    main = getattr(module, "main", None)
    if not callable(main):
        raise RuntimeError(
            "packaged runtime does not export a callable main"
        )
    return main
