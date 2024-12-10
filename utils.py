import pandas as pd
import re
import sqlite
from constants import *


def trim_lower_normalize(string: str) -> str:
    return string.strip().lower().replace(" ", "-")


def drop_columns_from_df(df: pd.Series) -> pd.Series:
    return df.drop(labels=[
        'Region', 'Resource Type', 'Tag', 'Tenant Name',
        'Tenant ID', 'VDC Name', 'VDC ID', 'Resource Space Name', 'Resource Space ID',
        'Enterprise Project ID', 'Metering Unit Name', 'Unit Price (PKR)', 'Unit',
        'Unit Price Unit', 'Fee (PKR)'
    ])


def parse_ecs_data(data_string: str) -> dict | None:
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


def constrain_value(value, month):
    if month in MONTH_31_DAYS:
        if value >= HOURS_31_DAYS:
            return STANDARD_CLOUD_HOURS
        else:
            return value
    elif month in MONTH_30_DAYS:
        if value >= HOURS_30_DAYS:
            return STANDARD_CLOUD_HOURS
        else:
            return value
    elif month in MONTH_28_DAYS:
        if value >= HOURS_28_DAYS:
            return STANDARD_CLOUD_HOURS
        else:
            return value
    else:
        return value


def calculate_usage_cost(data: pd.Series, rt: ResourceType, storage_type: StorageType = None, service_tag: ServiceTag = None):
    db = sqlite.DatabaseService()
    query = "SELECT * FROM unit_costs"
    costs: list = db.run_query(query)
    usage_cost = 0
    if rt == ResourceType.ECS:
        if service_tag == ServiceTag.CLUSTERED:
            usage_cost = ((data['Memory'] * costs[1][4]) +
                          (data['vCPUs'] * costs[6][4])) * data['Usage Duration']
        elif service_tag == ServiceTag.DEDICATED:
            usage_cost = ((data['Memory'] * costs[1][4]) +
                          (data['vCPUs'] * costs[0][4])) * data['Usage Duration']
    elif rt == ResourceType.EVS:
        if storage_type == StorageType.SSD:
            usage_cost = (data['Usage'] * costs[3][4]) * data['Usage Duration']
        elif storage_type == StorageType.HDD:
            usage_cost = (data['Usage'] * costs[2][4]) * data['Usage Duration']
    elif rt == ResourceType.EIP:
        usage_cost = (data['Usage'] * costs[14][4]) * data['Usage Duration']
    elif rt == ResourceType.EIP_BANDWIDTH:
        usage_cost = (data['Usage'] * costs[15][5])
    else:
        # TODO: update this when services are not value added
        pass

    return usage_cost


def parse_excel_report(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert time columns to datetime once
    df['Meter Begin Time (UTC+05:00)'] = pd.to_datetime(
        df['Meter Begin Time (UTC+05:00)'])
    df['Meter End Time (UTC+05:00)'] = pd.to_datetime(df['Meter End Time (UTC+05:00)'])

    report_month = df['Meter Begin Time (UTC+05:00)'].dt.month.unique()[0]
    # Calculate usage duration for all rows at once and truncate to 2 decimal places
    df['Usage Duration'] = (
        (df['Meter End Time (UTC+05:00)'] - df['Meter Begin Time (UTC+05:00)'])
        .dt.total_seconds() / 3600
    ).round(2).apply(constrain_value, args=(report_month,))

    # Create nested dictionary using groupby
    result = {'regions': []}
    for region, region_group in df.groupby('Region'):
        services_list = []
        for resource_type, rt_group in region_group.groupby('Resource Type'):
            instances_list = []

            if trim_lower_normalize(resource_type) == ResourceType.ECS.value:
                clustered_instances_list = []
                dedicated_instances_list = []

                # Filter rows where Tag contains 'cce' or 'cluster' (case-insensitive)
                rt_group_cluster = rt_group[rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                # Filter rows where Tag doesn't contains 'cce' or 'cluster' (case-insensitive)
                rt_group_dedicated = rt_group[~rt_group['Tag'].str.lower(
                ).str.contains('cce|cluster', na=False)]

                if len(rt_group_cluster) > 0:
                    for _, row in rt_group_cluster.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        combined_data = {
                            **drop_columns_from_df(row).to_dict(),
                            **parsed_metrics,
                            'Service Type': ServiceTag.CLUSTERED.value
                        }
                        usage_cost = calculate_usage_cost(
                            combined_data, rt=ResourceType.ECS, service_tag=ServiceTag.CLUSTERED)
                        clustered_instances_list.append({
                            **combined_data,
                            'Usage Cost': usage_cost
                        })

                if len(rt_group_dedicated) > 0:
                    for _, row in rt_group_dedicated.iterrows():
                        parsed_metrics = parse_ecs_data(row['Metering Metric'])
                        combined_data = {
                            **drop_columns_from_df(row).to_dict(),
                            **parsed_metrics,
                            'Service Type': ServiceTag.DEDICATED.value
                        }
                        usage_cost = calculate_usage_cost(
                            combined_data, rt=ResourceType.ECS, service_tag=ServiceTag.DEDICATED)
                        dedicated_instances_list.append({
                            **combined_data,
                            'Usage Cost': usage_cost
                        })

                services_list.append({
                    'serviceName': resource_type,
                    'instances': {
                        "dedicated": dedicated_instances_list,
                        "clustered": clustered_instances_list
                    }
                })
                continue

            elif trim_lower_normalize(resource_type) == ResourceType.EVS.value:
                # filter rows where Metering Metric contains 'ssd' or 'sata' (case-insensitive)
                rt_group_ssd = rt_group[rt_group['Metering Metric'].str.lower(
                ).str.contains('ssd', na=False)]
                rt_group_hdd = rt_group[rt_group['Metering Metric'].str.lower(
                ).str.contains('sata', na=False)]

                if len(rt_group_ssd) > 0:
                    for _, row in rt_group_ssd.iterrows():
                        usage_cost = calculate_usage_cost(
                            row, rt=ResourceType.EVS, storage_type=StorageType.SSD)
                        instances_list.append({
                            **drop_columns_from_df(row).to_dict(),
                            'Usage Cost': usage_cost,
                            'Storage Type': StorageType.SSD.value
                        })

                if len(rt_group_hdd) > 0:
                    for _, row in rt_group_hdd.iterrows():
                        usage_cost = calculate_usage_cost(
                            row, rt=ResourceType.EVS, storage_type=StorageType.HDD)
                        instances_list.append({
                            **drop_columns_from_df(row).to_dict(),
                            'Usage Cost': usage_cost,
                            'Storage Type': StorageType.HDD.value
                        })

            else:
                for _, row in rt_group.iterrows():
                    usage_cost = calculate_usage_cost(
                        row,
                        rt={e.value: e for e in ResourceType}.get(
                            trim_lower_normalize(resource_type)
                        )
                    )
                    instances_list.append({
                        **drop_columns_from_df(row).to_dict(),
                        'Usage Cost': usage_cost
                    })

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
