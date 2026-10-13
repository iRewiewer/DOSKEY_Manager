import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path


def print_error(message, error=None):
    if error is None:
        print(f"[DOSKEY Manager] {message}", file=sys.stderr)
    else:
        print(f"[DOSKEY Manager] {message}: {error}", file=sys.stderr)


def deep_merge(defaults, loaded):
    if not isinstance(defaults, dict) or not isinstance(loaded, dict):
        return loaded

    merged = dict(defaults)
    for key, value in loaded.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_json(file_path, default=None):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        if default is not None:
            return default
        raise


def atomic_write_text(target_path, text):
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target.with_name(f".tmp_{os.getpid()}_{int(time.time() * 1000)}")

    try:
        with open(temp_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_path, target)
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


@contextmanager
def file_lock(lock_path, timeout_seconds=10, stale_seconds=60):
    lock_file = Path(lock_path)
    start = time.time()
    fd = None

    while True:
        try:
            fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("ascii"))
            break
        except FileExistsError:
            try:
                age = time.time() - lock_file.stat().st_mtime
                if age > stale_seconds:
                    lock_file.unlink()
                    continue
            except OSError:
                pass

            if time.time() - start > timeout_seconds:
                raise TimeoutError(f"Timed out waiting for lock: {lock_file}")
            time.sleep(0.1)

    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_file.unlink()
        except OSError:
            pass
