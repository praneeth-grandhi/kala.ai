import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ChatInterface from "./ChatInterface";
import HistorySidebar from "./HistorySidebar";
import { Button } from "./ui/button";
import { PanelLeft, Sparkles } from "lucide-react";

const PosterGenerator = () => {
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [generatedPosters, setGeneratedPosters] = useState([]);

  const addToChatHistory = (message) => {
    setChatHistory(prev => [...prev, { ...message, id: Date.now() }]);
  };

  const addGeneratedPoster = (poster) => {
    setGeneratedPosters(prev => [poster, ...prev]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-50 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-96 h-96 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-50 animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-50 animate-pulse delay-2000"></div>
      </div>

      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 bg-white/80 backdrop-blur-sm border-b border-purple-100 shadow-sm"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsHistoryOpen(true)}
                className="hover:bg-purple-100 transition-colors"
              >
                <PanelLeft className="h-5 w-5" />
              </Button>
              <motion.div 
                className="flex items-center space-x-2"
                whileHover={{ scale: 1.05 }}
              >
                <Sparkles className="h-8 w-8 text-purple-600" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-cyan-600 bg-clip-text text-transparent">
                  kala.ai
                </h1>
              </motion.div>
            </div>
            <div className="text-sm text-gray-500">
              AI-Powered Poster Generation
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ChatInterface 
          onAddToHistory={addToChatHistory}
          onGeneratePoster={addGeneratedPoster}
        />
      </div>

      {/* History Sidebar */}
      <AnimatePresence>
        {isHistoryOpen && (
          <HistorySidebar 
            isOpen={isHistoryOpen}
            onClose={() => setIsHistoryOpen(false)}
            chatHistory={chatHistory}
            generatedPosters={generatedPosters}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default PosterGenerator;