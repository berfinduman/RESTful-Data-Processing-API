# app/models.py
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DailyCampaign(Base):
    __tablename__ = "tbl_daily_campaigns"
    campaign_id = Column(String, primary_key=True, index=True)
    campaign_name = Column(String)
    views = Column(Integer)
    impressions = Column(Integer)
    cpm = Column(Float)
    clicks = Column(Integer)
    date = Column(Date)

class DailyScore(Base):
    __tablename__ = "tbl_daily_scores"
    campaign_id = Column(String, primary_key=True, index=True)
    media = Column(Float)
    creative = Column(Float)
    effectiveness = Column(Float)
    date = Column(Date)
