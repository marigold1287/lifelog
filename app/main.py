from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.book import book_router
from app.bill import bill_router
from app.ndl import ndl_router
from app.db import UniqueConstraintError, DomainValidationError, NotFoundError, NotNullViolationError

app = FastAPI()
app.include_router(book_router)
app.include_router(bill_router)
app.include_router(ndl_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.exception_handler(UniqueConstraintError)
async def unique_constraint_exception_handler(request: Request, exc: UniqueConstraintError):
    return JSONResponse(
        status_code=409,
        content={
            "code": "unique_constraint_violation",
            "message": "すでに登録されています",
        }
    )

@app.exception_handler(NotNullViolationError)
async def not_null_violation_handler(request: Request, exc: NotNullViolationError):
    return JSONResponse(
        status_code=409,
        content={
            "code": "not_null_violation",
            "message": str(exc)
        }
    )

@app.exception_handler(DomainValidationError)
async def database_validation_error_handler(request: Request, exc: DomainValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "code": "database_validation_error",
            "message": str(exc),
        }
    )

@app.exception_handler(ValidationError)
async def database_validation_error_handler(request: Request, exc: ValidationError):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={
            "code": "database_validation_error",
            "message": str(exc),
        }
    )

@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "code": "not_found_error",
            "message": str(exc),
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    if exc.status_code == 405:
        return JSONResponse(
            status_code=405,
            content={
                "code": "method_not_allowed",
                "message": "許可されていないメソッドです",
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": "http_error",
            "message": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    error = exc.errors()[0]
    print(exc)

    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": str(error["msg"]).removeprefix("Value error, "),
        },
    )

