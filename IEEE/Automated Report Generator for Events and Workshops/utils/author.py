"""
utils/author.py
---------------
রিপোর্ট প্রস্তুতকারীর তথ্য (Name, Designation, Organization)
Word টেমপ্লেটের উপযোগী করে প্রস্তুত করে।

টেমপ্লেটের ট্যাগ:
    {{ author_name }}   {{ author_designation }}   {{ author_org }}
"""

DEFAULT_ORG = "IEEE GUB Student Branch"
DEFAULT_DES = "Executive Member"


def _clean(value) -> str:
    """
    value none asle empty string, nahole shei string er whitespace gula remove kore dewa
    """
    return "" if value is None else str(value).strip()


def validate_author(author_name, author_designation) -> list[str]:
    """
    আবশ্যক ফিল্ড ফাঁকা থাকলে error message-এর তালিকা রিটার্ন করে।
    তালিকা খালি মানে সব ঠিক আছে। (Organization ঐচ্ছিক, ফাঁকা হলে default বসবে)
    """
    errors = []
    if not _clean(author_name):
        errors.append("Author Name দিতে হবে।")
    if not _clean(author_designation):
        errors.append("Author Designation দিতে হবে।")
    return errors


def prepare_author(author_name, author_designation, author_org=None) -> dict:
    """
    প্রস্তুতকারীর তথ্য প্রসেস করে docxtpl-এর context dict-এর অংশ হিসেবে রিটার্ন করে।
    """
    return {
        "author_name": _clean(author_name),
        "author_designation": _clean(author_designation) or DEFAULT_DES,
        "author_org": _clean(author_org) or DEFAULT_ORG,
    }