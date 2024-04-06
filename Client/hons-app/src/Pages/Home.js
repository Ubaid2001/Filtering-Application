// Ubaid Mahmood
// S1906881
// BS/c Hons Project

// Import Libraries
import axios from "axios";
import { useState } from "react";
import { useDropzone } from 'react-dropzone';


export default function Home() {

    // True or False is assigned, if the model wants the image to be blocked.
    const [isBlocked, setBlocked] = useState(true); 

    // the usestate will check if the request is invoked.
    const [isCalled, setCalled] = useState(false);

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
            .post("http://127.0.0.1:5000/Image", formData, {
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
                        <div className="flex text-center p-2 FileUpload justify-center 
                        flex-1 flex-col items-center">
                            <img  className="border-2 border-dashed p-2  rounded-lg" style={{ height: "25%", width:"25%" }} src={URL.createObjectURL(file)} />

                            <ul className="">
                                {uploadedFiles.map((file) => (
                                <li key={file.name} className="text-white">{file.name}</li>
                                ))}
    
                            </ul>
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

    return(
        <div className="HomeContainer relative flex-1 justify-center flex-col">
            <div className="flex justify-center items-center">
                <h1 className="text-2xl text-white mt-10">Filtering Web-App</h1>
            </div> 

            <div className="flex text-center text-white mx-auto w-1/2 flex-col mt-10">
                <h2 className="text-center text text-xl">About</h2>
                <p className="text-justify">
                    This Web Application is a demostration of a Machine Learning pipeline. The pipeline will first identify the gender of the person in a image as either Male or Female via CNN VGG-16 Deep Learning model.
                    Subsequently, the image will be passed into a PoseNet model called MoveNet. This model will identify specific locations of the human body, for instance, knees or shoulder. Lastly, the image 
                    will be transmitted into an EfficientNetB0 model, which will classify the clothes worn by the person. 
                </p>
                <br/>
                <p className="text-justify">
                    After this process, the image will either be declared <span className="underline text-lime-500">APPROPRIATE</span> or <span className="underline text-red-500">INAPPROPRIATE</span>, by which the image will not be showcased.
                </p>
            </div>

            <div className="flex text-center text-white mx-auto w-1/2 flex-col mt-10">
                <h2 className="text-left text-xl">How to use:</h2>
                <ul className="text-left pl-10">
                    <li>Step 1 - Drag and Drop a local image of a person,</li>
                    <li>Step 2 - Once the result has been displayed, click on the button to Drag another image.</li>
                </ul>
            </div>

            <div className="flex text-center text-white mx-auto w-1/2 flex-col mt-10">
                <h2 className="text-left text-xl">Image Requirements:</h2>
                <ul className="text-left pl-10">
                    <li>1 - The image must be obtained from the local machine,</li>
                    <li>2 - The image must be a full body image of a person, either Male or Female,</li>
                    <li>3 - Lastly, the person in the image must be standing straight, in order for Movenet detection.</li>
                </ul>
            </div>

            <div className="block m-20">

                {!isBlocked ? Div :
                    <div className="text-center p-40 border-2 border-dotted rounded-md FileUpload max-w-full max-h-svh flex justify-center 
                                    flex-1 flex-col  items-center" {...getRootProps()}>
                        <input className="m-auto"{...getInputProps()} />
                            <p className="text-white text-center">Drag and drop files here or click to browse.</p>
    
                    </div>
                }

                { isCalled ? 
                    !isBlocked ?
                        <div className="text-center text-white mt-4">
                            <p>THE IMAGE IS <span className="underline text-lime-500">APPROPRIATE</span></p>
                        </div>
                        :
                        <div className="text-center text-white mt-4">
                            <p>THE IMAGE IS DEEMED <span className="underline text-red-500">INAPPROPRIATE</span>, TRY ANOTHER IMAGE</p>
                        </div>
                    :
                    <></>
                }

                <div className=" text-center text-white mt-10 pb-10">
                    <button className="border-4 border-solid rounded-lg p-2" onClick={ClearButton}>Clear Image</button>
                </div>

            </div>

        </div>
    );
};