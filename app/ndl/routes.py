
from fastapi import APIRouter, HTTPException
import httpx
import xml.etree.ElementTree as ET

router = APIRouter()

@router.get("/api/ndl/{isbn}")
async def get_ndl_link(isbn: str):
    url = "https://ndlsearch.ndl.go.jp/api/opensearch"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"isbn": isbn}, timeout=10.0)
            response.raise_for_status()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="NDLへの接続がタイムアウトしました"
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="NDLへのアクセスが多すぎます。しばらくしてから再試行してください"
            )
        raise HTTPException(
            status_code=502,
            detail="NDLからエラーが返されました"
        )

    root = ET.fromstring(response.text)

    link = root.findtext(".//item/link")

    if not link:
        raise HTTPException(
            status_code=404,
            detail="NDLに該当する書籍が見つかりません",
        )

    return {"link": link}
