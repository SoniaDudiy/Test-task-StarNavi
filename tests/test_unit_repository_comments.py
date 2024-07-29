import pytest
from sqlalchemy.orm import Session
from src.database.models import Comment
from src.schemas import CommentCreate
from src.repository.comments import create_comment, get_comments, get_comment_by_id, update_comment, delete_comment, block_comment

@pytest.fixture
def comment_data():
    return CommentCreate(
        content="Test comment",
        post_id=1
    )

def test_create_comment(session: Session, comment_data):
    user_id = 1
    comment = create_comment(session, comment_data, user_id)
    assert comment
    assert comment.content == comment_data.content
    assert comment.post_id == comment_data.post_id
    assert comment.user_id == user_id

def test_get_comments(session: Session, comment_data):
    user_id = 1
    create_comment(session, comment_data, user_id)
    comments = get_comments(session)
    assert len(comments) > 0

def test_get_comment_by_id(session: Session, comment_data):
    user_id = 1
    comment = create_comment(session, comment_data, user_id)
    retrieved_comment = get_comment_by_id(session, comment.id)
    assert retrieved_comment
    assert retrieved_comment.id == comment.id
    assert retrieved_comment.content == comment_data.content

def test_update_comment(session: Session, comment_data):
    user_id = 1
    comment = create_comment(session, comment_data, user_id)
    new_content = "Updated comment"
    updated_comment = update_comment(session, comment.id, new_content)
    assert updated_comment
    assert updated_comment.content == new_content

def test_delete_comment(session: Session, comment_data):
    user_id = 1
    comment = create_comment(session, comment_data, user_id)
    deleted_comment = delete_comment(session, comment.id)
    assert deleted_comment
    assert not get_comment_by_id(session, comment.id)

def test_block_comment(session: Session, comment_data):
    user_id = 1
    comment = create_comment(session, comment_data, user_id)
    blocked_comment = block_comment(session, comment.id)
    assert blocked_comment
    assert blocked_comment.is_blocked
