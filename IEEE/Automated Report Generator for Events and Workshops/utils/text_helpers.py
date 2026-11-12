"""
utils/text_helpers.py
---------------------
সাধারণ হেডার/ফুটার টেক্সট প্রস্তুত করে।

টেমপ্লেটের ট্যাগ:
    {{ header_text }}   {{ footer_text }}
"""

import re


def clean_text(value) -> str:
    """
    None হলে খালি স্ট্রিং রিটার্ন করে।
    নতুন লাইন, ট্যাব ও বাড়তি space কমিয়ে একটি পরিষ্কার লাইন বানায়,
    যাতে Word-এ লেআউট এলোমেলো না হয়।
    """
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def validate_header_footer(header_text, footer_text) -> list[str]:
    """
    Header বা Footer ফাঁকা থাকলে error message-এর তালিকা রিটার্ন করে।
    তালিকা খালি মানে সব ঠিক আছে।
    """
    errors = []
    if not clean_text(header_text):
        errors.append("Header দিতে হবে।")
    if not clean_text(footer_text):
        errors.append("Footer দিতে হবে।")
    return errors


def prepare_header_footer(header_text, footer_text) -> dict:
    """
    docxtpl-এর context dict-এর অংশ হিসেবে header ও footer রিটার্ন করে।

    Returns:
        {"header_text": str, "footer_text": str}
    """
    return {
        "header_text": clean_text(header_text),
        "footer_text": clean_text(footer_text),
    }