
from pathlib import Path

import cv2
import numpy as np


# ==========================================
# 1. 윤곽선 좌표 파일 읽기
# ==========================================

def read_contour(file_path):
    """
    TXT 파일에서 (x, y) 좌표를 읽는다.
    """

    points = np.loadtxt(
        file_path,
        dtype=np.float32
    )

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError(
            f"잘못된 윤곽선 좌표 형식: {file_path}"
        )

    if len(points) < 3:
        raise ValueError(
            "윤곽선을 구성할 좌표가 부족합니다."
        )

    return points


# ==========================================
# 2. 케이스와 영상 번호로 파일 찾기
# ==========================================

def load_contours(contour_root, case_id, image_stem):
    """
    case_id: SC-HF-I-01
    image_stem: IM-0001-0059

    Returns:
        {
            "inner": ndarray,
            "outer": ndarray
        }

    존재하는 윤곽선만 반환한다.
    """

    contour_dir = (
        Path(contour_root)
        / case_id
        / "contours-manual"
        / "IRCCI-expert"
    )

    contours = {}

    paths = {
        "inner": contour_dir / (
            f"{image_stem}-icontour-manual.txt"
        ),
        "outer": contour_dir / (
            f"{image_stem}-ocontour-manual.txt"
        ),
    }

    for name, path in paths.items():
        if path.is_file():
            contours[name] = read_contour(path)

    return contours


# ==========================================
# 3. 윤곽선 면적 계산
# ==========================================

def calculate_contour_areas(image_shape, contours):
    """
    윤곽선 내부의 픽셀 수를 계산한다.

    단위: px² (픽셀 기반 근사)
    """

    height, width = image_shape[:2]

    areas = {}

    for name, points in contours.items():

        mask = np.zeros(
            (height, width),
            dtype=np.uint8
        )

        polygon = np.rint(points).astype(np.int32)

        cv2.fillPoly(
            mask,
            [polygon],
            color=1
        )

        areas[name] = int(np.count_nonzero(mask))

    if "inner" in areas and "outer" in areas:
        areas["myocardium"] = max(
            0,
            areas["outer"] - areas["inner"]
        )

    return areas


# ==========================================
# 4. 윤곽선 표시 이미지 생성
# ==========================================

def draw_contours(image, contours):
    """
    inner: 초록색
    outer: 주황색
    """

    if image.ndim != 2:
        raise ValueError("2차원 흑백 영상이 필요합니다.")

    result = cv2.cvtColor(
        image,
        cv2.COLOR_GRAY2RGB
    )

    colors = {
        "inner": (0, 255, 0),
        "outer": (255, 165, 0),
    }

    for name, points in contours.items():

        polygon = np.rint(points).astype(np.int32)

        cv2.polylines(
            result,
            [polygon],
            isClosed=True,
            color=colors[name],
            thickness=2,
            lineType=cv2.LINE_AA
        )

    return result


# ==========================================
# 좌심실 윤곽선 기반 ROI 정량 분석
# ==========================================

def analyze_contour_roi(image, contours, region):
    """
    전문가 윤곽선 내부의 픽셀을 분석한다.

    region:
        inner      - 좌심실 내강
        outer      - 외벽 내부 전체
        myocardium - 외벽에서 내강을 제외한 심근 영역
    """

    if image.ndim != 2 or image.dtype != np.uint8:
        raise ValueError("2D uint8 MRI 영상이 필요합니다.")

    # 윤곽선 다각형을 마스크로 변환
    def make_mask(name):

        points = contours.get(name)

        if points is None or len(points) < 3:
            raise ValueError(
                f"{name} 윤곽선 데이터가 없습니다."
            )

        mask = np.zeros(
            image.shape,
            dtype=np.uint8
        )

        polygon = np.rint(points).astype(np.int32)

        cv2.fillPoly(
            mask,
            [polygon],
            color=1
        )

        return mask.astype(bool)

    # 분석할 영역 선택
    if region == "inner":

        mask = make_mask("inner")

    elif region == "outer":

        mask = make_mask("outer")

    elif region == "myocardium":

        outer_mask = make_mask("outer")
        inner_mask = make_mask("inner")

        # 외벽 내부에서 내벽 내부를 제외
        mask = outer_mask & ~inner_mask

    else:
        raise ValueError("알 수 없는 ROI 영역입니다.")

    # 마스크 안에 있는 픽셀만 추출
    pixels = image[mask]

    if pixels.size == 0:
        raise ValueError("ROI에 분석 가능한 픽셀이 없습니다.")

    histogram = np.bincount(
        pixels,
        minlength=256
    )

    return {
        "area": int(pixels.size),
        "mean": float(np.mean(pixels)),
        "std": float(np.std(pixels)),
        "min": int(np.min(pixels)),
        "max": int(np.max(pixels)),
        "histogram": histogram,
        "edge_density": float(
            np.count_nonzero(pixels) / pixels.size * 100
        ),
    }

