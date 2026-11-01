import json
import glob
import os

def update_notebook(fpath):
    print(f"Processing {fpath}...")
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Failed to read {fpath}: {e}")
        return

    changed = False
    cells = nb.get('cells', [])
    
    for cell in cells:
        if cell.get('cell_type') != 'code':
            continue
        
        source = cell.get('source', [])
        new_source = []
        cell_modified = False
        
        for line in source:
            # Look for lines assigning 'device' with cuda/cpu logic
            # Typical pattern: device = torch.device('cuda' ...)
            # We want to be careful not to replace things like 'if device == ...'
            stripped = line.strip()
            
            # Simple heuristic: starts with 'device =' and contains 'cuda' and 'cpu'
            # Or just matches roughly the assignment pattern
            if "device =" in line and "cuda" in line and "cpu" in line:
                # Keep indentation
                indent = line[:line.find("device =")]
                
                # New line with import and assignment
                # We use specific TPU setup
                # import torch_xla.core.xla_model as xm
                # device = xm.xla_device()
                
                # To be safe against multiple imports, we might put import on strict lines,
                # but putting it inline is robust for cell execution order.
                
                new_line = indent + "import torch_xla.core.xla_model as xm; device = xm.xla_device()"
                if line.endswith('\n'):
                     new_line += '\n'
                
                new_source.append(new_line)
                cell_modified = True
                changed = True
            elif "device =" in line and "torch.device('cuda'" in line:
                 # Catching cases like device = torch.device('cuda') without else cpu (rare but possible)
                 indent = line[:line.find("device =")]
                 new_line = indent + "import torch_xla.core.xla_model as xm; device = xm.xla_device()"
                 if line.endswith('\n'):
                     new_line += '\n'
                 new_source.append(new_line)
                 cell_modified = True
                 changed = True
            else:
                new_source.append(line)
        
        if cell_modified:
            cell['source'] = new_source

    if changed:
        print(f"Updating {fpath} with TPU/XLA changes.")
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
    else:
        print(f"No matching device definitions found in {fpath}.")

# Search for ipynb files recursively
current_dir = os.getcwd()
print(f"Searching in {current_dir}")

files = []
for root, dirs, filenames in os.walk(current_dir):
    for filename in filenames:
        if filename.endswith(".ipynb"):
             files.append(os.path.join(root, filename))

for f in files:
    update_notebook(f)
