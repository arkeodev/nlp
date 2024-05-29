import os
import sys
import json
from IPython.display import display
from ipywidgets import FileUpload

# Navigate to the root
repo_root = os.path.abspath('..')
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
kaggle_json_path = repo_root + '/helpers/kaggle/kaggle.json'

def setup_kaggle_api(file_content):
    # Save the uploaded file
    with open(kaggle_json_path, 'wb') as f:
        f.write(file_content)
    
    # Read the kaggle.json file
    with open(kaggle_json_path, 'r') as f:
        kaggle_token = json.load(f)
    
    # Set up environment variables for Kaggle API credentials
    os.environ['KAGGLE_USERNAME'] = kaggle_token['username']
    os.environ['KAGGLE_KEY'] = kaggle_token['key']
    
    print("Kaggle API credentials are set up successfully.")

def create_upload_widget():
    # Create a file upload widget
    upload_widget = FileUpload(accept='.json', multiple=False)

    def on_upload_change(change):
        # Ensure there's at least one file uploaded
        if not upload_widget.value:
            raise ValueError("No file uploaded.")
        
        # Get the uploaded file content
        uploaded_files = list(upload_widget.value)
        if len(uploaded_files) == 0:
            raise ValueError("No file content found.")
        
        uploaded_file = uploaded_files[0]
        
        # Check if the uploaded file is a dictionary and has the key 'content'
        if not isinstance(uploaded_file, dict) or 'content' not in uploaded_file:
            raise ValueError("Uploaded file is not valid or missing 'content'.")
        
        # Setup Kaggle API with the uploaded file content
        setup_kaggle_api(uploaded_file['content'])

    # Attach the callback function to the widget
    upload_widget.observe(on_upload_change, names='value')

    # Display the widget
    display(upload_widget)
