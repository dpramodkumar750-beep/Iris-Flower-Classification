import json
from pathlib import Path

patterns = [
    'import matplotlib.cm as mpl_cm',
    'mpl_cm.Pastel2',
    'mpl_cm.Set1',
    "ax.contour (",
    'df.head(10)',
    'importlib.metadata.version("seaborn")',
    'print(f\'  Pandas :',
    'print(f\'  Seaborn: {sns.__version__}'
]

for nb_name in ['iris_classification.ipynb', 'iris_classification_executed.ipynb']:
    path = Path(nb_name)
    print('===', nb_name)
    nb = json.loads(path.read_text(encoding='utf-8'))
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        src = ''.join(cell['source'])
        hits = [p for p in patterns if p in src]
        if hits:
            print('CELL', i, 'hits', hits)
            print(src)
            print('---')
