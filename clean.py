from tqdm import tqdm
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_clean_resize_images(root='images', size=(128, 128)):
    X = []
    y = []
    for age_dir in tqdm(os.listdir(root)):
        age = int(age_dir.split("_")[-1])
        folder = os.path.join(root, age_dir)
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            try:
                img = Image.open(path).convert('RGB')
                img = img.resize(size)
                X.append(np.array(img))
                y.append(age)
            except:
                continue
    return np.array(X), np.array(y)

X, y = load_clean_resize_images()
print("✅ Ảnh hợp lệ:", len(X))
