import json
from pathlib import Path
p = Path('iris_classification_executed.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
for idx, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell['source'])
    if 'Class labels         :' in src or 'np.unique(y_train' in src or 'np.unique(y_test' in src or 'train_test_split' in src:
        print('CELL', idx)
        for line in cell['source']:
            print(repr(line))
        print('-----')
