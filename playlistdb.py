import sqlite3
# import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer,FLOAT, DateTime,String,Unicode, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn = sqlite3.connect('ltg-pldb.db')

# 创建播放列表表
# status 状态：0 启用，1停用,2,已删除，20，待删除,10：待启用，11：准备中,
conn.execute('''
        CREATE TABLE IF NOT EXISTS playlist
        (
            playlistid varchar(36) PRIMARY KEY not null,
            iotpath varchar(255) not null,
            mediaid varchar(36),
            filename nvarchar(150),
            urlpath nvarchar(250),
            mediatype varchar(25),
            extension varchar(20),
            lastplaytime datetime,
            tag varchar(50),
            duration float,
            size int,
            playcount int default 0,
            status int default 10,
            createdon datetime,
            modifiedon datetime)
    ''')

# 播放日志
# status 状态: 0,已播放，1，播放中止
conn.execute('''
        CREATE TABLE IF NOT EXISTS playlog
        (
            playlogid varchar(36) PRIMARY KEY not null,
            playlistid varchar(36) not null,
            createdon datetime,
            startedon datetime,
            endon   datetime,
            status int default 0)
    ''')
conn.close()

# 使用SqlAlchemy
engine = create_engine('sqlite:///ltg-pldb.db?check_same_thread=False', echo=True)
EntityBase = declarative_base()

class PlayList(EntityBase):
    __tablename__ = 'playlist'
    playlistid = Column(String(36), primary_key=True)
    iotpath = Column(String(255))
    mediaid = Column(String(36))
    filename = Column(Unicode(150))
    mediatype = Column(String(25))
    urlpath = Column(Unicode(250))
    extension = Column(String(20))
    lastplaytime = Column(DateTime)
    duration = Column(FLOAT)
    size = Column(Integer)
    tag = Column(String(50))
    playcount = Column(Integer)
    status = Column(Integer)
    createdon = Column(DateTime)
    modifiedon = Column(DateTime)

class PlayLog(EntityBase):
    __tablename__ = 'playlog'
    playlogid = Column(String(36), primary_key=True)
    playlistid = Column(String(36))
    createdon = Column(DateTime)
    startedon = Column(DateTime)
    endon   = Column(DateTime)
    status = Column(Integer)


Session = sessionmaker(bind=engine)


def GetDbSession():
    session = Session()
    return session