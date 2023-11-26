import hashlib
import json
import traceback

import numpy as np
from geopy import distance

from fastapi import FastAPI, Depends, Query, status, HTTPException
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

LIMIT = 5

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
    atms = db.query(ATM).limit(LIMIT).all()
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


@app.get("/api/v1/locations/")
def get_all_locations(db: Session = Depends(get_db)):
    locations = db.query(Locations).all()
    return locations


@app.get("/api/v1/statistics/")
def get_all_statistics(db: Session = Depends(get_db)):
    statistics = db.query(Statistics).all()
    return statistics


@app.get("/api/v1/atms_list", response_model=list[StatisticsNormalized])
def get_ranged_atms(db: Session = Depends(get_db)):
    statistics = db.query(Statistics).all()
    max_pr, min_pr = get_max_min_priority()
    stats = map_statistics_to_statistics_normalized(statistics, max_pr, min_pr)
    return stats


@app.get("/api/v1/route")
def get_ranged_atms(db: Session = Depends(get_db)):
    from random import shuffle
    l = list(range(1, 4))
    locations = db.query(Locations.longitude, Locations.latitude).filter(Locations.atm_id.in_(l)).limit(3).all()
    shuffle(locations)
    new_locations = [tuple(map(float, point)) for point in locations]

    feature = Feature(geometry=LineString(coordinates=new_locations))
    crs = {
        'type': 'name',
        'properties': {
            'name': 'EPSG:4326',
        },
    }
    feature_collection = FeatureCollection([feature], crs=crs)

    return feature_collection


@app.get("/api/v1/distance")
def get_distance_matrix(db: Session = Depends(get_db)):
    locations = db.query(Locations.latitude, Locations.longitude).limit(LIMIT).all()
    num_points = len(locations)
    distance_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            distance_matrix[i, j] = int(distance.distance(locations[i], locations[j]).km)

    # print(distance_matrix)
    return json.dumps(distance_matrix.tolist())

