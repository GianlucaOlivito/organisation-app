import logging
from datetime import date

logger = logging.getLogger(__name__)


def validate_date_range(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        logger.warning(
            f"Operation failed: start_date ({start_date}) is after end_date ({end_date})."
        )
        raise ValueError("INVALID ARGUMENT: Start date cannot be after end date.")
