// Mock data for AI prompt enhancement and poster generation
export const mockData = {
  // Mock AI prompt enhancement
  enhancePrompt: (userInput) => {
    const enhancedPrompts = {
      "jazz concert": {
        prompt: "A vintage-inspired jazz concert poster featuring bold Art Deco typography with gold and deep blue color scheme. Include silhouettes of jazz musicians playing saxophone and trumpet, with musical notes flowing dynamically across the composition. The background should have a subtle textured pattern reminiscent of 1920s aesthetic, with elegant borders and sophisticated layout perfect for a classy jazz venue.",
        keywords: ["Art Deco", "vintage", "jazz musicians", "saxophone", "trumpet", "musical notes", "1920s aesthetic", "gold accents", "deep blue", "elegant typography"]
      },
      "charity run": {
        prompt: "An energetic and inspiring charity run poster with vibrant colors and dynamic motion graphics. Feature silhouettes of diverse runners in action, with a sunrise/sunset backdrop creating a sense of hope and determination. Include bold, motivational typography with a modern sans-serif font, and incorporate heart symbols and community elements. The color palette should be uplifting with oranges, blues, and greens to convey positivity and health.",
        keywords: ["energetic", "inspiring", "runners silhouettes", "sunrise backdrop", "motivational", "heart symbols", "community", "vibrant colors", "modern typography", "health"]
      },
      "tech conference": {
        prompt: "A sleek, minimalist tech conference poster with clean geometric shapes and a modern color palette of blues, whites, and accent colors. Feature abstract circuit patterns or network connections as background elements. Use contemporary typography with a mix of bold headers and clean body text. Include subtle tech iconography like connected nodes or digital grid patterns, maintaining a professional and innovative aesthetic.",
        keywords: ["minimalist", "geometric shapes", "circuit patterns", "network connections", "contemporary typography", "tech iconography", "digital grid", "professional", "innovative", "modern"]
      },
      "default": {
        prompt: "A creative and eye-catching poster design with balanced composition, vibrant yet harmonious color scheme, and modern typography. The design should incorporate relevant visual elements that complement the theme, with clear hierarchy and professional layout. Include dynamic elements that draw attention while maintaining readability and visual appeal.",
        keywords: ["creative", "eye-catching", "balanced composition", "vibrant colors", "modern typography", "visual hierarchy", "professional layout", "dynamic elements", "readability"]
      }
    };

    // Find the best match or use default
    const key = Object.keys(enhancedPrompts).find(k => 
      userInput.toLowerCase().includes(k.toLowerCase())
    ) || "default";

    return enhancedPrompts[key];
  },

  // Mock poster generation
  generatePoster: (prompt, logo, position) => {
    // Generate a mock poster with placeholder image
    const posterStyles = [
      "Modern Minimalist",
      "Vintage Retro",
      "Contemporary Art",
      "Digital Futuristic",
      "Classic Elegant"
    ];

    const dimensions = [
      "1080x1350 (Instagram)",
      "1920x1080 (Landscape)",
      "1080x1920 (Portrait)",
      "2480x3508 (A4 Print)"
    ];

    const mockPosters = [
      "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400&h=600&fit=crop"
    ];

    return {
      id: Date.now(),
      image: mockPosters[Math.floor(Math.random() * mockPosters.length)],
      prompt: prompt,
      logo: logo,
      logoPosition: position,
      style: posterStyles[Math.floor(Math.random() * posterStyles.length)],
      dimensions: dimensions[Math.floor(Math.random() * dimensions.length)],
      timestamp: new Date().toLocaleString(),
      createdAt: new Date().toISOString()
    };
  },

  // Mock chat responses
  getChatResponse: (message) => {
    const responses = [
      "That's a great concept! Let me enhance that for you.",
      "Excellent idea! I'll create a detailed prompt for the AI.",
      "Perfect! I can see this becoming an amazing poster.",
      "Wonderful concept! Let me work on optimizing this prompt."
    ];

    return responses[Math.floor(Math.random() * responses.length)];
  },

  // Mock keywords extraction
  extractKeywords: (text) => {
    const keywords = [
      "modern", "vintage", "minimalist", "bold", "elegant", "creative",
      "dynamic", "professional", "artistic", "colorful", "typography",
      "geometric", "abstract", "retro", "contemporary", "sleek"
    ];

    return keywords
      .sort(() => 0.5 - Math.random())
      .slice(0, Math.floor(Math.random() * 5) + 3);
  }
};