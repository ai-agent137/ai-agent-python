from fastapi import Depends, Header, HTTPException, status
from app.dependencies.settings import get_app_settings
from app.schema.user import CurrentUser, UserRole
from app.core.config import settings

async def verify_api_key(
        x_api_key: str | None = Header(default=None),
        ) -> str:
    if(not x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少请求头 x-api-key",
        )
    if x_api_key != settings.app_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key 不正确",
        )

    return x_api_key

async def get_current_user(
        api_key:str = Depends(verify_api_key),
        x_user_id: str | None = Header(default=None),
        x_username: str | None = Header(default=None),
        x_user_role: str = Header(default="user"),
) ->CurrentUser:
    if not x_user_id:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="缺少请求头 x-user-id"
        )
    if not x_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少请求头 x-username",
        )
    role = UserRole.ADMIN if x_user_role == "admin" else UserRole.USER
    return CurrentUser(
        user_id=x_user_id,
        username=x_username,
        role=role,
        is_active=True,
    )

async def require_admin(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )

    return current_user