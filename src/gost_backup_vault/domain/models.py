from typing import List, Optional
from pydantic import BaseModel, Field
from .enums import BackupBackendType, GostCipher, CryptoMode, RetentionPolicyType

class NodeConfig(BaseModel):
    id: str
    os: Optional[str] = None

class BackendConfig(BaseModel):
    type: BackupBackendType
    repo: str
    extra_args: List[str] = Field(default_factory=list)

class CryptoProfile(BaseModel):
    name: str
    gost_cipher: GostCipher
    mode: CryptoMode = CryptoMode.WRAP_KEY
    provider: str = "local_software"
    key_id: Optional[str] = None

class RetentionPolicy(BaseModel):
    type: RetentionPolicyType
    daily: Optional[int] = None
    weekly: Optional[int] = None
    monthly: Optional[int] = None
    keep_last: Optional[int] = None

class BackupJob(BaseModel):
    name: str
    paths: List[str]
    exclude: List[str] = Field(default_factory=list)
    schedule: str
    retention: Optional[RetentionPolicy] = None

class BackupConfig(BaseModel):
    node: NodeConfig
    backend: BackendConfig
    crypto_profile: CryptoProfile
    jobs: List[BackupJob]

class BackupResult(BaseModel):
    job_name: str
    success: bool
    duration_seconds: float
    size_bytes: int
    error_message: Optional[str] = None
    snapshot_id: Optional[str] = None
