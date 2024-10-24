#MapUp Assessment - Yash Desale

from typing import Dict, List
import pandas as pd
import re


def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    res = []
    for i in range(0, len(lst), n):
        chunk = lst[i:i+n]
        res.extend(chunk[::-1])
    return res


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    result = {}
    for word in lst:
        length = len(word)
        if length not in result:
            result[length] = []
        result[length].append(word)
    return dict(sorted(result.items()))


def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    flat_dict = {}
    
    def flatten(d, parent_key=''):
        for key in d:
            new_key = parent_key + sep + key if parent_key else key
            value = d[key]
            
            if type(value) == dict:
                flatten(value, new_key)
            elif type(value) == list:
                for i in range(len(value)):
                    flat_dict[new_key + f"[{i}]"] = value[i]
            else:
                flat_dict[new_key] = value

    flatten(nested_dict)
    return flat_dict


def unique_permutations(nums: List[int]) -> List[List[int]]:
    result = []
    nums.sort()

    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result


def find_all_dates(text: str) -> List[str]:
    date_patterns = [
        r'\b\d{2}-\d{2}-\d{4}\b',
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{4}\.\d{2}\.\d{2}\b'
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    return dates


def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    rotated = [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]
    result = []
    for i in range(n):
        row_sum = sum(rotated[i])
        new_row = []
        for j in range(n):
            col_sum = sum(rotated[k][j] for k in range(n))
            new_row.append(row_sum + col_sum - rotated[i][j])
        result.append(new_row)
    return result


def time_check(df: pd.DataFrame) -> pd.Series:
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['diff'] = df['end'] - df['start']

    def check_full_week(id_group):
        total_coverage = id_group['diff'].sum()
        return total_coverage >= pd.Timedelta('7 days')

    return df.groupby(['id', 'id_2']).apply(check_full_week)
