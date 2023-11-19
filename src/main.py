import hashlib
import traceback
from http.client import HTTPException

from fastapi import FastAPI, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from geojson import Feature, Point, FeatureCollection, LineString
from sqlalchemy.orm import Session

from src.database import get_db
from src.db_models import ATMStatistics, ATM, Locations, Statistics
from src.middleware import LowerCaseMiddleware
from src.models.wmts_request_base import RequestBase
from src.models.wmts_service import WmtsService
from src.schemas import StatisticsNormalized
from src.utils import get_request, map_statistics_to_statistics_normalized, \
    get_max_min_priority

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(LowerCaseMiddleware())


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    error_response = {
        'message': str(exc),
        'traceback': traceback.format_exc(),
        'url': request.url._url,
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


@app.get("/ping")
async def ping():
    return 'pong'


# Route to create ATM statistics
@app.get("/api/v1/atm_statistics/")
async def get_atm_statistics(atm_id: int = Query(..., title="ATM ID"), db: Session = Depends(get_db)):
    statistics = db.query(ATMStatistics).filter(ATMStatistics.atm_id == atm_id).first()
    if statistics is None:
        raise HTTPException(status_code=404, detail="Statistics not found")
    return statistics


# Route to get a list of all ATMs
@app.get("/api/v1/atms/")
def get_all_atms(db: Session = Depends(get_db)):
    atms = db.query(ATM).all()
    return atms


# Route to get details of a specific ATM by ID
@app.get("/api/v1/atms/{atm_id}")
def get_atm_by_id(atm_id: int, db: Session = Depends(get_db)):
    atm = db.query(ATM).filter(ATM.atm_id == atm_id).first()
    if atm is None:
        raise HTTPException(status_code=404, detail="ATM not found")
    return atm


@app.get("/api/v1/atm_geojson")
def get_atm_geojson(db: Session = Depends(get_db)):
    atms = db.query(ATM).all()
    features = []

    for atm in atms:
        feature = Feature(
            geometry=Point((atm.longitude, atm.latitude)),
            properties={
                "atm_id": atm.atm_id,
                "location_name": atm.location_name,
                "address": atm.address,
                "city": atm.city,
                "state": atm.state,
                "country": atm.country,
                "last_service_date": str(atm.last_service_date),
                "is_operational": atm.is_operational
            }
        )
        features.append(feature)
    crs = {
        'type': 'name',
        'properties': {
            'name': 'EPSG:4326',
        },
    }

    feature_collection = FeatureCollection(features, crs=crs)
    return feature_collection


@app.get("/wmts", response_class=Response)
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
