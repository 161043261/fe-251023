from fastapi import HTTPException, Request, status
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from os import getenv
from dotenv import load_dotenv
from typing import Optional

load_dotenv("./.env.local")

clerk_sdk = Clerk(bearer_auth=getenv("CLERK_SECRET_KEY"))


def get_user_info(request: Request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request=request,
            options=AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],
                jwt_key=getenv("JWKS_PUBLIC_KEY"),
            ),
        )

        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="request_state.is_signed_in == False",
            )

        user_id: Optional[str] = None
        if request_state.payload is not None:
            user_id = request_state.payload.get("sub")

        user_info = {"user_id": user_id}
        return user_info

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
