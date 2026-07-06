import json
from pathlib import Path
p = Path('iris_classification_executed.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
changed = False
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    for i, line in enumerate(cell['source']):
        if 'Class labels         : {np.unique(y)} -> {list(CLASS_NAMES)}' in line:
            print('Found line:', repr(line))
            cell['source'][i] = line.replace(
                'print(f\'Class labels         : {np.unique(y)} -> {list(CLASS_NAMES)}\')',
                'print(f\'Class labels         : {np.unique(np.asarray(y, dtype=np.int64))} -> {list(CLASS_NAMES)}\')'
            )
            changed = True
        if 'np.unique(y_train' in line and 'return_counts=True' in line and 'np.asarray' not in line:
            cell['source'][i] = line.replace(
                'np.unique(y_train, return_counts=True)',
                'np.unique(np.asarray(y_train, dtype=np.int64), return_counts=True)'
            )
            changed = True
        if 'np.unique(y_test' in line and 'return_counts=True' in line and 'np.asarray' not in line:
            cell['source'][i] = line.replace(
                'np.unique(y_test,  return_counts=True)',
                'np.unique(np.asarray(y_test, dtype=np.int64), return_counts=True)'
            )
            changed = True
if changed:
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    print('Notebook patched successfully.')
else:
    print('No changes made.')
