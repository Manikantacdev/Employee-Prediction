"""
Script to fix the XGBoost model by re-saving it with the current version.
This resolves the serialization warning and loading issues.
"""
import pickle
import os
import warnings

warnings.filterwarnings('ignore')

print("=" * 60)
print("XGBoost Model Fix Script")
print("=" * 60)

# Load the old model
model_path = 'gwp.pkl'
print(f"\n1. Loading model from: {model_path}")

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("   ✓ Model loaded successfully")
    print(f"   Model type: {type(model)}")
except Exception as e:
    print(f"   ✗ Error loading model: {e}")
    exit(1)

# Check if it's an XGBoost model
try:
    model_type = type(model).__name__
    print(f"   Model class: {model_type}")
    
    # Try to get XGBoost version info
    if hasattr(model, 'get_xgb_params'):
        print("   XGBoost model detected")
except Exception as e:
    print(f"   Warning: {e}")

# Create backup
backup_path = 'gwp_backup.pkl'
print(f"\n2. Creating backup: {backup_path}")
try:
    with open(model_path, 'rb') as f_in:
        with open(backup_path, 'wb') as f_out:
            f_out.write(f_in.read())
    print("   ✓ Backup created")
except Exception as e:
    print(f"   ✗ Error creating backup: {e}")
    exit(1)

# Re-save the model with current pickle protocol
print(f"\n3. Re-saving model with updated serialization...")
try:
    # If it's an XGBoost model, save using both methods
    if hasattr(model, 'save_model'):
        # XGBoost native format (recommended)
        xgb_path = 'gwp.json'
        model.save_model(xgb_path)
        print(f"   ✓ Saved in XGBoost native format: {xgb_path}")
    
    # Re-pickle with current protocol
    with open(model_path, 'wb') as f:
        pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"   ✓ Re-saved as pickle: {model_path}")
    
except Exception as e:
    print(f"   ✗ Error re-saving model: {e}")
    print("   Restoring backup...")
    with open(backup_path, 'rb') as f_in:
        with open(model_path, 'wb') as f_out:
            f_out.write(f_in.read())
    exit(1)

# Verify the new model works
print(f"\n4. Verifying re-saved model...")
try:
    with open(model_path, 'rb') as f:
        test_model = pickle.load(f)
    print("   ✓ Model loads successfully")
    
    # Test prediction with sample data
    test_data = [[2, 1, 2, 3, 0.8, 15.5, 5000, 100, 0.0, 0, 0, 50.0, 2]]
    prediction = test_model.predict(test_data)
    print(f"   ✓ Prediction test successful: {prediction[0]:.4f}")
    
except Exception as e:
    print(f"   ✗ Error verifying model: {e}")
    print("   Restoring backup...")
    with open(backup_path, 'rb') as f_in:
        with open(model_path, 'wb') as f_out:
            f_out.write(f_in.read())
    exit(1)

print("\n" + "=" * 60)
print("✓ Model fixed successfully!")
print("=" * 60)
print("\nThe model has been re-saved with current XGBoost version.")
print("You can now deploy it without serialization warnings.")
print(f"\nBackup saved as: {backup_path}")
print("\nNext steps:")
print("  1. Test locally: python app.py")
print("  2. Commit changes: git add gwp.pkl")
print("  3. Push to deploy: git push")
