from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models.chapter import Chapter, ChapterCreate, ChapterResponse
from utils.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ChapterResponse])
async def get_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all chapters
    """
    from models.chapter import Chapter
    chapters = db.query(Chapter).offset(skip).limit(limit).all()
    return chapters

@router.get("/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific chapter by ID
    """
    from models.chapter import Chapter
    
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return chapter

@router.post("/", response_model=ChapterResponse)
async def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):
    """
    Create a new chapter
    """
    from models.chapter import Chapter
    
    db_chapter = Chapter(**chapter.dict())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    
    return db_chapter

@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(chapter_id: int, chapter: ChapterCreate, db: Session = Depends(get_db)):
    """
    Update an existing chapter
    """
    from models.chapter import Chapter
    
    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    for field, value in chapter.dict().items():
        setattr(db_chapter, field, value)
    
    db.commit()
    db.refresh(db_chapter)
    
    return db_chapter

@router.delete("/{chapter_id}")
async def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """
    Delete a chapter
    """
    from models.chapter import Chapter
    
    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    db.delete(db_chapter)
    db.commit()
    
    return {"message": "Chapter deleted successfully"}
