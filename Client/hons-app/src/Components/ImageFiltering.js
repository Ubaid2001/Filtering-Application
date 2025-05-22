import React from "react";
import { useState } from "react";
import { useDropzone } from 'react-dropzone';
import axios from "axios";

function ImageFiltering() {

    // True or False is assigned, if the model wants the image to be blocked.
    const [isBlocked, setBlocked] = useState(true); 

    // the usestate will check if the request is invoked.
    const [isCalled, setCalled] = useState(false);

    const localhost = process.env.REACT_APP_LOCALHOST; 
    const port = process.env.REACT_APP_PORT;

    const [Div, setDiv] = useState(); 
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop: (acceptedFiles) => {
            setUploadedFiles(acceptedFiles);
            // Call your backend API endpoint to upload files

            // get the selected file from the input
            const file = acceptedFiles[0];

            // create a new FormData object and append the file to it
            const formData = new FormData();
            formData.append("img", file);


            // make a POST request to the File Upload endpoint with the FormData object and API headers
            axios
            .post(`http://${localhost}:${port}/Image`, formData, {
                headers: {
                "Content-Type": "multipart/form-data",
                },
            })
            .then((response) => {
                // handle the response
                console.log(response);
                console.log(response.data[0]);
                
                // message variable with the response from the server.
                var mes = response.data[0];

                // isCalled is set to true.
                setCalled(true);

                // If the message determines the image to be blocked then isBlocked set to true,
                // else if the the image isBlocked false then a new div element is created with the image.
                if(mes == "Image is Blocked: True"){
                    console.log("isBlocked is set to True");
                    setBlocked(true);

                }
                else if (mes == "Image is Blocked: False"){
                    console.log("isBlocked is set to False");
                    setBlocked(false);

                    setDiv(
                        <div className="ImageContainerBlock">
                            <img  className="AppropriateImage"  src={URL.createObjectURL(file)} />
                        </div>
                    );

                }
            })
            .catch((error) => {

                // handle errors
                console.log(error);
                setCalled(false)
            });

            

        }
        
    });

    // Clears the image from the drop box.
    const ClearButton = () => {
        setBlocked(true);
        setCalled(false)

        console.log("button clicked");


    }

    return (
        <div className="ImageFilteringContainer">

            {!isBlocked ? Div :
                <div className="ImageContainerBlock" {...getRootProps()}>
                    <input className="m-auto"{...getInputProps()} />
                        <p className="BoxText">Drag and drop files here or click to browse</p>

                </div>
            }

            { isCalled ? 
                !isBlocked ?
                    <div className="ResultText">
                        <p>THE IMAGE IS <span className="ResultAppropriate">APPROPRIATE</span></p>
                    </div>
                    :
                    <div className="ResultText">
                        <p>THE IMAGE IS DEEMED <span className="ResultInappropriate">INAPPROPRIATE</span>, TRY ANOTHER IMAGE</p>
                    </div>
                :
                <></>
            }

            <div className="mt-10 pb-10">
                <button className="ButtonClearImage" onClick={ClearButton} data-text="CLEAR IMAGE">CLEAR IMAGE</button>
            </div>


        </div>
    );
};

export default ImageFiltering;