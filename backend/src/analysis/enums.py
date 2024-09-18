from enum import Enum


class AnalysisStatus(Enum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    FAILED = "failed"
    REVOKED = "revoked"
