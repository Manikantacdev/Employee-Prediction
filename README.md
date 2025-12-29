# 🏭 Employee Performance Prediction System

> **New "Acid Void" Aesthetic Update** - High-contrast, futuristic design system.

A machine learning-based web application to predict garment worker productivity using historical data. This project helps manufacturers optimize workforce planning and identify factors affecting employee performance.

## 📋 Table of Contents
- [Overview](#overview)
- [New Features](#new-features)
- [Project Structure](#project-structure)
- [Dataset Information](#dataset-information)
- [Installation & Setup](#installation--setup)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [Technologies Used](#technologies-used)

## 🎯 Overview

This project predicts employee productivity in garment manufacturing using machine learning algorithms. The system analyzes various factors like:
- Team performance metrics
- Work hours and overtime
- Incentives
- Department efficiency
- Style changes and complexity

The Flask web application provides an intuitive interface with a **custom "Acid Void" design system** (Dark Mode + Acid Lime accents), offering instant productivity predictions and dynamic visual analytics.

## ✨ New Features (v2.0)

- **Acid Void Aesthetic**: A completely custom, high-contrast dark theme designed for visual impact.
- **Modern UI Components**: Bento grid layouts, glassmorphism, and animated transitions.
- **Python 3.12 Support**: Updated environment for better performance and security.
- **Production Ready**: Configured with `waitress` for production serving.
- **Dynamic Visualizations**: Real-time charts showing:
  - Correlation heatmaps
  - Productivity distributions
  - Department-wise comparisons
  - Overtime impact analysis
  - Incentive effectiveness

## 📁 Project Structure

```
Employee Performance Prediction/
├── Dataset/
│   └── garments_worker_productivity.csv    # Training dataset
├── Flask/
│   ├── app.py                              # Dev Flask application
│   ├── production_server.py                # Production server (Waitress)
│   ├── gwp.pkl                             # Trained ML model
│   ├── templates/                          # HTML templates (Refactored)
│   │   ├── home.html
│   │   ├── predict.html
│   │   ├── submit.html
│   │   └── about.html
│   └── static/
│       └── css/
│           └── style.css                   # Global Acid Void stylesheet
├── requirements.txt                        # Python dependencies
├── render.yaml                             # Render deployment config
└── README.md                               # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- Git

### Step 1: Clone the Project
```bash
git clone https://github.com/yourusername/employee-performance-prediction.git
cd "Employee Performance Prediction"
```

### Step 2: Set Up Virtual Environment
```bash
# Windows
py -3.12 -m venv venv
.\venv\Scripts\Activate

# Mac/Linux
python3.12 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

**Development Mode:**
```bash
cd Flask
python app.py
```

**Production Mode:**
```bash
cd Flask
python production_server.py
```

Access at `http://localhost:8080` (Production) or `http://localhost:5000` (Dev).

## ☁️ Deployment

### Recommended: Render (Free Tier)

This project includes a `render.yaml` for automatic deployment.

1. Push your code to GitHub.
2. Sign up at [Render.com](https://render.com).
3. Create a **New Web Service** and connect your repo.
4. Render will auto-detect the configuration and deploy.

**Manual Configuration on Render:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python production_server.py`
- **Environment Variable**: `PYTHON_VERSION` = `3.12.0`

## � Usage Guide

1. **Home Page**: Experience the new hero section and bento grid features.
2. **Predict**: Use the "Control Panel" style form to input employee data.
3. **Analyze**: View high-contrast result dashboards with inverted charts for dark mode compatibility.

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3 (Acid Void Design System), FontAwesome, Google Fonts (Unbounded, Plus Jakarta Sans)
- **Backend**: Python 3.12, Flask, Waitress
- **Machine Learning**: XGBoost, Scikit-learn, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn

## � Model Performance

The machine learning model (XGBoost/Random Forest) was trained on historical data to predict productivity with high accuracy, analyzing over 1198 records.

---

**Happy Predicting! 🎉**
