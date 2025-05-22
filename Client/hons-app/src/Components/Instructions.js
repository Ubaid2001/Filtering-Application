import React from 'react';

function Intrustions(){
    return( 
        <div className="InstructionsContainer">
            <div className="flex-row width-full ml-10 mt-10">
                <h2 className="InstructionsHeadline">Headline</h2>
                <ul className="InstructionsText">
                    <li>1. Drag and Drop a local image of a person</li>
                    <li>2. Once the result has been displayed, click on the button to Drag another image</li>
                </ul>
            </div>
            <div className="flex-row width-full ml-10 mt-10">
                <h2 className="InstructionsHeadline">Image Requirements:</h2>
                <ul className="InstructionsText">
                    <li>1. The image must be obtained from the local machine</li>
                    <li>2. The image must be a full body image of a person</li>
                    <li>3. The person in the image must be standing straight</li>
                </ul>
            </div>
        </div>
    );
};

export default Intrustions;