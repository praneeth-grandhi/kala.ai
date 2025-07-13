import os
import base64
from typing import Optional, Dict
from PIL import Image, ImageDraw, ImageFont
import io
import requests

class ImagenService:
    def __init__(self):
        self.service_account_key = os.environ.get('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY', 'placeholder-key')
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID', 'placeholder-project')
        self.region = "us-central1"
        
    async def generate_poster(self, enhanced_prompt: str, logo_data: Optional[dict] = None, logo_position: Optional[str] = None) -> Dict[str, any]:
        """
        Generate a poster using Imagen 4 API
        """
        try:
            # For now, use placeholder images until real API keys are provided
            if self.service_account_key == 'placeholder-key':
                return await self._generate_placeholder_poster(enhanced_prompt, logo_data, logo_position)
            
            # TODO: Implement real Imagen 4 API call
            # This would include:
            # 1. Setting up Google Cloud authentication
            # 2. Making API call to Vertex AI Imagen 4 endpoint
            # 3. Processing the response
            # 4. Adding logo overlay if provided
            
            return await self._generate_placeholder_poster(enhanced_prompt, logo_data, logo_position)
            
        except Exception as e:
            print(f"Error generating poster: {str(e)}")
            return await self._generate_placeholder_poster(enhanced_prompt, logo_data, logo_position)
    
    async def _generate_placeholder_poster(self, enhanced_prompt: str, logo_data: Optional[dict] = None, logo_position: Optional[str] = None) -> Dict[str, any]:
        """
        Generate a placeholder poster for testing
        """
        try:
            # Create a gradient background poster
            width, height = 800, 1200
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Create gradient background
            for y in range(height):
                # Purple to cyan gradient
                r = int(147 + (64 - 147) * y / height)  # 147 to 64
                g = int(51 + (224 - 51) * y / height)   # 51 to 224
                b = int(234 + (208 - 234) * y / height) # 234 to 208
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add some design elements
            # Central rectangle
            rect_width, rect_height = 600, 400
            rect_x = (width - rect_width) // 2
            rect_y = (height - rect_height) // 2
            
            # Semi-transparent overlay
            overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [rect_x, rect_y, rect_x + rect_width, rect_y + rect_height],
                fill=(255, 255, 255, 180)
            )
            
            # Composite the overlay
            image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
            draw = ImageDraw.Draw(image)
            
            # Add text (simplified - would need proper font handling)
            try:
                # Try to use a nice font if available
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Add title
            title_text = "AI Generated Poster"
            title_bbox = draw.textbbox((0, 0), title_text, font=font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            title_y = rect_y + 50
            
            draw.text((title_x, title_y), title_text, fill=(50, 50, 50), font=font)
            
            # Add description
            desc_lines = self._wrap_text(enhanced_prompt[:100] + "...", 50)
            desc_y = title_y + 80
            
            for line in desc_lines[:3]:  # Max 3 lines
                line_bbox = draw.textbbox((0, 0), line, font=small_font)
                line_width = line_bbox[2] - line_bbox[0]
                line_x = (width - line_width) // 2
                draw.text((line_x, desc_y), line, fill=(80, 80, 80), font=small_font)
                desc_y += 30
            
            # Add logo if provided
            if logo_data and logo_position:
                image = self._add_logo_to_image(image, logo_data, logo_position)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "image_base64": f"data:image/png;base64,{img_base64}",
                "style": self._determine_style(enhanced_prompt),
                "dimensions": "800x1200",
                "success": True
            }
            
        except Exception as e:
            print(f"Error generating placeholder poster: {str(e)}")
            return {
                "image_base64": self._get_fallback_image(),
                "style": "Modern",
                "dimensions": "400x600",
                "success": False
            }
    
    def _add_logo_to_image(self, image: Image.Image, logo_data: dict, position: str) -> Image.Image:
        """Add logo to the poster image at specified position"""
        try:
            # Decode logo from base64
            logo_base64 = logo_data['base64'].split(',')[1] if ',' in logo_data['base64'] else logo_data['base64']
            logo_bytes = base64.b64decode(logo_base64)
            logo_image = Image.open(io.BytesIO(logo_bytes))
            
            # Convert to RGBA if needed
            if logo_image.mode != 'RGBA':
                logo_image = logo_image.convert('RGBA')
            
            # Resize logo to reasonable size
            logo_size = 80
            logo_image = logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calculate position
            img_width, img_height = image.size
            margin = 20
            
            positions = {
                'top-left': (margin, margin),
                'top-right': (img_width - logo_size - margin, margin),
                'top-center': ((img_width - logo_size) // 2, margin),
                'bottom-left': (margin, img_height - logo_size - margin),
                'bottom-right': (img_width - logo_size - margin, img_height - logo_size - margin),
                'bottom-center': ((img_width - logo_size) // 2, img_height - logo_size - margin),
            }
            
            logo_pos = positions.get(position, positions['top-right'])
            
            # Create a new image with logo
            result = image.copy()
            result.paste(logo_image, logo_pos, logo_image)
            
            return result
            
        except Exception as e:
            print(f"Error adding logo: {str(e)}")
            return image
    
    def _wrap_text(self, text: str, width: int) -> list:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _determine_style(self, prompt: str) -> str:
        """Determine style based on prompt content"""
        prompt_lower = prompt.lower()
        
        if 'vintage' in prompt_lower or 'retro' in prompt_lower:
            return "Vintage Retro"
        elif 'modern' in prompt_lower or 'contemporary' in prompt_lower:
            return "Modern Contemporary"
        elif 'minimalist' in prompt_lower or 'clean' in prompt_lower:
            return "Minimalist Clean"
        elif 'art deco' in prompt_lower or 'elegant' in prompt_lower:
            return "Art Deco Elegant"
        else:
            return "Creative Modern"
    
    def _get_fallback_image(self) -> str:
        """Get a fallback image URL"""
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgdmlld0JveD0iMCAwIDQwMCA2MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iNjAwIiBmaWxsPSJsaW5lYXItZ3JhZGllbnQoNDVkZWcsICM5MzMzZWEsICMwZjE0MTkpIi8+Cjx0ZXh0IHg9IjIwMCIgeT0iMzAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSIyNCI+QUkgUG9zdGVyPC90ZXh0Pgo8L3N2Zz4K"