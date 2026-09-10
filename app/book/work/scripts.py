import argparse
from sqlalchemy import delete
from pathlib import Path
import pandas as pd
import numpy as np
from app.db import SessionLocal
from app.book.author.repository import get_all as get_all_authors
from app.book.publisher.repository import get_all as get_all_publishers
from app.book.book.models import Book, BookReading
from .models import Work, WorkAuthor

PWD = Path(__file__).parent

def create_author_mapping():
    with SessionLocal() as session:
        authors = get_all_authors(session)
        return {
            author.name: author
            for author in authors
        }

def create_label_mapping():
    with SessionLocal() as session:
        publishers = get_all_publishers(session)
        return {
            f"{publisher.name}_{label.name}": label
            for publisher in publishers
            for label in publisher.labels
        }

def import_from_booklist():
    work_df = pd.read_csv(PWD / "resources" / "books.csv")
    book_df = pd.read_csv(PWD / "resources" / "series.csv")
    read_df = pd.read_csv(PWD / "resources" / "read_record.csv")

    labels = create_label_mapping()
    authors = create_author_mapping()


    with SessionLocal() as session:
        for _, row in work_df.iterrows():
            label_name = row["label"] if pd.notna(row["label"]) else "レーベルなし"

            label = labels[f"{row["publisher"].strip()}_{label_name.strip()}"]
            author = authors[row["author"].strip()]
            work = Work(
                title=row["title"],
                label=label,
            )
            session.add(work)
            work_author = WorkAuthor(
                work=work,
                author=author
            )
            session.add(work_author)
            work_books_df = book_df[book_df["book_id"] == row["book_id"]]
            for _, work_row in work_books_df.iterrows():
                book = Book(
                    title=work_row["title"] if pd.notna(work_row["title"]) else None,
                    volume=work_row["volume"] if pd.notna(work_row["volume"]) else None,
                    registration_date=work_row["registration_date"],
                    amazon_asin=work_row["amazon_id"] if pd.notna(work_row["amazon_id"]) else None,
                    work=work,
                )
                session.add(book)
                book_read_df = read_df[read_df["series_id"] == work_row["series_id"]]
                for _, read_row in book_read_df.iterrows():
                    read = BookReading(
                        read_date=read_row["read_date"],
                        book=book,
                    )
                    session.add(read)

        session.commit()


def delete_all_records():
    with SessionLocal() as session:
        session.execute(delete(WorkAuthor))
        session.execute(delete(BookReading))
        session.execute(delete(Book))
        session.execute(delete(Work))
        session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publisher スクリプト実行ツール")
    # 実行したい関数名を引数として受け取る
    parser.add_argument("command", choices=["import_publisher", "delete", "import"], help="実行するコマンド")

    args = parser.parse_args()

    if args.command == "import":
        import_from_booklist()

    if args.command == "delete":
        delete_all_records()