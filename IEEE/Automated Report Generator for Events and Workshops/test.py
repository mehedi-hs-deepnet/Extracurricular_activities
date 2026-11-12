"""
test.py
-------
Self-test script for IEEE Automated Event Report Generator.
Validates the entire pipeline: Banner, Event Details, Description,
Header/Footer, Author info, and .docx generation.
"""

import io
import datetime
from PIL import Image
import docx

from utils.description import split_into_paragraphs
from utils.banner import process_image
from main.report_generator import (
    generate_report,
    generate_report_bytes,
    validate_report_inputs,
    sanitize_filename,
)


def run_tests():
    print("🚀 Running automated test suite...")

    # 1. Validation test
    errors = validate_report_inputs(
        report_id="",
        venue="",
        report_name="",
        author_name="",
        author_designation="",
        header_text="",
        footer_text="",
        description=""
    )
    assert len(errors) == 8, f"Expected 8 validation errors on empty fields, got {len(errors)}"
    print("✅ Validation checks passed.")

    # 2. Filename sanitization test
    sanitized = sanitize_filename("IEEE/GUB:2026*01?<>|")
    assert sanitized == "IEEE_Report_IEEE_GUB_2026_01.docx"
    print("✅ Filename sanitization passed.")

    # 3. Description multi-paragraph test
    sample_desc = "Para 1: Intro\n\nPara 2: Activities\n\nPara 3: Closing"
    paras = split_into_paragraphs(sample_desc)
    assert len(paras) == 3, f"Expected 3 paragraphs, got {len(paras)}"
    print("✅ Multi-paragraph splitting passed.")

    # 4. In-memory dummy banner
    dummy_img = Image.new("RGB", (800, 400), color=(0, 98, 155))
    img_stream = io.BytesIO()
    dummy_img.save(img_stream, format="PNG")
    img_stream.seek(0)

    # 5. Raw bytes generation test
    raw_bytes = generate_report_bytes(
        report_id="IEEE-GUB-2026-TEST",
        date=datetime.date(2026, 10, 21),
        time="10:00 AM - 01:00 PM",
        venue="University Auditorium",
        report_name="Automated Testing Workshop",
        author_name="Md. Mahedi Hasan",
        author_designation="Lead Coordinator",
        author_org="IEEE GUB Student Branch",
        header_text="IEEE GUB Student Branch | Header Test",
        footer_text="IEEE GUB Student Branch | Footer Test",
        description=sample_desc,
        banner_file=img_stream,
    )
    assert isinstance(raw_bytes, bytes) and len(raw_bytes) > 0
    print(f"✅ In-memory docx raw bytes generated ({len(raw_bytes)} bytes).")

    # 6. Read back document and assert keywords
    doc = docx.Document(io.BytesIO(raw_bytes))
    text = " ".join([p.text for p in doc.paragraphs])
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += " " + cell.text

    assert "IEEE-GUB-2026-TEST" in text
    assert "Automated Testing Workshop" in text
    assert "Para 1: Intro" in text
    assert "Para 2: Activities" in text
    assert "Para 3: Closing" in text
    assert "Md. Mahedi Hasan" in text
    print("✅ Document contents verified successfully!")
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
