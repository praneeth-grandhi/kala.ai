#!/usr/bin/env python3
"""
Debug script to check poster database operations
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

async def check_database():
    """Check what's in the database"""
    mongo_url = os.environ.get('MONGO_URL')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'kala_ai')]
    
    print("🔍 Checking database contents...")
    
    # Check generated_posters collection
    posters_count = await db.generated_posters.count_documents({})
    print(f"📊 Generated posters count: {posters_count}")
    
    if posters_count > 0:
        print("\n📋 Sample posters:")
        async for poster in db.generated_posters.find().limit(3):
            print(f"   ID: {poster.get('id', 'NO_ID')}")
            print(f"   _id: {poster.get('_id', 'NO_MONGO_ID')}")
            print(f"   Session: {poster.get('session_id', 'NO_SESSION')}")
            print(f"   Created: {poster.get('created_at', 'NO_DATE')}")
            print("   ---")
    
    # Check chat_messages collection
    messages_count = await db.chat_messages.count_documents({})
    print(f"\n📊 Chat messages count: {messages_count}")
    
    # Check enhanced_prompts collection
    prompts_count = await db.enhanced_prompts.count_documents({})
    print(f"📊 Enhanced prompts count: {prompts_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_database())