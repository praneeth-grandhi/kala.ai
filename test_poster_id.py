#!/usr/bin/env python3
"""
Test specific poster ID retrieval
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

async def test_specific_poster():
    """Test getting a specific poster that exists"""
    poster_id = "de8796cd-37b5-49ab-a127-6546688933d3"  # From database check
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/poster/{poster_id}") as response:
                print(f"Status: {response.status}")
                print(f"Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Success: Retrieved poster {data.get('id')}")
                else:
                    text = await response.text()
                    print(f"❌ Failed: {text}")
                    
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_specific_poster())