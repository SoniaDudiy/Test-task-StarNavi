from src.repository.comments import create_comment, get_comment_by_id, block_comment

def contains_profanity(content: str) -> bool:
    profanity_list = ["badword1", "badword2"]
    return any(word in content.lower() for word in profanity_list)

def create_new_comment(db, comment, user_id):
    if contains_profanity(comment.content):
        comment.is_blocked = True
    return create_comment(db, comment, user_id)

def handle_blocking(db, comment_id):
    return block_comment(db, comment_id)
