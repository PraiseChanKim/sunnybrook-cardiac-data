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

**Gaussian Blur 영상처리 알고리즘 구현**

- OpenCV를 활용한 Gaussian Blur 영상 평활화 알고리즘 구현
- src/imaging/image_processing.py에 apply_gaussian_blur() 함수 추가
- Kernel Size 및 Sigma 파라미터 조절 기능 구현
- Streamlit에서 원본 MRI, CLAHE, Gaussian Blur 결과 비교 기능 추가
- Kernel Size 15, Sigma 4.5 설정에서 영상 평활화 결과 확인
- 기존 CLAHE 알고리즘과 독립적으로 동작하도록 구현
- 새로운 라이브러리 추가 없음 (기존 OpenCV 사용)
- 관련 PR: 45debf6bf16669fe61e6f4264d2783609cfa7ab6

**2026-11-23 | 팀원 yechan**

**Canny Edge Detection 알고리즘 구현**

- OpenCV를 활용한 Canny 경계선 검출 알고리즘 구현
- `src/imaging/image_processing.py`에 `apply_canny()` 함수 추가
- Low Threshold 및 High Threshold 조절 기능 구현
- Canny 적용 전 Gaussian Blur 전처리 추가
- Streamlit에서 원본, CLAHE, Gaussian Blur, Canny 영상 4종 비교 기능 구현
- 임계값 변화에 따른 경계선 검출 결과 테스트 완료
- 영상처리 알고리즘 3종 구현 및 기본 동작 검증 완료
- 관련 PR: 6b79c2a033c892305b1d079e75c866ef07d91d57

## 2026-11-24

**2026-11-24 | 팀원 yechan**

**Sunnybrook Cardiac PACS 웹사이트 및 MRI 분석 기능 구현**

**작업 내용**

- Streamlit을 활용한 Sunnybrook Cardiac PACS 웹사이트 기본 UI 개발
- 대시보드, MRI 뷰어, 케이스 관리, 검토 관리, 사용자 관리 메뉴 구성
- Case Browser를 통한 DICOM 케이스 검색 및 영상 선택 기능 구현
- 기존 CLAHE, Gaussian Blur, Canny Edge 알고리즘을 PACS 웹사이트에 통합
- 영상처리 파라미터 조절 및 원본·처리 결과 비교 기능 구현
- streamlit-cropper를 이용한 마우스 기반 ROI 선택 기능 추가
- ROI 평균, 표준편차, 최솟값, 최댓값, 픽셀 면적 및 히스토그램 계산 기능 구현
- Plotly를 활용한 MRI 확대·축소·이동·초기화 기능 구현
- PACS 사이드바, 메뉴 글씨 및 MRI 뷰어 크기 조정

**담당 및 수정 파일**

- app.py : PACS 웹사이트 UI 및 영상 분석 기능 통합
- src/imaging/roi_analysis.py : ROI 통계 및 히스토그램 계산
- .streamlit/config.toml : 웹사이트 다크 테마 설정
- requirements.txt : 필요한 라이브러리 추가

**테스트 및 검증**

- Sunnybrook DICOM 영상 로딩 및 케이스 전환 확인
- CLAHE, Gaussian Blur, Canny Edge 정상 동작 확인
- ROI 사각형 크기와 위치에 따른 통계값 및 히스토그램 변화 확인
- 일반 MRI 모드와 ROI 분석 모드 전환 확인
- MRI 확대·축소, 드래그 이동 및 화면 초기화 확인
- 원본 MRI와 처리 영상의 동시 비교 확인

**향후 개선 사항**

- 영상처리 파라미터 변경 시 확대 위치가 초기화되는 현상 개선
- 원본과 처리 영상의 ROI 통계 비교 기능 추가
- Sunnybrook 좌심실 윤곽선 분석 기능 구현
- B·C 담당 기능과 PACS 웹사이트 연동

- 관련 PR: ce47f79bcf449fe6bd647a086d78cf92f98d13a2

**2026-11-24 | 팀원 yechan**

**Sunnybrook 좌심실 윤곽선 분석 기능 구현**

**작업 내용**

- Sunnybrook Cardiac MR Database의 ContoursPart3 데이터셋 활용
- 전문가 수동 윤곽선 좌표 파일(icontour, ocontour) 로딩 기능 구현
- 케이스 ID와 DICOM 파일명을 기준으로 MRI 영상 및 윤곽선 데이터 매칭
- 좌심실 내벽(Endocardium)과 외벽(Epicardium) 윤곽선 시각화
- OpenCV 기반 좌심실 내벽·외벽의 픽셀 면적 계산
- 외벽과 내벽의 면적 차이를 이용한 심근(Myocardium) 영역 면적 계산
- PACS Analysis Tools에 좌심실 윤곽선 표시 ON/OFF 기능 추가
- Case Browser에 '윤곽선 있는 영상만 보기' 필터 구현
- 기존 CLAHE, Gaussian Blur, Canny Edge 및 ROI 분석 기능과 연동

**담당 및 수정 파일**

- src/imaging/contour.py: 윤곽선 좌표 로딩, 시각화 및 면적 계산
- app.py: 좌심실 윤곽선 표시 및 영상 필터 기능 통합
- 테스트 및 검증
- SC-HF-I-01 / IM-0001-0059.dcm의 내벽 및 외벽 윤곽선 파일 로딩 확인
- 내벽 좌표 210개, 외벽 좌표 269개 확인
- 내벽 면적 1,097 px², 외벽 면적 1,782 px², 심근 면적 685 px² 계산 확인
- MRI 원본 및 CLAHE 처리 영상에 윤곽선이 표시되는 것 확인
- 윤곽선이 존재하는 MRI만 선택하는 필터 정상 작동 확인
- 윤곽선 데이터가 없는 영상에서도 기존 MRI 조회 기능 유지

**향후 개선 사항**

- DICOM PixelSpacing을 활용한 실제 면적(mm²) 계산
- 원본 및 처리 영상의 동일 ROI 통계 비교
- 특화 기능에 대한 정량적 검증 및 보고서 작성
- Firebase 및 케이스 검토 시스템과 연동

- 관련 PR: 7670ebc3b2293a5cf539b2c951c151a0cca834f3

**2026-11-24 | 팀원 yechan**

**좌심실 ROI 기반 영상처리 전후 정량 비교 기능 통합**

**작업 내용**

- 기존 좌심실 윤곽선 분석 기능에 영상처리 전후 정량 비교 기능 통합
- 내강(LV Cavity), 외벽 내부(Epicardium), 심근(Myocardium) 영역의 자동 ROI 지정
- 동일 ROI에서 원본 및 처리 영상의 평균·표준편차 비교
- 원본 및 처리 영상의 밝기 히스토그램 비교
- Canny Edge 적용 시 에지 픽셀 밀도 계산
- 기존 수동 사각형 ROI에도 영상처리 전후 비교 기능 적용
- CLAHE, Gaussian Blur, Canny Edge 알고리즘과 연동

**구현 및 수정 파일**

- src/imaging/contour.py
- app.py

**테스트 결과**

- 좌심실 내강 및 심근 영역 변경에 따라 ROI 면적과 통계가 갱신되는 것 확인
- 영상처리 설정값 변경 시 원본·처리 ROI 비교 결과가 갱신되는 것 확인
- 원본 및 처리 결과 히스토그램 출력 확인
- 기존 MRI Viewer 및 윤곽선 분석 기능과 통합 작동 확인

**향후 개선**

- DICOM PixelSpacing 기반 실제 면적(mm²) 계산
- 정량 비교 결과의 저장 및 검토 업무 연동
- 통합 특화 기능의 보고서 및 시연 자료 작성

- 관련 PR: b3e1f5729c73f90f7c4e7f7dc872da67e2b5f147

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

