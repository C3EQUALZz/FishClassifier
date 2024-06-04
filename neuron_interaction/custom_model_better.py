import numpy as np
import tensorflow as tf
from PIL import Image

dict_fish_classes = {
    0: 'Black Sea Sprat',
    1: 'Gilt-Head Bream',
    2: 'Hourse Mackerel',
    3: 'Red Mullet',
    4: 'Red Sea Bream',
    5: 'Sea Bass',
    6: 'Shrimp',
    7: 'Striped Red Mullet',
    8: 'Trout'
}


class CustomModelBetter:

    def __init__(self):
        self.model = tf.keras.models.load_model('notebooks/egor_grishkov/my_model_better.keras')

    def predict(self, image_path):
        # Использование модели для предсказания класса изображения
        predictions = self.model.predict(CustomModelBetter.__preprocess_image(image_path))
        # Возвращение индекса наиболее вероятного класса
        predicted_class_index = np.argmax(predictions[0])
        return dict_fish_classes.get(predicted_class_index)

    @staticmethod
    def __preprocess_image(image_path, target_size=(590, 445)):
        # Загрузка изображения
        img = Image.open(image_path)
        # Изменение размера изображения
        img = img.resize(target_size)
        # Преобразование изображения в массив numpy
        img_array = np.array(img)
        # Добавление дополнительных измерений для соответствия требованиям модели
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        # Предварительная обработка изображения
        preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded_dims)

        return preprocessed_img
