import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";
import { Badge } from "./ui/badge";
import { X, Clock, Image, MessageSquare, Download } from "lucide-react";

const HistorySidebar = ({ isOpen, onClose, chatHistory, generatedPosters }) => {
  const handleDownload = (poster) => {
    const link = document.createElement("a");
    link.href = poster.image;
    link.download = `kala-poster-${poster.id}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
            onClick={onClose}
          />

          {/* Sidebar */}
          <motion.div
            initial={{ x: -400 }}
            animate={{ x: 0 }}
            exit={{ x: -400 }}
            transition={{ type: "spring", damping: 20, stiffness: 200 }}
            className="fixed left-0 top-0 h-full w-80 bg-white shadow-2xl z-50 flex flex-col"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800">History</h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="hover:bg-gray-100"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>

            {/* Content */}
            <ScrollArea className="flex-1 p-6">
              <div className="space-y-6">
                {/* Generated Posters */}
                {generatedPosters.length > 0 && (
                  <div>
                    <div className="flex items-center space-x-2 mb-4">
                      <Image className="h-5 w-5 text-purple-600" />
                      <h3 className="font-semibold text-gray-800">
                        Generated Posters
                      </h3>
                      <Badge variant="secondary" className="ml-auto">
                        {generatedPosters.length}
                      </Badge>
                    </div>
                    
                    <div className="grid gap-4">
                      {generatedPosters.map((poster) => (
                        <motion.div
                          key={poster.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="group"
                        >
                          <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                            <div className="relative">
                              <img
                                src={poster.image}
                                alt="Generated poster"
                                className="w-full h-32 object-cover"
                              />
                              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                                <Button
                                  variant="secondary"
                                  size="sm"
                                  onClick={() => handleDownload(poster)}
                                  className="opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                  <Download className="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                            <CardContent className="p-3">
                              <div className="flex items-start justify-between">
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm font-medium text-gray-800 truncate">
                                    {poster.style}
                                  </p>
                                  <p className="text-xs text-gray-600 mt-1">
                                    {poster.timestamp}
                                  </p>
                                </div>
                                <Badge
                                  variant="outline"
                                  className="ml-2 text-xs"
                                >
                                  {poster.dimensions}
                                </Badge>
                              </div>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Chat History */}
                {chatHistory.length > 0 && (
                  <div>
                    <div className="flex items-center space-x-2 mb-4">
                      <MessageSquare className="h-5 w-5 text-cyan-600" />
                      <h3 className="font-semibold text-gray-800">
                        Chat History
                      </h3>
                      <Badge variant="secondary" className="ml-auto">
                        {chatHistory.length}
                      </Badge>
                    </div>
                    
                    <div className="space-y-3">
                      {chatHistory.slice(-10).reverse().map((message, index) => (
                        <motion.div
                          key={message.id || index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                        >
                          <Card className="hover:shadow-md transition-shadow">
                            <CardContent className="p-4">
                              <div className="flex items-start space-x-3">
                                <div className={`w-2 h-2 rounded-full mt-2 ${
                                  message.type === "user" ? "bg-purple-500" :
                                  message.type === "ai" ? "bg-cyan-500" :
                                  "bg-gray-500"
                                }`} />
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center space-x-2 mb-2">
                                    <span className={`text-xs font-medium ${
                                      message.type === "user" ? "text-purple-600" :
                                      message.type === "ai" ? "text-cyan-600" :
                                      "text-gray-600"
                                    }`}>
                                      {message.type === "user" ? "You" :
                                       message.type === "ai" ? "AI" : "System"}
                                    </span>
                                    <span className="text-xs text-gray-500">
                                      <Clock className="h-3 w-3 inline mr-1" />
                                      {new Date(message.timestamp).toLocaleTimeString()}
                                    </span>
                                  </div>
                                  <p className="text-sm text-gray-700 line-clamp-3">
                                    {message.content}
                                  </p>
                                  {message.keywords && (
                                    <div className="flex flex-wrap gap-1 mt-2">
                                      {message.keywords.slice(0, 3).map((keyword, i) => (
                                        <Badge
                                          key={i}
                                          variant="outline"
                                          className="text-xs"
                                        >
                                          {keyword}
                                        </Badge>
                                      ))}
                                    </div>
                                  )}
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Empty State */}
                {generatedPosters.length === 0 && chatHistory.length === 0 && (
                  <div className="text-center py-12">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Clock className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-600 mb-2">
                      No History Yet
                    </h3>
                    <p className="text-gray-500">
                      Your generated posters and chat history will appear here
                    </p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default HistorySidebar;