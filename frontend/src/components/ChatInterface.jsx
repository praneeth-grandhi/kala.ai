import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Send, RefreshCw, Upload, Download, Sparkles, Wand2 } from "lucide-react";
import { toast } from "sonner";
import LogoUpload from "./LogoUpload";
import PositionSelector from "./PositionSelector";
import PosterDisplay from "./PosterDisplay";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ChatInterface = ({ onAddToHistory, onGeneratePoster }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState("input"); // input, prompt, logo, position, generate
  const [enhancedPrompt, setEnhancedPrompt] = useState("");
  const [keywords, setKeywords] = useState([]);
  const [uploadedLogo, setUploadedLogo] = useState(null);
  const [selectedPosition, setSelectedPosition] = useState("");
  const [generatedPoster, setGeneratedPoster] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      type: "user",
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    onAddToHistory(userMessage);
    setInputValue("");
    setIsLoading(true);

    try {
      // Call backend API for prompt enhancement
      const response = await axios.post(`${BACKEND_URL}/api/poster/enhance-prompt`, {
        user_prompt: inputValue,
        session_id: Date.now().toString() // Simple session ID for now
      });

      const enhanced = response.data;
      setEnhancedPrompt(enhanced.enhanced_prompt);
      setKeywords(enhanced.keywords);
      
      const aiMessage = {
        type: "ai",
        content: enhanced.enhanced_prompt,
        keywords: enhanced.keywords,
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, aiMessage]);
      onAddToHistory(aiMessage);
      setCurrentStep("prompt");
    } catch (error) {
      console.error('Error enhancing prompt:', error);
      toast.error("Failed to enhance prompt. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegeneratePrompt = async () => {
    if (messages.length > 0) {
      const lastUserMessage = messages.filter(m => m.type === "user").pop();
      if (lastUserMessage) {
        setIsLoading(true);
        try {
          const response = await axios.post(`${BACKEND_URL}/api/poster/enhance-prompt`, {
            user_prompt: lastUserMessage.content,
            session_id: Date.now().toString()
          });

          const enhanced = response.data;
          setEnhancedPrompt(enhanced.enhanced_prompt);
          setKeywords(enhanced.keywords);
          
          const aiMessage = {
            type: "ai",
            content: enhanced.enhanced_prompt,
            keywords: enhanced.keywords,
            timestamp: new Date().toISOString(),
          };
          
          setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
          console.error('Error regenerating prompt:', error);
          toast.error("Failed to regenerate prompt. Please try again.");
        } finally {
          setIsLoading(false);
        }
      }
    }
  };

  const handleProceedToLogo = () => {
    setCurrentStep("logo");
    const logoMessage = {
      type: "system",
      content: "Great! Now, would you like to add a logo to your poster?",
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, logoMessage]);
  };

  const handleLogoUpload = (logo) => {
    setUploadedLogo(logo);
    setCurrentStep("position");
    const positionMessage = {
      type: "system",
      content: "Perfect! Now choose where you'd like to position your logo on the poster.",
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, positionMessage]);
  };

  const handlePositionSelect = (position) => {
    setSelectedPosition(position);
    setCurrentStep("generate");
  };

  const handleGeneratePoster = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/api/poster/generate`, {
        enhanced_prompt: enhancedPrompt,
        session_id: Date.now().toString(),
        user_prompt: messages.filter(m => m.type === "user").pop()?.content || "",
        keywords: keywords,
        logo: uploadedLogo,
        logo_position: selectedPosition
      });

      const poster = {
        id: response.data.id,
        image: response.data.poster_image,
        prompt: enhancedPrompt,
        logo: uploadedLogo,
        logoPosition: selectedPosition,
        style: response.data.style,
        dimensions: response.data.dimensions,
        timestamp: new Date().toLocaleString(),
        createdAt: response.data.created_at
      };

      setGeneratedPoster(poster);
      onGeneratePoster(poster);
      toast.success("Poster generated successfully!");
    } catch (error) {
      console.error('Error generating poster:', error);
      toast.error("Failed to generate poster. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartNew = () => {
    setMessages([]);
    setCurrentStep("input");
    setEnhancedPrompt("");
    setKeywords([]);
    setUploadedLogo(null);
    setSelectedPosition("");
    setGeneratedPoster(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Welcome Message */}
      <AnimatePresence>
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="text-center space-y-4 mb-12"
          >
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              <Wand2 className="h-16 w-16 text-purple-600 mx-auto mb-4" />
            </motion.div>
            <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-cyan-600 bg-clip-text text-transparent">
              Create Amazing Posters with AI
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Describe your poster idea and watch AI transform it into a stunning visual masterpiece
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Messages */}
      <div className="space-y-4 mb-6">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ delay: index * 0.1 }}
            >
              {message.type === "user" && (
                <div className="flex justify-end">
                  <Card className="max-w-2xl bg-gradient-to-r from-purple-500 to-cyan-500 text-white">
                    <CardContent className="p-4">
                      <p className="font-medium">{message.content}</p>
                    </CardContent>
                  </Card>
                </div>
              )}
              
              {message.type === "ai" && (
                <div className="flex justify-start">
                  <Card className="max-w-3xl bg-white shadow-lg border-l-4 border-l-purple-500">
                    <CardContent className="p-6">
                      <div className="flex items-start space-x-3">
                        <Sparkles className="h-6 w-6 text-purple-600 mt-1 flex-shrink-0" />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-3">
                            <h3 className="font-semibold text-gray-800">Enhanced Prompt</h3>
                            <Badge variant="secondary">AI Generated</Badge>
                          </div>
                          <p className="text-gray-700 mb-4 leading-relaxed">{message.content}</p>
                          
                          {message.keywords && (
                            <div className="space-y-2">
                              <h4 className="font-medium text-gray-800">Key Elements:</h4>
                              <div className="flex flex-wrap gap-2">
                                {message.keywords.map((keyword, i) => (
                                  <Badge key={i} variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
                                    {keyword}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          <div className="flex space-x-2 mt-4">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={handleRegeneratePrompt}
                              disabled={isLoading}
                              className="hover:bg-purple-50"
                            >
                              <RefreshCw className="h-4 w-4 mr-2" />
                              Regenerate
                            </Button>
                            <Button
                              onClick={handleProceedToLogo}
                              size="sm"
                              className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700"
                            >
                              Use This Prompt
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
              
              {message.type === "system" && (
                <div className="flex justify-center">
                  <Card className="bg-gray-50 border-dashed">
                    <CardContent className="p-4 text-center">
                      <p className="text-gray-600">{message.content}</p>
                    </CardContent>
                  </Card>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading Animation */}
        <AnimatePresence>
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex justify-start"
            >
              <Card className="bg-white shadow-lg">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <Sparkles className="h-5 w-5 text-purple-600 animate-spin" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Step-based Components */}
      <AnimatePresence>
        {currentStep === "logo" && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <LogoUpload onUpload={handleLogoUpload} />
          </motion.div>
        )}

        {currentStep === "position" && uploadedLogo && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <PositionSelector
              logo={uploadedLogo}
              onSelect={handlePositionSelect}
              onGenerate={handleGeneratePoster}
            />
          </motion.div>
        )}

        {generatedPoster && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <PosterDisplay poster={generatedPoster} onStartNew={handleStartNew} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input Area */}
      <AnimatePresence>
        {currentStep === "input" && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="sticky bottom-0 bg-white/80 backdrop-blur-sm border-t border-purple-100 p-6 rounded-t-3xl shadow-lg"
          >
            <div className="flex space-x-4">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Describe your poster idea... (e.g., 'A jazz concert poster with a retro vibe')"
                className="flex-1 h-12 text-lg border-purple-200 focus:border-purple-500 focus:ring-purple-500"
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="h-12 px-8 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 transform hover:scale-105 transition-all duration-200"
              >
                <Send className="h-5 w-5 mr-2" />
                Generate
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatInterface;