
import numpy as np


def analyze_roi(image, x, y, width, height):
    """
    Analyze a rectangular ROI in an 8-bit grayscale image.

    Parameters
    ----------
    image : np.ndarray
        2D uint8 grayscale MRI image.
    x, y : int
        Top-left position of the ROI.
    width, height : int
        ROI dimensions in pixels.

    Returns
    -------
    dict
        ROI coordinates, statistics, pixels and histogram.
    """

    if image.ndim != 2 or image.dtype != np.uint8:
        raise ValueError(
            "ROI 분석에는 2D uint8 흑백 영상이 필요합니다."
        )

    image_height, image_width = image.shape

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    if width <= 0 or height <= 0:
        raise ValueError("ROI 크기는 0보다 커야 합니다.")

    # Clamp ROI coordinates to the image boundaries.
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(image_width, x + width)
    y2 = min(image_height, y + height)

    if x1 >= x2 or y1 >= y2:
        raise ValueError("ROI가 영상 범위를 벗어났습니다.")

    roi = image[y1:y2, x1:x2]

    mean_value = float(np.mean(roi))
    std_value = float(np.std(roi))
    min_value = int(np.min(roi))
    max_value = int(np.max(roi))

    # Count pixels for each grayscale value (0~255).
    histogram = np.bincount(
        roi.flatten(),
        minlength=256,
    )

    return {
        "x": x1,
        "y": y1,
        "width": x2 - x1,
        "height": y2 - y1,
        "area": int(roi.size),
        "mean": mean_value,
        "std": std_value,
        "min": min_value,
        "max": max_value,
        "histogram": histogram,
        "roi_image": roi.copy(),
    }
