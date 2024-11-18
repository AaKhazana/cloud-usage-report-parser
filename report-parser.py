#!/usr/bin/env python3

import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re


def drop_columns_from_df(df: pd.Series):
    return df.drop(labels=[
        'Region', 'Resource Type', 'Tag', 'Tenant Name',
        'Tenant ID', 'VDC Name', 'VDC ID', 'Resource Space Name', 'Resource Space ID',
        'Enterprise Project ID', 'Metering Unit Name', 'Unit Price (PKR)', 'Unit',
        'Unit Price Unit', 'Fee (PKR)'
    ])


def parse_ecs_data(data_string):
    # regex to parse the metering metric string
    pattern = r"ECS-(\d+)\s*vCPUs?\s*\|?\s*(\d+)\s*(GiB|GB)?"

    match = re.search(pattern, data_string)

    if match:
        # Extract values and normalize memory unit if missing
        vcpus = int(match.group(1))
        memory = int(match.group(2))
        memory_unit = match.group(3) if match.group(3) else "GB"

        return {
            "vCPUs": vcpus,
            "Memory": memory,
            "MemoryUnit": memory_unit
        }
    else:
        return None


def parse_excel_report(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert time columns to datetime once
    df['Meter Begin Time (UTC+05:00)'] = pd.to_datetime(
        df['Meter Begin Time (UTC+05:00)'])
    df['Meter End Time (UTC+05:00)'] = pd.to_datetime(df['Meter End Time (UTC+05:00)'])

    # Calculate usage duration for all rows at once and truncate to 2 decimal places
    df['Usage Duration'] = ((df['Meter End Time (UTC+05:00)'] -
                            df['Meter Begin Time (UTC+05:00)']).dt.total_seconds() / 3600).round(2)

    # Create nested dictionary using groupby
    result = {'regions': []}
    for region, region_group in df.groupby('Region'):
        services_list = []
        for resource_type, rt_group in region_group.groupby('Resource Type'):
            instances_list = []

            if resource_type.lower() == 'ecs':
                # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                rt_group_cluster = rt_group[rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                # Filter rows where Tag doesn't contains 'cce' or 'cluster' (case-insensitive)
                rt_group_dedicated = rt_group[~rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                if len(rt_group_cluster) > 0:
                    max_duration_rows = rt_group_cluster.loc[rt_group_cluster.groupby(
                        'Resource ID')['Usage Duration'].idxmax()]
                    for _, row in max_duration_rows.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        instances_list.append(
                            {**drop_columns_from_df(row).to_dict(), **parsed_metrics, 'serviceType': 'clustered'})

                if len(rt_group_dedicated) > 0:
                    max_duration_rows = rt_group_dedicated.loc[rt_group_dedicated.groupby(
                        'Resource ID')['Usage Duration'].idxmax()]
                    for _, row in max_duration_rows.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        instances_list.append(
                            {**drop_columns_from_df(row).to_dict(), **parsed_metrics, 'serviceType': 'dedicated'})

            elif resource_type.lower() == 'evs':
                # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                rt_group_cluster = rt_group[rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                # Filter rows where Tag doesn't contains 'cce' or 'cluster' (case-insensitive)
                rt_group_dedicated = rt_group[~rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                if len(rt_group_cluster) > 0:
                    # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                    rt_group_ssd = rt_group_cluster[rt_group_cluster['Metering Metric'].str.lower(
                    ).str.contains('ssd', na=False)]
                    rt_group_hdd = rt_group_cluster[rt_group_cluster['Metering Metric'].str.lower(
                    ).str.contains('sata', na=False)]

                    if len(rt_group_ssd) > 0:
                        max_duration_rows = rt_group_ssd.loc[rt_group_ssd.groupby(
                            'Resource ID')['Usage Duration'].idxmax()]
                        for _, row in max_duration_rows.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'serviceType': 'clustered', 'storageType': 'ssd'})

                    if len(rt_group_hdd) > 0:
                        max_duration_rows = rt_group_hdd.loc[rt_group_hdd.groupby(
                            'Resource ID')['Usage Duration'].idxmax()]
                        for _, row in max_duration_rows.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'serviceType': 'clustered', 'storageType': 'hdd'})

                if len(rt_group_dedicated) > 0:
                    # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                    rt_group_ssd = rt_group_dedicated[rt_group_dedicated['Metering Metric'].str.lower(
                    ).str.contains('ssd', na=False)]
                    rt_group_hdd = rt_group_dedicated[rt_group_dedicated['Metering Metric'].str.lower(
                    ).str.contains('sata', na=False)]

                    if len(rt_group_ssd) > 0:
                        max_duration_rows = rt_group_ssd.loc[rt_group_ssd.groupby(
                            'Resource ID')['Usage Duration'].idxmax()]
                        for _, row in max_duration_rows.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'serviceType': 'dedicated', 'storageType': 'ssd'})

                    if len(rt_group_hdd) > 0:
                        max_duration_rows = rt_group_hdd.loc[rt_group_hdd.groupby(
                            'Resource ID')['Usage Duration'].idxmax()]
                        for _, row in max_duration_rows.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'serviceType': 'dedicated', 'storageType': 'hdd'})
            else:
                max_duration_rows = rt_group.loc[rt_group.groupby(
                    'Resource ID')['Usage Duration'].idxmax()]

                for _, row in max_duration_rows.iterrows():
                    instances_list.append(drop_columns_from_df(row).to_dict())

            services_list.append({
                'serviceName': resource_type,
                'instances': instances_list
            })

        result['regions'].append({
            'regionName': region,
            'services': services_list
        })

    return result


app = Flask(__name__)
CORS(app)


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
        file_path = os.path.join(os.path.dirname(
            __file__), 'uploads', file.filename)
        file.save(file_path)
        parsed_report_data = parse_excel_report(file_path)
        # delete the uploaded file
        os.remove(file_path)
        return parsed_report_data


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
