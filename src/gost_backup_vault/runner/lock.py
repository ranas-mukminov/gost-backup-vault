import fcntl
import os
from contextlib import contextmanager

class LockError(Exception):
    pass

@contextmanager
def acquire_lock(lock_file: str):
    """
    Acquires an exclusive lock on the given file.
    """
    lock_path = os.path.abspath(lock_file)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)
    
    f = open(lock_path, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    except IOError:
        raise LockError(f"Could not acquire lock on {lock_path}. Another instance is running.")
    finally:
        try:
            fcntl.lockf(f, fcntl.LOCK_UN)
        except IOError:
            pass
        f.close()
