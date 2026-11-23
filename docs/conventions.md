# 개발 규칙

> 평가에서 Issue · 커밋 · PR이 개인 기여 근거로 쓰인다. 아래 흐름을 지켜 기록이 남게 한다.

## 작업 흐름
1. **Issue 작성** (담당 기능, 완료 기준)
2. **브랜치 생성** → 작업 → 커밋
3. **PR 생성** → 다른 팀원이 **코드리뷰** → 승인 후 merge
4. 완료 후 [history.md](../history.md)에 작업 내용 기록

`main`에는 직접 push하지 않는다. 모든 변경은 PR로 올린다.

## 브랜치 이름
`<종류>/<짧은-설명>` (영문 소문자, 하이픈)

| 종류 | 용도 | 예시 |
|---|---|---|
| `feature/` | 기능 추가 | `feature/dicom-loader` |
| `fix/` | 버그 수정 | `fix/contour-offset` |
| `docs/` | 문서 | `docs/update-history` |
| `chore/` | 설정, 환경 | `chore/gitignore` |

## 커밋 메시지
`<종류>: <무엇을 했는지>`

```
feat: add contour overlay on cine viewer
fix: correct frame index in slider
docs: update data guide
chore: update .gitignore
```
종류는 `feat`, `fix`, `docs`, `chore`, `refactor`, `test`를 쓴다. 하나의 커밋에는 하나의 변경만 담는다.

## PR 규칙
- 제목은 커밋 메시지와 같은 형식, 본문은 PR 템플릿을 채운다.
- 관련 Issue를 연결한다. (`Closes #번호`)
- **본인 외 최소 1명의 승인** 후 merge한다. 리뷰어는 코멘트로 확인한 내용을 남긴다.
- PR은 작게 유지한다. 한 PR에 기능 하나.

## 코드 규칙
- 공통으로 쓰는 코드는 `src/`, 개인 실험은 `personal/<이름>/`에 둔다.
- 경로는 `Path(__file__)` 기준으로 계산하고 절대 경로를 쓰지 않는다.
- 비밀 정보(Firebase 키, 비밀번호)는 절대 커밋하지 않는다. `.env` 또는 `.streamlit/secrets.toml`을 쓰고 공유는 레포 밖에서 한다.
- 데이터 파일(`data/`, `*.dcm`)은 커밋하지 않는다. ([data.md](data.md) 참고)
- 새 라이브러리를 쓰면 `requirements.txt`에 추가한다.
