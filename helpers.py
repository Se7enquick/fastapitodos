from fastapi import HTTPException, status


def successful_response(status_code: int):
    return {
        'status_code': status_code,
        'transaction': 'Successful'
    }


def http_exception(status_code: int, detail: str, headers=None):
    return HTTPException(status_code=status_code, detail=detail)


def get_user_exception():
    credentials_exception = http_exception(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        {"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def token_exception():
    token_exception_response = http_exception(status.HTTP_401_UNAUTHORIZED,
                                              "Incorrect username or password",
                                              {"WWW-Authenticate": "Bearer"})
    return token_exception_response
