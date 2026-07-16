# 👕 Wardrobe AI – A Virtual Try-On Companion

<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi">

<img src="https://img.shields.io/badge/React-Vite-61DAFB?logo=react">

<img src="https://img.shields.io/badge/AI-FASHN--VTON-orange">

<img src="https://img.shields.io/badge/Status-Active-success">

</p>

---

## 📖 Overview

Wardrobe AI is a full-stack AI-powered Virtual Try-On web application that enables users to visualize clothing on a person before purchase.

The application combines a **React (Vite)** frontend with a **FastAPI** backend and integrates the **FASHN-VTON v1.5** model to generate realistic virtual try-on images.

The project was developed to provide a simple and interactive interface for AI-powered fashion visualization while exposing REST APIs for future integration with e-commerce platforms and fashion applications.

---

## ✨ Features

- AI-powered virtual try-on
- Upload person image
- Upload garment image
- Drag-and-drop interface
- FastAPI REST API
- React + Vite frontend
- Download generated images
- Supports:
  - Tops
  - Bottoms
  - One-Pieces
- GPU acceleration (CUDA supported)

---

## 🛠 Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- Pillow

### AI

- FASHN-VTON v1.5
- PyTorch
- ONNX Runtime
- DWPose

---

## 📂 Project Structure

```
Wardrobe-Ai---A-VTON-Companion/
│
├── backend/
│   ├── app/
│   ├── scripts/
│   ├── fashn-vton-1.5/
│   ├── weights/
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Vimal-Antony-J/Wardrobe-Ai---A-VTON-Companion.git

cd Wardrobe-Ai---A-VTON-Companion
```

---

## Backend Setup

Navigate to backend

```bash
cd backend
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create environment file

```bash
copy .env.example .env
```

Run backend

```bash
python run.py
```

Backend URL

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## Frontend Setup

Open another terminal

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Create

```bash
copy .env.example .env
```

Run

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

## AI Model Setup

This repository **does not include pretrained model weights** because they exceed GitHub's file size limit.

Download the required model weights from the official FASHN-VTON repository:

https://github.com/fashn-AI/fashn-vton-1.5

Place the downloaded files inside

```
backend/weights/
```

Expected structure

```
backend/
└── weights/
    ├── model.safetensors
    └── dwpose/
        ├── yolox_l.onnx
        └── dw-ll_ucoco_384.onnx
```

---

## API Endpoints

### Health Check

```
GET /api/health
```

Returns backend status.

### Virtual Try-On

```
POST /api/tryon
```

Input

- Person Image
- Garment Image
- Clothing Category

Output

- Generated Virtual Try-On Image

---

## Supported Categories

| Category | Description |
|----------|-------------|
| Tops | T-shirts, Shirts, Jackets |
| Bottoms | Pants, Shorts, Skirts |
| One-Pieces | Dresses, Jumpsuits |

---

## Known Limitations

The application currently inherits the limitations of the underlying **FASHN-VTON v1.5** model.

- Best suited for western-style garments.
- Performance on Indian ethnic wear (such as sarees, kurtas, lehengas, and similar traditional clothing) is currently limited and may produce unrealistic results.
- CPU inference is significantly slower than CUDA-enabled GPU inference.
- Performance may degrade with:
  - Multiple people in one image
  - Heavy occlusions
  - Low-resolution images
  - Complex poses
- Currently supports a single person per inference.

---

## Future Improvements

Planned enhancements include:

- Support for Indian ethnic wear
- Improved cloth deformation
- Faster inference through optimization
- Higher-resolution outputs
- Multi-garment try-on
- Mobile-friendly interface
- Cloud deployment
- User authentication
- Wardrobe management
- Integration of newer virtual try-on models for broader clothing support

---

## Screenshots

### Home Page

_Add a screenshot of your application here._

### Generated Result

_Add a screenshot of a generated virtual try-on result here._

---

## Acknowledgements

This project integrates the open-source **FASHN-VTON v1.5** model developed by **FASHN AI**.

Original Repository:

https://github.com/fashn-AI/fashn-vton-1.5

Special thanks to the FASHN AI team for making their research and pretrained model publicly available.

---

## Disclaimer

This project is an independent application built around the FASHN-VTON v1.5 model.

The application architecture, backend APIs, and frontend interface were developed as part of this project.

The pretrained model, weights, and related research belong to their respective authors.

---

## 👨‍💻 Author

**Vimal Antony J**

Mechatronics Engineer | AI & Machine Learning Enthusiast

GitHub

https://github.com/Vimal-Antony-J

---

⭐ If you found this project useful, consider giving it a Star.