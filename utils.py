import pandas as pd
import re


def drop_columns_from_df(df: pd.Series) -> pd.Series:
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


def constrain_value(value):
    return value if value <= 730 else 730


def parse_excel_report(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert time columns to datetime once
    df['Meter Begin Time (UTC+05:00)'] = pd.to_datetime(
        df['Meter Begin Time (UTC+05:00)'])
    df['Meter End Time (UTC+05:00)'] = pd.to_datetime(df['Meter End Time (UTC+05:00)'])

    # Calculate usage duration for all rows at once and truncate to 2 decimal places
    df['Usage Duration'] = ((df['Meter End Time (UTC+05:00)'] -
                            df['Meter Begin Time (UTC+05:00)']).dt.total_seconds() / 3600).round(2).map(constrain_value)

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
                    for _, row in rt_group_cluster.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        instances_list.append(
                            {**drop_columns_from_df(row).to_dict(), **parsed_metrics, 'Service Type': 'clustered'})

                if len(rt_group_dedicated) > 0:
                    for _, row in rt_group_dedicated.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        instances_list.append(
                            {**drop_columns_from_df(row).to_dict(), **parsed_metrics, 'Service Type': 'dedicated'})

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
                        for _, row in rt_group_ssd.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'Service Type': 'clustered', 'Storage Type': 'ssd'})

                    if len(rt_group_hdd) > 0:
                        for _, row in rt_group_hdd.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'Service Type': 'clustered', 'Storage Type': 'hdd'})

                if len(rt_group_dedicated) > 0:
                    # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                    rt_group_ssd = rt_group_dedicated[rt_group_dedicated['Metering Metric'].str.lower(
                    ).str.contains('ssd', na=False)]
                    rt_group_hdd = rt_group_dedicated[rt_group_dedicated['Metering Metric'].str.lower(
                    ).str.contains('sata', na=False)]

                    if len(rt_group_ssd) > 0:
                        for _, row in rt_group_ssd.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'Service Type': 'dedicated', 'Storage Type': 'ssd'})

                    if len(rt_group_hdd) > 0:
                        for _, row in rt_group_hdd.iterrows():
                            instances_list.append(
                                {**drop_columns_from_df(row).to_dict(), 'Service Type': 'dedicated', 'Storage Type': 'hdd'})
            else:
                for _, row in rt_group.iterrows():
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


def validate_po_data(data):
    if not data.get('user-info') or data['user-info']['name'] == '' or data['user-info']['email'] == '':
        return (False, "User info is required")

    if len(data['services']) == 0:
        return (False, "Services are required")

    if '@' not in data['user-info']['email']:
        return (False, "Invalid email")

    return (True, None)

