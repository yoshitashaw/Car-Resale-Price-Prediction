import streamlit as st
import requests
import json
import os
from streamlit_lottie import st_lottie
import time

st.set_page_config(page_title="Car Resale Predictor", page_icon="🚗", layout="centered")

# Function to load Lottie animations locally
def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
    
# Using local Lottie JSON files to load animations
loading_animation = load_lottie_file("animations/loading.json")
success_animation = load_lottie_file("animations/success.json")
error_animation = load_lottie_file("animations/error.json")
car_animation = load_lottie_file("animations/car.json")

# Streamlit UI
st.title("🚗 CAR RESALE PRICE PREDICTOR")

# Load Lottie Animations
def load_lottie_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP failures (404, 500, etc.)
        return response.json()  # Attempt to parse JSON
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Lottie animation failed to load: {e}")
        return None  # Return None to prevent crashing
    except json.JSONDecodeError:
        st.error("⚠️ Failed to decode Lottie animation JSON.")
        return None


# Azure ML Endpoint Details
API_URL = "http://d8a72203-fb49-44da-b92a-e0c59e31cf58.eastus2.azurecontainer.io/score"
API_KEY = "EARVG8B19Eudr8j2GfVF5i2gfkzuRCEm"


# Header
st.markdown(
    """
    <style>
        .main-title {
            font-size: 80px;
            font-weight: bold;
            text-align: center;
            color: #1E88E5;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">🚗 Enter your car details to predict its resale price</p>', unsafe_allow_html=True)
# Car Animation
st_lottie(car_animation, height=400, width=400, key="car")  # Increased height & width
st.markdown("---")

# Layout Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🔹 Basic Details")
    make = st.selectbox("Make", ["alfa-romero", "audi", "bmw", "chevrolet"])
    fuel_type = st.selectbox("Fuel Type", ["gas", "diesel"])
    body_style = st.selectbox("Body Style", ["convertible", "hatchback", "sedan", "wagon"])
    drive_wheels = st.selectbox("Drive Wheels", ["fwd", "rwd", "4wd"])
    engine_location = st.selectbox("Engine Location", ["front", "rear"])
    engine_type = st.selectbox("Engine Type", ["dohc", "ohc", "ohcv", "l", "rotor"])
    num_of_cylinders = st.selectbox("Number of Cylinders", [3, 4, 5, 6, 8])
    fuel_system = st.selectbox("Fuel System", ["mpfi", "2bbl", "mfi", "spfi"])
    num_of_doors = st.selectbox("Number of Doors", ["two", "four"])
    aspiration = st.selectbox("Aspiration", ["std", "turbo"])

with col2:
    st.markdown("### 🔹 Performance & Dimensions")
    engine_size = st.number_input("Engine Size", min_value=60, max_value=400, value=109)
    compression_ratio = st.number_input("Compression Ratio", min_value=7.0, max_value=12.0, value=10.0)
    horsepower = st.number_input("Horsepower", min_value=40, max_value=300, value=102)
    peak_rpm = st.number_input("Peak RPM", min_value=3000, max_value=7000, value=5500)
    city_mpg = st.number_input("City MPG", min_value=10, max_value=60, value=24)
    highway_mpg = st.number_input("Highway MPG", min_value=10, max_value=80, value=30)
    curb_weight = st.number_input("Curb Weight", min_value=1500, max_value=4000, value=2500)
    length = st.number_input("Length", min_value=140.0, max_value=200.0, value=170.2)
    width = st.number_input("Width", min_value=50.0, max_value=80.0, value=65.4)
    height = st.number_input("Height", min_value=45.0, max_value=70.0, value=54.3)

st.markdown("---")

# Predict Button
if st.button("🚀 PREDICT RESALE PRICE", help="Click to predict the car's resale value", use_container_width=True):
    
    # Show loading animation
    with st.spinner("🔄 Analyzing..."):
        st_lottie(loading_animation, height=150, key="loading")
        time.sleep(2)

    # Prepare Data
    data = {
        "Inputs": {
            "WebServiceInput0": [
                {
                    "symboling": 0,
                    "normalized-losses": 120,
                    "make": make,
                    "fuel-type": fuel_type,
                    "body-style": body_style,
                    "drive-wheels": drive_wheels,
                    "engine-location": engine_location,
                    "engine-type": engine_type,
                    "num-of-cylinders": int(num_of_cylinders),
                    "engine-size": engine_size,
                    "fuel-system": fuel_system,
                    "compression-ratio": compression_ratio,
                    "horsepower": horsepower,
                    "peak-rpm": peak_rpm,
                    "city-mpg": city_mpg,
                    "highway-mpg": highway_mpg,
                    "width": width,
                    "aspiration": aspiration,
                    "bore": 3.31,
                    "num-of-doors": num_of_doors,
                    "curb-weight": curb_weight,
                    "length": length,
                    "stroke": 3.39,
                    "height": height,
                    "wheel-base": 102.7
                }
            ]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Check for errors
        result = response.json()

        if "Results" in result:
            predicted_price = result["Results"]["WebServiceOutput0"][0]["predicted_price"]
            st_lottie(success_animation, height=150, key="success")
            st.success(f"✅ Predicted Resale Price: **${predicted_price:,.2f}**")
        else:
            st_lottie(error_animation, height=150, key="error")
            st.error("⚠️ Unexpected API response format. Please check the response structure.")

    except requests.exceptions.RequestException as e:
        st_lottie(error_animation, height=150, key="error_request")
        st.error(f"❌ API Request Failed: {e}")

    except json.JSONDecodeError:
        st_lottie(error_animation, height=150, key="error_json")
        st.error("⚠️ Failed to parse JSON response. Check API output.")


# import streamlit as st
# import requests
# import json
# import os

# # Azure ML Endpoint Details
# API_URL = "http://d8a72203-fb49-44da-b92a-e0c59e31cf58.eastus2.azurecontainer.io/score"
# API_KEY = "EARVG8B19Eudr8j2GfVF5i2gfkzuRCEm"

# # Streamlit UI
# st.title("🚗 CAR RESALE PRICE PREDICTOR")

# st.markdown("Enter the car details to predict its resale price.")

# # User Inputs
# make = st.selectbox("Make", ["alfa-romero", "audi", "bmw", "chevrolet"])
# fuel_type = st.selectbox("Fuel Type", ["gas", "diesel"])
# body_style = st.selectbox("Body Style", ["convertible", "hatchback", "sedan", "wagon"])
# drive_wheels = st.selectbox("Drive Wheels", ["fwd", "rwd", "4wd"])
# engine_location = st.selectbox("Engine Location", ["front", "rear"])
# engine_type = st.selectbox("Engine Type", ["dohc", "ohc", "ohcv", "l", "rotor"])
# num_of_cylinders = st.selectbox("Number of Cylinders", [3, 4, 5, 6, 8])
# engine_size = st.number_input("Engine Size", min_value=60, max_value=400, value=109)
# fuel_system = st.selectbox("Fuel System", ["mpfi", "2bbl", "mfi", "spfi"])
# compression_ratio = st.number_input("Compression Ratio", min_value=7.0, max_value=12.0, value=10.0)
# horsepower = st.number_input("Horsepower", min_value=40, max_value=300, value=102)
# peak_rpm = st.number_input("Peak RPM", min_value=3000, max_value=7000, value=5500)
# city_mpg = st.number_input("City MPG", min_value=10, max_value=60, value=24)
# highway_mpg = st.number_input("Highway MPG", min_value=10, max_value=80, value=30)

# symboling = st.number_input("Symboling", min_value=-2, max_value=3, value=0)
# normalized_losses = st.number_input("Normalized Losses", min_value=50, max_value=300, value=120)
# width = st.number_input("Width", min_value=50.0, max_value=80.0, value=65.4)
# aspiration = st.selectbox("Aspiration", ["std", "turbo"])
# bore = st.number_input("Bore", min_value=2.5, max_value=4.0, value=3.31)
# num_of_doors = st.selectbox("Number of Doors", ["two", "four"])
# curb_weight = st.number_input("Curb Weight", min_value=1500, max_value=4000, value=2500)
# length = st.number_input("Length", min_value=140.0, max_value=200.0, value=170.2)
# stroke = st.number_input("Stroke", min_value=2.0, max_value=4.5, value=3.39)
# height = st.number_input("Height", min_value=45.0, max_value=70.0, value=54.3)
# wheel_base = st.number_input("Wheel Base", min_value=85.0, max_value=120.0, value=102.7)

# # Predict Button
# if st.button("Predict Resale Price"):
#     data = {
#     "Inputs": {
#         "WebServiceInput0": [
#             {
#                     "symboling": symboling,
#                     "normalized-losses": normalized_losses,
#                     "make": make,
#                     "fuel-type": fuel_type,
#                     "body-style": body_style,
#                     "drive-wheels": drive_wheels,
#                     "engine-location": engine_location,
#                     "engine-type": engine_type,
#                     "num-of-cylinders": int(num_of_cylinders),
#                     "engine-size": engine_size,
#                     "fuel-system": fuel_system,
#                     "compression-ratio": compression_ratio,
#                     "horsepower": horsepower,
#                     "peak-rpm": peak_rpm,
#                     "city-mpg": city_mpg,
#                     "highway-mpg": highway_mpg,
#                     "width": width,
#                     "aspiration": aspiration,
#                     "bore": bore,
#                     "num-of-doors": num_of_doors,
#                     "curb-weight": curb_weight,
#                     "length": length,
#                     "stroke": stroke,
#                     "height": height,
#                     "wheel-base": wheel_base
#             }
#         ]
#      }
#     }


#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=data)
#         response.raise_for_status()  # Raise error if request failed
#         result = response.json()
        
#         st.write("🔍 API Response:", result)  # Debugging line

#         if isinstance(result, dict) and "Results" in result:
#             try:
#                 predicted_price = result["Results"]["WebServiceOutput0"][0]["predicted_price"]
#                 st.success(f"🚘 Predicted Resale Price: **${predicted_price:,.2f}**")
#             except (KeyError, IndexError, TypeError):
#                 st.error("⚠️ Error: Unexpected response structure. Check API output.")
#         else:
#             st.error("⚠️ Error: Response format incorrect. Check API response.")

#     except requests.exceptions.RequestException as e:
#         st.error(f"🔴 API Request Failed: {e}")

#     except json.JSONDecodeError:
#         st.error("⚠️ Failed to parse JSON response. Check API output.")