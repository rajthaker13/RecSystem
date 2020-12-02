from typing import Any, Union, List

import pandas as pd
import numpy as np
import fastcountvectorizer as cv
from pandas import Series, DataFrame
from pandas.core.arrays import ExtensionArray




patient_info1 = pd.read_csv(r'/Users/rajthaker/Desktop/Penn Data/patient_info_CONFIDENTIAL.csv')
video_watched1 = pd.read_csv(r'/Users/rajthaker/Desktop/Penn Data/video_watched_events_CONFIDENTIAL.csv')

# Important columns from patient info
patient_info_headers = ['patient_id', 'age', 'sex', 'has_bh_specialist']
patient_info = patient_info1[patient_info_headers]

# Important columns from videos watched
videos_watched_headers = ['datetime_created', 'patient_id', 'video_id', 'url', 'primary_category', 'secondary_category']
videos_watched = video_watched1[videos_watched_headers]

# Create new column of important data
print(patient_info)
patient_info['patient_data'] = patient_info[patient_info_headers].apply(lambda row: '_'.join(row.values.astype(str)))
print(patient_info)



#patient_info1[[“patient_id”, “age”, “sex”, “has_bh_specialist”]]
#define function to merge videos watches for each user