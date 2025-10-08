import os
from nbformat import read, write
from nbconvert.preprocessors import ExecutePreprocessor

nb_path = os.path.abspath(r'C:\Users\kumar\OneDrive\Desktop\imginvs\image-inpainting-pjt.ipynb')
print('Notebook path:', nb_path)
nb_dir = os.path.dirname(nb_path)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = read(f, as_version=4)

proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
try:
    proc.preprocess(nb, {'metadata': {'path': nb_dir}})
    out_path = nb_path.replace('.ipynb', '.executed.ipynb')
    with open(out_path, 'w', encoding='utf-8') as f:
        write(nb, f)
    print('Execution finished, saved executed notebook to', out_path)
except Exception as e:
    print('Notebook execution failed or timed out:', repr(e))

# After execution, check saved_models/generator_saved_model
p = os.path.join(nb_dir, 'saved_models', 'generator_saved_model')
print('\nChecking saved model path:', p)
if os.path.exists(p):
    print('Path exists:', os.path.abspath(p))
    for root, dirs, files in os.walk(p):
        print('DIR:', root)
        for f in files[:200]:
            print(' -', f)
else:
    print('Path not found:', p)
