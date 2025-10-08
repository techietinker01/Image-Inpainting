import os
print('Running check_saved_model.py')
print('CWD:', os.getcwd())

p = os.path.join('saved_models', 'generator_saved_model')

if os.path.exists(p):
    print('Path exists:', os.path.abspath(p))
    for root, dirs, files in os.walk(p):
        print('DIR:', root)
        for f in files[:200]:
            print(' -', f)
else:
    print('Path not found:', p)
    print('Attempting to save a tiny dummy model to that path to validate TF save...')
    try:
        import importlib
        keras_mod = None
        try:
            keras_mod = importlib.import_module('tensorflow.keras')
        except ModuleNotFoundError:
            try:
                keras_mod = importlib.import_module('keras')
            except ModuleNotFoundError:
                keras_mod = None

        if keras_mod is None:
            print('TensorFlow/Keras not installed; skipping dummy model save.')
        else:
            layers = keras_mod.layers
            Model = keras_mod.Model
            Input = keras_mod.Input
            os.makedirs(p, exist_ok=True)
            inp = Input((28,28,1))
            x = layers.Conv2D(4, 3, activation='relu')(inp)
            m = Model(inp, x)
            if hasattr(m, 'export'):
                m.export(p)
            else:
                m.save(p, save_format='tf')
            print('Saved dummy model to', os.path.abspath(p))
            for root, dirs, files in os.walk(p):
                print('DIR:', root)
                for f in files[:200]:
                    print(' -', f)
    except Exception as e:
        print('Failed to save dummy model:', e)
