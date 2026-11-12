"""
utils/banner.py
---------------
ইমেজ প্রসেসিং এবং হেল্পার ফাংশন।
Pillow (PIL) ব্যবহার করে আপলোড করা ইমেজকে
Word টেমপ্লেটে বসানোর উপযোগী করে প্রস্তুত করে।
"""

import io
import os
from PIL import Image, ImageOps
from docxtpl import InlineImage
from docx.shared import Mm


def process_image(uploaded_file, max_width=1200, max_height=800):
    """
    যেকোনো ধরনের ইমেজ ইনপুট (UploadedFile, BytesIO, bytes, PIL Image, বা ফাইল পাথ)
    নিরাপদে প্রসেস করে RAM-এ PNG ফরম্যাটে প্রস্তুত করে।
    EXIF ওরিয়েন্টেশন ঠিক করে এবং আলফা ট্রান্সপারেন্সি সাদা ব্যাকগ্রাউন্ডে রূপান্তর করে।
    """
    if uploaded_file is None:
        return None

    try:
        # ইনপুট টাইপ অনুযায়ী সেফলি PIL Image তৈরি করা
        if isinstance(uploaded_file, Image.Image):
            image = uploaded_file.copy()
        elif isinstance(uploaded_file, (bytes, bytearray)):
            image = Image.open(io.BytesIO(uploaded_file))
        elif isinstance(uploaded_file, str) and os.path.isfile(uploaded_file):
            image = Image.open(uploaded_file)
        elif hasattr(uploaded_file, "read"):
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            data = uploaded_file.read()
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            if not data:
                return None
            image = Image.open(io.BytesIO(data))
        else:
            return None

        # EXIF orientation fix
        try:
            transposed = ImageOps.exif_transpose(image)
            if transposed is not None:
                image = transposed
        except Exception:
            pass

        # Transparency docx এ সাপোর্ট করে না, তাই সাদা background বসানো।
        if image.mode != "RGB":
            image = image.convert("RGBA")
            background = Image.new("RGB", image.size, (255, 255, 255))
            alpha_channel = image.split()[3]
            background.paste(image, mask=alpha_channel)
            image = background

        # রিসাইজিং (Aspect Ratio বজায় রেখে)
        resample_filter = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.LANCZOS)
        image.thumbnail((max_width, max_height), resample_filter)

        img_stream = io.BytesIO()
        image.save(img_stream, format="PNG", optimize=True)
        img_stream.seek(0)
        return img_stream

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def prepare_banner(doc, uploaded_file, width_mm=170):
    """
    docxtpl এর {{ banner }} ট্যাগের জন্য context dict রিটার্ন করে।
    ছবি না থাকলে বা প্রসেসিং ব্যর্থ হলে খালি স্ট্রিং বসবে।

    doc: DocxTemplate object
    """
    if uploaded_file is None:
        return {"banner": ""}

    stream = process_image(uploaded_file)
    if stream is None:
        return {"banner": ""}

    try:
        return {"banner": InlineImage(doc, stream, width=Mm(width_mm))}
    except Exception as e:
        print(f"Error creating InlineImage: {e}")
        return {"banner": ""}
