# Sunnybrook Cardiac Data - Development History

프로젝트 개발 과정과 팀원별 작업 내역을 기록합니다.

## 2026-11-21

**2026-11-21 | 팀원 yechan**

**의료영상 기능 개발**

- src/imaging/dicom_loader.py 구현
- pydicom을 활용한 심장 MRI 영상 로딩 기능 개발
- DICOM 픽셀 데이터 정규화 및 메타데이터 추출
- personal/yechan/에 Streamlit 테스트 뷰어 구현
- Sunnybrook 심장 MRI 영상 출력 테스트 성공
- MRI 케이스 선택 및 영상 번호 슬라이더 기능 구현
- 관련 PR: 8cec8ba647a650a5ece99047f50fd58014818c12

### 프로젝트 환경 설정
- 팀원별 개인 작업 폴더(`personal/`) 구성
- GitHub 협업 환경 정리
- 개발 이력 관리용 `history.md` 파일 생성


## 2026-11-23

**2026-11-23 | 팀원 yusin**

**검토(review) 기능 개발**

- `personal/yu/review_status.py` 구현
- 검토 상태 전이 규칙 및 역할별 권한 검사
- 업무 목록 분리 및 메모 작성 가능 여부 함수 추가
- `personal/yu/test_review_status.py` 테스트 15개 작성, 전체 통과
- 관련 PR: #3

**2026-11-23 | 팀원 yechan**

**CLAHE 영상처리 알고리즘 구현**

- OpenCV를 활용한 CLAHE 명암 대비 개선 알고리즘 구현
- `src/imaging/image_processing.py`에 `apply_clahe()` 함수 추가
- Clip Limit 및 Tile Grid Size 파라미터 조절 기능 구현
- Streamlit에서 원본 심장 MRI와 CLAHE 처리 결과 비교 기능 추가
- Clip Limit 2.0 → 10.0, Tile Grid Size 8 → 16 변경 테스트 완료
- 파라미터 변경에 따른 명암 대비 변화 확인
- `requirements.txt`에 `opencv-python-headless` 의존성 추가
- 관련 PR: 0aa19b6c571c56bec9c3bc283cca6ff84e07196e

---

## 작성 규칙

작업을 완료한 팀원은 다음 내용을 추가합니다.

- **날짜:** YYYY-MM-DD
- **작업자:** 팀원 이름
- **작업 내용:** 추가하거나 수정한 기능
- **관련 PR:** PR 번호 또는 링크 (있는 경우)

### 작성 예시

**2026-11-22 | 팀원 A**
- DICOM 영상 로딩 기능 구현
- 영상 출력 테스트 완료
- 관련 PR: #1

