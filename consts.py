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
    '1234 Farm Road, Lodi, CA 95242': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '5678 County Road 200, Ridgway, CO 81432': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '9012 Country Lane, Dalton, GA 30721': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '3456 Farmington Road, Mocksville, NC 27028': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '7890 County Road 17, Adams, NY 13605': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '2345 Farm-to-Market Road 123, Giddings, TX 78942': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '6789 Highway 89, Logan, UT 84321': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '3210 County Road 200, Bellevue, OH 44811': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '9012 Route 4, Mendon, VT 05701': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    },
    '3456 County Road 230, La Grange, TX 78945': {
        'Bacteria': np.random.randint(0, 50),
        'Archaea': np.random.randint(0, 50),
        'Fungi': np.random.randint(0, 50),
        'Protozoa': np.random.randint(0, 50)
    }
}
box_plot_farm_data = {
    '1234 Farm Road, Lodi, CA 95242': np.random.normal(20, 5, 100),
    '5678 County Road 200, Ridgway, CO 81432': np.random.normal(20, 5, 100),
    '9012 Country Lane, Dalton, GA 30721': np.random.normal(20, 5, 100),
    '3456 Farmington Road, Mocksville, NC 27028': np.random.normal(20, 5, 100),
    '7890 County Road 17, Adams, NY 13605': np.random.normal(20, 5, 100),
    '2345 Farm-to-Market Road 123, Giddings, TX 78942': np.random.normal(20, 5, 100),
    '6789 Highway 89, Logan, UT 84321': np.random.normal(20, 5, 100),
    '3210 County Road 200, Bellevue, OH 44811': np.random.normal(20, 5, 100),
    '9012 Route 4, Mendon, VT 05701': np.random.normal(20, 5, 100),
    '3456 County Road 230, La Grange, TX 78945': np.random.normal(20, 5, 100)
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
    {'label': '1234 Farm Road, Lodi, CA 95242', 'value': '1234 Farm Road, Lodi, CA 95242'},
    {'label': '5678 County Road 200, Ridgway, CO 81432', 'value': '5678 County Road 200, Ridgway, CO 81432'},
    {'label': '9012 Country Lane, Dalton, GA 30721', 'value': '9012 Country Lane, Dalton, GA 30721'},
    {'label': '3456 Farmington Road, Mocksville, NC 27028', 'value': '3456 Farmington Road, Mocksville, NC 27028'},
    {'label': '7890 County Road 17, Adams, NY 13605', 'value': '7890 County Road 17, Adams, NY 13605'},
    {'label': '2345 Farm-to-Market Road 123, Giddings, TX 78942', 'value': '2345 Farm-to-Market Road 123, Giddings, TX 78942'},
    {'label': '6789 Highway 89, Logan, UT 84321', 'value': '6789 Highway 89, Logan, UT 84321'},
    {'label': '3210 County Road 200, Bellevue, OH 44811', 'value': '3210 County Road 200, Bellevue, OH 44811'},
    {'label': '9012 Route 4, Mendon, VT 05701', 'value': '9012 Route 4, Mendon, VT 05701'},
    {'label': '3456 County Road 230, La Grange, TX 78945', 'value': '3456 County Road 230, La Grange, TX 78945'},
]

RACHELS_STYLE = {
    'width': '100%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px'
                    }