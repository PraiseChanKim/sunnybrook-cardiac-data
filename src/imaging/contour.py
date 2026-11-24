
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
