from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import os
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

import hashlib
import json
import sys
import traceback

app = Flask(__name__)

# Get absolute paths for deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

print(f"Base directory: {BASE_DIR}")
print(f"Project root: {PROJECT_ROOT}")

# Load model - Try JSON format first (better for deployment), then fallback to pickle
model = None
model_type = None

try:
    import xgboost as xgb
    
    # Try JSON format first (recommended for production)
    json_model_path = os.path.join(BASE_DIR, 'gwp.json')
    pkl_model_path = os.path.join(BASE_DIR, 'gwp.pkl')
    
    if os.path.exists(json_model_path) and os.path.getsize(json_model_path) > 100:
        print(f"Loading model from JSON: {json_model_path}")
        model = xgb.Booster()
        model.load_model(json_model_path)
        model_type = 'json'
        print(f"✓ Model loaded successfully from JSON format!")
        
        # Test with dummy data
        test_data = xgb.DMatrix(np.array([[2, 1, 2, 3, 0.8, 15.5, 5000, 100, 0.0, 0, 0, 50.0, 2]]))
        test_pred = model.predict(test_data)
        print(f"✓ Model test prediction: {test_pred[0]:.4f}")
        
    elif os.path.exists(pkl_model_path):
        print(f"JSON not found, loading model from pickle: {pkl_model_path}")
        
        # Suppress XGBoost serialization warnings for old models
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=UserWarning)
            with open(pkl_model_path, 'rb') as f:
                model = pickle.load(f)
        
        model_type = 'pickle'
        
        if model is None:
            raise ValueError("Model loaded as None")
        
        print(f"✓ Model loaded successfully from pickle! Type: {type(model).__name__}")
        
        # Test with dummy data
        test_pred = model.predict([[2, 1, 2, 3, 0.8, 15.5, 5000, 100, 0.0, 0, 0, 50.0, 2]])
        print(f"✓ Model test prediction: {test_pred[0]:.4f}")
    else:
        raise FileNotFoundError(f"No model file found (tried {json_model_path} and {pkl_model_path})")
        
except Exception as e:
    print(f"✗ ERROR loading model: {str(e)}")
    traceback.print_exc()
    model = None
    model_type = None

# Load dataset once at startup with error handling
try:
    dataset_path = os.path.join(PROJECT_ROOT, 'Dataset', 'garments_worker_productivity.csv')
    print(f"Loading dataset from: {dataset_path}")
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}")
    data = pd.read_csv(dataset_path)
    print(f"Dataset loaded successfully! Shape: {data.shape}")
except Exception as e:
    print(f"ERROR loading dataset: {str(e)}")
    traceback.print_exc()
    data = None

# Create static directory for saving graphs with proper permissions
static_dir = os.path.join(BASE_DIR, 'static')
try:
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
        print(f"Created static directory: {static_dir}")
    # Test write permissions
    test_file = os.path.join(static_dir, 'test_write.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print("Static directory is writable!")
except Exception as e:
    print(f"ERROR with static directory: {str(e)}")
    traceback.print_exc()

# Cache for generated graphs to improve performance
graph_cache = {}

def generate_cache_key(input_data_dict, predicted_value):
    """Generate unique cache key based on input parameters"""
    # Convert numpy types to Python native types for JSON serialization
    cache_data = {**input_data_dict, 'predicted_value': round(float(predicted_value), 4)}
    cache_string = json.dumps(cache_data, sort_keys=True)
    return hashlib.md5(cache_string.encode()).hexdigest()

# Dynamic graph generation functions
def generate_dynamic_correlation_heatmap(input_data_dict):
    """Generate correlation heatmap with submitted data highlighted"""
    plt.figure(figsize=(10, 8))
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    corrMatrix = data[numeric_cols].corr()
    sns.heatmap(corrMatrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Feature Correlation Heatmap (Your Data Context)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    heatmap_path = os.path.join(static_dir, 'correlation_heatmap.png')
    plt.savefig(heatmap_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'correlation_heatmap.png'

def generate_dynamic_productivity_distribution(predicted_value):
    """Generate productivity distribution with submitted data marked"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data['actual_productivity'], bins=30, kde=True, color='skyblue', alpha=0.6)
    plt.axvline(x=predicted_value, color='red', linestyle='--', linewidth=2, label=f'Your Prediction: {predicted_value:.3f}')
    plt.title('Productivity Distribution - Your Position', fontsize=16, fontweight='bold')
    plt.xlabel('Actual Productivity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    dist_path = os.path.join(static_dir, 'productivity_distribution.png')
    plt.savefig(dist_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'productivity_distribution.png'

def generate_dynamic_department_productivity(department_id, predicted_value):
    """Generate department-wise productivity with submitted department highlighted"""
    plt.figure(figsize=(10, 6))
    dept_prod = data.groupby('department')['actual_productivity'].mean().sort_values()
    colors = ['red' if dept == department_id else 'coral' for dept in dept_prod.index]
    dept_prod.plot(kind='barh', color=colors)
    plt.axvline(x=predicted_value, color='blue', linestyle='--', linewidth=2, alpha=0.7, label=f'Your Prediction: {predicted_value:.3f}')
    plt.title('Average Productivity by Department (Your Dept in Red)', fontsize=16, fontweight='bold')
    plt.xlabel('Average Productivity')
    plt.ylabel('Department')
    plt.legend()
    plt.tight_layout()
    dept_path = os.path.join(static_dir, 'department_productivity.png')
    plt.savefig(dept_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'department_productivity.png'

def generate_dynamic_overtime_productivity(overtime_value, predicted_value):
    """Generate overtime vs productivity with submitted data point highlighted"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='over_time', y='actual_productivity', alpha=0.4, color='green', s=50)
    plt.scatter(overtime_value, predicted_value, color='red', s=200, marker='*', 
                edgecolors='black', linewidth=2, label='Your Data', zorder=5)
    plt.title('Overtime vs Productivity (Your Data: Red Star)', fontsize=16, fontweight='bold')
    plt.xlabel('Over Time (minutes)')
    plt.ylabel('Actual Productivity')
    plt.legend()
    plt.tight_layout()
    overtime_path = os.path.join(static_dir, 'overtime_productivity.png')
    plt.savefig(overtime_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'overtime_productivity.png'

def generate_dynamic_incentive_impact(incentive_value, predicted_value):
    """Generate incentive impact with submitted data highlighted"""
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='incentive', y='actual_productivity', palette='Set2')
    
    # Add scatter for user's data
    plt.scatter(incentive_value, predicted_value, color='red', s=200, marker='D', 
                edgecolors='black', linewidth=2, label='Your Data', zorder=5)
    plt.title('Impact of Incentive on Productivity (Your Data: Red Diamond)', fontsize=16, fontweight='bold')
    plt.xlabel('Incentive')
    plt.ylabel('Actual Productivity')
    plt.legend()
    plt.tight_layout()
    incentive_path = os.path.join(static_dir, 'incentive_impact.png')
    plt.savefig(incentive_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'incentive_impact.png'

def generate_dynamic_team_productivity(team_id, num_workers, predicted_value):
    """Generate team size vs productivity with submitted data highlighted"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='no_of_workers', y='actual_productivity', hue='team', 
                   alpha=0.4, palette='viridis', s=50, legend=False)
    plt.scatter(num_workers, predicted_value, color='red', s=200, marker='*', 
                edgecolors='black', linewidth=2, label=f'Your Team {team_id}', zorder=5)
    plt.title('Team Size vs Productivity (Your Team: Red Star)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Workers')
    plt.ylabel('Actual Productivity')
    plt.legend()
    plt.tight_layout()
    team_path = os.path.join(static_dir, 'team_productivity.png')
    plt.savefig(team_path, dpi=100, bbox_inches='tight')
    plt.close()
    return 'team_productivity.png'
    plt.ylabel('Actual Productivity')
    plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    team_path = os.path.join(static_dir, 'team_productivity.png')
    plt.savefig(team_path, dpi=100, bbox_inches='tight')
    plt.close()
@app.route("/")
def about():
    return render_template('home.html')

@app.route("/about")
def home():
    return render_template('about.html')

@app.route("/predict")
def home1():
    return render_template('predict.html')

@app.route("/submit")
def home2():
    return render_template('submit.html')

@app.route("/pred", methods=['POST'])
def predict():
    try:
        # Check if model and data are loaded
        if model is None:
            raise Exception("Model failed to load during startup. Check server logs.")
        if data is None:
            raise Exception("Dataset failed to load during startup. Check server logs.")
        
        # Extract form data
        quarter = int(request.form['quarter'])
        department = int(request.form['department'])
        day = int(request.form['day'])
        team = int(request.form['team'])
        targeted_productivity = float(request.form['targeted_productivity'])
        smv = float(request.form['smv'])
        over_time = int(request.form['over_time'])
        incentive = int(request.form['incentive'])
        idle_time = float(request.form['idle_time'])
        idle_men = int(request.form['idle_men'])
        no_of_style_change = int(request.form['no_of_style_change'])
        no_of_workers = float(request.form['no_of_workers'])
        month = int(request.form['month'])
        
        print(f"Received form data: quarter={quarter}, dept={department}, day={day}, team={team}")
        
        # Prepare data for model prediction
        total = [[quarter, department, day, team, targeted_productivity, smv, over_time, 
                  incentive, idle_time, idle_men, no_of_style_change, no_of_workers, month]]
        
        # Create input data dictionary for graph generation and caching
        input_data_dict = {
            'quarter': quarter,
            'department': department,
            'day': day,
            'team': team,
            'targeted_productivity': targeted_productivity,
            'smv': smv,
            'over_time': over_time,
            'incentive': incentive,
            'idle_time': idle_time,
            'idle_men': idle_men,
            'no_of_style_change': no_of_style_change,
            'no_of_workers': no_of_workers,
            'month': month
        }
        
        print("Input data:", total)
        
        # Make prediction - handle both JSON and pickle model types
        try:
            if model_type == 'json':
                # XGBoost JSON format requires DMatrix
                import xgboost as xgb
                dmatrix = xgb.DMatrix(np.array(total))
                prediction = model.predict(dmatrix)
            else:
                # Standard pickle format (scikit-learn interface)
                prediction = model.predict(total)
            
            predicted_value = float(prediction[0])
            print(f"Prediction successful ({model_type} format): {predicted_value}")
        except Exception as pred_error:
            print(f"Prediction error: {str(pred_error)}")
            traceback.print_exc()
            raise Exception(f"Model prediction failed: {str(pred_error)}")
        
        # Determine productivity level
        if predicted_value <= 0.3:
            text = 'The employee is averagely productive.'
            productivity_class = 'average'
        elif predicted_value > 0.3 and predicted_value <= 0.8:
            text = 'The employee is medium productive.'
            productivity_class = 'medium'
        else:
            text = 'The employee is highly productive.'
            productivity_class = 'high'
        
        # Generate dynamic graphs based on submitted data
        print("Generating dynamic analysis graphs...")
        graphs = []
        
        try:
            # Check cache first for performance optimization
            cache_key = generate_cache_key(input_data_dict, predicted_value)
            
            if cache_key in graph_cache:
                print(f"Using cached graphs for request (cache key: {cache_key[:8]}...)")
                graphs = graph_cache[cache_key]
            else:
                # Generate fresh graphs for this specific data submission
                print("Generating new graphs...")
                try:
                    graphs.append(generate_dynamic_correlation_heatmap(input_data_dict))
                    print("Generated correlation heatmap")
                except Exception as e:
                    print(f"Error generating correlation heatmap: {str(e)}")
                
                try:
                    graphs.append(generate_dynamic_productivity_distribution(predicted_value))
                    print("Generated productivity distribution")
                except Exception as e:
                    print(f"Error generating productivity distribution: {str(e)}")
                
                try:
                    graphs.append(generate_dynamic_department_productivity(department, predicted_value))
                    print("Generated department productivity")
                except Exception as e:
                    print(f"Error generating department productivity: {str(e)}")
                
                try:
                    graphs.append(generate_dynamic_overtime_productivity(over_time, predicted_value))
                    print("Generated overtime productivity")
                except Exception as e:
                    print(f"Error generating overtime productivity: {str(e)}")
                
                try:
                    graphs.append(generate_dynamic_incentive_impact(incentive, predicted_value))
                    print("Generated incentive impact")
                except Exception as e:
                    print(f"Error generating incentive impact: {str(e)}")
                
                try:
                    graphs.append(generate_dynamic_team_productivity(team, no_of_workers, predicted_value))
                    print("Generated team productivity")
                except Exception as e:
                    print(f"Error generating team productivity: {str(e)}")
                
                print(f"Successfully generated {len(graphs)} dynamic graphs")
                
                # Cache the results (limit cache size to prevent memory issues)
                if len(graph_cache) > 100:  # Keep only last 100 unique predictions
                    # Remove oldest entry
                    graph_cache.pop(next(iter(graph_cache)))
                if graphs:  # Only cache if we have graphs
                    graph_cache[cache_key] = graphs
                    
        except Exception as graph_error:
            print(f"Error in graph generation process: {str(graph_error)}")
            traceback.print_exc()
            # Continue without graphs
            graphs = []
        
        print(f"Returning results with {len(graphs)} graphs")
        return render_template('submit.html', 
                             prediction_text=text,
                             prediction_value=round(predicted_value, 4),
                             productivity_class=productivity_class,
                             graphs=graphs)
                             
    except Exception as e:
        error_msg = str(e)
        print(f"Error in prediction: {error_msg}")
        traceback.print_exc()
        
        # Return more detailed error message
        return render_template('submit.html', 
                             prediction_text=f'Error in prediction: {error_msg}',
                             prediction_value=0,
                             productivity_class='error',
                             graphs=[])

# For Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
