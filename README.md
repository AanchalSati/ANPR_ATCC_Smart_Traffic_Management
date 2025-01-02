# 🚗✨ ANPR and ATCC for Smart Traffic Management

## 🎀 Project Overview
This project implements an intelligent traffic management system utilizing **Automatic Number Plate Recognition (ANPR)** and **Automatic Traffic Classification and Control (ATCC)**. By leveraging Deep Learning and Object Detection techniques, the system automates traffic monitoring and control in smart city environments.

### 🌟 Key Features
- 📋 **Automatic Number Plate Recognition (ANPR)**
- 🚥 **Automatic Traffic Classification and Control (ATCC)**
- 📉 **Data interpolation for accurate tracking**
- 🎥 **Visualization capabilities**

### 🎬 Results
You can find the result video at this location:  
📂 **"Provide the link to the output video here."**

---

## 🏗️ Project Structure
├── CV_Basics/                                     # Computer vision and OCR learning materials 
├── data/                                          # Input data and videos 
├── number_plate_detection_model_training/         # Model training files 
├── object_tracker/                                # Main detection and vehicle tracking code 
├── output_videos/                                 # Generated output videos 
├── output/                                        # Initial detection CSV files 
├── main_1.py                                      # Main execution file (old) 
├── add_missing_data.py                            # Data interpolation script 
├── main.py                                        # Main execution file 
├── requirements.txt                               # Project dependencies 
└── visualize.py                                   # Video visualization script

---

## 🚀 Workflow
1. 🏎️ **Execute `main.py`**  
   Perform initial vehicle detection and generate a CSV file in the `output/` directory.

2. 📈 **Run `add_missing_data.py`**  
   Perform data interpolation and generate an enhanced CSV file in the `output/` directory.

3. 🎥 **Run `visualize.py`**  
   Create a visualization video using interpolated data, saved in the `output_video/` directory.

---

## 🛠️ Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AanchalSati/ANPR_ATCC_Smart_Traffic_Management.git
   cd anpr-atcc-traffic-management
   
2. Create and activate a virtual environment (recommended):
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
bash
pip install -r requirements.txt

4. Configure environment variables:
Create a copy of .env.example (if provided) and rename it to .env.
Update the necessary secret keys and configurations.

🏃‍♂️ Running the Project
Replace the path to your input video and your desired output directory.

Run the main detection:

python main.py
Perform data interpolation:
python add_missing_data.py
Generate visualization:
python visualize.py

