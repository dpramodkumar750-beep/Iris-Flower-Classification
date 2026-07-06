import json
from pathlib import Path
p = Path('iris_classification_executed.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
changed = False
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    new_source = []
    for line in cell['source']:
        if 'axes[0].text(float(i), float(v) + 0.5, str(v),' in line:
            new_source.append("    axes[0].text(float(i), float(v) + 0.5, str(v), ha='center', fontweight='bold', fontsize=12)\n")
            changed = True
        else:
            new_source.append(line)
    cell['source'] = new_source
if changed:
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    print('patched')
else:
    print('no changes')
