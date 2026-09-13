
from fastapi import APIRouter, HTTPException
import httpx
import xml.etree.ElementTree as ET

router = APIRouter()

@router.get("/api/ndl/{isbn}")
async def get_ndl_link(isbn: str):
    url = "https://ndlsearch.ndl.go.jp/api/opensearch"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"isbn": isbn})
        response.raise_for_status()

    root = ET.fromstring(response.text)

    link = root.findtext(".//item/link")

    if not link:
        raise HTTPException(
            status_code=404,
            detail="NDLに該当する書籍が見つかりません",
        )

    return {"link": link}
