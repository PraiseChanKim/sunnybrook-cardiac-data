
import cv2
import numpy as np


def apply_clahe(image, clip_limit=2.0, tile_size=8):
    """
    CLAHE를 이용한 명암 대비 개선

    Parameters
    ----------
    image : numpy.ndarray
        2차원 흑백 영상 (uint8)
    clip_limit : float
        명암 대비 제한값
    tile_size : int
        가로/세로 분할 영역 개수

    Returns
    -------
    numpy.ndarray
        CLAHE 적용 영상
    """

    # 1. 영상 형태 확인
    if image.ndim != 2:
        raise ValueError("2차원 흑백 영상만 지원합니다.")

    if image.dtype != np.uint8:
        raise ValueError("uint8 영상만 지원합니다.")

    if clip_limit <= 0 or tile_size < 1:
        raise ValueError("CLAHE 파라미터가 올바르지 않습니다.")

    # 2. CLAHE 객체 생성
    clahe = cv2.createCLAHE(
        clipLimit=float(clip_limit),
        tileGridSize=(int(tile_size), int(tile_size))
    )

    # 3. 영상처리
    result = clahe.apply(image)

    return result
