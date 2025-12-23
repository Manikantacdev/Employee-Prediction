"""
Convert the pickled XGBoost model to native JSON format for better deployment compatibility.
This solves Render deployment issues with pickle serialization.
"""
import pickle
import os
import warnings

warnings.filterwarnings('ignore')

print("=" * 70)
print("Converting Model to XGBoost Native JSON Format")
print("=" * 70)

# Step 1: Load the existing pickle model
model_path = 'gwp.pkl'
json_path = 'gwp.json'

print(f"\n[1/4] Loading pickle model from: {model_path}")

if not os.path.exists(model_path):
    print(f"✗ Error: {model_path} not found!")
    print("\nYou need to train the model first using:")
    print("  TrainingFiles/Employee_Prediction.ipynb")
    exit(1)

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f"✓ Model loaded successfully")
    print(f"  Type: {type(model).__name__}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit(1)

# Step 2: Verify it's an XGBoost model
print(f"\n[2/4] Verifying model type...")

model_type = type(model).__name__
if not hasattr(model, 'save_model'):
    print(f"✗ Error: Model is {model_type}, not XGBoost")
    print("  This script only works with XGBoost models")
    exit(1)

print(f"✓ Confirmed XGBoost model")

# Step 3: Test prediction before conversion
print(f"\n[3/4] Testing model prediction...")

try:
    test_data = [[2, 1, 2, 3, 0.8, 15.5, 5000, 100, 0.0, 0, 0, 50.0, 2]]
    prediction = model.predict(test_data)
    print(f"✓ Test prediction successful: {prediction[0]:.4f}")
except Exception as e:
    print(f"✗ Prediction failed: {e}")
    exit(1)

# Step 4: Save in JSON format
print(f"\n[4/4] Saving model in JSON format: {json_path}")

try:
    # Save using XGBoost's native JSON format
    model.save_model(json_path)
    print(f"✓ Model saved successfully in JSON format")
    
    # Check file size
    size = os.path.getsize(json_path)
    print(f"  File size: {size:,} bytes ({size / 1024:.2f} KB)")
    
    # Verify the saved model
    print(f"\n[5/5] Verifying saved JSON model...")
    
    # For verification, we need to load it back
    import xgboost as xgb
    
    # Create a booster and load the JSON
    test_model = xgb.Booster()
    test_model.load_model(json_path)
    
    # Test prediction with the loaded model
    import numpy as np
    test_dmatrix = xgb.DMatrix(np.array(test_data))
    test_pred = test_model.predict(test_dmatrix)
    print(f"✓ Verification prediction: {test_pred[0]:.4f}")
    
    print("\n" + "=" * 70)
    print("✓ SUCCESS! Model converted to JSON format")
    print("=" * 70)
    print(f"\nCreated file: {json_path}")
    print("\nBenefits of JSON format:")
    print("  ✓ Platform-independent (works across Python versions)")
    print("  ✓ No pickle serialization warnings")
    print("  ✓ Better for cloud deployment (Render, AWS, Azure)")
    print("  ✓ Human-readable and debuggable")
    print("\nNext steps:")
    print("  1. The app.py will be updated to load from gwp.json")
    print("  2. Commit and push: git add Flask/gwp.json && git commit -m 'Add JSON model'")
    print("  3. Deploy to Render")
    
except Exception as e:
    print(f"✗ Error saving model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
