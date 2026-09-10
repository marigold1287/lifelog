import argparse
from sqlalchemy import delete
from pathlib import Path
import pandas as pd
import numpy as np
from app.db import SessionLocal
from .models import AuthorAlias, Author
# from .repository import get_publishers

PWD = Path(__file__).parent

# def insert_publisher_from_file():
#     csv_path = PWD / "resources" / "publishers.csv"

#     with csv_path.open(encoding="utf-8") as f:
#         next(f)  # ヘッダーを飛ばす

#         with SessionLocal() as session:
#             for line in f:
#                 row = line.strip().split(",")
#                 name = row[0].strip()
#                 yomigana = row[1].strip()
#                 aliases = row[2:]

#                 publisher = Publisher(
#                     name=name,
#                     yomigana=yomigana
#                 )
#                 session.add(publisher)
#                 for a in aliases:
#                     if a.strip():
#                         alias = PublisherAlias(
#                             publisher=publisher,
#                             alias=a.strip()
#                         )
#                         session.add(alias)
#             session.commit()

def import_author_from_booklist():
    df = pd.read_csv(PWD.parent / "resources" / "booklist.csv", usecols=["author"])
    df["author"] = df["author"].str.strip()
    df = df.drop_duplicates()

    with SessionLocal() as session:
        records = [
            Author(name=author_name)
            for author_name in df["author"].to_list() if author_name
        ]
        session.add_all(records)

        session.commit()


# def delete_all_records():
#     with SessionLocal() as session:
#         session.execute(delete(PublisherAlias))
#         session.execute(delete(Label))
#         session.execute(delete(Publisher))
#         session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publisher スクリプト実行ツール")
    # 実行したい関数名を引数として受け取る
    parser.add_argument("command", choices=["import_publisher", "delete", "import"], help="実行するコマンド")

    args = parser.parse_args()

    # if args.command == "import_publisher":
    #     insert_publisher_from_file()
    # if args.command == "delete":
    #     delete_all_records()
    if args.command == "import":
        import_author_from_booklist()