# Islamic Filtering Web Application

<img width="1430" alt="1" src="https://github.com/user-attachments/assets/5d2e8c6d-8fef-4d0c-a1e6-5f61aa01fed7" />


## Overview

The **Islamic Filtering Web Application** is a full-stack solution created as a frontend demonstration for the [Model-Configs Repository](https://github.com/your-org/model-configs). It integrates a **three-stage Machine Learning pipeline** using **Flask (backend)** and **React (frontend)** technologies.

The pipeline consists of the following deep learning architectures:
- **VGG-16**: for gender classification,
- **MoveNet**: for keypoint detection on the human body,
- **EfficientNet-B0**: for clothing classification.

This tool is designed to **filter out images that are deemed inappropriate** according to Islamic principles, thereby assisting users or systems in maintaining visual content modesty and compliance in religious or culturally sensitive contexts.

---

## Application Logic and Flow

<img width="1424" alt="2" src="https://github.com/user-attachments/assets/2a56d34e-8d12-4fe6-a30b-b23c8b8e35b9" />


1. **Step 1**: An image is uploaded by the user via drag-and-drop or file picker.
2. **Step 2**: The pipeline determines the gender using **VGG-16**.
3. **Step 3**: **MoveNet** pinpoints body parts (knees, shoulders, etc.).
4. **Step 4**: The image is classified via **EfficientNet-B0** into either `APPROPRIATE` or `INAPPROPRIATE`.

If the image is classified as `INAPPROPRIATE`, it will **not be displayed**. Otherwise, it is shown as an acceptable image under Islamic standards.

---

## Interface and Styling

<img width="1430" alt="3" src="https://github.com/user-attachments/assets/12d4193e-eddd-4f88-bdc6-2b0c2db66ded" />

The design of the app embraces a **neon futuristic theme**, utilizing deep blues and glowing cyan highlights to create a visually engaging and modern experience. Key styling features include:

- **Glow effects** for text and borders to enhance visual clarity.
- **Minimalist layout** with clear content hierarchy.
- A large **drag-and-drop panel** for intuitive image uploads.
- Mobile-first responsive design for use across:
  - Desktops
  - Tablets
  - Mobile phones

The interface cleanly separates **instructions**, **requirements**, and **upload zone** to prevent confusion and ensure ease-of-use.

---

## Benefits

- ✅ **Automated Modesty Filter**: Automatically screens for modest clothing aligned with Islamic ethics.
- ✅ **Privacy-First**: Images are processed locally or within a controlled backend.
- ✅ **Multi-Model Fusion**: Uses a robust ML pipeline for increased classification accuracy.
- ✅ **Device Adaptive**: Fully responsive design means it works seamlessly across screen sizes.
- ✅ **Scalable**: Can be easily extended to integrate additional checks or religious standards.

---

## Setup & Deployment

This web app is deployed via Flask for backend inference and React for the frontend UI.

To deploy locally:
1. Clone this repository.
2. Set up Python or Conda (GPU Usage) virtual environment and install requirements.
3. Run the Flask backend `app.py`.
4. Launch React frontend with `npm start`.

Ensure the Flask server and React app are connected through proxy settings or reverse proxy.

---



