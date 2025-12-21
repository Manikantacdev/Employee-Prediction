# 🏭 Employee Performance Prediction System

A machine learning-based web application to predict garment worker productivity using historical data. This project helps manufacturers optimize workforce planning and identify factors affecting employee performance.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Dataset Information](#dataset-information)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Example Data for Beginners](#example-data-for-beginners)
- [Understanding the Predictions](#understanding-the-predictions)
- [Technologies Used](#technologies-used)
- [Model Performance](#model-performance)

## 🎯 Overview

This project predicts employee productivity in garment manufacturing using machine learning algorithms. The system analyzes various factors like:
- Team performance metrics
- Work hours and overtime
- Incentives
- Department efficiency
- Style changes and complexity

The Flask web application provides an intuitive interface where users can input employee/team data and receive instant productivity predictions along with visual analytics.

## ✨ Features

- **Predictive Analytics**: Machine learning model to predict worker productivity
- **Interactive Web Interface**: User-friendly Flask application
- **Dynamic Visualizations**: Real-time charts showing:
  - Correlation heatmaps
  - Productivity distributions
  - Department-wise comparisons
  - Overtime impact analysis
  - Incentive effectiveness
- **Data-Driven Insights**: Understand factors affecting productivity
- **Beginner-Friendly**: Easy to understand and use

## 📁 Project Structure

```
Employee Performance Prediction/
├── Dataset/
│   └── garments_worker_productivity.csv    # Training dataset (1198 records)
├── Flask/
│   ├── app.py                              # Main Flask application
│   ├── gwp.pkl                             # Trained ML model (pickle file)
│   ├── run_app.bat                         # Windows batch file to run app
│   ├── templates/                          # HTML templates
│   │   ├── home.html                       # Landing page
│   │   ├── predict.html                    # Input form
│   │   ├── submit.html                     # Results page
│   │   └── about.html                      # Project information
│   └── static/                             # CSS and generated graphs
│       └── css/
├── TrainingFiles/
│   └── Employee_Prediction.ipynb           # Model training notebook
└── README.md                               # This file
```

## 📊 Dataset Information

The dataset contains **1198 records** of garment worker productivity with the following features:

### Features Description

| Feature | Description | Data Type | Example |
|---------|-------------|-----------|---------|
| **date** | Date of production | Date | 1/1/2015 |
| **quarter** | Quarter of the year | Categorical | Quarter1 |
| **department** | Department name | Categorical | sewing, finishing |
| **day** | Day of the week | Categorical | Thursday, Monday |
| **team** | Team number (1-12) | Numeric | 8 |
| **targeted_productivity** | Target set by management | Float (0-1) | 0.8 |
| **smv** | Standard Minute Value (time allocated) | Float | 26.16 |
| **wip** | Work in progress (units) | Integer | 1108 |
| **over_time** | Overtime in minutes | Integer | 7080 |
| **incentive** | Incentive amount (BDT) | Integer | 98 |
| **idle_time** | Idle time (minutes) | Integer | 0 |
| **idle_men** | Number of idle workers | Integer | 0 |
| **no_of_style_change** | Number of style changes | Integer | 0 |
| **no_of_workers** | Number of workers | Float | 59 |
| **actual_productivity** | Actual productivity achieved | Float (0-1) | 0.940 |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "d:\Py and ipynb\Employee Performance Prediction"
```

### Step 2: Install Required Libraries
```bash
pip install flask pandas numpy scikit-learn matplotlib seaborn xgboost
```

### Step 3: Verify Files
Ensure you have:
- `Flask/gwp.pkl` (trained model)
- `Dataset/garments_worker_productivity.csv` (dataset)
- `Flask/app.py` (web application)

### Step 4: Run the Application

**On Windows:**
```bash
cd Flask
python app.py
```
or simply double-click `run_app.bat`

**On Mac/Linux:**
```bash
cd Flask
python3 app.py
```

### Step 5: Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## 📖 Usage Guide

1. **Home Page**: Click "Get Started" or "Predict Productivity"
2. **Input Form**: Fill in the employee/team data
3. **Submit**: Click "Predict" to see results
4. **Results**: View prediction and interactive charts
5. **Insights**: Analyze the visualizations to understand performance factors

## 🎓 Example Data for Beginners

Here are **5 real examples** from the dataset to help you understand and test the application:

### Example 1: High Productivity Team (Sewing Department)
```
Month: 1 (January)
Quarter: Quarter 1
Department: Sewing
Day: Thursday
Team: 8
Targeted Productivity: 0.8
SMV: 26.16
WIP: 1108
Over Time: 7080
Incentive: 98
Idle Time: 0
Idle Men: 0
No of Style Change: 0
No of Workers: 59
```
**Expected Actual Productivity:** ~0.94 (Excellent performance with overtime and incentives)

---

### Example 2: Medium Productivity Team (Finishing Department)
```
Month: 1 (January)
Quarter: Quarter 1
Department: Finishing
Day: Thursday
Team: 1
Targeted Productivity: 0.75
SMV: 3.94
WIP: 0 (leave empty or 0)
Over Time: 960
Incentive: 0
Idle Time: 0
Idle Men: 0
No of Style Change: 0
No of Workers: 8
```
**Expected Actual Productivity:** ~0.89 (Good performance in finishing department)

---

### Example 3: Lower Productivity (No Incentive, Less Overtime)
```
Month: 1 (January)
Quarter: Quarter 1
Department: Finishing
Day: Thursday
Team: 11
Targeted Productivity: 0.7
SMV: 4.15
WIP: 0
Over Time: 1440
Incentive: 0
Idle Time: 0
Idle Men: 0
No of Style Change: 0
No of Workers: 12
```
**Expected Actual Productivity:** ~0.44 (Lower performance, factors: no incentive, lower target)

---


## 💡 Understanding the Predictions

### Productivity Scale
- **0.0 - 0.4**: Low productivity (needs improvement)
- **0.4 - 0.7**: Moderate productivity (acceptable)
- **0.7 - 0.85**: Good productivity (on target)
- **0.85 - 1.0**: Excellent productivity (exceeds expectations)

### Key Factors Affecting Productivity

1. **Targeted Productivity**: Higher targets often correlate with better performance
2. **Incentives**: Financial rewards typically improve output
3. **Over Time**: Moderate overtime can boost productivity, but excessive hours may reduce efficiency
4. **Department**: Different departments have varying baseline productivity levels
5. **Team Size (No of Workers)**: Optimal team size varies by task complexity
6. **Style Changes**: Frequent style changes can reduce productivity due to adjustment time
7. **Idle Time/Idle Men**: Direct negative impact on productivity

## 🛠️ Technologies Used

- **Python 3.x**: Core programming language
- **Flask**: Web framework for the application
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning library
- **XGBoost**: Gradient boosting algorithm
- **Matplotlib & Seaborn**: Data visualization
- **HTML/CSS**: Frontend design

## 📈 Model Performance

The machine learning model (Random Forest / XGBoost) was trained on historical data to predict productivity with:
- **Multiple algorithms tested**: Linear Regression, Random Forest, XGBoost
- **Feature engineering**: Label encoding for categorical variables
- **Performance metrics**: MSE, MAE, R² Score
- **Best model saved**: `gwp.pkl` (Garment Worker Productivity)

## 🎯 Tips for Best Results

1. **Data Quality**: Ensure all fields are filled accurately
2. **Realistic Values**: 
   - Productivity: 0.0 to 1.0
   - Overtime: Typically 0 to 10,000 minutes
   - Incentive: 0 to 150 BDT
   - Workers: 1 to 100
3. **Department Selection**: Use dropdown to choose between "Sewing" or "Finishing"
4. **Categorical Fields**: Month, Quarter, Department, and Day use dropdown menus for easy selection
5. **WIP Field**: Optional - can be left empty or set to 0
4. **Analyze Charts**: Look at the generated visualizations to understand your prediction context

## 🚦 Troubleshooting

**Issue**: Application won't start
- **Solution**: Ensure all required libraries are installed: `pip install flask pandas numpy scikit-learn matplotlib seaborn`

**Issue**: Model file not found
- **Solution**: Verify `gwp.pkl` exists in the Flask folder

**Issue**: Dataset not found
- **Solution**: Ensure `garments_worker_productivity.csv` is in the Dataset folder

## 📝 Next Steps for Learning

1. **Explore the Notebook**: Open `TrainingFiles/Employee_Prediction.ipynb` to see how the model was trained
2. **Modify Features**: Try adding new features or removing some to see the impact
3. **Experiment**: Test different values in the web application
4. **Analyze Patterns**: Study the charts to identify productivity patterns
5. **Improve Model**: Try different algorithms or hyperparameter tuning

## 📧 Support

For questions or issues:
- Review the example data above
- Check the troubleshooting section
- Examine the code comments in `app.py` and the notebook

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Predicting! 🎉**

*This project demonstrates how machine learning can be applied to real-world workforce management challenges.*
