

from fastapi import Query


class PaginationParams:
    def __init__(
            self,
            page: int = Query(default=1, ge=1, description="页码"),
            pageSize: int = Query(default=10, ge=1, le=1000, description="每页数量")
            ) -> None:
        self.page = page
        self.pageSize = pageSize
    @property
    def offset(self) -> str:
        return (self.page - 1) * self.pageSize    