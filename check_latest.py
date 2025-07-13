#!/usr/bin/env python3
"""
Check if the poster was actually saved
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

async def check_latest_poster():
    """Check the latest poster in database"""
    mongo_url = os.environ.get('MONGO_URL')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'kala_ai')]
    
    print("🔍 Latest posters in database:")
    
    # Get latest posters
    async for poster in db.generated_posters.find().sort("created_at", -1).limit(3):
        print(f"   ID: {poster.get('id')}")
        print(f"   Session: {poster.get('session_id')}")
        print(f"   Created: {poster.get('created_at')}")
        print("   ---")
    
    # Check specific ID
    target_id = "65f1068e-1eb5-4583-be4e-7d850524ce4f"
    poster = await db.generated_posters.find_one({"id": target_id})
    print(f"\n🎯 Poster with ID {target_id}: {'Found' if poster else 'Not Found'}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_latest_poster())