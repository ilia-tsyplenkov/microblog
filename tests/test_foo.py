from datetime import datetime, timedelta
from app.models import User, Post
from app import db

# def test_password_hashing(prepare_db):
def test_password_hashing():
    u = User(username='susan')
    u.set_password('cat')
    assert u.check_password('cat')
    assert not u.check_password('dog')


def test_avatar():
    u = User(username='john', email='john@example.com')
    assert u.avatar(128) == 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'


def test_follow():
    john = User(username="john", email='john@example.com')
    sara = User(username="sara", email='sara@example.com')
    db.session.add(john)
    db.session.add(sara)
    db.session.commit()
    assert john.followed.all() == []
    assert sara.followed.all() == []

    john.follow(sara)

    db.session.commit()
    assert john.is_following(sara)
    assert john.followed.count() == 1
    assert john.followed.first().username == 'sara'
    assert sara.followers.count() == 1
    assert sara.followers.first().username == "john"

    john.unfollow(sara)
    assert not john.is_following(sara)
    assert john.followed.count() == 0
    assert sara.followers.count() == 0

def test_follow_posts():
    john = User(username="john", email='john@example.com')
    sara = User(username="sara", email='sara@example.com')
    mary = User(username="mary", email='mary@example.com')
    david = User(username="david", email='david@example.com')
    db.session.add_all([john, sara, mary, david])
    db.session.commit()

    now = datetime.utcnow()
    post_john = Post(body="from john", author=john, timestamp=now + timedelta(seconds=1))
    post_sara = Post(body="from sara", author=sara, timestamp=now + timedelta(seconds=4))
    post_mary = Post(body="from mary", author=mary, timestamp=now + timedelta(seconds=3))
    post_david = Post(body="from david", author=david, timestamp=now + timedelta(seconds=2))


    db.session.add_all([post_john, post_sara, post_mary, post_david])
    db.session.commit()
    john.follow(sara)
    john.follow(david)
    sara.follow(mary)
    mary.follow(david)
    db.session.commit()

    f_john = john.followed_posts().all()
    f_sara = sara.followed_posts().all()
    f_mary = mary.followed_posts().all()
    f_david = david.followed_posts().all()


    assert f_john == [post_sara, post_david, post_john]
    assert f_sara == [post_sara, post_mary]
    assert f_mary == [post_mary, post_david]
    assert f_david == [post_david]
