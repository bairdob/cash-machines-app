from functools import lru_cache
from pathlib import Path
from typing import Tuple

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, func

from src.database import engine
from src.db_models import Statistics
from src.models.get_tile_request import TileRequestParameters, TilePosition, TileAttributes, \
    GetTileRequest
from src.models.wmts_request_base import WmtsRequestBase, RequestBase
from src.schemas import StatisticsNormalized


@lru_cache(maxsize=64)
def get_first_file_in_folder(path: str, extension: str) -> str:
    """
    Возвращает полный путь к первому файлу в папке с заданным расширением.

    :param path: Путь к папке.
    :param extension: Расширение файла.
    :return: Полный путь к первому файлу по расширению.
    :raises FileNotFoundError: Если в папке не найден файл с указанным расширением.
    """
    path = Path(path)
    if path.is_file():
        return str(path)
    for file_path in path.iterdir():
        if file_path.is_file() and file_path.name.endswith(extension):
            return str(file_path)
    raise FileNotFoundError(f"В папке '{path}' не найден файл с расширением '{extension}'.")


async def get_request(
        layer: str,
        style: str,
        tilematrixset: str,
        service: str,
        request: str,
        version: str,
        format: str,
        tilematrix: str,
        tilecol: int,
        tilerow: int,
) -> RequestBase:
    """Возвращает класс по типу операции (request)."""
    # валидируем базовые операции
    try:
        WmtsRequestBase(
            service=service,
            request=request,
            version=version, )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

    if request == 'gettile':
        return GetTileRequest(
            tilerequestparameters=TileRequestParameters(layer=layer, style=style),
            tileattributes=TileAttributes(
                format=format,
                tileposition=TilePosition(
                    tilematrixset=tilematrixset,
                    tilecol=tilecol,
                    tilerow=tilerow,
                    tilematrix=tilematrix
                )
            )
        )
    else:
        # TODO: заглушка для getCapabilities, getFeatureInfo
        pass


def map_statistics_to_statistics_normalized(statistics, max_priority, min_priority):
    StatisticsNormalized.max_priority = max_priority
    StatisticsNormalized.min_priority = min_priority
    result = []
    for statistic in statistics:
        result.append(
            StatisticsNormalized(
                atm_id=statistic.atm_id,
                services_per_day=statistic.services_per_day,
                amount_per_day=statistic.amount_per_day,
            )
        )
    sorted_result = sorted(
        result,
        key=lambda stat: stat.priority,
        reverse=True,
    )
    return sorted_result


def get_max_min_priority() -> Tuple[float, float]:
    with engine.connect() as connection:
        query_max_pr = select(func.max(Statistics.amount_per_day / Statistics.services_per_day))
        query_min_pr = select(func.min(Statistics.amount_per_day / Statistics.services_per_day))

        max_priority = connection.execute(query_max_pr).fetchone()
        min_priority = connection.execute(query_min_pr).fetchone()

    return max_priority[0], min_priority[0]
