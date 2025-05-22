import React from "react";
import { motion } from "motion/react"


function Head(){

    return(
        <div>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 3 }}
                className="HeadContainer">

                    <div className="HeadingContainer">
                        <h1 className=" text-start HeadingFont" data-text="ISLAMIC FILTERING">ISLAMIC FILTERING</h1>
                    </div> 
                    <div className="rain"></div>

            </motion.div>
        </div>
    )
};

export default Head; 