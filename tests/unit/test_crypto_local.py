from io import BytesIO

from gost_backup_vault.crypto.local_software_gost import LocalSoftwareGostProvider
from gost_backup_vault.domain.enums import GostCipher
from gost_backup_vault.domain.models import CryptoProfile


def test_encrypt_decrypt_roundtrip():
    provider = LocalSoftwareGostProvider()
    profile = CryptoProfile(name="test", gost_cipher=GostCipher.MAGMA)

    plaintext = b"secret-data"
    encrypted = BytesIO()
    decrypted = BytesIO()

    provider.encrypt_stream(BytesIO(plaintext), encrypted, profile)
    encrypted.seek(0)
    provider.decrypt_stream(encrypted, decrypted, profile)

    assert decrypted.getvalue() == plaintext


def test_encrypt_decrypt_noop_cipher():
    provider = LocalSoftwareGostProvider()
    profile = CryptoProfile(name="none", gost_cipher=GostCipher.NONE)

    plaintext = b"no-encrypt"
    encrypted = BytesIO()
    decrypted = BytesIO()

    provider.encrypt_stream(BytesIO(plaintext), encrypted, profile)
    encrypted.seek(0)
    provider.decrypt_stream(encrypted, decrypted, profile)

    assert decrypted.getvalue() == plaintext
