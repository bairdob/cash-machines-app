import hashlib

from fastapi import APIRouter, Depends, Response

from src.wmts.models.wmts_request_base import RequestBase
from src.wmts.utils import get_request
from src.wmts.wmts_service import WmtsService

router = APIRouter()


@router.get("/wmts", response_class=Response)
async def get_resource(request: RequestBase = Depends(get_request)) -> Response:
    """Возвращает ответ по типу запроса Wmts сервиса."""
    tile = await WmtsService.get_tile(
        layer=request.tilerequestparameters.layer,
        tilematrix=int(request.tileattributes.tileposition.tilematrix),
        tilerow=request.tileattributes.tileposition.tilerow,
        tilecol=request.tileattributes.tileposition.tilecol
    )

    return Response(
        content=tile,
        media_type=request.tileattributes.format,
        headers={
            'ETag': str(hashlib.sha256(tile).hexdigest()),
            "Cache-Control": "max-age=604800"
        }
    )
