"""
main/app.py
-----------
Streamlit Frontend for IEEE Automated Event Report Generator.
ব্রাউজার থেকে ইউজার ইনপুট ও ব্যানার গ্রহণ করে স্বয়ংক্রিয়ভাবে
Word (.docx) রিপোর্ট তৈরি ও ডাউনলোড করার আধুনিক ডায়নামিক ওয়েব অ্যাপ্লিকেশন।
"""

import sys
import os
import datetime
import html
from PIL import Image
import streamlit as st

# Add project root directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main.report_generator import (
    generate_report_bytes,
    validate_report_inputs,
    get_default_template_path,
    sanitize_filename,
)
from utils.description import split_into_paragraphs

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="IEEE Event Report Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --gub-green: #00D084;
        --gub-dark: #0A231C;
        --gub-deep: #061814;
        --gub-mint: #A7F3D0;
    }

    .main-header {
        background: linear-gradient(135deg, #061814 0%, #0A2D23 60%, #0D3E30 100%);
        padding: 22px 26px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 18px rgba(0, 208, 132, 0.15);
        border: 1px solid rgba(0, 208, 132, 0.25);
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: #A7F3D0;
        font-size: 0.95rem;
        margin-top: 5px;
        margin-bottom: 0;
    }
    
    .badge {
        display: inline-block;
        background-color: rgba(0, 208, 132, 0.15);
        color: #00E676;
        border: 1px solid rgba(0, 208, 132, 0.4);
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .summary-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #00D084;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px dashed #e2e8f0;
        font-size: 0.88rem;
    }

    .summary-item:last-child {
        border-bottom: none;
    }

    .summary-label {
        color: #64748b;
        font-weight: 500;
    }

    .summary-value {
        color: #0f172a;
        font-weight: 600;
        text-align: right;
        max-width: 65%;
    }

    .success-card {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 14px;
    }

    .stButton>button[kind="primary"] {
        background-color: #00D084 !important;
        border-color: #00D084 !important;
        color: #061814 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out;
    }

    .stButton>button[kind="primary"]:hover {
        background-color: #00bf72 !important;
        box-shadow: 0 4px 12px rgba(0, 208, 132, 0.4) !important;
    }

    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Default Sample Data
# ---------------------------------------------------------
SAMPLE_PARAGRAPHS = [
    "The IEEE GUB Student Branch proudly hosted an intensive, hands-on Technical Workshop on Software Quality Assurance (SQA). The primary objective of this program was to equip engineering students with industry-relevant skills in software verification, validation strategies, automated testing pipelines, and standard defect life-cycle management.",
    "The technical sessions commenced with an introductory overview of modern testing methodologies, contrasting manual QA processes with automated continuous integration workflows. Participants actively practiced drafting high-impact test suites, identifying edge cases, and utilizing standard industry issue tracking systems.",
    "Special focus was given to the integration of Artificial Intelligence in modern software testing. The keynote speaker demonstrated how automated test generation and self-healing test scripts are shaping the future of enterprise software deployment. The event concluded with an interactive Q&A session and a certificate handover ceremony honoring the distinguished speakers."
]

DEFAULT_VALUES = {
    "report_id": "IEEE-GUB-2026-SQA01",
    "report_name": "Software Quality Assurance (SQA) Technical Workshop",
    "venue": "University Auditorium, Green University of Bangladesh",
    "event_date": datetime.date(2026, 10, 21),
    "time_str": "10:30 AM - 01:30 PM",
    "header_text": (
        "IEEE GUB Student Branch, Green University of Bangladesh | Workshop Report: "
        "Software Quality Assurance (SQA) Technical Workshop | Student Development Program | "
        "Organised by: IEEE GUB Student Branch in collaboration with IEEE CS, IEEE PES and IEEE WIE. "
        "Date: 21 October 2026 | Venue: University Auditorium | Department: Artificial Intelligence and Data Science (ADS) | "
        "Theme: Software Testing, Quality Engineering & AI-driven Innovation."
    ),
    "footer_text": (
        "The IEEE GUB Student Branch, Green University of Bangladesh, organised a workshop on Software Quality Assurance (SQA), "
        "co-organised by IEEE Computer Society (IEEE CS), IEEE Power and Energy Society (IEEE PES) and IEEE Women in Engineering (IEEE WIE). "
        "The workshop introduced participants to software testing fundamentals, manual and automation testing, security testing, "
        "test case design, bug reporting, and AI-driven quality engineering. Contact: ieee.gub@example.com | Website: https://example.com/ieee "
        "© 2026 IEEE GUB Student Branch. All rights reserved."
    ),
    "author_name": "Md. Mahedi Hasan",
    "author_designation": "Executive Member & Lead Coordinator",
    "author_org": "IEEE GUB Student Branch",
}

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
for key, val in DEFAULT_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "para_ids" not in st.session_state:
    st.session_state["para_ids"] = [1, 2, 3]
    for idx, p_text in enumerate(SAMPLE_PARAGRAPHS, 1):
        st.session_state[f"para_field_{idx}"] = p_text

if "next_para_id" not in st.session_state:
    st.session_state["next_para_id"] = 4

if "report_bytes" not in st.session_state:
    st.session_state["report_bytes"] = None
if "generated_report_name" not in st.session_state:
    st.session_state["generated_report_name"] = ""


# ---------------------------------------------------------
# Callbacks for Form Management & Dynamic Paragraphs
# ---------------------------------------------------------
def action_load_demo():
    for k, v in DEFAULT_VALUES.items():
        st.session_state[k] = v
    st.session_state["para_ids"] = [1, 2, 3]
    st.session_state["next_para_id"] = 4
    for idx, p_text in enumerate(SAMPLE_PARAGRAPHS, 1):
        st.session_state[f"para_field_{idx}"] = p_text
    st.session_state["report_bytes"] = None
    st.toast("✅ Demo report data loaded successfully!", icon="📋")


def action_clear_form():
    st.session_state["report_id"] = ""
    st.session_state["report_name"] = ""
    st.session_state["venue"] = ""
    st.session_state["event_date"] = datetime.date.today()
    st.session_state["time_str"] = "10:00 AM - 01:00 PM"
    st.session_state["header_text"] = ""
    st.session_state["footer_text"] = ""
    st.session_state["para_ids"] = [1]
    st.session_state["next_para_id"] = 2
    st.session_state["para_field_1"] = ""
    st.session_state["author_name"] = ""
    st.session_state["author_designation"] = "Executive Member"
    st.session_state["author_org"] = "IEEE GUB Student Branch"
    st.session_state["report_bytes"] = None
    st.toast("🧹 Form fields cleared.", icon="🔄")


def action_add_paragraph():
    new_id = st.session_state["next_para_id"]
    st.session_state["next_para_id"] += 1
    st.session_state["para_ids"].append(new_id)
    st.session_state[f"para_field_{new_id}"] = ""


def action_delete_paragraph(target_id: int):
    if len(st.session_state["para_ids"]) > 1:
        st.session_state["para_ids"] = [pid for pid in st.session_state["para_ids"] if pid != target_id]
        st.session_state.pop(f"para_field_{target_id}", None)
    else:
        st.session_state[f"para_field_{target_id}"] = ""


def action_move_paragraph_up(index: int):
    if index > 0:
        pids = st.session_state["para_ids"]
        pids[index - 1], pids[index] = pids[index], pids[index - 1]


def action_move_paragraph_down(index: int):
    pids = st.session_state["para_ids"]
    if index < len(pids) - 1:
        pids[index], pids[index + 1] = pids[index + 1], pids[index]


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.image(
        "img/IEEE_SB.png",
        width=350,
    )
    st.markdown("### Quick Actions")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.button("Load Demo", use_container_width=True, on_click=action_load_demo)
    with col_sb2:
        st.button("Clear Form", use_container_width=True, on_click=action_clear_form)

    st.markdown("---")
    st.markdown("### Template Status")
    tmpl_path = get_default_template_path()
    if os.path.exists(tmpl_path):
        size_kb = os.path.getsize(tmpl_path) / 1024
        st.success(f"**Template Ready**: `report_template.docx` ({size_kb:.1f} KB)")
    else:
        st.error(f"❌ Template not found at: `{tmpl_path}`")

    st.markdown("---")
    st.markdown("### Developer Profile")
    st.markdown(
        """<div style="background: #1e293b; padding: 14px 16px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 12px;">
<p style="margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700; color: #ffffff;">Md. Mehedi Hasan</p>
<p style="margin: 0 0 12px 0; font-size: 0.82rem; color: #00D084; font-weight: 500; line-height: 1.4;">Technical Coordinator<br><span style="color: #94a3b8; font-weight: 400;">IEEE GUB Student Branch</span></p>
<div style="display: flex; flex-direction: column; gap: 8px;">
<a href="https://www.linkedin.com/in/md-mehedi-hasan-284537360" target="_blank" style="display: flex; align-items: center; justify-content: center; gap: 8px; background: #0f172a; color: #ffffff !important; text-decoration: none !important; padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; border: 1px solid #334155; transition: 0.2s;">
<svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
LinkedIn Profile
</a>
<a href="https://github.com/mehedi-hs-deepnet" target="_blank" style="display: flex; align-items: center; justify-content: center; gap: 8px; background: #0f172a; color: #ffffff !important; text-decoration: none !important; padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; border: 1px solid #334155; transition: 0.2s;">
<svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
GitHub Profile
</a>
</div>
</div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Main UI Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <span class="badge">IEEE GUB Student Branch ExCom Tool</span>
        <h1>Automated Report Generator for Events and Workshops</h1>
        <p>Interactive, dynamic system to create standardized IEEE Word (.docx) reports with custom paragraphs and banner embedding.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2-Column Responsive Dashboard Layout
# ---------------------------------------------------------
col_left, col_right = st.columns([1.5, 1], gap="medium")

with col_left:
    # ----------------- SECTION 1: Event Details -----------------
    with st.expander("1 - Event Basic Information", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input(
                "Report ID *",
                key="report_id",
                placeholder="e.g. IEEE-GUB-2026-001",
                help="Unique identifier for this report.",
            )
            st.text_input(
                "Event or Report Title *",
                key="report_name",
                placeholder="e.g. Workshop on SQA & Automation",
            )
            st.text_input(
                "Venue *",
                key="venue",
                placeholder="e.g. University Auditorium",
            )
        with c2:
            st.date_input(
                "Event Date *",
                key="event_date",
            )
            st.text_input(
                "Event Time *",
                key="time_str",
                placeholder="e.g. 10:30 AM - 01:30 PM",
            )

    # ----------------- SECTION 2: Banner Image -----------------
    with st.expander("2 - Banner / Poster Image", expanded=True):
        st.caption("ইভেন্ট ব্যানার বা পোস্টার আপলোড করুন (optional)। এটি ডকুমেন্টের হেডারে ইনলাইন ইমেজ হিসেবে বসবে।")
        uploaded_banner = st.file_uploader(
            "Upload Image (PNG, JPG, JPEG, WEBP)",
            type=["png", "jpg", "jpeg", "webp"],
            key="uploaded_banner_file",
        )
        if uploaded_banner is not None:
            st.image(
                uploaded_banner,
                caption=f"Banner: {uploaded_banner.name} ({uploaded_banner.size / 1024:.1f} KB)",
                use_container_width=True,
            )

    # ----------------- SECTION 3: Dynamic Description -----------------
    with st.expander(f"3 - Event Description & Paragraphs ({len(st.session_state['para_ids'])} Block/s)", expanded=True):
        st.markdown(
            "প্রতিটি প্যারাগ্রাফ আলাদা কার্ডে এডিট করুন। (Ctrl+Enter চেপে টেক্সট অ্যাপ্লাই করতে পারেন, কোনো সমস্যা ছাড়াই)।"
        )

        mode_choice = st.radio(
            "Editing Mode:",
            ["Interactive Paragraph Cards", "Bulk Paste Mode"],
            horizontal=True,
            key="editing_mode_choice",
        )

        if mode_choice == "Interactive Paragraph Cards":
            # Render each paragraph block safely with unique keys and NO conflicting value= args
            for idx, p_id in enumerate(st.session_state["para_ids"]):
                st.markdown(f"**Paragraph #{idx + 1}**")

                # Guarantee session state key exists before widget renders
                if f"para_field_{p_id}" not in st.session_state:
                    st.session_state[f"para_field_{p_id}"] = ""

                # Text area tied directly to session_state key without value=
                st.text_area(
                    label=f"Content for Paragraph #{idx + 1}",
                    key=f"para_field_{p_id}",
                    height=105,
                    label_visibility="collapsed",
                    placeholder=f"Enter content for paragraph {idx + 1}...",
                )

                # Control buttons
                btn_c1, btn_c2, btn_c3, btn_c4 = st.columns([1, 1, 1, 3])
                with btn_c1:
                    if idx > 0:
                        st.button("⬆️ Up", key=f"btn_up_{p_id}", on_click=action_move_paragraph_up, args=(idx,))
                with btn_c2:
                    if idx < len(st.session_state["para_ids"]) - 1:
                        st.button("⬇️ Down", key=f"btn_down_{p_id}", on_click=action_move_paragraph_down, args=(idx,))
                with btn_c3:
                    st.button("🗑️ Delete", key=f"btn_del_{p_id}", on_click=action_delete_paragraph, args=(p_id,))

                st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)

            st.button("➕ Add New Paragraph", type="secondary", on_click=action_add_paragraph)

        else:
            # Bulk Paste Mode
            current_paragraphs = [
                str(st.session_state.get(f"para_field_{pid}", "")).strip()
                for pid in st.session_state["para_ids"]
                if str(st.session_state.get(f"para_field_{pid}", "")).strip()
            ]
            if "bulk_paste_text" not in st.session_state:
                st.session_state["bulk_paste_text"] = "\n\n".join(current_paragraphs)

            st.text_area(
                "Paste multiple paragraphs here (separated by double Enter / blank line):",
                key="bulk_paste_text",
                height=220,
            )

            if st.button("🔄 Sync Bulk Text into Paragraph Cards"):
                parsed = split_into_paragraphs(st.session_state.get("bulk_paste_text", ""))
                if parsed:
                    new_ids = list(range(1, len(parsed) + 1))
                    st.session_state["para_ids"] = new_ids
                    st.session_state["next_para_id"] = len(parsed) + 1
                    for idx, p in enumerate(parsed, 1):
                        st.session_state[f"para_field_{idx}"] = p
                    st.success(f"✅ {len(parsed)} টি প্যারাগ্রাফ সফলভাবে সিঙ্ক করা হয়েছে!")
                    st.rerun()

    # ----------------- SECTION 4: Header & Footer -----------------
    with st.expander("4 - Document Header & Footer Text", expanded=False):
        st.text_area(
            "Header Text *",
            key="header_text",
            height=110,
            placeholder="Enter header details (Organiser, Branch, Theme, Focus Areas)...",
        )
        st.text_area(
            "Footer Text *",
            key="footer_text",
            height=110,
            placeholder="Enter summary or footer remarks (Copyright, Contact details, Topics covered)...",
        )

    # ----------------- SECTION 5: Author Info -----------------
    with st.expander("5 - Report Prepared By (Author)", expanded=False):
        ca1, ca2 = st.columns(2)
        with ca1:
            st.text_input(
                "Author / Prepared By Name *",
                key="author_name",
                placeholder="e.g. Md. Mahedi Hasan",
            )
            st.text_input(
                "Designation *",
                key="author_designation",
                placeholder="e.g. Executive Member / Vice Chair",
            )
        with ca2:
            st.text_input(
                "Organization / Branch",
                key="author_org",
                placeholder="e.g. IEEE GUB Student Branch",
            )

# ---------------------------------------------------------
# RIGHT COLUMN: Live Document Summary & Generation Hub
# ---------------------------------------------------------
with col_right:
    st.markdown("### Document Overview")

    # Extract non-empty paragraphs safely
    active_paragraphs = [
        str(st.session_state.get(f"para_field_{pid}", "")).strip()
        for pid in st.session_state.get("para_ids", [])
        if str(st.session_state.get(f"para_field_{pid}", "")).strip()
    ]

    # Safely escaped HTML values
    esc_id = html.escape(str(st.session_state.get('report_id') or '—'))
    esc_name = html.escape(str(st.session_state.get('report_name') or '—'))
    esc_date = html.escape(str(st.session_state.get('event_date')))
    esc_time = html.escape(str(st.session_state.get('time_str') or '—'))
    esc_venue = html.escape(str(st.session_state.get('venue') or '—'))
    esc_author = html.escape(str(st.session_state.get('author_name') or '—'))
    esc_desig = html.escape(str(st.session_state.get('author_designation') or '—'))
    esc_org = html.escape(str(st.session_state.get('author_org') or '—'))

    # Real-time summary card
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-item">
                <span class="summary-label">Report ID:</span>
                <span class="summary-value">{esc_id}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Title:</span>
                <span class="summary-value">{esc_name}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Date & Time:</span>
                <span class="summary-value">{esc_date} ({esc_time})</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Venue:</span>
                <span class="summary-value">{esc_venue}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Prepared By:</span>
                <span class="summary-value">{esc_author} ({esc_desig})</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Organization:</span>
                <span class="summary-value">{esc_org}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Paragraphs:</span>
                <span class="summary-value">{len(active_paragraphs)} active</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Banner:</span>
                <span class="summary-value">{'✅ Attached' if uploaded_banner is not None else '⚪ None (Clean)'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Real-time Validation Check
    val_errors = validate_report_inputs(
        report_id=st.session_state.get("report_id", ""),
        venue=st.session_state.get("venue", ""),
        report_name=st.session_state.get("report_name", ""),
        author_name=st.session_state.get("author_name", ""),
        author_designation=st.session_state.get("author_designation", ""),
        header_text=st.session_state.get("header_text", ""),
        footer_text=st.session_state.get("footer_text", ""),
        description=active_paragraphs,
    )

    if val_errors:
        st.warning(f"⚠️ {len(val_errors)} field(s) require attention:")
        for err in val_errors:
            st.markdown(f"<small style='color: #dc2626;'>• {html.escape(err)}</small>", unsafe_allow_html=True)
    else:
        st.success("✅ All required fields complete! Ready to generate.")

    st.markdown("---")

    # Generate Action
    if st.button(" Generate Word Report (.docx)", type="primary", use_container_width=True):
        if val_errors:
            st.error("অনুগ্রহ করে ওপরের লাল দাগ দেওয়া ফিল্ডগুলো পূরণ করুন।")
        else:
            with st.spinner("Word ডকুমেন্ট প্রস্তুত করা হচ্ছে..."):
                try:
                    docx_bytes = generate_report_bytes(
                        report_id=st.session_state["report_id"],
                        date=st.session_state["event_date"],
                        time=st.session_state["time_str"],
                        venue=st.session_state["venue"],
                        report_name=st.session_state["report_name"],
                        author_name=st.session_state["author_name"],
                        author_designation=st.session_state["author_designation"],
                        author_org=st.session_state["author_org"],
                        header_text=st.session_state["header_text"],
                        footer_text=st.session_state["footer_text"],
                        description=active_paragraphs,
                        banner_file=uploaded_banner,
                    )
                    safe_filename = sanitize_filename(st.session_state["report_id"])
                    st.session_state["report_bytes"] = docx_bytes
                    st.session_state["generated_report_name"] = safe_filename
                    st.toast(" রিপোর্ট তৈরি সম্পন্ন!", icon="✅")
                    st.balloons()
                except Exception as ex:
                    st.error(f"রিপোর্ট তৈরিতে সমস্যা হয়েছে: {ex}")

    # Download Button Area (Stays permanently available)
    if st.session_state.get("report_bytes"):
        file_kb = len(st.session_state["report_bytes"]) / 1024
        st.markdown(
            f"""
            <div class="success-card">
                <h4 style="margin: 0; color: #166534;">✅ ডাউনলোড রেডি!</h4>
                <p style="margin: 4px 0 0 0; color: #15803d; font-size: 0.9rem;">
                    <strong>{html.escape(st.session_state['generated_report_name'])}</strong> ({file_kb:.1f} KB)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            label=f"⬇️ Download {st.session_state['generated_report_name']}",
            data=st.session_state["report_bytes"],
            file_name=st.session_state["generated_report_name"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
            key="btn_download_active",
        )
# ---------------------------------------------------------
# Webpage Footer (Developer Info & Social Links)
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <style>
    .footer-container {
        text-align: center;
        padding: 28px 10px 10px 10px;
        color: #94a3b8;
        font-size: 0.9rem;
    }
    .footer-name {
        color: #00D084;
        font-weight: 600;
    }
    .social-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #1e293b;
        color: #ffffff !important;
        text-decoration: none !important;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 8px 6px;
        border: 1px solid #334155;
        transition: all 0.25s ease-in-out;
    }
    .social-btn:hover {
        background: #00D084;
        color: #061814 !important;
        border-color: #00D084;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 208, 132, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)