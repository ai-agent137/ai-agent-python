from enum import IntEnum


class ErrorCode(IntEnum):
    SUCCESS = 0

    BAD_REQUEST = 40000
    UNAUTHORIZED = 40100
    FORBIDDEN = 40300
    NOT_FOUND = 40400
    VALIDATION_ERROR = 42200

    MODEL_NOT_SUPPORTED = 50001
    LLM_CALL_FAILED = 50002
    RAG_QUERY_FAILED = 50003
    TOOL_CALL_FAILED = 50004
    AGENT_RUN_FAILED = 50005

    INTERNAL_ERROR = 50000


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: int = ErrorCode.BAD_REQUEST,
        status_code: int = 400,
        data: dict | list | None = None,
    ):
        self.message = message
        self.code = int(code)
        self.status_code = status_code
        self.data = data

        super().__init__(message)