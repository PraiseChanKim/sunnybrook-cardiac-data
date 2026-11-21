
import numpy as np
import pydicom

from pydicom.pixels import apply_modality_lut, apply_voi_lut


def load_dicom(file_path):
    # 1. DICOM 파일 읽기
    dicom = pydicom.dcmread(str(file_path))

    # 2. 픽셀 데이터 추출
    image = dicom.pixel_array

    # 현재는 2차원 흑백 영상만 지원
    if image.ndim != 2:
        raise ValueError("2차원 DICOM 영상만 지원합니다.")

    # 3. DICOM 영상 명암 변환
    image = apply_modality_lut(image, dicom)
    image = apply_voi_lut(image, dicom)

    image = np.asarray(image, dtype=np.float32)

    if not np.isfinite(image).all():
        raise ValueError("유효하지 않은 픽셀 값이 있습니다.")

    # 4. 최솟값과 최댓값 계산
    min_value = image.min()
    max_value = image.max()

    # 5. 화면 표시용 0~255 정규화
    if max_value > min_value:
        image = (
            (image - min_value)
            / (max_value - min_value)
            * 255
        )
    else:
        image = np.zeros_like(image)

    image = image.astype(np.uint8)

    # 6. 필요한 경우 흑백 반전
    if dicom.get("PhotometricInterpretation") == "MONOCHROME1":
        image = 255 - image

    # 7. 영상 메타데이터
    metadata = {
        "modality": str(dicom.get("Modality", "Unknown")),
        "rows": int(dicom.Rows),
        "columns": int(dicom.Columns),
        "instance_number": str(
            dicom.get("InstanceNumber", "N/A")
        )
    }

    return image, metadata
