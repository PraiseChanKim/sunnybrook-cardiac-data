
import sys
from pathlib import Path

import streamlit as st

# =====================================
# 1. 프로젝트 최상위 경로
# =====================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.imaging.dicom_loader import load_dicom


# =====================================
# 2. Streamlit 설정
# =====================================

st.set_page_config(
    page_title="Sunnybrook MRI Viewer",
    layout="wide"
)

st.title("Sunnybrook Cardiac MRI Viewer")
st.info("교육용 MRI 영상 뷰어입니다. 실제 의료 진단용이 아닙니다.")


# =====================================
# 3. 데이터셋 경로
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
# 4. MRI 케이스 검색
# =====================================

cases = sorted(
    folder
    for folder in TRAIN_DIR.iterdir()
    if folder.is_dir() and (folder / "DICOM").is_dir()
)

if not cases:
    st.error("MRI 케이스를 찾을 수 없습니다.")
    st.stop()


# =====================================
# 5. 케이스 선택
# =====================================

selected_case = st.selectbox(
    "MRI 케이스 선택",
    cases,
    format_func=lambda path: path.name
)


# =====================================
# 6. DICOM 파일 목록
# =====================================

dicom_files = sorted(
    (selected_case / "DICOM").glob("*.dcm")
)

if not dicom_files:
    st.error("DICOM 파일을 찾을 수 없습니다.")
    st.stop()


# =====================================
# 7. 영상 번호 선택
# =====================================

image_number = st.slider(
    "MRI 영상 번호",
    min_value=1,
    max_value=len(dicom_files),
    value=1
)

selected_file = dicom_files[image_number - 1]


# =====================================
# 8. 영상 읽기 및 출력
# =====================================

try:
    image, metadata = load_dicom(selected_file)

    st.success("DICOM 영상 로딩 성공!")

    st.subheader("Original Cardiac MRI")

    st.image(
        image,
        caption=selected_file.name,
        width=512
    )

    st.subheader("영상 정보")

    col1, col2, col3 = st.columns(3)

    col1.metric("가로", metadata["columns"])
    col2.metric("세로", metadata["rows"])
    col3.metric("Modality", metadata["modality"])

    st.write("케이스:", selected_case.name)
    st.write("파일 이름:", selected_file.name)
    st.write("Instance Number:", metadata["instance_number"])

except Exception as error:
    st.error(f"DICOM 처리 오류: {error}")
