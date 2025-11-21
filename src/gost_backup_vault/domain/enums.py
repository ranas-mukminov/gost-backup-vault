from enum import Enum

class BackupBackendType(str, Enum):
    RESTIC = "restic"
    BORG = "borg"
    TAR = "tar"

class GostCipher(str, Enum):
    MAGMA = "magma"
    KUZNYECHIK = "kuznyechik"
    NONE = "none"

class CryptoMode(str, Enum):
    WRAP_KEY = "wrap_key"
    FULL_ENCRYPT = "full_encrypt"

class RetentionPolicyType(str, Enum):
    TIERED = "tiered"
    SIMPLE = "simple"
