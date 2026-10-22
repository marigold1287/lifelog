"""NDLのIDリストからISBNのない行を取り除く"""
import pandas as pd
from pathlib import Path
from sqlalchemy import select
from app.db import SessionLocal
from app.book.book import Book



PWD = Path(__file__).parent

def filter_merged_file():
    first = True
    for chunk in pd.read_csv(PWD / "resources" / "merged.tsv", sep="\t", dtype=str, chunksize=100_000):
            chunk = chunk.dropna(subset=["ISBN"])
            chunk.to_csv(PWD / "resources" / "filtered.tsv", sep="\t", index=False,
                        mode="w" if first else "a",
                        header=first)
            first = False

def create_isbn_ndlbib_mapping():
    df = pd.read_csv(PWD / "resources" / "filtered.tsv", sep="\t", dtype=str)
    df_clean = df[df['ISBN'].notna()]

    mapping = df_clean.set_index("ISBN")["NDLBib"].to_dict()

    return mapping

def update_ndlbib_id():
     mapping = create_isbn_ndlbib_mapping()

     with SessionLocal() as session:
        books = session.execute(select(Book).where(Book.isbn.is_not(None))).scalars().all()
        for book in books:
            ndlbib = mapping.get(book.isbn, None)
            if ndlbib:
                book.ndlbib = ndlbib

        session.commit()


if __name__ == "__main__":
     update_ndlbib_id()