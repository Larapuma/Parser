from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.testing.suite.test_reflection import users

#Base Session - классы тут
Base = declarative_base()# класс от которого мы наследуемся
engine = create_engine("sqlite:///demo.db") #в скобках указываем бд
Session = sessionmaker(bind=engine)
session = Session()

class YoutubeUser(Base):
    __tablename__ = "youtube_users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    subs = Column(Integer, default=0)
    videos = relationship("Video", back_populates="author_id")

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    views = Column(Integer, default=0)
    creator_id = Column(Integer, ForeignKey('youtube_users.id')) # связь 1 ко многим в класс foreignKey приписываем по какомцу столбцу соединение
    author_id = relationship("YoutubeUser", back_populates="videos")

Base.metadata.create_all(engine)


# kuplinov = YoutubeUser(username="kuplinov")
# video1 = Video(title = "DL2")
# video2 = Video(title = "CS")
# kuplinov.videos = [video1,video2]
# session.add(kuplinov)
# session.commit()
users = session.query(YoutubeUser).all()
for user in users:
    print(f"Username: {user.username}")
    print("Videos")
    for video in user.videos:
        print(f"-- {video.title}")