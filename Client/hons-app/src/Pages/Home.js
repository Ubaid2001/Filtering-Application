// Import Libraries
import React from "react";
import Head from "../Components/Head";
import About from "../Components/About";
import Intructions from "../Components/Instructions";
import ImageFiltering from "../Components/ImageFiltering";


export default function Home() {

    return(
        <div className="">
            <div className="Head">
                <Head />
            </div>
            <div className="AboutComponent">
                <About />
            </div>
            <div className="FilterContainer">
                <div className="InstructionsComponent">
                    <Intructions />
                </div>
                <div className="ImageComponent">
                    <ImageFiltering />
                </div>
            </div>
        </div>
    );
};