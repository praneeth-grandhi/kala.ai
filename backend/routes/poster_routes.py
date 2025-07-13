from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
import uuid

from models.poster import (
    PosterRequest, EnhancedPrompt, GeneratedPoster, 
    ChatMessage, LogoData
)
from services.gemini_service import GeminiService
from services.imagen_service import ImagenService
from database import get_database

router = APIRouter(prefix="/poster", tags=["poster"])

# Initialize services
gemini_service = GeminiService()
imagen_service = ImagenService()

@router.post("/enhance-prompt")
async def enhance_prompt(request: dict):
    """
    Enhance a user's poster prompt using Gemini AI
    """
    try:
        user_prompt = request.get("user_prompt")
        session_id = request.get("session_id", str(uuid.uuid4()))
        
        if not user_prompt:
            raise HTTPException(status_code=400, detail="user_prompt is required")
        
        # Enhance prompt using Gemini
        result = await gemini_service.enhance_prompt(user_prompt, session_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail="Failed to enhance prompt")
        
        # Create enhanced prompt object
        enhanced_prompt = EnhancedPrompt(
            original_prompt=user_prompt,
            enhanced_prompt=result["enhanced_prompt"],
            keywords=result["keywords"],
            session_id=session_id
        )
        
        # Save to database
        db = get_database()
        await db.enhanced_prompts.insert_one(enhanced_prompt.dict())
        
        # Save chat message
        user_message = ChatMessage(
            session_id=session_id,
            message_type="user",
            content=user_prompt
        )
        
        ai_message = ChatMessage(
            session_id=session_id,
            message_type="ai",
            content=result["enhanced_prompt"],
            keywords=result["keywords"]
        )
        
        await db.chat_messages.insert_one(user_message.dict())
        await db.chat_messages.insert_one(ai_message.dict())
        
        return {
            "enhanced_prompt": result["enhanced_prompt"],
            "keywords": result["keywords"],
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"Error in enhance_prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_poster(request: dict):
    """
    Generate a poster using Imagen 4
    """
    try:
        enhanced_prompt = request.get("enhanced_prompt")
        session_id = request.get("session_id")
        user_prompt = request.get("user_prompt", "")
        keywords = request.get("keywords", [])
        logo_data = request.get("logo")
        logo_position = request.get("logo_position")
        
        if not enhanced_prompt:
            raise HTTPException(status_code=400, detail="enhanced_prompt is required")
        
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")
        
        # Generate poster using Imagen 4
        result = await imagen_service.generate_poster(
            enhanced_prompt, 
            logo_data, 
            logo_position
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail="Failed to generate poster")
        
        # Create poster object
        poster = GeneratedPoster(
            user_prompt=user_prompt,
            enhanced_prompt=enhanced_prompt,
            keywords=keywords,
            logo=LogoData(**logo_data) if logo_data else None,
            logo_position=logo_position,
            poster_image=result["image_base64"],
            style=result["style"],
            dimensions=result["dimensions"],
            session_id=session_id
        )
        
        # Save to database
        db = get_database()
        await db.generated_posters.insert_one(poster.dict())
        
        return {
            "id": poster.id,
            "poster_image": result["image_base64"],
            "style": result["style"],
            "dimensions": result["dimensions"],
            "created_at": poster.created_at.isoformat()
        }
        
    except Exception as e:
        print(f"Error in generate_poster: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_poster_history(session_id: str):
    """
    Get poster generation history for a session
    """
    try:
        db = get_database()
        
        # Get generated posters
        posters_cursor = db.generated_posters.find({"session_id": session_id})
        posters = []
        async for poster in posters_cursor:
            poster['_id'] = str(poster['_id'])
            posters.append(poster)
        
        # Get chat messages
        messages_cursor = db.chat_messages.find({"session_id": session_id})
        messages = []
        async for message in messages_cursor:
            message['_id'] = str(message['_id'])
            messages.append(message)
        
        return {
            "posters": posters,
            "messages": messages
        }
        
    except Exception as e:
        print(f"Error in get_poster_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/poster/{poster_id}")
async def get_poster(poster_id: str):
    """
    Get a specific poster by ID
    """
    try:
        db = get_database()
        poster = await db.generated_posters.find_one({"id": poster_id})
        
        if not poster:
            raise HTTPException(status_code=404, detail="Poster not found")
        
        poster['_id'] = str(poster['_id'])
        return poster
        
    except Exception as e:
        print(f"Error in get_poster: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/poster/{poster_id}")
async def delete_poster(poster_id: str):
    """
    Delete a poster by ID
    """
    try:
        db = get_database()
        result = await db.generated_posters.delete_one({"id": poster_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Poster not found")
        
        return {"message": "Poster deleted successfully"}
        
    except Exception as e:
        print(f"Error in delete_poster: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))