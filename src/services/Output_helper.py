import pandas as pd
import services.github_api as gh
from datetime import datetime
import os

# Function for creating an Excel output
def create_excel_report(owner, token):
    data = gh.get_full_data(owner, token)
    df = pd.DataFrame(data)
    
    # Using timestamp for unique report_name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # creating the output folder
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Fullpath
    report_name = f"report_{timestamp}.xlsx"
    file_path = os.path.join(output_dir, report_name)
    
    # Output
    df.to_excel(file_path, index=False)
