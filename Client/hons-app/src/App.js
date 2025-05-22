// Import Libraries
import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from "./Pages/Home";
import Footer from './Components/Footer';


export default function App() {


  return (
    <div className="App">
          <div className="">
            <Routes>
              <Route path="/" element={<Home />} />
            </Routes>
          </div>
          <Footer />
    </div>
  );
}

