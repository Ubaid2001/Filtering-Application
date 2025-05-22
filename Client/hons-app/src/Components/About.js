import React from 'react';
import { motion } from 'motion/react';

function About() {
    
    return (
        <div className="AboutContainer">
            <motion.div
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1}}
                transition={{ duration: 5 }}
                className="AboutMotion">
                    <motion.div initial={{ opacity: 0, width: 0 }} 
                    whileInView={{ opacity: 1, width: "100%" }}
                    transition={{ duration: 5, ease: "easeInOut" }}
                    viewport={{ once: true }}
                    className="AboutInfo">
                        This Web Application is a demostration of a Machine Learning pipeline. The pipeline will first identify the gender of the person in a image as either Male or Female via CNN VGG-16 Deep Learning model.
                        Subsequently, the image will be passed into a PoseNet model called MoveNet. This model will identify specific locations of the human body, for instance, knees or shoulder. Lastly, the image 
                        will be transmitted into an EfficientNetB0 model, which will classify the clothes worn by the person. 
                    </motion.div>
                    <br/>
                    <motion.div initial={{ opacity: 0, width: 0 }}
                        whileInView={{ opacity: 1, width: "100%" }}
                        transition={{ duration: 5, ease: "easeInOut" }}
                        viewport={{ once: true }}
                        className='AboutInfo'>
                        After this process, the image will either be declared <span className="AboutAppropriate">APPROPRIATE</span> or <span className="AboutInappropriate">INAPPROPRIATE</span>, by which the image will not be showcased.
                    </motion.div>
            </motion.div>
        </div>
    );
}

export default About;