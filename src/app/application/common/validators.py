import logging
from datetime import date

logger = logging.getLogger(__name__)


def validate_date_range(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        logger.warning(
            "Failed to validate date range: start_date '%s' is after end_date '%s'.",
            start_date,
            end_date,
        )
        raise ValueError("INVALID ARGUMENT: Start date cannot be after end date.")
