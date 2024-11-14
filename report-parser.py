import pandas as pd
from flask import Flask, request, jsonify
import os

def parse_excel_report(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Create a dictionary with VDC IDs as keys and corresponding rows as values
    result = {}
    for region in df['Region'].unique():
        vdc_data = df[df['Region'] == region]
        result[region] = {}
        
        for resource_type in vdc_data['Resource Type'].unique():
            resource_type_items = vdc_data[vdc_data['Resource Type'] == resource_type]
            result[region][resource_type] = {}
            
            for resource_id in resource_type_items['Resource ID'].unique():
            
                resource_id_items = resource_type_items[resource_type_items['Resource ID'] == resource_id]
                temp_item = None
                if len(resource_id_items) > 1:
                    for _index, resource_id_item in resource_id_items.iterrows():
                        begin_time = pd.to_datetime(resource_id_item['Meter Begin Time (UTC+05:00)'])
                        end_time = pd.to_datetime(resource_id_item['Meter End Time (UTC+05:00)'])
                        usage_duration = (end_time - begin_time).total_seconds() / 3600  # Convert to hours
                        resource_id_item['Usage Duration'] = usage_duration
                        if temp_item is None or usage_duration > temp_item['Usage Duration']:
                            temp_item = resource_id_item.to_dict()
                else:
                    temp_item = resource_id_items.to_dict('records')[0]

                result[region][resource_type][resource_id] = temp_item

    return result

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'uploads')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'))
        file_path = os.path.join(os.path.dirname(__file__), 'uploads', file.filename)
        file.save(file_path)
        parsed_report_data = parse_excel_report(file_path)
        return parsed_report_data

if __name__ == "__main__":
    app.run(debug=True)