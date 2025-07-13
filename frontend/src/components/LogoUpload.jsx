import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Upload, X, Image } from "lucide-react";
import { toast } from "sonner";

const LogoUpload = ({ onUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFile = (file) => {
    if (!file.type.startsWith("image/")) {
      toast.error("Please upload an image file");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target.result;
      setPreview(base64);
      
      // Simulate processing
      setTimeout(() => {
        onUpload({
          name: file.name,
          size: file.size,
          preview: base64,
          base64: base64
        });
        toast.success("Logo uploaded successfully!");
      }, 1000);
    };
    reader.readAsDataURL(file);
  };

  const handleSkip = () => {
    onUpload(null);
  };

  const clearPreview = () => {
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto"
    >
      <Card className="bg-white shadow-lg">
        <CardContent className="p-8">
          <div className="text-center mb-6">
            <Upload className="h-12 w-12 text-purple-600 mx-auto mb-3" />
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Upload Your Logo
            </h3>
            <p className="text-gray-600">
              Add your logo to make the poster truly yours
            </p>
          </div>

          {!preview ? (
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
                dragActive
                  ? "border-purple-500 bg-purple-50"
                  : "border-gray-300 hover:border-purple-400 hover:bg-purple-50"
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <Image className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">
                Drag and drop your logo here, or click to browse
              </p>
              <Button
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                className="mb-4"
              >
                <Upload className="h-4 w-4 mr-2" />
                Choose File
              </Button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileInput}
                className="hidden"
              />
              <p className="text-sm text-gray-500">
                Supports PNG, JPG, JPEG files up to 10MB
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative inline-block">
                <img
                  src={preview}
                  alt="Logo preview"
                  className="h-24 w-24 object-contain border rounded-lg mx-auto block"
                />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearPreview}
                  className="absolute -top-2 -right-2 h-6 w-6 rounded-full bg-red-500 hover:bg-red-600 text-white p-0"
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
              <p className="text-center text-sm text-gray-600">
                Logo ready to use!
              </p>
            </div>
          )}

          <div className="flex justify-center space-x-4 mt-8">
            <Button
              variant="outline"
              onClick={handleSkip}
              className="hover:bg-gray-50"
            >
              Skip Logo
            </Button>
            {preview && (
              <Button
                onClick={() => onUpload({
                  name: "logo.png",
                  size: 0,
                  preview: preview,
                  base64: preview
                })}
                className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700"
              >
                Continue
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default LogoUpload;