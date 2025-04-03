# 🚗 Car Resale Price Prediction

## 📌 Project Overview
This project is a **Car Resale Price Prediction** application built using **Streamlit** and **Azure Machine Learning**. Users can input various car features to get an estimated resale value based on a trained machine learning model. The app provides an intuitive UI, real-time predictions, and animated feedback for better user experience.

## 🏗️ Tech Stack
- **Frontend:** Streamlit (Python-based UI)
- **Backend:** Azure ML Endpoint (Deployed Model)
- **APIs:** REST API for ML model inference
- **Animations:** LottieFiles (Loading, Success, and Error animations)
- **Deployment:** Streamlit Community Cloud

## 🎯 Features
1. AI-Powered Price Prediction: Uses a trained ML model deployed on Azure to estimate resale value.
2. Interactive UI: Built with Streamlit for a seamless user experience.
3. Lottie Animations: Engaging visual animations for loading, success, and error messages.
4. Cloud-Based Deployment: Hosted on Streamlit Community Cloud (Free) or can be deployed on other platforms.
5. Real-Time API Calls: Sends user input to Azure ML and retrieves predictions dynamically.
6. Error Handling & Validation: Ensures proper API response formatting and displays meaningful error messages.

## 🎥 Demo
![App Preview]( https://car-resale-price-prediction.streamlit.app/)

Languages and tool used are: 
[![My Skills](https://skillicons.dev/icons?i=python,git,ai,azure)](https://skillicons.dev)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)
![Project Screenshot](images/img 1.jpg)
![Project Screenshot](images/img 2.jpg)

## 🚀 How to Run Locally
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/car-resale-price-predictor.git
cd car-resale-price-predictor
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # For Mac/Linux
env\Scripts\activate    # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

## 🛠️ Deployment on Streamlit Cloud
1. **Fork this repository**  
2. **Go to Streamlit Community Cloud** and sign in  
3. **Create a new app** → Select this repository  
4. **Set the main file** (`app.py`) and click Deploy  

## 📌 API Details
- **Endpoint:** `http://d8a72203-fb49-44da-b92a-e0c59e31cf58.eastus2.azurecontainer.io/score`
- **Auth:** Bearer Token (API Key)
- **Request Format:** JSON payload with car details
- **Response:** JSON with `predicted_price`


## 🤝 Contribution
Want to improve the project? Follow these steps:
1. Fork the repository
2. Create a new feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Added new feature'`)
4. Push to GitHub (`git push origin feature-name`)
5. Open a Pull Request 🎉
