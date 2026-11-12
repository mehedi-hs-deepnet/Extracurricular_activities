"""
utils/description.py
--------------------
ইভেন্টের বর্ণনা (Description) প্রসেস ও ভ্যালিডেট করে।
টেমপ্লেটে একাধিক প্যারাগ্রাফ ডায়নামিক ভাবে লুপ করার জন্য:
    {%p for para in description %}
    {{ para }}
    {%p endfor %}

এটি টেক্সট বা প্যারাগ্রাফের লিস্টকে পরিষ্কার ফরম্যাটে প্রস্তুত করে।
"""

import re
from typing import Union, List


def _clean_paragraph(text: str) -> str:
    """
    একটি একক প্যারাগ্রাফের অতিরিক্ত স্পেস দূর করে এবং ভিতরের অপ্রয়োজনীয় লাইনব্রেক এক লাইনে রূপান্তর করে।
    """
    if text is None:
        return ""
    # প্যারাগ্রাফের ভিতরের অযাচিত একাধিক স্পেস ও লাইনব্রেক সাধারণ স্পেসে রূপান্তর
    cleaned = re.sub(r"\s+", " ", str(text)).strip()
    return cleaned


def split_into_paragraphs(content: Union[str, List[str]]) -> List[str]:
    """
    স্ট্রিং বা লিস্ট অফ স্ট্রিং গ্রহণ করে একাধিক প্যারাগ্রাফের তালিকায় রূপান্তর করে।
    - যদি লিস্ট হয়: প্রতিটি আইটেমকে স্বতন্ত্র প্যারাগ্রাফ হিসেবে প্রসেস করে।
    - যদি স্ট্রিং হয়: ডাবল লাইনব্রেক (\\n\\n বা তার বেশি) দিয়ে স্পষ্ট প্যারাগ্রাফগুলো আলাদা করে।
    """
    if not content:
        return []

    if isinstance(content, list):
        paragraphs = [_clean_paragraph(p) for p in content if _clean_paragraph(p)]
        return paragraphs

    text = str(content).strip()
    if not text:
        return []

    # ডাবল বা ততোধিক নতুন লাইন দিয়ে স্প্লিট করা (স্ট্যান্ডার্ড প্যারাগ্রাফ বিভাজন)
    raw_parts = re.split(r"\n\s*\n+", text)
    paragraphs = [_clean_paragraph(p) for p in raw_parts if _clean_paragraph(p)]

    # যদি ডাবল লাইনব্রেক না থাকে, তবে পুরো টেক্সটটি একটি একক পূর্ণাঙ্গ প্যারাগ্রাফ
    if not paragraphs:
        cleaned_single = _clean_paragraph(text)
        if cleaned_single:
            paragraphs = [cleaned_single]

    return paragraphs


def validate_description(description_input: Union[str, List[str]]) -> List[str]:
    """
    ডেসক্রিপশন ভ্যালিডেশন: অন্তত একটি কার্যকর প্যারাগ্রাফ থাকতে হবে।
    """
    errors = []
    paragraphs = split_into_paragraphs(description_input)
    if not paragraphs:
        errors.append("Event Description দিতে হবে (অন্তত একটি প্যারাগ্রাফ আবশ্যক)।")
    return errors


def prepare_description(description_input: Union[str, List[str]]) -> dict:
    """
    Word টেমপ্লেটের context dict-এর 'description' কি-এর জন্য
    প্যারাগ্রাফের লিস্ট প্রস্তুত করে।

    Returns:
        {"description": ["Paragraph 1", "Paragraph 2", ...]}
    """
    paragraphs = split_into_paragraphs(description_input)
    return {"description": paragraphs}
