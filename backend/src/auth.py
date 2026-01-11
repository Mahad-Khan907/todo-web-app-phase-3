from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from .models import User
from .security import verify_access_token
from .database import get_session

# HTTP Bearer token scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user based on the JWT token in the Authorization header.

    Args:
        credentials: The HTTP authorization credentials from the header
        session: Database session dependency

    Returns:
        The authenticated User object

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    # Verify the token and get the payload
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extract user ID from the payload
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Query the database for the user
    # Handle potential UUID format issues
    try:
        user = session.get(User, user_id)
    except Exception as e:
        # If there's an error with the user_id format, try to handle it gracefully
        import uuid
        import re

        # Check if user_id is a hex string without dashes that needs to be formatted
        if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
            # Format as UUID: 12345678123456781234567812345678 -> 12345678-1234-5678-1234-567812345678
            formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
            user = session.get(User, formatted_uuid)
        elif isinstance(user_id, str) and not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', user_id):
            # If it's not a properly formatted UUID, try to convert it
            try:
                uuid_obj = uuid.UUID(user_id)
                user = session.get(User, str(uuid_obj))
            except ValueError:
                # If it's still not valid, raise the original exception
                raise credentials_exception
        else:
            # If it's a different error, raise the original exception
            raise credentials_exception

    if user is None:
        raise credentials_exception

    return user