import numpy as np
np.random.seed(0)

dairy_data = {
    'Dairy Farmers of America': np.random.randint(500, 1000, 12),
    'Dean Foods': np.random.randint(500, 1000, 12),
    'Land O Lakes': np.random.randint(500, 1000, 12),
    'Saputo': np.random.randint(500, 1000, 12),
    'Arla Foods': np.random.randint(500, 1000, 12),
    'Fonterra': np.random.randint(500, 1000, 12),
    'Groupe Lactalis': np.random.randint(500, 1000, 12),
    'Meiji Dairies': np.random.randint(500, 1000, 12)
}

DAIRY_COMPANY_OPTIONS = [
    {'label': 'None selected', 'value': 'None selected'},
    {'label': 'Dairy Farmers of America', 'value': 'Dairy Farmers of America'},
    {'label': 'Dean Foods', 'value': 'Dean Foods'},
    {'label': 'Land O Lakes', 'value': 'Land O Lakes'},
    {'label': 'Saputo', 'value': 'Saputo'},
    {'label': 'Arla Foods', 'value': 'Arla Foods'},
    {'label': 'Fonterra', 'value': 'Fonterra'},
    {'label': 'Groupe Lactalis', 'value': 'Groupe Lactalis'},
    {'label': 'Meiji Dairies', 'value': 'Meiji Dairies'},
]

FARM_OPTIONS = [
    {'label': 'Wisconsin', 'value': 'Wisconsin'},
    {'label': 'California', 'value': 'California'},
    {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
    {'label': 'New York', 'value': 'New York'},
    {'label': 'Michigan', 'value': 'Michigan'},
    {'label': 'Minnesota', 'value': 'Minnesota'},
    {'label': 'Idaho', 'value': 'Idaho'},
    {'label': 'Washington', 'value': 'Washington'},
    {'label': 'Oregon', 'value': 'Oregon'},
]