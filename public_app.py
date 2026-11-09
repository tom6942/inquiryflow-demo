"""Deploy entrypoint for the verified, synthetic-data InquiryFlow source bundle.
The ZIP contains readable source, prompts and demo fixtures; never user records.
"""
import hashlib
import importlib
import os
from pathlib import Path
import runpy
import sys
import tempfile
import threading
import types
import zipfile

archive = Path(__file__).with_name("inquiryflow_source.zip")
expected = "afca4eabf492b8cfe855e99951b5c8efa3d521cd5957e442498f90a86f1cce49"
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise RuntimeError("Source bundle integrity check failed")
code_root = Path(tempfile.gettempdir()) / ("inquiryflow-code-" + actual)
if not code_root.is_dir():
    with tempfile.TemporaryDirectory(prefix="inquiryflow-install-") as staging:
        unpacked = Path(staging) / "source"
        with zipfile.ZipFile(archive) as bundle:
            for name in bundle.namelist():
                parts = Path(name).parts
                if Path(name).is_absolute() or ".." in parts:
                    raise RuntimeError("Unsafe archive path")
            bundle.extractall(unpacked)
        try:
            os.rename(unpacked, code_root)
        except OSError:
            if not code_root.is_dir():
                raise
# Streamlit can hot-reload the entrypoint without restarting Python. Do not
# accidentally retain a backend module from a previous verified ZIP version.
runtime=sys.modules.setdefault('_inquiryflow_deploy_runtime',types.ModuleType('_inquiryflow_deploy_runtime'))
lock=runtime.__dict__.setdefault('lock',threading.RLock())
with lock:
    if runtime.__dict__.get('bundle') != actual:
        for name in list(sys.modules):
            if name=='inquiryflow' or name.startswith('inquiryflow.'):
                del sys.modules[name]
        sys.path[:]=[p for p in sys.path if not str(p).startswith(str(Path(tempfile.gettempdir())/'inquiryflow-code-'))]
        sys.path.insert(0,str(code_root))
        importlib.import_module('inquiryflow.public_demo')
        importlib.import_module('inquiryflow.public_ui')
        runtime.bundle=actual
runpy.run_path(str(code_root / "public_app.py"), run_name="__main__")
