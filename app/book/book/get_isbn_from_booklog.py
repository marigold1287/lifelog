from pathlib import Path
import pandas as pd
from sqlalchemy import select
from app.db import SessionLocal
from .models import Book

PWD = Path(__file__).parent

HEADERS = [
    "サービスID", 
    "アイテムID", 
    "ISBN", 
    "カテゴリ", 
    "評価", 
    "読書状況", 
    "レビュー", 
    "タグ", 
    "読書メモ(非公開)", 
    "登録日時", 
    "読了日", 
    "タイトル", 
    "作者名", 
    "出版社名", 
    "発行年", 
    "タイプ", 
    "ページ数" 
]

def main():
    df = pd.read_csv(PWD / "resources" / "booklog20261022092219.csv", encoding="sjis", header=None)
    df.columns = HEADERS
    df = df.astype(object).where(pd.notna(df), None)
    df_clean = df[df['ISBN'].notna()]
    isbn_str = df_clean['ISBN'].astype(str).str.replace(r'\.0$', '', regex=True)


    mapping = dict(zip(df_clean['アイテムID'], isbn_str))

    print(mapping)

    with SessionLocal() as session:
        books = session.execute(select(Book).where(Book.amazon_asin.is_not(None))).scalars().all()
        for book in books:
            isbn = mapping.get(book.amazon_asin, None)
            if isbn:
                book.isbn = isbn

        session.commit()


if __name__ == "__main__":
    main()