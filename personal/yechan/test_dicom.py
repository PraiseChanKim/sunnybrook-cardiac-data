
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.imaging.dicom_loader import load_dicom
from src.imaging.image_processing import (
    apply_clahe,
    apply_gaussian_blur,
    apply_canny
)


# =====================================
# 1. Streamlit 설정
# =====================================

st.set_page_config(
    page_title="Sunnybrook Cardiac MRI Viewer",
    layout="wide"
)

st.title("Sunnybrook Cardiac MRI Viewer")
st.info("교육용 영상처리 프로그램입니다. 실제 진단용이 아닙니다.")


# =====================================
# 2. 데이터셋 경로
# =====================================

TRAIN_DIR = (
    ROOT
    / "data"
    / "Sunnybrook Cardiac MR Database DICOMPart3"
    / "Sunnybrook Cardiac MR Database DICOMPart3"
    / "TrainingDataDICOM"
)

if not TRAIN_DIR.exists():
    st.error("TrainingDataDICOM 폴더를 찾을 수 없습니다.")
    st.stop()


# =====================================
# 3. MRI 케이스 선택
# =====================================

cases = sorted(
    folder
    for folder in TRAIN_DIR.iterdir()
    if folder.is_dir() and (folder / "DICOM").is_dir()
)

if not cases:
    st.error("MRI 케이스를 찾을 수 없습니다.")
    st.stop()

selected_case = st.selectbox(
    "MRI 케이스 선택",
    cases,
    format_func=lambda path: path.name
)

dicom_files = sorted(
    (selected_case / "DICOM").glob("*.dcm")
)

if not dicom_files:
    st.error("DICOM 파일이 없습니다.")
    st.stop()

image_number = st.slider(
    "MRI 영상 번호",
    min_value=1,
    max_value=len(dicom_files),
    value=1
)

selected_file = dicom_files[image_number - 1]


# =====================================
# 4. CLAHE 설정
# =====================================

st.subheader("CLAHE 설정")

clip_limit = st.slider(
    "Clip Limit",
    1.0, 10.0, 2.0, 0.5
)

tile_size = st.slider(
    "Tile Grid Size",
    2, 16, 8
)


# =====================================
# 5. Gaussian Blur 설정
# =====================================

st.subheader("Gaussian Blur 설정")

kernel_size = st.slider(
    "Kernel Size",
    min_value=3,
    max_value=15,
    value=5,
    step=2
)

sigma = st.slider(
    "Sigma",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.5
)


# =====================================
# 6. Canny 설정
# =====================================

st.subheader("Canny Edge Detection 설정")

low_threshold = st.slider(
    "Low Threshold",
    min_value=0,
    max_value=250,
    value=50
)

high_threshold = st.slider(
    "High Threshold",
    min_value=1,
    max_value=300,
    value=150
)

if low_threshold >= high_threshold:
    st.warning(
        "High Threshold는 Low Threshold보다 커야 합니다."
    )
    st.stop()


# =====================================
# 7. DICOM 로딩 및 영상처리
# =====================================

try:
    original, metadata = load_dicom(selected_file)

    clahe_result = apply_clahe(
        original,
        clip_limit=clip_limit,
        tile_size=tile_size
    )

    gaussian_result = apply_gaussian_blur(
        original,
        kernel_size=kernel_size,
        sigma=sigma
    )

    canny_result = apply_canny(
        original,
        low_threshold=low_threshold,
        high_threshold=high_threshold
    )

    st.success("DICOM 영상 및 3종 영상처리 성공!")

    # =================================
    # 8. 영상 비교
    # =================================

    st.subheader("MRI 영상 비교")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("Original MRI")
        st.image(
            original,
            caption="Original",
            use_container_width=True,
            clamp=True
        )

    with col2:
        st.write("CLAHE MRI")
        st.image(
            clahe_result,
            caption="CLAHE",
            use_container_width=True,
            clamp=True
        )

    with col3:
        st.write("Gaussian Blur MRI")
        st.image(
            gaussian_result,
            caption="Gaussian Blur",
            use_container_width=True,
            clamp=True
        )

    with col4:
        st.write("Canny Edge MRI")
        st.image(
            canny_result,
            caption="Canny Edge",
            use_container_width=True,
            clamp=True
        )

    # =================================
    # 9. 영상 정보
    # =================================

    st.subheader("영상 정보")

    c1, c2, c3 = st.columns(3)

    c1.metric("가로", metadata["columns"])
    c2.metric("세로", metadata["rows"])
    c3.metric("Modality", metadata["modality"])

    st.write("케이스:", selected_case.name)
    st.write("파일 이름:", selected_file.name)
    st.write(
        "Instance Number:",
        metadata["instance_number"]
    )

except Exception as error:
    st.error(f"영상 처리 오류: {error}")