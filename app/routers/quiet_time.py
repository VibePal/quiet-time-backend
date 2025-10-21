from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    QuietTimeEntryCreate,
    QuietTimeEntryResponse,
    APIResponse,
    SongSchema,
    ScriptureSchema,
    PrayerSchema
)
from app.models import QuietTimeEntry, Admin
from app.auth import get_current_admin

router = APIRouter(prefix="/api/v1/quiet-time", tags=["quiet-time"])


@router.post("/entries", response_model=APIResponse, status_code=201)
async def create_entry(
    entry: QuietTimeEntryCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Create a new quiet time entry (Admin only)
    """
    # Validate all fields are present (Pydantic already does this, but we can add custom logic)
    if not all([
        entry.song.title,
        entry.song.youtubeId,
        entry.scripture.reference,
        entry.scripture.text,
        entry.prayer.title,
        entry.prayer.content
    ]):
        return APIResponse(
            success=False,
            message="Please fill in all fields",
            data=None
        )
    
    # Create new entry in database
    new_entry = QuietTimeEntry(
        song_title=entry.song.title,
        song_youtube_id=entry.song.youtubeId,
        scripture_reference=entry.scripture.reference,
        scripture_text=entry.scripture.text,
        prayer_title=entry.prayer.title,
        prayer_content=entry.prayer.content
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    # Format response
    response_data = QuietTimeEntryResponse(
        id=str(new_entry.id),
        song=SongSchema(
            title=new_entry.song_title,
            youtubeId=new_entry.song_youtube_id
        ),
        scripture=ScriptureSchema(
            reference=new_entry.scripture_reference,
            text=new_entry.scripture_text
        ),
        prayer=PrayerSchema(
            title=new_entry.prayer_title,
            content=new_entry.prayer_content
        ),
        createdAt=new_entry.created_at.isoformat(),
        updatedAt=new_entry.updated_at.isoformat() if new_entry.updated_at else None
    )
    
    return APIResponse(
        success=True,
        message="Quiet time entry added successfully",
        data=response_data
    )


@router.get("/entries/today", response_model=APIResponse)
async def get_todays_entry(db: Session = Depends(get_db)):
    """
    Get today's quiet time entry (Public - No authentication required)
    Rotates through all entries daily, cycling back to the beginning when reaching the end.
    """
    from datetime import datetime, timezone
    
    # Get all entries ordered by creation date (oldest first for consistent rotation)
    entries = db.query(QuietTimeEntry).order_by(QuietTimeEntry.created_at.asc()).all()
    
    if not entries:
        return APIResponse(
            success=True,
            message="No entries available",
            data=None
        )
    
    # Calculate which entry to show based on current date
    # Use a fixed reference date (e.g., January 1, 2025) for consistent daily rotation
    reference_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    current_date = datetime.now(timezone.utc)
    
    # Calculate days since reference date
    days_passed = (current_date - reference_date).days
    
    # Use modulo to cycle through entries
    entry_index = days_passed % len(entries)
    selected_entry = entries[entry_index]
    
    # Format the selected entry
    formatted_entry = QuietTimeEntryResponse(
        id=str(selected_entry.id),
        song=SongSchema(
            title=selected_entry.song_title,
            youtubeId=selected_entry.song_youtube_id
        ),
        scripture=ScriptureSchema(
            reference=selected_entry.scripture_reference,
            text=selected_entry.scripture_text
        ),
        prayer=PrayerSchema(
            title=selected_entry.prayer_title,
            content=selected_entry.prayer_content
        ),
        createdAt=selected_entry.created_at.isoformat(),
        updatedAt=selected_entry.updated_at.isoformat() if selected_entry.updated_at else None
    )
    
    return APIResponse(
        success=True,
        message="Today's entry retrieved successfully",
        data=formatted_entry
    )


@router.get("/entries", response_model=APIResponse)
async def get_all_entries(db: Session = Depends(get_db)):
    """
    Get all quiet time entries (Public - No authentication required)
    """
    entries = db.query(QuietTimeEntry).order_by(QuietTimeEntry.created_at.desc()).all()
    
    if not entries:
        return APIResponse(
            success=True,
            message="No entries available",
            data=[]
        )
    
    # Format all entries
    formatted_entries = []
    for entry in entries:
        formatted_entry = QuietTimeEntryResponse(
            id=str(entry.id),
            song=SongSchema(
                title=entry.song_title,
                youtubeId=entry.song_youtube_id
            ),
            scripture=ScriptureSchema(
                reference=entry.scripture_reference,
                text=entry.scripture_text
            ),
            prayer=PrayerSchema(
                title=entry.prayer_title,
                content=entry.prayer_content
            ),
            createdAt=entry.created_at.isoformat(),
            updatedAt=entry.updated_at.isoformat() if entry.updated_at else None
        )
        formatted_entries.append(formatted_entry)
    
    return APIResponse(
        success=True,
        message="Entries retrieved successfully",
        data=formatted_entries
    )


@router.patch("/entries/{entry_id}", response_model=APIResponse)
async def update_entry(
    entry_id: int,
    entry: QuietTimeEntryCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Update a quiet time entry (Admin only)
    """
    # Find the existing entry
    existing_entry = db.query(QuietTimeEntry).filter(QuietTimeEntry.id == entry_id).first()
    
    if not existing_entry:
        return APIResponse(
            success=False,
            message="Entry not found",
            data=None
        )
    
    # Validate all fields are present
    if not all([
        entry.song.title,
        entry.song.youtubeId,
        entry.scripture.reference,
        entry.scripture.text,
        entry.prayer.title,
        entry.prayer.content
    ]):
        return APIResponse(
            success=False,
            message="Please fill in all fields",
            data=None
        )
    
    # Update the entry
    existing_entry.song_title = entry.song.title
    existing_entry.song_youtube_id = entry.song.youtubeId
    existing_entry.scripture_reference = entry.scripture.reference
    existing_entry.scripture_text = entry.scripture.text
    existing_entry.prayer_title = entry.prayer.title
    existing_entry.prayer_content = entry.prayer.content
    
    db.commit()
    db.refresh(existing_entry)
    
    # Format response
    response_data = QuietTimeEntryResponse(
        id=str(existing_entry.id),
        song=SongSchema(
            title=existing_entry.song_title,
            youtubeId=existing_entry.song_youtube_id
        ),
        scripture=ScriptureSchema(
            reference=existing_entry.scripture_reference,
            text=existing_entry.scripture_text
        ),
        prayer=PrayerSchema(
            title=existing_entry.prayer_title,
            content=existing_entry.prayer_content
        ),
        createdAt=existing_entry.created_at.isoformat(),
        updatedAt=existing_entry.updated_at.isoformat() if existing_entry.updated_at else None
    )
    
    return APIResponse(
        success=True,
        message="Entry updated successfully",
        data=response_data
    )


@router.delete("/entries/{entry_id}", response_model=APIResponse)
async def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Delete a quiet time entry (Admin only)
    """
    entry = db.query(QuietTimeEntry).filter(QuietTimeEntry.id == entry_id).first()
    
    if not entry:
        return APIResponse(
            success=False,
            message="Entry not found",
            data=None
        )
    
    db.delete(entry)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Entry removed successfully",
        data=None
    )


@router.get("/entries/rotation/days-remaining", response_model=APIResponse)
async def get_days_remaining_in_cycle(db: Session = Depends(get_db)):
    """
    Get the number of days remaining in the current rotation cycle before it loops back to the beginning.
    Public endpoint - No authentication required.
    """
    from datetime import datetime, timezone
    
    # Get all entries ordered by creation date (same as rotation logic)
    entries = db.query(QuietTimeEntry).order_by(QuietTimeEntry.created_at.asc()).all()
    
    if not entries:
        return APIResponse(
            success=True,
            message="No entries available",
            data={"days_remaining": 0, "total_entries": 0, "current_position": 0}
        )
    
    # Use the same reference date and calculation as the rotation logic
    reference_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    current_date = datetime.now(timezone.utc)
    days_passed = (current_date - reference_date).days
    
    # Calculate current position in the cycle (0-based)
    current_position = days_passed % len(entries)
    
    # Calculate days remaining until the cycle completes
    days_remaining = len(entries) - current_position - 1
    
    # If we're at the last entry, next cycle starts tomorrow
    if current_position == len(entries) - 1:
        days_remaining = 0
    
    return APIResponse(
        success=True,
        message="Days remaining in current cycle retrieved successfully",
        data={
            "days_remaining": days_remaining,
            "total_entries": len(entries),
            "current_position": current_position,
            "next_cycle_starts_in": days_remaining + 1
        }
    )


@router.get("/entries/rotation/entries-remaining", response_model=APIResponse)
async def get_entries_remaining_in_cycle(db: Session = Depends(get_db)):
    """
    Get the number of entries remaining in the current rotation cycle before it starts over.
    Public endpoint - No authentication required.
    """
    from datetime import datetime, timezone
    
    # Get all entries ordered by creation date (same as rotation logic)
    entries = db.query(QuietTimeEntry).order_by(QuietTimeEntry.created_at.asc()).all()
    
    if not entries:
        return APIResponse(
            success=True,
            message="No entries available",
            data={
                "entries_remaining": 0,
                "total_entries": 0,
                "current_position": 0
            }
        )
    
    # Use the same reference date and calculation as the rotation logic
    reference_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    current_date = datetime.now(timezone.utc)
    days_passed = (current_date - reference_date).days
    
    # Calculate current position in the cycle (0-based)
    current_position = days_passed % len(entries)
    
    # Calculate entries remaining until the cycle completes
    entries_remaining = len(entries) - current_position - 1
    
    # If we're at the last entry, no entries remaining
    if current_position == len(entries) - 1:
        entries_remaining = 0
    
    return APIResponse(
        success=True,
        message="Entries remaining in current cycle retrieved successfully",
        data={
            "entries_remaining": entries_remaining,
            "total_entries": len(entries),
            "current_position": current_position,
            "is_last_entry": current_position == len(entries) - 1
        }
    )