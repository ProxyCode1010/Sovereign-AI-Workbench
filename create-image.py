from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

random.seed(42)

W, H = 1240, 1650  # A4-ish at ~150dpi

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

f_title = get_font(28, bold=True)
f_h2 = get_font(20, bold=True)
f_body = get_font(17)
f_small = get_font(14)
f_mono = get_font(15)

img = Image.new("L", (W, H), color=250)
d = ImageDraw.Draw(img)

# --- Letterhead ---
d.rectangle([40, 30, W-40, 110], outline=80, width=2)
d.text((60, 40), "NATIONAL REFINERY & PETROCHEMICALS LTD.", font=f_h2, fill=20)
d.text((60, 68), "Mechanical Integrity & Inspection Department", font=f_small, fill=60)
d.text((W-260, 40), "Doc No: INS/2026/0847", font=f_small, fill=60)
d.text((W-260, 60), "Rev: 02", font=f_small, fill=60)
d.text((W-260, 80), "Confidential - Internal Use Only", font=f_small, fill=60)

y = 130
d.text((60, y), "PRESSURE VESSEL INTERNAL INSPECTION REPORT", font=f_title, fill=10)
y += 45
d.line([60, y, W-60, y], fill=100, width=2)
y += 20

# --- Info table ---
info_left = [
    ("Vessel Tag No.", "V-1042-A"),
    ("Vessel Type", "Vertical Separator"),
    ("Design Pressure", "18.5 kg/cm2"),
    ("Design Temp.", "150 deg C"),
    ("Service", "Sour Gas / Hydrocarbon"),
]
info_right = [
    ("Inspection Date", "03-Sep-2026"),
    ("Last Inspection", "11-Sep-2020"),
    ("Inspector Name", "R. Sharma (Cert# NB-4471)"),
    ("Shift In-Charge", "V. Krishnan"),
    ("Permit No.", "PTW-2026-3391"),
)

row_h = 26
tx1, tx2 = 60, 400
ty = y
for label, val in info_left:
    d.text((tx1, ty), f"{label}:", font=f_small, fill=40)
    d.text((tx1+180, ty), val, font=f_mono, fill=10)
    ty += row_h

tx1b = 660
ty = y
for label, val in info_right:
    d.text((tx1b, ty), f"{label}:", font=f_small, fill=40)
    d.text((tx1b+170, ty), val, font=f_mono, fill=10)
    ty += row_h

y = ty + 20
d.line([60, y, W-60, y], fill=150, width=1)
y += 25

# --- Findings section ---
d.text((60, y), "SECTION A: VISUAL & DIMENSIONAL FINDINGS", font=f_h2, fill=10)
y += 35

findings = [
    "1. Localized pitting corrosion observed on internal shell surface near",
    "   nozzle N2 (manway). Maximum pit depth measured: 1.2 mm.",
    "   Pit density: moderate, approx 6-8 pits per 100 sq.cm.",
    "",
    "2. Minor surface staining noted on shell course 2 (external), suspected",
    "   corrosion under insulation (CUI). Insulation cladding found intact,",
    "   no visible moisture ingress at time of inspection.",
    "",
    "3. Ultrasonic thickness (UT) gauging performed at 8 grid points on",
    "   shell courses 1 and 2. All readings within acceptable range",
    "   (min. required thickness: 9.2 mm). See Table 1 below.",
    "",
    "4. Dye penetrant testing (DPT) carried out on nozzle N2-to-shell weld",
    "   joint. No linear indications detected. Weld surface condition",
    "   satisfactory.",
    "",
    "5. Pressure relief valve (PRV) set at 19.8 kg/cm2, test certificate",
    "   verified valid until Dec-2026. Physical condition satisfactory,",
    "   no signs of leakage at flange connection.",
    "",
    "6. Internal demister pad found displaced by approximately 40mm from",
    "   original mounting position. Support clips show mild deformation.",
]
for line in findings:
    d.text((60, y), line, font=f_body, fill=15)
    y += 24

y += 10
d.text((60, y), "TABLE 1: UT THICKNESS READINGS (mm)", font=f_h2, fill=10)
y += 30

# small table
headers = ["Grid Pt", "Course 1", "Course 2", "Nominal", "Status"]
col_x = [60, 200, 340, 480, 620]
for i, htext in enumerate(headers):
    d.text((col_x[i], y), htext, font=f_small, fill=40)
y += 22
d.line([60, y, 760, y], fill=120, width=1)
y += 8

rows = [
    ("P1", "11.8", "11.6", "9.2", "OK"),
    ("P2", "11.5", "11.4", "9.2", "OK"),
    ("P3", "10.9", "11.1", "9.2", "OK"),
    ("P4", "9.8", "10.2", "9.2", "OK"),
    ("P5", "11.2", "11.0", "9.2", "OK"),
    ("P6", "10.6", "10.4", "9.2", "OK"),
    ("P7", "11.0", "10.8", "9.2", "OK"),
    ("P8", "10.3", "9.9", "9.2", "OK"),
]
for r in rows:
    for i, val in enumerate(r):
        d.text((col_x[i], y), val, font=f_mono, fill=15)
    y += 22

y += 15
d.line([60, y, W-60, y], fill=150, width=1)
y += 25

d.text((60, y), "SECTION B: RECOMMENDATION", font=f_h2, fill=10)
y += 32
rec_lines = [
    "Vessel condition is generally satisfactory for continued service.",
    "Nozzle N2 area to be flagged for close monitoring during next",
    "inspection cycle (recommended interval: 4 years, due Sep-2030).",
    "Demister pad support clips to be repaired/replaced during next",
    "shutdown as low-priority maintenance item. No immediate repair or",
    "re-rating required at this time. Vessel cleared for return to service.",
]
for line in rec_lines:
    d.text((60, y), line, font=f_body, fill=15)
    y += 24

y += 25
d.line([60, y, W-60, y], fill=100, width=1)
y += 20
d.text((60, y), "Inspected by: ____________________", font=f_small, fill=40)
d.text((450, y), "Approved by: ____________________", font=f_small, fill=40)
y += 30
d.text((60, y), "R. Sharma, Sr. Inspection Engineer", font=f_small, fill=60)
d.text((450, y), "Date: __________", font=f_small, fill=60)

# --- Add a faded circular "stamp" ---
stamp = Image.new("L", (200, 200), 255)
sd = ImageDraw.Draw(stamp)
sd.ellipse([10, 10, 190, 190], outline=180, width=4)
sd.ellipse([25, 25, 175, 175], outline=180, width=2)
sd.text((45, 80), "VERIFIED", font=get_font(22, bold=True), fill=190)
sd.text((55, 110), "QA/QC DEPT", font=get_font(14), fill=190)
stamp = stamp.rotate(-18, expand=True, fillcolor=255)
img.paste(stamp, (W-320, y-40), stamp.point(lambda p: 255-p if p < 255 else 0))

# --- Convert to RGB and apply scan-like degradation ---
img_rgb = img.convert("RGB")

# slight rotation to mimic uneven scan
img_rgb = img_rgb.rotate(0.6, expand=False, fillcolor=(250, 250, 248))

# add subtle paper texture noise
import numpy as np
arr = np.array(img_rgb).astype(np.int16)
noise = np.random.normal(0, 6, arr.shape).astype(np.int16)
arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
img_rgb = Image.fromarray(arr)

# slight blur to mimic scan softness
img_rgb = img_rgb.filter(ImageFilter.GaussianBlur(radius=0.6))

# vignette-ish darker edges
w, h = img_rgb.size
vignette = Image.new("L", (w, h), 0)
vd = ImageDraw.Draw(vignette)
vd.rectangle([0, 0, w, h], fill=0)
for i in range(30):
    alpha = int(255 * (i / 30) * 0.15)
    vd.rectangle([i*3, i*3, w-i*3, h-i*3], outline=alpha)
img_rgb = Image.composite(Image.new("RGB", (w, h), (230, 228, 222)), img_rgb, vignette)

img_rgb.save("/home/claude/inspection_report_complex.png", dpi=(150, 150))
print("saved")