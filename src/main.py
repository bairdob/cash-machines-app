import json
import traceback

import numpy as np
from fastapi import FastAPI, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from geojson import Feature, Point, FeatureCollection, LineString
from geopy import distance
from sqlalchemy.orm import Session

from src.db_models import Locations, Statistics
from src.middleware import LowerCaseMiddleware
from src.tsp_service import TSPService
from src.utils import get_db
from src.wmts.router import router as wmts_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(LowerCaseMiddleware())
app.include_router(wmts_router, prefix="", tags=["Wmts"])

LIMIT = 10
CRS_EPSG = 'EPSG:4326'


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    Обработчик исключений в человекочитаемый вид.

    :param request: Объект запроса
    :param exc: объект исключений
    :return: словарь с данными исключения
    """
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
    """Возвращает ответ на тестовый запрос."""
    return 'pong'


@app.get("/api/v1/atm_geojson")
def get_atms_geojson(db: Session = Depends(get_db)) -> dict:
    """
    Получаем GeoJSON с расположением банкоматов.

    :param db: сессия базы данных
    :return: словарь GeoJSON
    """
    # получаем записи из таблицы Locations
    locations = db.query(Locations).limit(LIMIT).all()

    # собираем фичи для GeoJSON
    features = [
        Feature(
            geometry=Point((location.longitude, location.latitude)),
            properties={
                "atm_id": location.atm_id,
                "address": location.address,
            }
        )
        for location in locations
    ]

    # устанавливаем систему координат для openlayers
    crs = {
        'type': 'name',
        'properties': {
            'name': CRS_EPSG,
        },
    }
    feature_collection = FeatureCollection(features, crs=crs)

    return feature_collection


@app.get("/api/v1/locations/")
def get_all_locations(db: Session = Depends(get_db), response_model=list[Locations]):
    """
    Получаем записи Locations.

    :param db: сессия базы данных
    :param response_model: список типа записей таблицы
    :return: список записей таблицы
    """
    locations = db.query(Locations).all()
    return locations


@app.get("/api/v1/statistics/")
def get_all_statistics(db: Session = Depends(get_db), response_model=list[Statistics]):
    """
    Получаем записи Statistics.

    :param db: сессия базы данных
    :param response_model: список типа записей таблицы
    :return: список записей таблицы
    """
    statistics = db.query(Statistics).all()
    return statistics


@app.get("/api/v1/route")
def get_route(db: Session = Depends(get_db)):
    """
    Получаем GeoJSON оптимального пути.

    :param db: сессия базы данных
    :return: словарь GeoJSON
    """
    # получаем матрицу расстояний
    distance_matrix = json.loads(get_distance_matrix(db=db))

    # находим оптимальный маршрут
    service = TSPService(distance_matrix)
    service.tsp_brute_force()
    route_list = service.get_route()  # type: list

    # получаем список координат маршрута
    locations = db.query(Locations).filter(Locations.atm_id.in_(route_list)).limit(
        LIMIT).all()
    points = [(float(location.longitude), float(location.latitude)) for location in locations]
    points = [points[atm_id - 1] for atm_id in route_list]

    # получаем данные о банкоматах
    atms = [{location.atm_id: location.address} for location in locations]
    atms = [atms[atm_id - 1] for atm_id in route_list]

    # собираем фичи для GeoJSON
    feature = Feature(
        geometry=LineString(coordinates=points),
        properties={'route_list': atms}
    )
    # устанавливаем систему координат для openlayers
    crs = {
        'type': 'name',
        'properties': {
            'name': CRS_EPSG,
        },
    }
    feature_collection = FeatureCollection([feature], crs=crs)

    return feature_collection


@app.get("/api/v1/distance")
def get_distance_matrix(db: Session = Depends(get_db)):
    """
    Возвращает матрицу расстояний между банкоматами.

    :param db: сессия базы данных
    :return: матрицу расстояний
    """
    # получаем список формата (широта, долгота) из таблицы Locations
    locations = db.query(Locations.latitude, Locations.longitude).limit(LIMIT).all()
    num_points = len(locations)

    # создаем матрицу NxN расстояний, где N - количество банкоматов
    distance_matrix = np.zeros((num_points, num_points))

    # считаем расстояние между банкоматами как евклидово расстояние между точками
    for i in range(num_points):
        for j in range(num_points):
            distance_matrix[i, j] = distance.distance(locations[i], locations[j]).km

    return json.dumps(distance_matrix.tolist())
