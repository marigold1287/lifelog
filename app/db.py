from sqlalchemy import create_engine
from collections.abc import Generator, Sequence, Callable
from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URI")

if DATABASE_URL is None:
    raise ValueError(".envファイルでDATABASE_URIを指定してください")

engine = create_engine(
    DATABASE_URL,
    echo=False
)

class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(engine)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

UNIQUE_CONSTRAINT_CODE = "23505"
NOT_NULL_VIOLATION_CODE = "23502"


class UniqueConstraintError(Exception):
    pass

class NotNullViolationError(Exception):
    pass

class NotFoundError(Exception):
    pass

class DomainValidationError(ValueError):
    pass



CurrentRecord = TypeVar("CurrentRecord")
UpdatedRecord = TypeVar("UpdatedRecord")

def sync_records(
        session: Session,
        current_records: Sequence[CurrentRecord],
        updated_records: Sequence[UpdatedRecord],
        update: Callable[[CurrentRecord, UpdatedRecord], None],
        create: Callable[[UpdatedRecord], None],
        is_valid: Callable[[UpdatedRecord], bool]=lambda record: True
) -> None:
    updated_by_id = {
        record.id: record
        for record in updated_records
        if record.id is not None
    }
    for current_record in current_records:
        updated_record = updated_by_id.get(current_record.id)
        if updated_record is not None and is_valid(updated_record):
            update(current_record, updated_record)
        else:
            session.delete(current_record)

    # 残ったものは新規追加
    for updated_record in updated_records:
        if updated_record.id is None and is_valid(updated_record):
            try:
                create(updated_record)
            except Exception as e:
                print("desERROR")
                raise e
        

def safe_commit(session: Session):
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()

        error_code = getattr(e.orig, "pgcode", None)

        if error_code and str(error_code) == UNIQUE_CONSTRAINT_CODE:
            raise UniqueConstraintError("一意制約違反, データが重複しています") from e
        if error_code and str(error_code) == NOT_NULL_VIOLATION_CODE:
            raise NotNullViolationError("非NULL違反, このレコードを必要としている他のレコードがあります") from e

        raise e
    except Exception as e:
        error_code = getattr(e.orig, "pgcode", None)
        session.rollback()

        raise e


def validate_non_empty_string(value: str, field_name: str = "名前") -> str:
    if not value or not value.strip():
        raise DomainValidationError(f"空文字列や空白のみの{field_name}は登録できません")
    return value.strip()
