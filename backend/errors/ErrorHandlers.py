from fastapi import FastAPI

from errors.ErrorValidationError import error_validation_error


def register_error_handlers(app: FastAPI):
    error_validation_error(app)
