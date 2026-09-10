import argparse
from sqlalchemy import delete
from pathlib import Path
import pandas as pd
import numpy as np
from app.db import SessionLocal
from .models import Publisher, Label, PublisherAlias
from .repository import get_publishers

PWD = Path(__file__).parent

def insert_publisher_from_file():
    csv_path = PWD / "resources" / "publishers.csv"

    with csv_path.open(encoding="utf-8") as f:
        next(f)  # ヘッダーを飛ばす

        with SessionLocal() as session:
            for line in f:
                row = line.strip().split(",")
                name = row[0].strip()
                yomigana = row[1].strip()
                aliases = row[2:]

                publisher = Publisher(
                    name=name,
                    yomigana=yomigana
                )
                session.add(publisher)
                for a in aliases:
                    if a.strip():
                        alias = PublisherAlias(
                            publisher=publisher,
                            alias=a.strip()
                        )
                        session.add(alias)
            session.commit()

def import_label_from_file():
    df = pd.read_csv(PWD.parent / "resources" / "booklist.csv")
    publisher_labels = (
        df[["publisher", "label"]]
        .drop_duplicates()
        .groupby("publisher")["label"]
        .apply(list)
        .to_dict()
    )
    print(publisher_labels)

    with SessionLocal() as session:
        publishers = get_publishers(session)
        publisher_mapping = {
            publisher.name: publisher
            for publisher in publishers
        }

        for publisher, labels in publisher_labels.items():
            label_record = Label(
                publisher = publisher_mapping[publisher],
                name = "レーベルなし",
            )
            session.add(label_record)
            for label in labels:
                if label is np.nan:
                    continue
                label_record = Label(
                    publisher=publisher_mapping[publisher],
                    name=label
                )
                session.add(label_record)

        session.commit()


def delete_all_records():
    with SessionLocal() as session:
        session.execute(delete(PublisherAlias))
        session.execute(delete(Label))
        session.execute(delete(Publisher))
        session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publisher スクリプト実行ツール")
    # 実行したい関数名を引数として受け取る
    parser.add_argument("command", choices=["import_publisher", "delete", "import_label"], help="実行するコマンド")

    args = parser.parse_args()

    if args.command == "import_publisher":
        insert_publisher_from_file()
    if args.command == "delete":
        delete_all_records()
    if args.command == "import_label":
        import_label_from_file()