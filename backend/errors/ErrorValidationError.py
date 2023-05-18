from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


def error_validation_error(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, e: RequestValidationError):
        errors = e.errors()

        error_messages = []  # refactoring by promotion

        for error in errors:
            if error["msg"] == "field required":
                field = error["loc"][1]
                error_messages.append({
                    "error": f"The field [{field}] is required",
                    "code": f"{field.upper()}_REQUIRED"  # LABEL_REQUIRED TODO_ID_REQUIRED
                })
            else:
                field = "unknown"
                error_messages.append({
                    "error": f"Unknown error",
                    "code": f"{field.upper()}_REQUIRED"
                })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({
                "messages": error_messages,
                "code": "INVALID_REQUEST",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            })
        )
