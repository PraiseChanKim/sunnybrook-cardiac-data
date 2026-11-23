"""review_status.py 테스트 — 실행: pytest test_review_status.py -v"""

import pytest

from review_status import (
    ADMIN, REGISTRAR, REVIEWER,
    RECEIVED, ASSIGNED, IN_REVIEW, REVISION, COMPLETED,
    TransitionError, apply_action, allowed_actions, can_edit_memo, split_work_list,
)


def make_case(status, assignee=None):
    return {"case_id": "MOCK-001", "status": status, "assignee": assignee}


# ── 정상 흐름 ──────────────────────────────────────────
def test_full_happy_path():
    case = make_case(RECEIVED)

    r = apply_action(case, "assign", "admin1", ADMIN, assignee="rev1")
    assert r.new_status == ASSIGNED and r.assignee == "rev1"
    case = {**case, "status": r.new_status, "assignee": r.assignee}

    r = apply_action(case, "start", "rev1", REVIEWER)
    assert r.new_status == IN_REVIEW
    case = {**case, "status": r.new_status}

    r = apply_action(case, "complete", "rev1", REVIEWER)
    assert r.new_status == COMPLETED


def test_revision_loop():
    case = make_case(IN_REVIEW, "rev1")
    r = apply_action(case, "request_revision", "rev1", REVIEWER, reason="영상 흐림")
    assert r.new_status == REVISION
    r = apply_action({**case, "status": REVISION}, "resubmit", "reg1", REGISTRAR)
    assert r.new_status == IN_REVIEW


def test_reopen_after_complete_records_reason():
    case = make_case(COMPLETED, "rev1")
    r = apply_action(case, "reopen", "admin1", ADMIN, reason="메모 누락")
    assert r.new_status == IN_REVIEW
    assert r.history_entry["reason"] == "메모 누락"
    assert r.history_entry["from_status"] == COMPLETED


def test_history_entry_fields():
    r = apply_action(make_case(RECEIVED), "assign", "admin1", ADMIN, assignee="rev1")
    for key in ("action", "from_status", "to_status", "by", "role", "assignee", "at"):
        assert key in r.history_entry


def test_original_case_not_modified():
    case = make_case(RECEIVED)
    apply_action(case, "assign", "admin1", ADMIN, assignee="rev1")
    assert case["status"] == RECEIVED  # 원본 dict는 그대로


# ── 거절되어야 하는 경우 ───────────────────────────────
def test_skip_state_rejected():
    with pytest.raises(TransitionError, match="할 수 없습니다"):
        apply_action(make_case(RECEIVED), "complete", "rev1", REVIEWER)


def test_wrong_role_rejected():
    with pytest.raises(TransitionError, match="권한"):
        apply_action(make_case(RECEIVED), "assign", "rev1", REVIEWER, assignee="rev1")


def test_other_reviewer_rejected():
    with pytest.raises(TransitionError, match="담당 검토자"):
        apply_action(make_case(ASSIGNED, "rev1"), "start", "rev2", REVIEWER)


def test_reason_required():
    with pytest.raises(TransitionError, match="사유"):
        apply_action(make_case(COMPLETED, "rev1"), "reopen", "admin1", ADMIN, reason="  ")


def test_assign_without_assignee_rejected():
    with pytest.raises(TransitionError, match="담당자"):
        apply_action(make_case(RECEIVED), "assign", "admin1", ADMIN)


def test_unknown_action_and_role():
    with pytest.raises(TransitionError):
        apply_action(make_case(RECEIVED), "delete", "admin1", ADMIN)
    with pytest.raises(TransitionError):
        apply_action(make_case(RECEIVED), "assign", "x", "hacker", assignee="rev1")


def test_double_complete_rejected():
    """연속 클릭으로 완료가 두 번 기록되지 않아야 함"""
    case = make_case(IN_REVIEW, "rev1")
    r = apply_action(case, "complete", "rev1", REVIEWER)
    with pytest.raises(TransitionError):
        apply_action({**case, "status": r.new_status}, "complete", "rev1", REVIEWER)


# ── 화면 보조 함수 ─────────────────────────────────────
def test_allowed_actions():
    assert allowed_actions(make_case(RECEIVED), "admin1", ADMIN) == ["assign"]
    assert allowed_actions(make_case(IN_REVIEW, "rev1"), "rev1", REVIEWER) == [
        "complete", "request_revision",
    ]
    assert allowed_actions(make_case(IN_REVIEW, "rev1"), "rev2", REVIEWER) == []


def test_can_edit_memo():
    assert can_edit_memo(make_case(IN_REVIEW, "rev1"), "rev1", REVIEWER)
    assert not can_edit_memo(make_case(COMPLETED, "rev1"), "rev1", REVIEWER)
    assert not can_edit_memo(make_case(IN_REVIEW, "rev1"), "rev2", REVIEWER)


def test_split_work_list():
    cases = [
        make_case(ASSIGNED, "rev1"),
        make_case(IN_REVIEW, "rev1"),
        make_case(COMPLETED, "rev1"),
        make_case(IN_REVIEW, "rev2"),
    ]
    lists = split_work_list(cases, "rev1")
    assert len(lists["todo"]) == 2 and len(lists["done"]) == 1
