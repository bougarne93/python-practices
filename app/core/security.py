from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.services.user_sql_service import UserSQLService

from typing import Optional

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    # Log the token clearly to see if it's truncated
    print(f"DEBUG: Token received (len={len(token)}): '{token}'")
    
    # Check if there are 3 segments
    segments = token.split('.')
    print(f"DEBUG: Number of segments: {len(segments)}")
    if len(segments) != 3:
        print(f"DEBUG: TOKEN IS MISSING SEGMENTS! segments found: {segments}")

    try:
        print(f"DEBUG: Decoding token with SECRET_KEY={SECRET_KEY} and ALGORITHM={ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Payload: {payload}")
        user_id = payload.get("sub")
        if not user_id:
            print("DEBUG: No 'sub' in payload")
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        print(f"DEBUG: JWTError: {e}")
        # En cas d'erreur de signature, essayons de voir si c'est la clé
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    user = await UserSQLService.get_user(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
