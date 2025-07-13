import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PosterGenerator from "./components/PosterGenerator";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PosterGenerator />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;