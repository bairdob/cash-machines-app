from typing import Tuple

from sqlalchemy import select, func

from src.wmts.database import engine
from src.db_models import Statistics
from src.schemas import StatisticsNormalized


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
