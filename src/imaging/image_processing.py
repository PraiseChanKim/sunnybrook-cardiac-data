
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
