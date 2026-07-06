import json
from pathlib import Path
p = Path('iris_classification_executed.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
for idx, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    for line_no, line in enumerate(cell['source'], start=1):
        if 'text(' in line:
            print(f'CELL {idx} LINE {line_no}: {repr(line)}')
