import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Download, RefreshCw, Share2, Heart } from "lucide-react";
import { toast } from "sonner";

const PosterDisplay = ({ poster, onStartNew }) => {
  const handleDownload = () => {
    // Create download link
    const link = document.createElement("a");
    link.href = poster.image;
    link.download = `kala-poster-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success("Poster downloaded successfully!");
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: "Check out my AI-generated poster!",
          text: "Created with kala.ai",
          url: window.location.href,
        });
      } catch (error) {
        console.log("Error sharing:", error);
      }
    } else {
      // Fallback to clipboard
      navigator.clipboard.writeText(window.location.href);
      toast.success("Link copied to clipboard!");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      <Card className="bg-white shadow-2xl overflow-hidden">
        <CardContent className="p-8">
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              className="inline-flex items-center space-x-2 mb-4"
            >
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-lg font-semibold text-gray-800">
                Your Poster is Ready!
              </span>
            </motion.div>
            <p className="text-gray-600">
              AI has transformed your idea into a beautiful poster
            </p>
          </div>

          {/* Poster Display */}
          <div className="relative group mb-8">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="relative mx-auto max-w-lg"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-lg transform rotate-1 group-hover:rotate-2 transition-transform duration-300"></div>
              <div className="relative bg-white rounded-lg shadow-lg p-2">
                <img
                  src={poster.image}
                  alt="Generated Poster"
                  className="w-full h-auto rounded-lg"
                />
                
                {/* Logo Overlay if present */}
                {poster.logo && (
                  <div className={`absolute w-12 h-12 ${
                    poster.logoPosition === "top-left" ? "top-4 left-4" :
                    poster.logoPosition === "top-right" ? "top-4 right-4" :
                    poster.logoPosition === "top-center" ? "top-4 left-1/2 transform -translate-x-1/2" :
                    poster.logoPosition === "bottom-left" ? "bottom-4 left-4" :
                    poster.logoPosition === "bottom-right" ? "bottom-4 right-4" :
                    poster.logoPosition === "bottom-center" ? "bottom-4 left-1/2 transform -translate-x-1/2" :
                    ""
                  }`}>
                    <img
                      src={poster.logo.preview}
                      alt="Logo"
                      className="w-full h-full object-contain bg-white/80 rounded border shadow-sm"
                    />
                  </div>
                )}
              </div>
            </motion.div>

            {/* Floating Action Buttons */}
            <div className="absolute top-4 right-4 flex flex-col space-y-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <Button
                variant="secondary"
                size="sm"
                onClick={handleDownload}
                className="bg-white/90 hover:bg-white shadow-lg"
              >
                <Download className="h-4 w-4" />
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={handleShare}
                className="bg-white/90 hover:bg-white shadow-lg"
              >
                <Share2 className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Poster Details */}
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <h3 className="font-semibold text-gray-800 mb-3">Poster Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-600">Prompt:</span>
                <p className="text-gray-700 mt-1">{poster.prompt}</p>
              </div>
              <div>
                <span className="font-medium text-gray-600">Generated:</span>
                <p className="text-gray-700 mt-1">{poster.timestamp}</p>
              </div>
              <div>
                <span className="font-medium text-gray-600">Dimensions:</span>
                <p className="text-gray-700 mt-1">{poster.dimensions}</p>
              </div>
              <div>
                <span className="font-medium text-gray-600">Style:</span>
                <p className="text-gray-700 mt-1">{poster.style}</p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap justify-center gap-4">
            <Button
              onClick={handleDownload}
              className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 px-6 py-3 text-lg font-semibold transform hover:scale-105 transition-all duration-200"
            >
              <Download className="h-5 w-5 mr-2" />
              Download High-Res
            </Button>
            
            <Button
              variant="outline"
              onClick={handleShare}
              className="px-6 py-3 text-lg font-semibold border-2 hover:bg-gray-50 transform hover:scale-105 transition-all duration-200"
            >
              <Share2 className="h-5 w-5 mr-2" />
              Share
            </Button>
            
            <Button
              variant="outline"
              onClick={onStartNew}
              className="px-6 py-3 text-lg font-semibold border-2 hover:bg-gray-50 transform hover:scale-105 transition-all duration-200"
            >
              <RefreshCw className="h-5 w-5 mr-2" />
              Create New
            </Button>
          </div>

          {/* Feedback */}
          <div className="text-center mt-8 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3">
              Love your poster? Give it a heart!
            </p>
            <Button
              variant="ghost"
              size="sm"
              className="text-red-500 hover:text-red-600 hover:bg-red-50"
            >
              <Heart className="h-5 w-5 mr-1" />
              <span className="font-medium">127</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PosterDisplay;