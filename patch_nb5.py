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
        if line.strip().startswith('ax.text(val + 0.005'):
            new_source.append('    ax.text(float(val + 0.005), float(bar.get_y() + bar.get_height()/2),\n')
            changed = True
        elif line.strip().startswith("axes[0].text(bar.get_x() + bar.get_width()/2"):
            new_source.append('    axes[0].text(float(bar.get_x() + bar.get_width()/2), float(bar.get_height() + 0.005),\n')
            changed = True
        else:
            new_source.append(line)
    cell['source'] = new_source
if changed:
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    print('patched')
else:
    print('no changes')
