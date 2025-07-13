#!/usr/bin/env python3
"""
Debug poster ID flow
"""

import asyncio
import aiohttp
import json
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

async def debug_poster_flow():
    """Debug the full poster creation and retrieval flow"""
    session_id = str(uuid.uuid4())
    
    async with aiohttp.ClientSession() as session:
        print("🔄 Step 1: Enhance prompt")
        async with session.post(
            f"{API_BASE_URL}/poster/enhance-prompt",
            json={
                "user_prompt": "debug test poster",
                "session_id": session_id
            }
        ) as response:
            if response.status == 200:
                enhanced_data = await response.json()
                print(f"✅ Enhanced prompt created")
            else:
                print(f"❌ Failed to enhance prompt: {response.status}")
                return
        
        print("\n🔄 Step 2: Generate poster")
        async with session.post(
            f"{API_BASE_URL}/poster/generate",
            json={
                "enhanced_prompt": enhanced_data["enhanced_prompt"],
                "session_id": session_id,
                "user_prompt": "debug test poster",
                "keywords": enhanced_data["keywords"]
            }
        ) as response:
            if response.status == 200:
                poster_data = await response.json()
                poster_id = poster_data["id"]
                print(f"✅ Poster generated with ID: {poster_id}")
            else:
                print(f"❌ Failed to generate poster: {response.status}")
                return
        
        print(f"\n🔄 Step 3: Retrieve poster by ID: {poster_id}")
        async with session.get(
            f"{API_BASE_URL}/poster/{poster_id}"
        ) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                retrieved_data = await response.json()
                print(f"✅ Successfully retrieved poster: {retrieved_data.get('id')}")
            else:
                text = await response.text()
                print(f"❌ Failed to retrieve poster: {text}")
        
        print(f"\n🔄 Step 4: Delete poster by ID: {poster_id}")
        async with session.delete(
            f"{API_BASE_URL}/poster/{poster_id}"
        ) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                delete_data = await response.json()
                print(f"✅ Successfully deleted poster: {delete_data}")
            else:
                text = await response.text()
                print(f"❌ Failed to delete poster: {text}")

if __name__ == "__main__":
    asyncio.run(debug_poster_flow())