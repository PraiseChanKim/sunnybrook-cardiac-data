
import plotly.graph_objects as go
from PIL import Image
from streamlit_cropper import st_cropper
from src.imaging.roi_analysis import analyze_roi
from pathlib import Path

import streamlit as st

from src.imaging.dicom_loader import load_dicom
from src.imaging.image_processing import (
    apply_clahe,
    apply_gaussian_blur,
    apply_canny,
)

st.set_page_config(
    page_title="Sunnybrook Cardiac PACS",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state=320,
)


st.markdown("""
<style>

/* ==============================
   1. 사이드바 제목
============================== */

section[data-testid="stSidebar"] h1 {
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* ==============================
   2. 사이드바 메뉴
============================== */

section[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 10px 8px !important;
    margin-bottom: 5px !important;
    border-radius: 8px !important;
    min-height: 45px !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] label p {
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* ==============================
   3. 메인 화면 제목
============================== */

[data-testid="stMain"] h2 {
    font-size: 30px !important;
}

[data-testid="stMain"] h3 {
    font-size: 24px !important;
}

/* ==============================
   4. 입력창 라벨
============================== */

[data-testid="stMain"] [data-testid="stWidgetLabel"] p {
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* ==============================
   5. 검색창 및 선택창
============================== */

[data-testid="stMain"] input {
    font-size: 16px !important;
    min-height: 40px !important;
}

[data-testid="stMain"] [data-baseweb="select"] {
    font-size: 16px !important;
    min-height: 44px !important;
}

[data-testid="stMain"] [data-baseweb="select"] span {
    font-size: 16px !important;
}

/* ==============================
   6. 보조 설명
============================== */

[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)


ROOT = Path(__file__).resolve().parent

TRAIN_DIR = (
    ROOT
    / "data"
    / "Sunnybrook Cardiac MR Database DICOMPart3"
    / "Sunnybrook Cardiac MR Database DICOMPart3"
    / "TrainingDataDICOM"
)

# ==========================================
# MRI 확대 / 축소 / 이동 뷰어
# ==========================================

def render_zoomable_image(image, key):
    height, width = image.shape

    fig = go.Figure(
        data=go.Heatmap(
            z=image,
            colorscale=[
                [0.0, "#000000"],
                [1.0, "#FFFFFF"],
            ],
            zmin=0,
            zmax=255,
            showscale=False,
            hoverinfo="skip",
            zsmooth=False,
        )
    )

    fig.update_layout(
        height=460,
        dragmode="pan",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=key,
    )

    # X축: 왼쪽에서 오른쪽
    fig.update_xaxes(
        range=[-0.5, width - 0.5],
        visible=False,
        showgrid=False,
        zeroline=False,
    )

    # Y축: MRI 영상처럼 위에서 아래 방향
    fig.update_yaxes(
        range=[height - 0.5, -0.5],
        visible=False,
        showgrid=False,
        zeroline=False,
        scaleanchor="x",
        scaleratio=1,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        key=key,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "displaylogo": False,
        },
    )

# ------------------------------------------
# Sidebar
# ------------------------------------------

st.sidebar.title("■ Sunnybrook PACS")
st.sidebar.caption("Cardiac MRI Management System")
st.sidebar.divider()

page = st.sidebar.radio(
    "메뉴",
    [
        "대시보드",
        "MRI 뷰어",
        "케이스 관리",
        "검토 관리",
        "사용자 관리",
    ],
    index=1,
)

st.sidebar.divider()
st.sidebar.caption("교육 및 연구용 시스템")
st.sidebar.caption("실제 의료 진단용이 아닙니다.")

# ------------------------------------------
# Main Header
# ------------------------------------------

st.title("Sunnybrook Cardiac PACS")
st.caption("Medical Image Management & Analysis")
st.divider()

# ------------------------------------------
# Local Dataset
# ------------------------------------------

if TRAIN_DIR.exists():
    cases = sorted(
        folder
        for folder in TRAIN_DIR.iterdir()
        if folder.is_dir() and (folder / "DICOM").is_dir()
    )
else:
    cases = []

# ------------------------------------------
# Dashboard
# ------------------------------------------

if page == "대시보드":
    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("로컬 MRI 케이스", len(cases))
    col2.metric("영상처리 알고리즘", "3종")
    col3.metric("개발 상태", "진행 중")

    st.subheader("구현된 기능")
    st.success("DICOM 영상 로딩")
    st.success("CLAHE / Gaussian Blur / Canny Edge")

    st.info("Firebase 및 검토 관리 기능은 추후 연동 예정입니다.")

# ------------------------------------------
# MRI Viewer
# ------------------------------------------

elif page == "MRI 뷰어":
    st.header("MRI Viewer")

    if not cases:
        st.error(
            "로컬 DICOM 데이터를 찾을 수 없습니다. "
            "data 폴더에 Sunnybrook 데이터셋이 있는지 확인하세요."
        )
        st.stop()

    browser_col, viewer_col, tool_col = st.columns(
    [2, 7.5, 3],
    gap="medium",
    )

    # Case Browser
    with browser_col:
        st.subheader("Case Browser")

        keyword = st.text_input(
            "케이스 검색",
            placeholder="SC-HF-I-01",
        )

        filtered_cases = [
            case for case in cases
            if keyword.lower() in case.name.lower()
        ]

        if not filtered_cases:
            st.warning("검색 결과가 없습니다.")
            st.stop()

        selected_case = st.selectbox(
            "케이스 선택",
            filtered_cases,
            format_func=lambda path: path.name,
        )

        dicom_files = sorted(
            (selected_case / "DICOM").glob("*.dcm")
        )

        if not dicom_files:
            st.warning("이 케이스에 DICOM 파일이 없습니다.")
            st.stop()

        image_number = st.slider(
            "영상 번호",
            min_value=1,
            max_value=len(dicom_files),
            value=1,
        )

        selected_file = dicom_files[image_number - 1]

        st.caption(f"총 {len(dicom_files)}개 영상")
        st.caption(f"파일: {selected_file.name}")

    # Analysis Tools
    with tool_col:
        st.subheader("Analysis Tools")

        algorithm = st.selectbox(
            "영상처리 선택",
            [
                "Original",
                "CLAHE",
                "Gaussian Blur",
                "Canny Edge",
            ],
        )

        params = {}

        if algorithm == "CLAHE":
            params["clip_limit"] = st.slider(
                "Clip Limit", 1.0, 10.0, 2.0, 0.5
            )
            params["tile_size"] = st.slider(
                "Tile Grid Size", 2, 16, 8
            )

        elif algorithm == "Gaussian Blur":
            params["kernel_size"] = st.slider(
                "Kernel Size", 3, 15, 5, 2
            )
            params["sigma"] = st.slider(
                "Sigma", 0.0, 5.0, 1.0, 0.5
            )

        elif algorithm == "Canny Edge":
            params["low"] = st.slider(
                "Low Threshold", 0, 250, 50
            )
            params["high"] = st.slider(
                "High Threshold", 1, 300, 150
            )

        compare = st.checkbox(
            "원본 / 결과 비교",
            value=True,
        )
        
        roi_enabled = st.checkbox(
            "ROI 분석 모드",
        value=False,
        )

        st.divider()
        st.caption("추가 예정: ROI 분석")
        st.caption("추가 예정: 확대 / 이동 / 초기화")
        st.caption("추가 예정: 좌심실 윤곽선")

    # Load and process the selected MRI
    try:
        original, metadata = load_dicom(selected_file)

        if algorithm == "CLAHE":
            processed = apply_clahe(
                original,
                clip_limit=params["clip_limit"],
                tile_size=params["tile_size"],
            )

        elif algorithm == "Gaussian Blur":
            processed = apply_gaussian_blur(
                original,
                kernel_size=params["kernel_size"],
                sigma=params["sigma"],
            )

        elif algorithm == "Canny Edge":
            if params["low"] >= params["high"]:
                st.error(
                    "High Threshold는 Low Threshold보다 커야 합니다."
                )
                st.stop()

            processed = apply_canny(
                original,
                low_threshold=params["low"],
                high_threshold=params["high"],
            )
        else:
            processed = original

        
        
        with viewer_col:
            st.subheader("Image Viewer")

            # ==================================
            # ROI 분석 모드
            # ==================================

            if roi_enabled:

                # 원본 MRI와 처리 결과를 나란히 배치
                original_col, processed_col = st.columns(
                    [1, 1],
                    gap="medium",
                )

                roi_result = None

                # ==================================
                # 왼쪽: 원본 MRI + ROI 선택
                # ==================================

                with original_col:

                    st.caption("Original MRI + ROI")

                    img_height, img_width = original.shape

                    display_width = 400
                    display_height = round(
                        img_height * display_width / img_width
                    )

                    display_image = Image.fromarray(
                        original
                    ).resize(
                        (display_width, display_height),
                        resample=Image.Resampling.NEAREST,
                    )

                    rect = st_cropper(
                        display_image,
                        realtime_update=True,
                        box_color="#00FF00",
                        aspect_ratio=None,
                        return_type="box",
                        should_resize_image=False,
                        key=(
                            f"roi_{selected_case.name}_"
                            f"{selected_file.name}"
                        ),
                    )

                    # 표시 좌표 -> 실제 MRI 픽셀 좌표
                    scale_x = img_width / display_width
                    scale_y = img_height / display_height

                    x1 = round(rect["left"] * scale_x)
                    y1 = round(rect["top"] * scale_y)

                    x2 = round(
                        (rect["left"] + rect["width"]) * scale_x
                    )

                    y2 = round(
                        (rect["top"] + rect["height"]) * scale_y
                    )

                    try:
                        roi_result = analyze_roi(
                            original,
                            x=x1,
                            y=y1,
                            width=x2 - x1,
                            height=y2 - y1,
                        )

                    except ValueError as error:
                        st.warning(str(error))

                # ==================================
                # 오른쪽: 영상처리 결과
                # ==================================

                with processed_col:

                    if algorithm != "Original":

                        st.caption(f"Processed MRI - {algorithm}")

                         # 확대 / 축소 / 이동 가능한 MRI 뷰어
                        render_zoomable_image(
                            processed,
                            key=(
                                f"roi_processed_{selected_case.name}_"
                                f"{selected_file.stem}_{algorithm}"
                            ),
                        )

                    else:

                        st.caption("Processed MRI")

                        st.info(
                            "오른쪽 Analysis Tools에서 "
                            "CLAHE, Gaussian Blur 또는 "
                            "Canny Edge를 선택하세요."
                        )

                # ==================================
                # 아래: ROI 통계
                # ==================================

                if roi_result is not None:

                    st.divider()
                    st.subheader("ROI Statistics")
                    st.caption("원본 MRI의 8비트 밝기값 기준")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Mean",
                        f"{roi_result['mean']:.2f}",
                    )

                    col2.metric(
                        "Std",
                        f"{roi_result['std']:.2f}",
                    )

                    col3.metric(
                        "Area",
                        f"{roi_result['area']} px²",
                    )

                    col4, col5 = st.columns(2)

                    col4.metric(
                        "Min",
                        roi_result["min"],
                    )

                    col5.metric(
                        "Max",
                        roi_result["max"],
                    )

                    st.caption(
                        f"ROI 좌표: "
                        f"x={roi_result['x']}, "
                        f"y={roi_result['y']}, "
                        f"width={roi_result['width']}, "
                        f"height={roi_result['height']}"
                    )

                    # ==================================
                    # 선택된 ROI + 히스토그램
                    # ==================================

                    roi_col, hist_col = st.columns(
                        [1, 2],
                        gap="medium",
                    )

                    with roi_col:

                        st.subheader("Selected ROI")

                        st.image(
                            roi_result["roi_image"],
                            clamp=True,
                            use_container_width=True,
                        )

                    with hist_col:

                        st.subheader("ROI Histogram")

                        st.bar_chart(
                            roi_result["histogram"],
                            x_label="Gray Level (0-255)",
                            y_label="Pixel Count",
                            height=260,
                        )

            # ==================================
            # 일반 MRI 뷰어 모드
            # ==================================

            
            # ==================================
            # 일반 MRI 뷰어 모드
            # ==================================

            else:

                st.caption(
                    "마우스 휠: 확대/축소 | "
                    "드래그: 이동 | "
                    "상단 도구: 초기화"
                )

                if compare and algorithm != "Original":

                    left, right = st.columns(2)

                    with left:
                        st.caption("Original MRI")

                        render_zoomable_image(
                            original,
                            key=(
                                f"original_{selected_case.name}_"
                                f"{selected_file.stem}"
                            ),
                        )

                    with right:
                        st.caption(f"Processed MRI - {algorithm}")

                        render_zoomable_image(
                            processed,
                            key=(
                                f"processed_{selected_case.name}_"
                                f"{selected_file.stem}_{algorithm}"
                            ),
                        )

                else:

                    st.caption(algorithm)

                    render_zoomable_image(
                        processed,
                        key=(
                            f"viewer_{selected_case.name}_"
                            f"{selected_file.stem}_{algorithm}"
                        ),
                    )


            # ==================================
            # DICOM Metadata
            # ==================================

            st.divider()
            st.subheader("DICOM Metadata")

            m1, m2, m3 = st.columns(3)

            m1.metric("Width", metadata["columns"])
            m2.metric("Height", metadata["rows"])
            m3.metric("Modality", metadata["modality"])

            st.caption(
                f"Instance Number: "
                f"{metadata['instance_number']}"
            )



    except Exception as error:
        st.error(f"MRI 처리 오류: {error}")

# ------------------------------------------
# Team B / C Integration Placeholders
# ------------------------------------------

elif page == "케이스 관리":
    st.header("Case Management")
    st.info("C 담당 케이스 관리 기능을 연결할 예정입니다.")

elif page == "검토 관리":
    st.header("Review Management")
    st.info("C 담당 검토 기능을 연결할 예정입니다.")

elif page == "사용자 관리":
    st.header("User Management")
    st.info("B 담당 Firebase 인증 기능을 연결할 예정입니다.")
