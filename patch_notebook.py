import json
from pathlib import Path
p = Path('iris_classification_executed.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
changed = False
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    source = cell['source']
    if any('X = df[features].to_numpy(dtype=float)' in line for line in source):
        new_source = []
        for line in source:
            if line == "X = df[features].to_numpy(dtype=float)\n":
                new_source.append("X: np.ndarray = np.asarray(df[features], dtype=float)\n")
                changed = True
            elif line == "y = df['species_id'].to_numpy(dtype=np.int64)\n":
                new_source.append("y: np.ndarray = np.asarray(df['species_id'], dtype=np.int64)\n")
                changed = True
            elif line == "print(f'Class labels         : {np.unique(y)} -> {list(CLASS_NAMES)}')\n":
                new_source.append("print(f'Class labels         : {np.unique(np.asarray(y, dtype=np.int64))} -> {list(CLASS_NAMES)}')\n")
                changed = True
            else:
                new_source.append(line)
        cell['source'] = new_source
    if any('train_test_split' in line for line in source):
        new_source = []
        for line in source:
            if line == "print(f'Train class distribution: {dict(zip(*np.unique(y_train, return_counts=True)))}')\n":
                new_source.append("print(f'Train class distribution: {dict(zip(*np.unique(np.asarray(y_train, dtype=np.int64), return_counts=True)))}')\n")
                changed = True
            elif line == "print(f'Test  class distribution: {dict(zip(*np.unique(y_test,  return_counts=True)))}')\n":
                new_source.append("print(f'Test  class distribution: {dict(zip(*np.unique(np.asarray(y_test, dtype=np.int64), return_counts=True)))}')\n")
                changed = True
            else:
                new_source.append(line)
        cell['source'] = new_source
if changed:
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    print('Notebook patched successfully.')
else:
    print('No changes made.')
