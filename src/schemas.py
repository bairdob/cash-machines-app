from typing import ClassVar

from pydantic import BaseModel, computed_field


class StatisticsNormalized(BaseModel):
    atm_id: int
    services_per_day: int
    amount_per_day: float
    min_priority: ClassVar[float]
    max_priority: ClassVar[float]

    @computed_field
    @property
    def priority(self) -> float:
        if self.services_per_day != 0:
            priority = self.amount_per_day / self.services_per_day
        else:
            priority = 0.0
        if self.max_priority - self.min_priority != 0:
            normalized_priority = (priority - self.min_priority) / (self.max_priority - self.min_priority)
        else:
            normalized_priority = 0.0

        return normalized_priority
