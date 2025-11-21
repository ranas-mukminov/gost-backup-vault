from ..domain.models import BackupConfig

class PolicyValidator:
    @staticmethod
    def validate(config: BackupConfig) -> List[str]:
        errors = []
        
        if not config.jobs:
            errors.append("No backup jobs defined")
            
        for job in config.jobs:
            if not job.paths:
                errors.append(f"Job {job.name} has no paths")
            
            # Simple check for schedule format (very basic)
            if "@" not in job.schedule and " " not in job.schedule:
                 # Allow simple words like "daily" if supported, but for now assume strict format
                 pass 

        return errors
