# app/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Union
from datetime import date


from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class CampaignQueryParams(BaseModel):
    campaign_id: Optional[str]
    start_date: str
    end_date: str

    # Field-level validation
    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date '{value}' is not in the required format 'YYYY-MM-DD'.")
        return value


# Campaign Card Information
class CampaignCard(BaseModel):
    campaignName: str  # Campaign Name
    range: str  # Campaign Start and End Date
    days: int  # Total days between start and end date


# Performance Metrics
class CurrentMetrics(BaseModel):
    impressions: int  # Total number of impressions
    clicks: int  # Total number of clicks
    views: int  # Total number of views


class PerformanceMetrics(BaseModel):
    currentMetrics: CurrentMetrics  # Nested Current Metrics


# Volume Unit Cost Trends
class ImpressionCPM(BaseModel):
    impression: Dict[str, int]  # Daily impressions (date -> value mapping)
    cpm: Dict[str, float]  # Daily CPMs (date -> value mapping)


class VolumeUnitCostTrend(BaseModel):
    impressionsCpm: ImpressionCPM  # Trends for impressions and CPM


# Campaign Table
class CampaignTable(BaseModel):
    start_date: List[str]  # Start dates for each campaign
    end_date: List[str]  # End dates for each campaign
    adin_id: List[str]  # Campaign IDs
    campaign: List[str]  # Campaign names
    effectiveness: List[float]  # Effectiveness scores
    media: List[int]  # Media scores
    creative: List[float]  # Creative scores


# Final Response Schema
class CampaignResponse(BaseModel):
    campaignCard: CampaignCard
    performanceMetrics: PerformanceMetrics
    volumeUnitCostTrend: VolumeUnitCostTrend
    campaignTable: CampaignTable

    class Config:
        json_schema_extra = {
            "example": {
                "campaignCard": {
                    "campaignName": "Crypto Analysis",
                    "range": "20 Mar - 30 Dec",
                    "days": 5399
                },
                "performanceMetrics": {
                    "currentMetrics": {
                        "impressions": 39531680,
                        "clicks": 446806,
                        "views": 1891950
                    }
                },
                "volumeUnitCostTrend": {
                    "impressionsCpm": {
                        "impression": {
                            "2023-03-20": 6167,
                            "2023-03-21": 8439,
                            # ...
                        },
                        "cpm": {
                            "2023-03-20": 315.43,
                            "2023-03-21": 249.44,
                            # ...
                        }
                    }
                },
                "campaignTable": {
                    "start_date": ["2023-03-20", "2022-12-29"],
                    "end_date": ["2037-12-30", "2023-01-29"],
                    "adin_id": ["36963290188b", "f9bedbbf3c17d"],
                    "campaign": ["Crypto Analysis", "Future Vision"],
                    "effectiveness": [50, 77],
                    "media": [50, 88],
                    "creative": [64, 54]
                }
            }
        }
