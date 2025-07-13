#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Kala.ai Poster Generation App
Tests all API endpoints, services, and database operations
"""

import asyncio
import aiohttp
import json
import base64
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.test_session_id = str(uuid.uuid4())
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup(self):
        """Cleanup test session"""
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.test_results['passed'] += 1
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
            
    async def test_server_health(self):
        """Test basic server health"""
        try:
            async with self.session.get(f"{API_BASE_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_result("Server Health Check", True, f"Server is running: {data.get('message')}")
                    return True
                else:
                    self.log_result("Server Health Check", False, f"Server returned status {response.status}")
                    return False
        except Exception as e:
            self.log_result("Server Health Check", False, f"Connection error: {str(e)}")
            return False
            
    async def test_enhance_prompt_endpoint(self):
        """Test POST /api/poster/enhance-prompt"""
        test_cases = [
            {
                "name": "Valid jazz concert prompt",
                "payload": {
                    "user_prompt": "jazz concert poster",
                    "session_id": self.test_session_id
                },
                "should_pass": True
            },
            {
                "name": "Valid charity run prompt",
                "payload": {
                    "user_prompt": "charity run event poster for community fundraising",
                    "session_id": self.test_session_id
                },
                "should_pass": True
            },
            {
                "name": "Missing user_prompt",
                "payload": {
                    "session_id": self.test_session_id
                },
                "should_pass": False
            },
            {
                "name": "Empty user_prompt",
                "payload": {
                    "user_prompt": "",
                    "session_id": self.test_session_id
                },
                "should_pass": False
            }
        ]
        
        for test_case in test_cases:
            try:
                async with self.session.post(
                    f"{API_BASE_URL}/poster/enhance-prompt",
                    json=test_case["payload"]
                ) as response:
                    
                    if test_case["should_pass"]:
                        if response.status == 200:
                            data = await response.json()
                            required_fields = ["enhanced_prompt", "keywords", "session_id"]
                            
                            if all(field in data for field in required_fields):
                                self.log_result(
                                    f"Enhance Prompt - {test_case['name']}", 
                                    True, 
                                    f"Enhanced prompt generated with {len(data['keywords'])} keywords"
                                )
                            else:
                                missing = [f for f in required_fields if f not in data]
                                self.log_result(
                                    f"Enhance Prompt - {test_case['name']}", 
                                    False, 
                                    f"Missing fields: {missing}"
                                )
                        else:
                            self.log_result(
                                f"Enhance Prompt - {test_case['name']}", 
                                False, 
                                f"Expected 200, got {response.status}"
                            )
                    else:
                        # Should fail
                        if response.status == 400:
                            self.log_result(
                                f"Enhance Prompt - {test_case['name']}", 
                                True, 
                                "Correctly rejected invalid request"
                            )
                        else:
                            self.log_result(
                                f"Enhance Prompt - {test_case['name']}", 
                                False, 
                                f"Expected 400, got {response.status}"
                            )
                            
            except Exception as e:
                self.log_result(
                    f"Enhance Prompt - {test_case['name']}", 
                    False, 
                    f"Exception: {str(e)}"
                )
                
    async def test_generate_poster_endpoint(self):
        """Test POST /api/poster/generate"""
        # First get an enhanced prompt
        enhanced_prompt_data = None
        try:
            async with self.session.post(
                f"{API_BASE_URL}/poster/enhance-prompt",
                json={
                    "user_prompt": "tech conference poster",
                    "session_id": self.test_session_id
                }
            ) as response:
                if response.status == 200:
                    enhanced_prompt_data = await response.json()
        except:
            pass
            
        if not enhanced_prompt_data:
            self.log_result("Generate Poster - Setup", False, "Could not get enhanced prompt for testing")
            return
            
        # Create test logo data
        test_logo_data = {
            "name": "test-logo.png",
            "size": 1024,
            "preview": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }
        
        test_cases = [
            {
                "name": "Valid poster generation without logo",
                "payload": {
                    "enhanced_prompt": enhanced_prompt_data["enhanced_prompt"],
                    "session_id": self.test_session_id,
                    "user_prompt": "tech conference poster",
                    "keywords": enhanced_prompt_data["keywords"]
                },
                "should_pass": True
            },
            {
                "name": "Valid poster generation with logo",
                "payload": {
                    "enhanced_prompt": enhanced_prompt_data["enhanced_prompt"],
                    "session_id": self.test_session_id,
                    "user_prompt": "tech conference poster",
                    "keywords": enhanced_prompt_data["keywords"],
                    "logo": test_logo_data,
                    "logo_position": "top-right"
                },
                "should_pass": True
            },
            {
                "name": "Missing enhanced_prompt",
                "payload": {
                    "session_id": self.test_session_id
                },
                "should_pass": False
            },
            {
                "name": "Missing session_id",
                "payload": {
                    "enhanced_prompt": enhanced_prompt_data["enhanced_prompt"]
                },
                "should_pass": False
            }
        ]
        
        for test_case in test_cases:
            try:
                async with self.session.post(
                    f"{API_BASE_URL}/poster/generate",
                    json=test_case["payload"]
                ) as response:
                    
                    if test_case["should_pass"]:
                        if response.status == 200:
                            data = await response.json()
                            required_fields = ["id", "poster_image", "style", "dimensions", "created_at"]
                            
                            if all(field in data for field in required_fields):
                                # Verify poster_image is base64
                                if data["poster_image"].startswith("data:image/"):
                                    self.log_result(
                                        f"Generate Poster - {test_case['name']}", 
                                        True, 
                                        f"Poster generated with style: {data['style']}"
                                    )
                                else:
                                    self.log_result(
                                        f"Generate Poster - {test_case['name']}", 
                                        False, 
                                        "Invalid poster image format"
                                    )
                            else:
                                missing = [f for f in required_fields if f not in data]
                                self.log_result(
                                    f"Generate Poster - {test_case['name']}", 
                                    False, 
                                    f"Missing fields: {missing}"
                                )
                        else:
                            self.log_result(
                                f"Generate Poster - {test_case['name']}", 
                                False, 
                                f"Expected 200, got {response.status}"
                            )
                    else:
                        # Should fail
                        if response.status == 400:
                            self.log_result(
                                f"Generate Poster - {test_case['name']}", 
                                True, 
                                "Correctly rejected invalid request"
                            )
                        else:
                            self.log_result(
                                f"Generate Poster - {test_case['name']}", 
                                False, 
                                f"Expected 400, got {response.status}"
                            )
                            
            except Exception as e:
                self.log_result(
                    f"Generate Poster - {test_case['name']}", 
                    False, 
                    f"Exception: {str(e)}"
                )
                
    async def test_history_endpoint(self):
        """Test GET /api/poster/history/{session_id}"""
        try:
            async with self.session.get(
                f"{API_BASE_URL}/poster/history/{self.test_session_id}"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    required_fields = ["posters", "messages"]
                    
                    if all(field in data for field in required_fields):
                        self.log_result(
                            "Get History", 
                            True, 
                            f"Retrieved {len(data['posters'])} posters and {len(data['messages'])} messages"
                        )
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_result(
                            "Get History", 
                            False, 
                            f"Missing fields: {missing}"
                        )
                else:
                    self.log_result(
                        "Get History", 
                        False, 
                        f"Expected 200, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Get History", False, f"Exception: {str(e)}")
            
    async def test_get_poster_endpoint(self):
        """Test GET /api/poster/{poster_id}"""
        # First generate a poster to get an ID
        poster_id = None
        try:
            # Get enhanced prompt first
            async with self.session.post(
                f"{API_BASE_URL}/poster/enhance-prompt",
                json={
                    "user_prompt": "music festival poster",
                    "session_id": self.test_session_id
                }
            ) as response:
                if response.status == 200:
                    enhanced_data = await response.json()
                    
                    # Generate poster
                    async with self.session.post(
                        f"{API_BASE_URL}/poster/generate",
                        json={
                            "enhanced_prompt": enhanced_data["enhanced_prompt"],
                            "session_id": self.test_session_id,
                            "user_prompt": "music festival poster",
                            "keywords": enhanced_data["keywords"]
                        }
                    ) as gen_response:
                        if gen_response.status == 200:
                            gen_data = await gen_response.json()
                            poster_id = gen_data["id"]
        except:
            pass
            
        if not poster_id:
            self.log_result("Get Poster - Setup", False, "Could not generate poster for testing")
            return
            
        # Test getting the poster
        try:
            async with self.session.get(
                f"{API_BASE_URL}/poster/{poster_id}"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "id" in data and data["id"] == poster_id:
                        self.log_result(
                            "Get Poster", 
                            True, 
                            f"Retrieved poster with ID: {poster_id}"
                        )
                    else:
                        self.log_result(
                            "Get Poster", 
                            False, 
                            "Poster ID mismatch"
                        )
                else:
                    self.log_result(
                        "Get Poster", 
                        False, 
                        f"Expected 200, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Get Poster", False, f"Exception: {str(e)}")
            
        # Test with non-existent poster ID
        try:
            fake_id = str(uuid.uuid4())
            async with self.session.get(
                f"{API_BASE_URL}/poster/{fake_id}"
            ) as response:
                
                if response.status == 404:
                    self.log_result(
                        "Get Poster - Non-existent", 
                        True, 
                        "Correctly returned 404 for non-existent poster"
                    )
                else:
                    self.log_result(
                        "Get Poster - Non-existent", 
                        False, 
                        f"Expected 404, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Get Poster - Non-existent", False, f"Exception: {str(e)}")
            
    async def test_delete_poster_endpoint(self):
        """Test DELETE /api/poster/{poster_id}"""
        # First generate a poster to delete
        poster_id = None
        try:
            # Get enhanced prompt first
            async with self.session.post(
                f"{API_BASE_URL}/poster/enhance-prompt",
                json={
                    "user_prompt": "art exhibition poster",
                    "session_id": self.test_session_id
                }
            ) as response:
                if response.status == 200:
                    enhanced_data = await response.json()
                    
                    # Generate poster
                    async with self.session.post(
                        f"{API_BASE_URL}/poster/generate",
                        json={
                            "enhanced_prompt": enhanced_data["enhanced_prompt"],
                            "session_id": self.test_session_id,
                            "user_prompt": "art exhibition poster",
                            "keywords": enhanced_data["keywords"]
                        }
                    ) as gen_response:
                        if gen_response.status == 200:
                            gen_data = await gen_response.json()
                            poster_id = gen_data["id"]
        except:
            pass
            
        if not poster_id:
            self.log_result("Delete Poster - Setup", False, "Could not generate poster for testing")
            return
            
        # Test deleting the poster
        try:
            async with self.session.delete(
                f"{API_BASE_URL}/poster/{poster_id}"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "message" in data:
                        self.log_result(
                            "Delete Poster", 
                            True, 
                            f"Successfully deleted poster: {poster_id}"
                        )
                    else:
                        self.log_result(
                            "Delete Poster", 
                            False, 
                            "Missing success message"
                        )
                else:
                    self.log_result(
                        "Delete Poster", 
                        False, 
                        f"Expected 200, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Delete Poster", False, f"Exception: {str(e)}")
            
        # Test deleting non-existent poster
        try:
            fake_id = str(uuid.uuid4())
            async with self.session.delete(
                f"{API_BASE_URL}/poster/{fake_id}"
            ) as response:
                
                if response.status == 404:
                    self.log_result(
                        "Delete Poster - Non-existent", 
                        True, 
                        "Correctly returned 404 for non-existent poster"
                    )
                else:
                    self.log_result(
                        "Delete Poster - Non-existent", 
                        False, 
                        f"Expected 404, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Delete Poster - Non-existent", False, f"Exception: {str(e)}")
            
    async def test_existing_status_endpoints(self):
        """Test existing status endpoints for compatibility"""
        try:
            # Test POST /api/status
            test_client = {
                "client_name": "test_client_kala_ai"
            }
            
            async with self.session.post(
                f"{API_BASE_URL}/status",
                json=test_client
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    required_fields = ["id", "client_name", "timestamp"]
                    
                    if all(field in data for field in required_fields):
                        self.log_result(
                            "Status Create", 
                            True, 
                            f"Created status check for: {data['client_name']}"
                        )
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_result(
                            "Status Create", 
                            False, 
                            f"Missing fields: {missing}"
                        )
                else:
                    self.log_result(
                        "Status Create", 
                        False, 
                        f"Expected 200, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Status Create", False, f"Exception: {str(e)}")
            
        try:
            # Test GET /api/status
            async with self.session.get(f"{API_BASE_URL}/status") as response:
                
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        self.log_result(
                            "Status List", 
                            True, 
                            f"Retrieved {len(data)} status checks"
                        )
                    else:
                        self.log_result(
                            "Status List", 
                            False, 
                            "Response is not a list"
                        )
                else:
                    self.log_result(
                        "Status List", 
                        False, 
                        f"Expected 200, got {response.status}"
                    )
                    
        except Exception as e:
            self.log_result("Status List", False, f"Exception: {str(e)}")
            
    async def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("🚀 Starting Kala.ai Backend API Tests")
        print(f"📍 Testing against: {API_BASE_URL}")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Test server health first
            server_healthy = await self.test_server_health()
            
            if not server_healthy:
                print("\n❌ Server is not healthy. Stopping tests.")
                return
                
            print("\n📋 Testing Poster API Endpoints...")
            await self.test_enhance_prompt_endpoint()
            await self.test_generate_poster_endpoint()
            await self.test_history_endpoint()
            await self.test_get_poster_endpoint()
            await self.test_delete_poster_endpoint()
            
            print("\n📋 Testing Existing Status Endpoints...")
            await self.test_existing_status_endpoints()
            
        finally:
            await self.cleanup()
            
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🔍 FAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
                
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if self.test_results['failed'] == 0:
            print("\n🎉 All tests passed! Backend is working correctly.")
        else:
            print(f"\n⚠️  {self.test_results['failed']} test(s) failed. Check the details above.")
            
        return self.test_results['failed'] == 0

async def main():
    """Main test runner"""
    tester = BackendTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)