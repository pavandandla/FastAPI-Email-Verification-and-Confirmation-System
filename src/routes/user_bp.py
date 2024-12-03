# routes/user_bp.py
from fastapi import APIRouter
from controllers.user_controller import (
    signup,
    confirm_user,
    send_email_password_reset,
    update_password,
    login
)

user_bp = APIRouter()

user_bp.add_api_route("/signup", signup, methods=["POST"])
user_bp.add_api_route("/confirm-user/{token}", confirm_user, methods=["GET"])
user_bp.add_api_route("/login", login, methods=["POST"])
# user_bp.add_api_route("/password-reset-request", send_email_password_reset, methods=["POST"])
user_bp.add_api_route(
    "/password-reset-request", 
    send_email_password_reset, 
    methods=["POST"],
    summary="Request password reset email",
    description="Requires JWT token in Authorization header. Email extracted from token."
)
user_bp.add_api_route("/update-password/{token}", update_password, methods=["POST"])
