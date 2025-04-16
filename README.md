# Smart Gym Equipment Recommender

A personalized gym equipment recommendation system built using Streamlit, Power BI, Excel, and Python.

## Project Description
This app helps users discover gym equipment that best suits their personal needs based on:
- Age
- Gender
- Fitness goals
- Health conditions
- Budget
- Impact level preference (Low/Medium/High)

The system filters a master dataset and suggests equipment accordingly, offering a customized experience for both beginners and fitness enthusiasts.

---

## Features
- Interactive web app using **Streamlit**
- Reads and processes data from **Excel**
- Recommends equipment using multiple filters (goal, health, age, budget, impact)
- Visualization dashboard in **Power BI**

---

## Tech Stack
- **Python**: Core logic and filtering
- **Streamlit**: Frontend web application
- **Excel**: Data storage and preprocessing
- **Power BI**: Visual analytics dashboard

---

## Files Included
- `smart_gym_recommender_cleaned.py`: Main Streamlit app
- `gym_equipment_master_dataset.xlsx`: Equipment database
- `requirements.txt`: Python packages
- `gym equipment recommender.pbix`: Power BI dashboard

---

## How to Run the App

### 1. Install required packages
```bash
pip install -r requirements.txt

### Run the Streamlit app
```bash
streamlit run smart_gym_recommender_cleaned.py

