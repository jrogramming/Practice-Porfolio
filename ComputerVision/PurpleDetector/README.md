# ♠ &nbsp; Purple Detector &nbsp; ♠

<p align="center">
  <em>Real-time color detection using OpenCV and Python.</em>
</p>

---

### &nbsp; ♜ &nbsp; ABOUT THE PROJECT

A real-time computer vision experiment that uses a webcam to detect purple objects and draw a bounding box around detected regions.

**Purpose:**
- Reading live webcam footage with OpenCV.
- Understanding RGB, BGR, and HSV color spaces.
- Creating binary masks with color thresholds.
- Extracting bounding boxes from detected pixels.
- Displaying real-time image processing results.

---

### &nbsp; ♥ &nbsp; HOW IT WORKS

The detection process follows five steps:

| Step | Operation | Purpose |
|:---:|:---|:---|
| 01 | `VideoCapture(0)` | Access the webcam. |
| 02 | `cvtColor()` | Convert the frame from BGR to HSV. |
| 03 | `get_limits()` | Calculate the target color's HSV range. |
| 04 | `inRange()` | Create a binary mask of matching pixels. |
| 05 | `getbbox()` | Find the bounding box around detected regions. |

**The processing pipeline:**

```text
Webcam Feed
     |
     v
BGR to HSV Conversion
     |
     v
Define Color Thresholds
     |
     v
Create Binary Mask
     |
     v
Extract Bounding Box
     |
     v
Display Detection
```

---

### &nbsp; ♦ &nbsp; GETTING STARTED

**01. Clone the repository**

```bash
git clone <repository-url>
cd <repository-folder>
```

**02. Install dependencies**

```bash
pip install -r requirements.txt
```

**03. Run the program**

```bash
python main.py
```

**04. Exit**

Press `Q` to close the webcam feed.

---

### &nbsp; ♣ &nbsp; UNDERSTANDING THE CODE

**Color Detection — `util.py`**

The `get_limits()` function converts a target color into HSV and calculates upper and lower color thresholds.

- Hue determines the color.
- Saturation determines color intensity.
- Value determines brightness.

A tolerance range is applied to Hue, while minimum saturation and brightness thresholds help filter out grayish and dark pixels.

**Image Processing — `main.py`**

- `cv2.VideoCapture()` reads webcam frames.
- `cv2.cvtColor()` converts BGR images into HSV.
- `cv2.inRange()` isolates pixels within the specified color range.
- `Image.fromarray()` converts the mask into a PIL image.
- `getbbox()` identifies the boundaries of nonzero pixels.
- `cv2.rectangle()` draws the detection boundary.

---

### &nbsp; ♠ &nbsp; REPOSITORY STRUCTURE

```text
.
├── main.py
├── util.py
└── requirements.txt
```

---

### &nbsp; ♥ &nbsp; TECHNOLOGIES

| Technology | Application |
|:---|:---|
| Python | Core programming language |
| OpenCV | Webcam access and computer vision |
| NumPy | Array manipulation and color conversion |
| Pillow | Image manipulation and bounding box extraction |

---

<p align="center">
  <sub>♠ &nbsp; Have fun! &nbsp; ♠</sub>
</p>
