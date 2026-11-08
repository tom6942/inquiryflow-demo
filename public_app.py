"""Deploy entrypoint for the verified, synthetic-data InquiryFlow source bundle.
The ZIP contains readable source, prompts and demo fixtures; never user records.
"""
import hashlib
import os
from pathlib import Path
import runpy
import sys
import tempfile
import zipfile

archive = Path(__file__).with_name("inquiryflow_source.zip")
expected = "072c44c88aaa0f71d8f37e7ed98703e5ff84923bf091a4f679e556b98d56631a"
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
if str(code_root) not in sys.path:
    sys.path.insert(0, str(code_root))
runpy.run_path(str(code_root / "public_app.py"), run_name="__main__")
