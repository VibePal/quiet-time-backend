from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, List


class SongSchema(BaseModel):
    title: str = Field(..., min_length=1)
    youtubeId: str = Field(..., min_length=1)


class ScriptureSchema(BaseModel):
    reference: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class PrayerSchema(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class QuietTimeEntryCreate(BaseModel):
    song: SongSchema
    scripture: ScriptureSchema
    prayer: PrayerSchema


class QuietTimeEntryResponse(BaseModel):
    id: str
    song: SongSchema
    scripture: ScriptureSchema
    prayer: PrayerSchema
    createdAt: str
    updatedAt: Optional[str] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    username: str


class LoginData(BaseModel):
    token: str
    user: UserResponse


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

