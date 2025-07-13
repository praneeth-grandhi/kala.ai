import React, { useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { Label } from "./ui/label";
import { Wand2 } from "lucide-react";

const PositionSelector = ({ logo, onSelect, onGenerate }) => {
  const [selectedPosition, setSelectedPosition] = useState("");

  const positions = [
    { id: "top-left", label: "Top Left", description: "Classic corner placement" },
    { id: "top-right", label: "Top Right", description: "Professional header position" },
    { id: "top-center", label: "Top Center", description: "Centered header" },
    { id: "bottom-left", label: "Bottom Left", description: "Subtle footer position" },
    { id: "bottom-right", label: "Bottom Right", description: "Standard footer placement" },
    { id: "bottom-center", label: "Bottom Center", description: "Centered footer" },
  ];

  const handleGenerate = () => {
    if (selectedPosition) {
      onSelect(selectedPosition);
      onGenerate();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto"
    >
      <Card className="bg-white shadow-lg">
        <CardContent className="p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <img
                src={logo.preview}
                alt="Logo"
                className="h-10 w-10 object-contain border rounded"
              />
              <div className="text-2xl text-gray-400">→</div>
              <div className="w-20 h-14 bg-gray-100 rounded border-2 border-dashed border-gray-300 flex items-center justify-center">
                <span className="text-xs text-gray-500">Poster</span>
              </div>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Choose Logo Position
            </h3>
            <p className="text-gray-600">
              Select where you'd like your logo to appear on the poster
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <RadioGroup 
              value={selectedPosition} 
              onValueChange={setSelectedPosition}
              className="space-y-0"
            >
              {positions.map((position) => (
                <motion.div
                  key={position.id}
                  whileHover={{ scale: 1.02 }}
                  className="flex items-center space-x-3"
                >
                  <Card className={`w-full p-4 cursor-pointer transition-all duration-200 ${
                    selectedPosition === position.id
                      ? "ring-2 ring-purple-500 bg-purple-50 border-purple-200"
                      : "hover:bg-gray-50 border-gray-200"
                  }`}>
                    <div className="flex items-center space-x-3">
                      <RadioGroupItem value={position.id} id={position.id} />
                      <div className="flex-1">
                        <Label 
                          htmlFor={position.id}
                          className="cursor-pointer block font-medium text-gray-800"
                        >
                          {position.label}
                        </Label>
                        <p className="text-sm text-gray-600 mt-1">
                          {position.description}
                        </p>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </RadioGroup>

            {/* Visual Preview */}
            <div className="flex items-center justify-center">
              <div className="relative w-48 h-64 bg-gradient-to-br from-purple-100 to-cyan-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
                <span className="text-gray-500 text-sm">Preview</span>
                
                {/* Position Preview */}
                {selectedPosition && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className={`absolute w-8 h-8 ${
                      selectedPosition === "top-left" ? "top-2 left-2" :
                      selectedPosition === "top-right" ? "top-2 right-2" :
                      selectedPosition === "top-center" ? "top-2 left-1/2 transform -translate-x-1/2" :
                      selectedPosition === "bottom-left" ? "bottom-2 left-2" :
                      selectedPosition === "bottom-right" ? "bottom-2 right-2" :
                      selectedPosition === "bottom-center" ? "bottom-2 left-1/2 transform -translate-x-1/2" :
                      ""
                    }`}
                  >
                    <img
                      src={logo.preview}
                      alt="Logo preview"
                      className="w-full h-full object-contain bg-white rounded border shadow-sm"
                    />
                  </motion.div>
                )}
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <Button
              onClick={handleGenerate}
              disabled={!selectedPosition}
              className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 px-8 py-3 text-lg font-semibold transform hover:scale-105 transition-all duration-200"
            >
              <Wand2 className="h-5 w-5 mr-2" />
              Generate Poster
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PositionSelector;