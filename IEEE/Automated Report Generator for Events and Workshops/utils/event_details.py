"""
utils/event_details.py
----------------------
ইভেন্টের মূল তথ্য (Report ID, Date, Time, Venue, Report Name)
Word টেমপ্লেটের উপযোগী করে প্রস্তুত করে।

টেমপ্লেটের ট্যাগ:
    {{ report_id }}   {{ date }}   {{ time }}   {{ venue }}   {{ report_name }}
"""

from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time


def _clean(value) -> str:
    """
    joid value none ashe tahole empty string return korte hobe, nahole whitespace komiye
    sudhu string ei return korte hobe.
    """
    return "" if value is None else str(value).strip()



def format_date(value, fmt: str = "%d %B %Y") -> str:
    """
    st.date_input() এর date/datetime অথবা স্ট্রিং গ্রহণ করে
    সুন্দর ফরম্যাটে (যেমন: 21 October 2026) রিটার্ন করে।
    """
    if isinstance(value, (_date, _datetime)):
        return value.strftime(fmt)
    return _clean(value)




def format_time(value, fmt: str = "%I:%M %p") -> str:
    """
    st.time_input() এর time/datetime অথবা স্ট্রিং গ্রহণ করে
    12 ঘণ্টার ফরম্যাটে (যেমন: 03:30 PM) রিটার্ন করে।
    """
    if isinstance(value, (_time, _datetime)):
        return value.strftime(fmt)
    return _clean(value)




def validate_event_details(report_id, venue, report_name) -> list[str]:
    """
    eta kaj hocche input validate kora like fastapi e pydantic er kaj
    """
    errors = []
    if not _clean(report_id):
        errors.append("Report ID দিতে হবে।")
    if not _clean(venue):
        errors.append("Venue দিতে হবে।")
    if not _clean(report_name):
        errors.append("Report Name দিতে হবে।")
    return errors


def prepare_event_details(
    report_id,
    date,
    time,
    venue,
    report_name,
) -> dict:
    """
    ইভেন্টের তথ্য প্রসেস করে docxtpl-এর context dict-এর অংশ হিসেবে রিটার্ন করে।

    Returns:
        {
            "report_id":   str,
            "date":        str,
            "time":        str,
            "venue":       str,
            "report_name": str,
        }
    """
    return {
        "report_id": _clean(report_id),
        "date": format_date(date),
        "time": format_time(time),
        "venue": _clean(venue),
        "report_name": _clean(report_name),
    }
