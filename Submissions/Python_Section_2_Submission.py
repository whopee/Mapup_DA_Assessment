#MapUp Assessment - Yash Desale

import pandas as pd
import datetime

def calculate_distance_matrix(df) -> pd.DataFrame:
    distances = {(row['id_start'], row['id_end']): row['distance'] for _, row in df.iterrows()}
    distances.update({(row['id_end'], row['id_start']): row['distance'] for _, row in df.iterrows()})
    
    ids = sorted(set(df['id_start']).union(df['id_end']))
    matrix = pd.DataFrame(float('inf'), index=ids, columns=ids)
    matrix.values[[range(len(ids))]*2] = 0

    for (start, end), distance in distances.items():
        matrix.loc[start, end] = distance

    for k in ids:
        for i in ids:
            for j in ids:
                matrix.loc[i, j] = min(matrix.loc[i, j], matrix.loc[i, k] + matrix.loc[k, j])

    return matrix

 
df = pd.read_csv("/mnt/data/dataset-2.csv")
result = calculate_distance_matrix(df)
print(result)


def unroll_distance_matrix(df)->pd.DataFrame():
    melted_df = df.melt(id_vars=['id_start', 'id_end'], var_name='vehicle', value_name='toll_rate')
    unrolled_df = melted_df[melted_df['id_start'] != melted_df['id_end']]
    return unrolled_df

distance_matrix = pd.read_csv("distance_matrix.csv")
result = unroll_distance_matrix(distance_matrix)
print(result)


def find_ids_within_ten_percentage_threshold(df, reference_id) -> pd.DataFrame:
    reference_df = df[df['id_start'] == reference_id]
    reference_avg_distance = reference_df['distance'].mean()
    threshold = reference_avg_distance * 0.1
    filtered_df = df[(df['distance'] >= reference_avg_distance - threshold) & (df['distance'] <= reference_avg_distance + threshold)]
    result_df = filtered_df[['id_start']].drop_duplicates()
    return result_df


distance_matrix = pd.read_csv("distance_matrix.csv")
reference_id = 1001400
result = find_ids_within_ten_percentage_threshold(distance_matrix, reference_id)
print(result)


def calculate_toll_rate(df) -> pd.DataFrame:
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient
    return df
distance_matrix = pd.read_csv("distance_matrix.csv") 
result = calculate_toll_rate(distance_matrix)
print(result)



def calculate_time_based_toll_rates(df) -> pd.DataFrame:
    time_intervals = [
        (datetime.time(0, 0), datetime.time(10, 0), 0.8),
        (datetime.time(10, 0), datetime.time(18, 0), 1.2),
        (datetime.time(18, 0), datetime.time(23, 59, 59), 0.8),
        (datetime.time(0, 0), datetime.time(23, 59, 59), 0.7)
    ]
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    def get_discount_factor(day, start_time, end_time):
        for interval, discount_factor in time_intervals:
            if interval[0] <= start_time < interval[1] and interval[0] <= end_time < interval[1]:
                if day in weekdays:
                    return discount_factor
                else:
                    return time_intervals[-1][2]
        return None

    for index, row in df.iterrows():
        discount_factor = get_discount_factor(row['start_day'], row['start_time'], row['end_time'])
        if discount_factor is not None:
            df.loc[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor

    return df

distance_matrix = pd.read_csv("distance_matrix.csv")
result = calculate_time_based_toll_rates(distance_matrix)
print(result)
