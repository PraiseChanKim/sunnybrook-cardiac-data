# sunnybrook-cardiac-data

[Term_Project] Sunnybrook 심장 cine MRI(DICOM)를 이용해 좌심실 윤곽을 시각화하고 수축/이완을 비교하는 Python·Streamlit 기반 교육용 웹 PACS 프로젝트.

> 교육용이며 실제 의료 진단용이 아닙니다.

## 빠른 시작
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
데이터는 [docs/data.md](docs/data.md)를 따라 준비한 뒤 실행합니다.

메인 앱 (진입점):
```bash
streamlit run app.py
```

현재 동작하는 개인 테스트 뷰어 (`app.py`가 채워지기 전까지):
```bash
streamlit run personal/yechan/test_dicom.py
```

## 문서
작업 전에 아래 문서를 먼저 확인하세요.

| 문서 | 내용 |
|---|---|
| [docs/project-guide.md](docs/project-guide.md) | 과제 기준 (구현 요구사항, 제출 방법, 평가 관련) |
| [docs/data.md](docs/data.md) | 데이터 다운로드와 폴더 구조 |
| [history.md](history.md) | 팀원별 개발 이력 |

## 폴더 구조
- `src/`: 공통 모듈 (`imaging`, `backend`, `review`)
- `personal/`: 팀원별 개인 작업 폴더
- `docs/`: 프로젝트 기준과 문서
