import os
import tensorflow as tf
from tensorflow import keras
layers = keras.layers

# Generator architecture (copied from notebook)

def downsample(filters, size, apply_batchnorm=True):
    result = keras.Sequential()
    result.add(layers.Conv2D(filters, size, strides=2, padding='same',
                             kernel_initializer='he_normal', use_bias=False))
    if apply_batchnorm:
        result.add(layers.BatchNormalization())
    result.add(layers.LeakyReLU())
    return result

def upsample(filters, size, apply_dropout=False):
    result = keras.Sequential()
    result.add(layers.Conv2DTranspose(filters, size, strides=2, padding='same',
                                      kernel_initializer='he_normal', use_bias=False))
    result.add(layers.BatchNormalization())
    if apply_dropout:
        result.add(layers.Dropout(0.5))
    result.add(layers.ReLU())
    return result

def Generator():
    inputs = layers.Input(shape=(256,256,3))
    down_stack = [
        downsample(64, 4, apply_batchnorm=False),
        downsample(128, 4),
        downsample(256, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
        downsample(512, 4),
    ]
    up_stack = [
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4, apply_dropout=True),
        upsample(512, 4),
        upsample(256, 4),
        upsample(128, 4),
        upsample(64, 4),
    ]
    initializer = tf.random_normal_initializer(0., 0.02)
    last = layers.Conv2DTranspose(3, 4, strides=2, padding='same',
                                  kernel_initializer=initializer,
                                  activation='tanh')
    x = inputs
    skips = []
    for down in down_stack:
        x = down(x)
        skips.append(x)
    skips = list(reversed(skips[:-1]))
    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = layers.Concatenate()([x, skip])
    x = last(x)
    return keras.Model(inputs=inputs, outputs=x)

if __name__ == '__main__':
    save_dir = os.path.join('saved_models','generator_saved_model')
    os.makedirs('saved_models', exist_ok=True)
    model = Generator()
    # Build once to establish shapes
    model(tf.zeros((1,256,256,3), dtype=tf.float32))
    try:
        # Keras 3 inference export to SavedModel
        model.export(save_dir)
        print('Exported generator SavedModel to', os.path.abspath(save_dir))
    except Exception as e:
        print('model.export failed, trying tf.saved_model.save:', e)
        tf.saved_model.save(model, save_dir)
        print('Saved via tf.saved_model.save to', os.path.abspath(save_dir))
