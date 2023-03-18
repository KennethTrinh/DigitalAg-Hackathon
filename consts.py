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

farm_data = {
    'Wisconsin': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'California': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Pennsylvania': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'New York': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Michigan': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Minnesota': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Iowa': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Idaho': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Washington': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    'Oregon': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    }
}
box_plot_farm_data = {
    'Wisconsin': np.random.normal(20, 5, 100),
    'California': np.random.normal(20, 5, 100),
    'Pennsylvania': np.random.normal(20, 5, 100),
    'New York': np.random.normal(20, 5, 100),
    'Michigan': np.random.normal(20, 5, 100),
    'Minnesota': np.random.normal(20, 5, 100),
    'Iowa': np.random.normal(20, 5, 100),
    'Idaho': np.random.normal(20, 5, 100),
    'Washington': np.random.normal(20, 5, 100),
    'Oregon': np.random.normal(20, 5, 100)
}
benchmark_data = np.random.normal(30, 10, 100)


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
    {'label': 'None selected', 'value': 'None selected'},
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