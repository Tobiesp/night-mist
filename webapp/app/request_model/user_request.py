from app.request_model.signup_request import SignupRequest


class UserRequest(SignupRequest):
    role: str = None
    