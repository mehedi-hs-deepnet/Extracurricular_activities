<div align="center">

<img src="img/IEEE_SB.png" alt="IEEE Student Branch" width="300"/>

<br/>

***Automated Event Report Generator***

Fill in a form and download a professional Word report in one click.

<br/>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ieee-automated-report-generator.streamlit.app)

<br/>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![docxtpl](https://img.shields.io/badge/docxtpl-Jinja2-E8860A?style=for-the-badge)
![Output](https://img.shields.io/badge/Output-.docx-2B579A?style=for-the-badge&logo=microsoftword&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-00D084?style=for-the-badge&logo=streamlit&logoColor=white)](https://ieee-automated-report-generator.streamlit.app)


<br/>


[🌐 Live App](https://ieee-automated-report-generator.streamlit.app) •
[ Features](#-key-features) •
[ Workflow](#-system-architecture--visual-workflow) •
[ Tech Stack](#️-tech-stack) •
[ Structure](#-project-structure) •
[ Run](#-how-to-run) •
[ Contributing](#-contributing)

</div>

---

## Description

> A powerful tool that uses a Streamlit UI to automatically generate Word (.docx) reports.
> 
> 🌐 **Live Web Application:** [https://ieee-automated-report-generator.streamlit.app](https://ieee-automated-report-generator.streamlit.app)

---

## System Architecture & Visual Workflow

The complete system workflow, step by step:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AUTOMATED REPORT GENERATOR                       │
│                      — Visual Workflow —                            │
└─────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │   STEP 1 │ User Browser (Streamlit UI)        │
 └──────────────────────────────────────────────┘
        │
        ├──► User enters text input
        │      (e.g., Report ID, Name, Venue, etc.)
        │
        └──► User uploads an image or banner
        │
        ▼

 ┌──────────────────────────────────────────────────────────────────┐
 │   STEP 2 │ Data Capture & Pre-processing (Streamlit + Pillow)    │
 └──────────────────────────────────────────────────────────────────┘
        │
        ├──► Streamlit captures all text data and converts it
        │      into a Python dictionary (context).
        │
        └──► Pillow (PIL) receives the uploaded image and
               prepares it for placement in the Word template.
        │
        ▼

 ┌──────────────────────────────────────────────────────────────────────────┐
 │   STEP 3 │ Engine & Template Rendering (docxtpl + Jinja2 + python-docx)  │
 └──────────────────────────────────────────────────────────────────────────┘
        │
        ├──► The docxtpl library loads the
        │      templates/report_template.docx file.
        │
        ├──► The Jinja2 engine works in the backend, finding the tags
        │      (e.g., {{ report_id }}) and loops inside the template.
        │
        └──► Using python-docx's base structure, it replaces the tags with
               real data and the Pillow-processed image, then renders the file.
        │
        ▼

 ┌────────────────────────────────────────────────────┐
 │   STEP 4 │ Memory Stream Generation (io.BytesIO)   │
 └────────────────────────────────────────────────────┘
        │
        └──► The generated file is not saved to a folder on the PC;
               it is held in Python's memory (BytesIO stream).
        │
        ▼

 ┌────────────────────────────────────────────────────────────────────────────┐
 │   STEP 5 │ Browser Output & "Save As" Popup (Streamlit Download Button)    │
 └────────────────────────────────────────────────────────────────────────────┘
        │
        └──► The file is sent to the user's browser via Streamlit's
               st.download_button(), and the "Save As" popup appears! 🎉
```

---

## Workflow Diagram

```mermaid
flowchart TD
    subgraph S1["🌐  STEP 1 — User Browser  (Streamlit UI)"]
        A1["📝 Text Input\nReport ID · Name · Venue · Date"]
        A2["🖼️ Image / Banner Upload"]
    end

    subgraph S2["⚙️  STEP 2 — Data Capture & Pre-processing"]
        B1["📦 Python Dictionary\ncontext = { report_id, name, … }"]
        B2["🎨 Pillow  PIL\nImage Resize & Format"]
    end

    subgraph S3["🔧  STEP 3 — Engine & Template Rendering"]
        C1["📄 Load Template\ntemplates/report_template.docx"]
        C2["🔍 Jinja2 Engine\n{{ report_id }}  ·  for loops"]
        C3["✍️ python-docx\nInject Data + Images"]
    end

    subgraph S4["💾  STEP 4 — Memory Stream Generation"]
        D1["🧠 io.BytesIO\nIn-Memory File — No Disk Write"]
    end

    subgraph S5["📥  STEP 5 — Browser Output"]
        E1["⬇️ st.download_button\nTriggers Save As Popup in Browser 🎉"]
    end

    A1 -->|"text fields"| B1
    A2 -->|"raw image"| B2
    B1 -->|"context dict"| C1
    B2 -->|"processed image"| C1
    C1 --> C2
    C2 -->|"resolved tags"| C3
    C3 -->|"rendered .docx"| D1
    D1 -->|"BytesIO stream"| E1

    classDef step1 fill:#4A90D9,color:#fff,stroke:#2c6fad,stroke-width:2px
    classDef step2 fill:#7B68EE,color:#fff,stroke:#5a4dbf,stroke-width:2px
    classDef step3 fill:#E8860A,color:#fff,stroke:#b5670a,stroke-width:2px
    classDef step4 fill:#27AE60,color:#fff,stroke:#1e8449,stroke-width:2px
    classDef step5 fill:#E74C3C,color:#fff,stroke:#c0392b,stroke-width:2px

    class A1,A2 step1
    class B1,B2 step2
    class C1,C2,C3 step3
    class D1 step4
    class E1 step5
```

---

## Tech Stack

| Library | Purpose |
|---|---|
| **Streamlit** | Builds the browser-based UI and accepts user input |
| **Pillow (PIL)** | Processes and resizes uploaded images |
| **docxtpl** | Loads and renders Jinja2-powered Word templates |
| **Jinja2** | Fills the `{{ tags }}` and loops inside the template |
| **python-docx** | Provides the base structure of the `.docx` file |
| **io.BytesIO** | Keeps the file in memory instead of writing it to disk |

---

## Project Structure

```
Automated Event Report Generator/
│
├── utils/                  # Prepares/processes text and image data for the Word/docx file
│   ├── banner.py           # Banner
│   ├── description.py      # Description
│   ├── event_details.py    # Core event information
│   ├── author.py           # Author / preparer information
│   └── text_helpers.py     # Common header/footer
│
├── templates/                      # Word template
│   └── report_template.docx        # Main .docx file (with Jinja2 tags)
│
├── main/
│   ├── app.py                      # Streamlit frontend (form input & download button)
│   └── report_generator.py         # Report generation engine
│
├── img/
│   └── IEEE_SB.png                 # Logo
│
├── app.py                          # Root entrypoint for Streamlit
├── requirements.txt                # Library dependencies
└── README.md                       # Project documentation
```

---

## How to Run

### 🌐 Live Online (No Installation Needed)

Directly open the live web app in your browser:  
👉 **[https://ieee-automated-report-generator.streamlit.app](https://ieee-automated-report-generator.streamlit.app)**

---

### 💻 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the app
streamlit run app.py
```

Then visit `http://localhost:8501` in your browser.

---

## Key Features

- ✅ Simple browser-based UI — usable with no installation
- ✅ Image/banner upload support
- ✅ Dynamic report generation from a Word template
- ✅ File is created in memory — no data is stored on the server
- ✅ One-click `.docx` download

---

## Screenshots

| Streamlit Form | Generated Report |
|---|---|
| ![Form](img/ss_1.png) | ![Report](img/ss_2.png) |



---

## Contributing

Contributions are always welcome! 🎉

```bash
# 1. Fork the repo, then clone it
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git

# 2. Create a new branch
git checkout -b feature/your-feature-name

# 3. Commit your changes and push
git commit -m "Add: your feature"
git push origin feature/your-feature-name
```

Then open a **Pull Request** on GitHub.

---

## Author

**Md. Mehedi Hasan** — IEEE GUB Student Branch
🔗 GitHub: [Md. Mehedi Hasan](https://github.com/mehedi-hs-deepnet)

---