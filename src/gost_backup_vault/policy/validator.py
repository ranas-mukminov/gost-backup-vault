from typing import List, Set

from ..domain.models import BackupConfig

class PolicyValidator:
    @staticmethod
    def validate(config: BackupConfig) -> List[str]:
        """
        Perform lightweight, deterministic validation of a loaded BackupConfig.
        This is intentionally conservative to keep validation predictable for tests.
        """
        errors: List[str] = []
        seen_names: Set[str] = set()

        if not config.jobs:
            errors.append("No backup jobs defined")

        for job in config.jobs:
            if job.name in seen_names:
                errors.append(f"Duplicate job name detected: {job.name}")
            else:
                seen_names.add(job.name)

            if not job.paths:
                errors.append(f"Job {job.name} has no paths")

            if not job.schedule:
                errors.append(f"Job {job.name} is missing schedule")

        return errors
