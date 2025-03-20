# app/main.py
from fastapi import FastAPI, Depends, Query
from collections import defaultdict
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app import models, schemas
from app.database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Database session provider
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/campaigns/", response_model=schemas.CampaignResponse)

def get_campaign_data(query_params: schemas.CampaignQueryParams = Depends(),db: Session = Depends(get_db)):
    campaign_id = query_params.campaign_id
    start_date = query_params.start_date
    end_date = query_params.end_date


    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    formatted_start_date = start_date_obj.strftime("%d %B %Y")
    formatted_end_date = end_date_obj.strftime("%d %B %Y")
# Join the tables and make sure both campaign_id and date match
    query = db.query(
        models.DailyCampaign.campaign_id,
        models.DailyCampaign.campaign_name,
        models.DailyCampaign.views,
        models.DailyCampaign.impressions,
        models.DailyCampaign.cpm,
        models.DailyCampaign.clicks,
        models.DailyScore.media,
        models.DailyScore.creative,
        models.DailyScore.effectiveness,
        models.DailyCampaign.date,
    ).join(
        models.DailyScore,
        and_(
            models.DailyCampaign.campaign_id == models.DailyScore.campaign_id,
            models.DailyCampaign.date == models.DailyScore.date
        )
    )


    # Filtering: If there is a campaign id, it takes the campaign id, 
    # otherwise it takes all of them with the "All" tag.
    if campaign_id:
        query = query.filter(models.DailyCampaign.campaign_id == campaign_id)
    query = query.filter(models.DailyCampaign.date.between(start_date_obj, end_date_obj))
    results = query.all()
    # Calculating campaign performance data
    current_metrics = {
        "impressions": sum([r.impressions for r in results]),
        "clicks": sum([r.clicks for r in results]),
        "views": int(sum([r.views for r in results])),
    }
    # Generate daily metrics
    impressions_cpm = {
    "impression": {r.date: r.impressions for r in results},
    "cpm": {r.date: r.cpm for r in results},
    }



    # A defaultdict to group data by Campaign ID
    campaign_data = defaultdict(lambda: {
        "start_date": None,
        "end_date": None,
        "effectiveness": 0,
        "media": 0,
        "creative": 0,
    })

# Group data by Campaign ID
    for r in results:
        campaign_id_check = r.campaign_id


        campaign_data[campaign_id_check]["start_date"] = (
            min(campaign_data[campaign_id_check]["start_date"], r.date)
            if campaign_data[campaign_id_check]["start_date"]
            else r.date
        )
        campaign_data[campaign_id_check]["end_date"] = (
            max(campaign_data[campaign_id_check]["end_date"], r.date)
            if campaign_data[campaign_id_check]["end_date"]
            else r.date
        )

        campaign_data[campaign_id_check]["effectiveness"] += r.effectiveness
        campaign_data[campaign_id_check]["media"] += r.media
        campaign_data[campaign_id_check]["creative"] += r.creative
    
    campaign_table = {
    "start_date": [data["start_date"] for data in campaign_data.values()],
    "end_date": [data["end_date"] for data in campaign_data.values()],
    "adin_id": list(campaign_data.keys()),
    "campaign": set(r.campaign_name for r in results),
    "effectiveness": [data["effectiveness"] for data in campaign_data.values()],
    "media": [data["media"] for data in campaign_data.values()],
    "creative": [data["creative"] for data in campaign_data.values()],
}

    response = schemas.CampaignResponse(
        campaignCard=schemas.CampaignCard(
            campaignName=results[0].campaign_name if campaign_id else "All",
            range=f"{formatted_start_date} - {formatted_end_date}",
            days=(end_date_obj - start_date_obj).days,
        ),
        performanceMetrics=schemas.PerformanceMetrics(
            currentMetrics=schemas.CurrentMetrics(**current_metrics)
        ),
        volumeUnitCostTrend=schemas.VolumeUnitCostTrend(
            impressionsCpm=schemas.ImpressionCPM(**impressions_cpm)
        ),
        campaignTable=schemas.CampaignTable(**campaign_table),
    )

    return response
