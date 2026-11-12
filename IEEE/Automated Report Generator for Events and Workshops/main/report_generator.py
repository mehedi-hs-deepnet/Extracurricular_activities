"""
main/report_generator.py
------------------------
Word (.docx) রিপোর্ট তৈরি করার মূল ইঞ্জিন।
docxtpl, python-docx এবং Pillow ব্যবহার করে টেমপ্লেটে ডেটা ও ইমেজ ইনজেক্ট করে
মেমরি স্ট্রিম (BytesIO বা কাঁচা bytes)-এ সম্পূর্ণ রিপোর্ট তৈরি করে।
"""

import io
import os
import re
from typing import Dict, Any, List, Optional
from docxtpl import DocxTemplate

from utils.event_details import prepare_event_details, validate_event_details
from utils.author import prepare_author, validate_author
from utils.text_helpers import prepare_header_footer, validate_header_footer
from utils.description import prepare_description, validate_description
from utils.banner import prepare_banner


def get_default_template_path() -> str:
    """
    রিপোর্ট টেমপ্লেট ফাইলের এবসলিউট পাথ রিটার্ন করে,
    যাতে যেকোনো ডিরেক্টরি থেকে স্ক্রিপ্ট চালালেও ফাইল পাওয়া যায়।
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "templates", "report_template.docx")
    return template_path


def sanitize_filename(report_id: str, prefix: str = "IEEE_Report") -> str:
    r"""
    অপারেটিং সিস্টেম ও ব্রাউজার ডাউনলোডের জন্য নিরাপদ ফাইলনেম তৈরি করে।
    অবৈধ ক্যারেক্টার যেমন \ / : * ? " < > | স্পেস ইত্যাদি আন্ডারস্কোর দিয়ে রিপ্লেস করে।
    """
    cleaned_id = re.sub(r'[\\/*?:"<>| ]+', '_', str(report_id).strip())
    cleaned_id = cleaned_id.strip('_')
    if not cleaned_id:
        cleaned_id = "Event"
    return f"{prefix}_{cleaned_id}.docx"


def validate_report_inputs(
    report_id: str,
    venue: str,
    report_name: str,
    author_name: str,
    author_designation: str,
    header_text: str,
    footer_text: str,
    description: Any,
) -> List[str]:
    """
    রিপোর্ট তৈরির সমস্ত প্রয়োজনীয় ইনপুট ভ্যালিডেট করে এবং
    কোনো এরর থাকলে তার তালিকা রিটার্ন করে।
    """
    errors: List[str] = []
    errors.extend(validate_event_details(report_id, venue, report_name))
    errors.extend(validate_author(author_name, author_designation))
    errors.extend(validate_header_footer(header_text, footer_text))
    errors.extend(validate_description(description))
    return errors


def generate_report_bytes(
    report_id: str,
    date: Any,
    time: Any,
    venue: str,
    report_name: str,
    author_name: str,
    author_designation: str,
    author_org: Optional[str],
    header_text: str,
    footer_text: str,
    description: Any,
    banner_file: Optional[Any] = None,
    template_path: Optional[str] = None,
) -> bytes:
    """
    সমস্ত ফিল্ড এবং ব্যানার ইমেজ প্রসেস করে Word (.docx) ফাইলের বাইনারি bytes রিটার্ন করে।
    ডিস্কে ফাইল রাইট না করেই শতভাগ র‍্যাম মেমোরিতে রেন্ডার হয়।

    Returns:
        bytes: জেনারেট হওয়া .docx ফাইলের কাঁচা বাইনারি ডাটা।
    """
    if template_path is None:
        template_path = get_default_template_path()

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found at: {template_path}")

    doc = DocxTemplate(template_path)

    # Context তৈরিকরণ
    context: Dict[str, Any] = {}

    # ১. ব্যানার প্রসেসিং
    banner_dict = prepare_banner(doc, banner_file)
    context.update(banner_dict)

    # ২. ইভেন্ট ডিটেইলস
    event_dict = prepare_event_details(
        report_id=report_id,
        date=date,
        time=time,
        venue=venue,
        report_name=report_name,
    )
    context.update(event_dict)

    # ৩. হেডার ও ফুটার
    hf_dict = prepare_header_footer(
        header_text=header_text,
        footer_text=footer_text,
    )
    context.update(hf_dict)

    # ৪. ডেসক্রিপশন (একাধিক প্যারাগ্রাফ)
    desc_dict = prepare_description(description)
    context.update(desc_dict)

    # ৫. প্রস্তুতকারী (Author)
    author_dict = prepare_author(
        author_name=author_name,
        author_designation=author_designation,
        author_org=author_org,
    )
    context.update(author_dict)

    # Jinja2 দিয়ে টেমপ্লেট রেন্ডারিং
    doc.render(context)

    # মেমরি স্ট্রিমে আউটপুট রাইট
    output_stream = io.BytesIO()
    doc.save(output_stream)
    return output_stream.getvalue()


def generate_report(
    report_id: str,
    date: Any,
    time: Any,
    venue: str,
    report_name: str,
    author_name: str,
    author_designation: str,
    author_org: Optional[str],
    header_text: str,
    footer_text: str,
    description: Any,
    banner_file: Optional[Any] = None,
    template_path: Optional[str] = None,
) -> io.BytesIO:
    """
    generate_report_bytes-কে কল করে একটি io.BytesIO অবজেক্ট রিটার্ন করে।
    """
    raw_bytes = generate_report_bytes(
        report_id=report_id,
        date=date,
        time=time,
        venue=venue,
        report_name=report_name,
        author_name=author_name,
        author_designation=author_designation,
        author_org=author_org,
        header_text=header_text,
        footer_text=footer_text,
        description=description,
        banner_file=banner_file,
        template_path=template_path,
    )
    stream = io.BytesIO(raw_bytes)
    return stream
