# 데이터 준비

데이터는 용량이 커서 git에 올리지 않는다(`.gitignore`의 `data/`). **팀원 각자 공식 출처에서 받아 아래 위치에 둔다.**

## 데이터셋 정보
| 항목 | 내용 |
|---|---|
| 이름 | Sunnybrook Cardiac Data (심장 cine MRI, DICOM) |
| 규모 | 45명, 배포 파일 합계 약 608MB |
| 배포처 | SourceForge (원 배포 프로젝트) |
| 이용 조건 | 공개 배포, CC0 1.0 (데이터 README 기준) |
| 정답 | 좌심실 endocardial/epicardial contour 텍스트 (일부 프레임/슬라이스만 존재) |

## 준비 방법
1. 원 배포 프로젝트에서 **DICOM part와 contour part를 함께** 받는다.
2. 압축을 풀어 레포 루트의 `data/` 아래에 둔다. (`data/`가 없으면 직접 만든다.)
3. 현재 코드(`personal/yechan/test_dicom.py`)가 기대하는 경로:

```
data/
└── Sunnybrook Cardiac MR Database DICOMPart3/
    └── Sunnybrook Cardiac MR Database DICOMPart3/
        └── TrainingDataDICOM/
```

> contour part의 폴더 구조는 받은 뒤 이 문서에 추가한다.

## 주의
- 모든 프레임에 정답 윤곽이 있는 것은 아니다. 처음에는 한 slice의 시간축 cine와 윤곽 표시부터 구현한다.
- 경로는 `Path(__file__)` 기준으로 계산하고 `/Users/이름/...` 같은 절대 경로를 코드에 쓰지 않는다.
- 데이터 파일(`*.dcm` 등)을 커밋하지 않는다.
