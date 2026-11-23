
import cv2
import numpy as np


# ==========================================
# 1. CLAHE 명암 대비 개선
# ==========================================

def apply_clahe(image, clip_limit=2.0, tile_size=8):

    if image.ndim != 2:
        raise ValueError("2차원 흑백 영상만 지원합니다.")

    if image.dtype != np.uint8:
        raise ValueError("uint8 영상만 지원합니다.")

    if clip_limit <= 0 or tile_size < 1:
        raise ValueError("CLAHE 파라미터가 올바르지 않습니다.")

    clahe = cv2.createCLAHE(
        clipLimit=float(clip_limit),
        tileGridSize=(int(tile_size), int(tile_size))
    )

    result = clahe.apply(image)

    return result


# ==========================================
# 2. Gaussian Blur 노이즈 감소
# ==========================================

def apply_gaussian_blur(image, kernel_size=5, sigma=1.0):

    if image.ndim != 2:
        raise ValueError("2차원 흑백 영상만 지원합니다.")

    if image.dtype != np.uint8:
        raise ValueError("uint8 영상만 지원합니다.")

    # 커널 크기는 양의 홀수여야 함
    if kernel_size < 1 or kernel_size % 2 == 0:
        raise ValueError("Kernel Size는 양의 홀수여야 합니다.")

    if sigma < 0:
        raise ValueError("Sigma는 0 이상이어야 합니다.")

    result = cv2.GaussianBlur(
        image,
        (kernel_size, kernel_size),
        sigmaX=float(sigma),
        sigmaY=float(sigma)
    )

    return result


# ==========================================
# 3. Canny Edge Detection
# ==========================================

def apply_canny(image, low_threshold=50, high_threshold=150):
    """
    Canny 경계선 검출

    image: 2차원 uint8 흑백 영상
    low_threshold: 하한 임계값
    high_threshold: 상한 임계값
    """

    if image.ndim != 2:
        raise ValueError("2차원 흑백 영상만 지원합니다.")

    if image.dtype != np.uint8:
        raise ValueError("uint8 영상만 지원합니다.")

    if not (0 <= low_threshold < high_threshold):
        raise ValueError(
            "High Threshold는 Low Threshold보다 커야 합니다."
        )

    # 1. Gaussian Blur로 잡음 완화
    blurred = cv2.GaussianBlur(
        image,
        (5, 5),
        sigmaX=0
    )

    # 2. Canny 경계선 검출
    edges = cv2.Canny(
        blurred,
        threshold1=int(low_threshold),
        threshold2=int(high_threshold)
    )

    return edges

