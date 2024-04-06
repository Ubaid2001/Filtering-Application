// Ubaid Mahmood
// S1906881
// BS/c Hons Project

// Import Libraries
import './App.css';
import { Routes, Route } from 'react-router-dom';
import Infobar from "./Components/Infobar";
import Home from "./Pages/Home";


export default function App() {


  return (
    <div className="App">
        <Infobar />
          <div className="">
            <Routes>
              <Route path="/" element={<Home />} />
            </Routes>
          </div>
    </div>
  );
}

