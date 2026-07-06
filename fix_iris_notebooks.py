import json
from pathlib import Path

notebooks = [Path('iris_classification.ipynb'), Path('iris_classification_executed.ipynb')]

for nb_path in notebooks:
    nb = json.loads(nb_path.read_text(encoding='utf-8'))
    changed = False
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        if 'print(f' in source and 'np.__version__' in source and 'Seaborn' in source:
            lines = []
            for line in cell['source']:
                if 'print(' in line and 'NumPy' in line:
                    lines.append(line)
                elif 'print(' in line and 'Pandas' in line:
                    lines.append(line)
                elif 'print(' in line and 'Seaborn' in line and 'importlib.metadata.version' in line:
                    lines.append(line)
                elif 'print(' in line and 'Seaborn' in line and 'sns.__version__' in line:
                    continue
                elif 'print(' in line and 'All libraries imported successfully!' in line:
                    lines.append(line)
                else:
                    if 'print(' in line and 'Seaborn' in line and 'sns.__version__' in line:
                        continue
                    lines.append(line)
            new_source = ''.join(lines)
            if new_source != source:
                cell['source'] = new_source.splitlines(keepends=True)
                changed = True
        if nb_path.name == 'iris_classification_executed.ipynb' and source.count('df.head(10)') > 1:
            new_source = source.replace('df.head(10)\n', '', source.count('df.head(10)') - 1)
            cell['source'] = new_source.splitlines(keepends=True)
            changed = True
        if 'matplotlib.cm as mpl_cm' in source:
            source = source.replace('import matplotlib.cm as mpl_cm\n', '')
            cell['source'] = source.splitlines(keepends=True)
            changed = True
        if 'ax.contourf(xx, yy, Z, alpha=0.35, cmap=mpl_cm.Pastel2)' in source:
            source = source.replace('ax.contourf(xx, yy, Z, alpha=0.35, cmap=mpl_cm.Pastel2)', "ax.contourf(xx, yy, Z, alpha=0.35, cmap='Pastel2')")
            source = source.replace("ax.contour (xx, yy, Z, colors='grey', linewidths=0.7, alpha=0.6)", "ax.contour(xx, yy, Z, colors='grey', linewidths=0.7, alpha=0.6)")
            source = source.replace('c = mpl_cm.Set1(cls/3)', "c = plt.get_cmap('Set1')(cls/3)")
            cell['source'] = source.splitlines(keepends=True)
            changed = True
    if changed:
        nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'Updated {nb_path}')
