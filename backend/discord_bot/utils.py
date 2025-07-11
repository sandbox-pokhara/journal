import re
from datetime import datetime, timedelta

from django.utils import timezone


def get_date_from_message(message: str):
    message = message.lower()
    today = timezone.localtime(timezone.now()).date()
    # Check for specific keywords
    if "day after tomorrow" in message:
        return today + timedelta(days=2)
    if "tomorrow" in message:
        return today + timedelta(days=1)
    if "today" in message:
        return today

    # Check for a date pattern (YYYY-MM-DD)
    date_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", message)
    if date_match:
        try:
            return datetime.strptime(date_match.group(), "%Y-%m-%d").date()
        except ValueError:
            # Return today on invalid date
            return today

    # Default to today if no valid date is found
    return today
