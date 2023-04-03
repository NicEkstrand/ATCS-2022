"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    tweets = relationship("Tweet", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))
    

class Tweet(Base):
    __tablename__ = "tweets"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT)
    timestamp = Column("timestamp", INTEGER)
    username = Column("username", TEXT, ForeignKey("users.username"))
    user = relationship("User", back_populates="tweets")
    tags = relationship("Tag", secondary="tweettags",back_populates="tweets")

    def __init__(self, content, timestamp, username):
        self.content = content
        self.timestamp = timestamp
        self.username = username

    def __repr__(self):
        tag_text = ""
        for tag in self.tags:
            tag_text = tag_text + tag.content + " "
        return "@" + self.username + "\n" + self.content + "\n" + tag_text + "\n" + self.timestamp
        

class Tag(Base):
    __tablename__ = "tags"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT)
    tweets = relationship("Tweet", secondary="tweettags", back_populates="tags")

    def __init__(self, content):
        self.content = content

class TweetTag(Base):
    __tablename__ = "tweettags"
    id = Column("id", INTEGER, primary_key=True)
    tweet_id = Column("tweet_id", INTEGER, ForeignKey("tweets.id"))
    tag_id = Column("tag_id", INTEGER, ForeignKey("tags.id"))

    def __init__(self, tweet_id, tag_id):
        self.tweet_id = tweet_id
        self.tag_id = tag_id
