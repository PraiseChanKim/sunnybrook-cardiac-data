"""검토 상태 전이 규칙 (review 파트)

Firebase·Streamlit 없이 동작하는 순수 함수 모듈입니다.
나중에 src/review/ 로 옮기고, 백엔드(Firestore)에서는
apply_action()의 결과(new_status, history_entry)만 저장하면 됩니다.

상태 흐름
    접수(RECEIVED) --assign--> 배정(ASSIGNED) --start--> 검토 중(IN_REVIEW)
    검토 중 --complete--> 완료(COMPLETED)
    검토 중 --request_revision--> 보완 요청(REVISION)
    보완 요청 --resubmit--> 검토 중
    완료 --reopen--> 검토 중   (사유 필수, 이력에 남음)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

# ── 상태 ──────────────────────────────────────────────
RECEIVED = "received"
ASSIGNED = "assigned"
IN_REVIEW = "in_review"
REVISION = "revision"
COMPLETED = "completed"

STATUS_LABELS = {
    RECEIVED: "접수",
    ASSIGNED: "배정",
    IN_REVIEW: "검토 중",
    REVISION: "보완 요청",
    COMPLETED: "완료",
}

# ── 역할 ──────────────────────────────────────────────
REGISTRAR = "registrar"  # 등록 담당자: 케이스·영상 접수
REVIEWER = "reviewer"    # 검토 담당자: 처리·비교·메모
ADMIN = "admin"          # 관리 담당자: 배정·진행 현황

ROLES = {REGISTRAR, REVIEWER, ADMIN}

# ── 전이 규칙 ─────────────────────────────────────────
# action: (출발 상태, 도착 상태, 실행 가능한 역할, 담당 검토자 본인만 가능?, 사유 필수?)
@dataclass(frozen=True)
class Rule:
    from_status: str
    to_status: str
    roles: frozenset
    assignee_only: bool = False
    reason_required: bool = False


RULES: dict[str, Rule] = {
    "assign": Rule(RECEIVED, ASSIGNED, frozenset({ADMIN})),
    "start": Rule(ASSIGNED, IN_REVIEW, frozenset({REVIEWER}), assignee_only=True),
    "complete": Rule(IN_REVIEW, COMPLETED, frozenset({REVIEWER}), assignee_only=True),
    "request_revision": Rule(
        IN_REVIEW, REVISION, frozenset({REVIEWER}), assignee_only=True, reason_required=True
    ),
    "resubmit": Rule(REVISION, IN_REVIEW, frozenset({REGISTRAR})),
    "reopen": Rule(COMPLETED, IN_REVIEW, frozenset({ADMIN}), reason_required=True),
}

ACTION_LABELS = {
    "assign": "담당자 배정",
    "start": "검토 시작",
    "complete": "검토 완료",
    "request_revision": "보완 요청",
    "resubmit": "보완 후 재제출",
    "reopen": "완료 후 재검토",
}


class TransitionError(Exception):
    """허용되지 않은 상태 변경. message는 화면에 그대로 보여줄 수 있는 한국어 안내."""


@dataclass(frozen=True)
class TransitionResult:
    new_status: str
    assignee: str | None
    history_entry: dict  # Firestore history 컬렉션에 그대로 저장할 기록


def apply_action(
    case: dict,
    action: str,
    user_uid: str,
    user_role: str,
    *,
    assignee: str | None = None,
    reason: str = "",
    now: datetime | None = None,
) -> TransitionResult:
    """케이스에 action을 적용해 새 상태와 이력 기록을 돌려준다.

    case: {"status": ..., "assignee": ...} 를 포함한 dict
    허용되지 않으면 TransitionError를 던진다. (case 자체는 변경하지 않음)
    """
    rule = RULES.get(action)
    if rule is None:
        raise TransitionError(f"알 수 없는 동작입니다: {action}")

    if user_role not in ROLES:
        raise TransitionError(f"알 수 없는 역할입니다: {user_role}")

    current = case.get("status")
    if current != rule.from_status:
        raise TransitionError(
            f"'{STATUS_LABELS.get(current, current)}' 상태에서는 "
            f"'{ACTION_LABELS[action]}'을(를) 할 수 없습니다. "
            f"('{STATUS_LABELS[rule.from_status]}' 상태에서만 가능)"
        )

    if user_role not in rule.roles:
        raise TransitionError(f"'{ACTION_LABELS[action]}' 권한이 없는 역할입니다.")

    if rule.assignee_only and case.get("assignee") != user_uid:
        raise TransitionError("이 케이스의 담당 검토자만 할 수 있습니다.")

    if rule.reason_required and not reason.strip():
        raise TransitionError(f"'{ACTION_LABELS[action]}'에는 사유를 입력해야 합니다.")

    new_assignee = case.get("assignee")
    if action == "assign":
        if not assignee:
            raise TransitionError("배정할 검토 담당자를 선택해야 합니다.")
        new_assignee = assignee

    entry = {
        "action": action,
        "from_status": current,
        "to_status": rule.to_status,
        "by": user_uid,
        "role": user_role,
        "assignee": new_assignee,
        "reason": reason.strip(),
        "at": (now or datetime.now(timezone.utc)).isoformat(),
    }
    return TransitionResult(rule.to_status, new_assignee, entry)


def allowed_actions(case: dict, user_uid: str, user_role: str) -> list[str]:
    """화면에 보여줄 버튼 목록. (실제 실행 때도 apply_action에서 다시 검사함)"""
    result = []
    for action, rule in RULES.items():
        if case.get("status") != rule.from_status or user_role not in rule.roles:
            continue
        if rule.assignee_only and case.get("assignee") != user_uid:
            continue
        result.append(action)
    return result


def can_edit_memo(case: dict, user_uid: str, user_role: str) -> bool:
    """메모 작성 가능 여부: 검토 중인 케이스의 담당 검토자만. 완료 후엔 재검토(reopen)가 필요."""
    return (
        case.get("status") == IN_REVIEW
        and user_role == REVIEWER
        and case.get("assignee") == user_uid
    )


def split_work_list(cases: list[dict], user_uid: str) -> dict[str, list[dict]]:
    """검토자 업무 목록: 내가 처리할 업무 / 완료된 업무."""
    todo = [
        c for c in cases
        if c.get("assignee") == user_uid and c.get("status") in (ASSIGNED, IN_REVIEW)
    ]
    done = [c for c in cases if c.get("assignee") == user_uid and c.get("status") == COMPLETED]
    return {"todo": todo, "done": done}
