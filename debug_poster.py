#!/usr/bin/env python3
"""
Debug poster retrieval
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

async def debug_poster_retrieval():
    """Debug poster retrieval"""
    mongo_url = os.environ.get('MONGO_URL')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'kala_ai')]
    
    poster_id = "de8796cd-37b5-49ab-a127-6546688933d3"
    
    print(f"🔍 Looking for poster with ID: {poster_id}")
    
    # Try different query methods
    poster1 = await db.generated_posters.find_one({"id": poster_id})
    print(f"Query by 'id' field: {poster1 is not None}")
    
    poster2 = await db.generated_posters.find_one({"_id": poster_id})
    print(f"Query by '_id' field: {poster2 is not None}")
    
    # Show all posters with their ID fields
    print("\n📋 All posters and their ID fields:")
    async for poster in db.generated_posters.find():
        print(f"   id: {poster.get('id')}")
        print(f"   _id: {poster.get('_id')}")
        print(f"   type(id): {type(poster.get('id'))}")
        print(f"   type(_id): {type(poster.get('_id'))}")
        print("   ---")
        break  # Just show first one
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_poster_retrieval())