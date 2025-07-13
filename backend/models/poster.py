from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class LogoData(BaseModel):
    name: str
    size: int
    preview: str  # base64 encoded image
    base64: str   # base64 encoded image
    position: Optional[str] = None

class PosterRequest(BaseModel):
    user_prompt: str
    session_id: str
    logo: Optional[LogoData] = None
    logo_position: Optional[str] = None

class EnhancedPrompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_prompt: str
    enhanced_prompt: str
    keywords: List[str]
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GeneratedPoster(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_prompt: str
    enhanced_prompt: str
    keywords: List[str]
    logo: Optional[LogoData] = None
    logo_position: Optional[str] = None
    poster_image: str  # base64 encoded image
    style: str
    dimensions: str
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    message_type: str  # 'user', 'ai', 'system'
    content: str
    keywords: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PosterHistory(BaseModel):
    session_id: str
    posters: List[GeneratedPoster]
    messages: List[ChatMessage]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)