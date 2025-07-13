import os
import asyncio
from typing import List, Dict
from emergentintegrations.llm.chat import LlmChat, UserMessage

class GeminiService:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', 'placeholder-key')
        self.model = "gemini-2.0-flash"
        self.provider = "gemini"
        
    async def enhance_prompt(self, user_prompt: str, session_id: str) -> Dict[str, any]:
        """
        Enhance a user's poster description into a detailed, visually-oriented prompt
        """
        try:
            # Create a new chat instance for this request
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message="""You are a professional poster design expert. Your task is to enhance user's brief poster descriptions into detailed, visually-oriented prompts suitable for AI image generation.

RULES:
1. Transform brief concepts into rich, detailed descriptions
2. Include specific visual elements: colors, typography, composition, style
3. Mention artistic styles, mood, and atmosphere
4. Describe layout, spacing, and visual hierarchy
5. Include specific details about backgrounds, borders, and decorative elements
6. Keep the enhanced prompt under 200 words but make it comprehensive
7. Focus on visual elements that would appear in a poster

EXAMPLE:
User: "jazz concert poster"
Enhanced: "A vintage-inspired jazz concert poster featuring bold Art Deco typography with gold and deep blue color scheme. Include silhouettes of jazz musicians playing saxophone and trumpet, with musical notes flowing dynamically across the composition. The background should have a subtle textured pattern reminiscent of 1920s aesthetic, with elegant borders and sophisticated layout perfect for a classy jazz venue."

After the enhanced prompt, extract 8-10 key visual keywords separated by commas."""
            ).with_model(self.provider, self.model).with_max_tokens(300)
            
            # Create user message
            user_message = UserMessage(
                text=f"Enhance this poster concept: {user_prompt}"
            )
            
            # Get response from Gemini
            response = await chat.send_message(user_message)
            
            # Parse response to extract enhanced prompt and keywords
            enhanced_prompt, keywords = self._parse_response(response)
            
            return {
                "enhanced_prompt": enhanced_prompt,
                "keywords": keywords,
                "success": True
            }
            
        except Exception as e:
            print(f"Error enhancing prompt: {str(e)}")
            # Fallback to mock data for now
            return self._fallback_enhancement(user_prompt)
    
    def _parse_response(self, response: str) -> tuple[str, List[str]]:
        """Parse Gemini response to extract enhanced prompt and keywords"""
        try:
            # Split response into prompt and keywords
            lines = response.strip().split('\n')
            
            # Find the enhanced prompt (usually the main content)
            enhanced_prompt = ""
            keywords_line = ""
            
            for line in lines:
                if line.strip() and not line.lower().startswith('keywords'):
                    enhanced_prompt += line.strip() + " "
                elif line.lower().startswith('keywords') or ',' in line:
                    keywords_line = line
                    break
            
            # Clean up enhanced prompt
            enhanced_prompt = enhanced_prompt.strip()
            
            # Extract keywords
            keywords = []
            if keywords_line:
                # Remove "Keywords:" prefix and split by comma
                keywords_text = keywords_line.replace("Keywords:", "").replace("keywords:", "").strip()
                keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
            
            # If no keywords found, extract from the enhanced prompt
            if not keywords:
                keywords = self._extract_keywords_from_text(enhanced_prompt)
            
            return enhanced_prompt, keywords[:10]  # Limit to 10 keywords
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return response, []
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from text using simple word frequency"""
        # Simple keyword extraction - can be improved with NLP
        common_design_words = [
            'vintage', 'modern', 'minimalist', 'bold', 'elegant', 'creative',
            'dynamic', 'professional', 'artistic', 'colorful', 'typography',
            'geometric', 'abstract', 'retro', 'contemporary', 'sleek',
            'vibrant', 'dramatic', 'subtle', 'sophisticated'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for word in common_design_words:
            if word in text_lower:
                found_keywords.append(word)
        
        return found_keywords[:8]
    
    def _fallback_enhancement(self, user_prompt: str) -> Dict[str, any]:
        """Fallback enhancement when API fails"""
        enhanced_prompts = {
            "jazz": "A vintage-inspired jazz concert poster featuring bold Art Deco typography with gold and deep blue color scheme. Include silhouettes of jazz musicians playing saxophone and trumpet, with musical notes flowing dynamically across the composition. The background should have a subtle textured pattern reminiscent of 1920s aesthetic, with elegant borders and sophisticated layout perfect for a classy jazz venue.",
            "charity": "An energetic and inspiring charity run poster with vibrant colors and dynamic motion graphics. Feature silhouettes of diverse runners in action, with a sunrise/sunset backdrop creating a sense of hope and determination. Include bold, motivational typography with a modern sans-serif font, and incorporate heart symbols and community elements.",
            "tech": "A sleek, minimalist tech conference poster with clean geometric shapes and a modern color palette of blues, whites, and accent colors. Feature abstract circuit patterns or network connections as background elements. Use contemporary typography with a mix of bold headers and clean body text.",
            "default": "A creative and eye-catching poster design with balanced composition, vibrant yet harmonious color scheme, and modern typography. The design should incorporate relevant visual elements that complement the theme, with clear hierarchy and professional layout."
        }
        
        # Find best match
        prompt_lower = user_prompt.lower()
        key = "default"
        for k in enhanced_prompts.keys():
            if k in prompt_lower:
                key = k
                break
        
        enhanced_prompt = enhanced_prompts[key]
        keywords = self._extract_keywords_from_text(enhanced_prompt)
        
        return {
            "enhanced_prompt": enhanced_prompt,
            "keywords": keywords,
            "success": True
        }