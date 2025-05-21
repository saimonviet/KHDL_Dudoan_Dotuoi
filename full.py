import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ========== 1. Tạo từ khóa theo độ tuổi ==========
def get_keywords(age):
    if age <= 3:
        return [
            f"khuôn mặt em bé {age} tuổi",
            f"baby face {age} years old child",
            f"portrait baby {age} years old child close-up",
            f"face of toddler {age} years",
            f"baby face Vietnamese {age} years old"
        ]
    elif age <= 12:
        return [
            f"khuôn mặt trẻ em {age} tuổi",
            f"child face {age} years old",
            f"portrait of a {age}-year-old kid",
            f"young Vietnamese boy or girl {age} years old",
            f"face of child aged {age} years"
        ]
    elif age <= 17:
        return [
            f"khuôn mặt thiếu niên {age} tuổi",
            f"teenager face {age} years old",
            f"portrait of {age}-year-old adolescent",
            f"Vietnamese teenage face {age}",
            f"teenage boy or girl {age} years old"
        ]
    elif age <= 29:
        return [
            f"khuôn mặt thanh niên {age} tuổi",
            f"young adult face {age} years old",
            f"portrait of Vietnamese {age} years old",
            f"male or female face {age} years",
            f"student portrait {age} years old"
        ]
    elif age <= 49:
        return [
            f"khuôn mặt người trưởng thành {age} tuổi",
            f"adult face {age} years old",
            f"professional Vietnamese face {age} years",
            f"working person portrait {age} years",
            f"businessman or woman {age} years old face"
        ]
    else:
        return [
            f"khuôn mặt người cao tuổi {age} tuổi",
            f"elderly face {age} years old",
            f"senior Vietnamese person face {age}",
            f"retired man or woman {age} years portrait",
            f"old person face close-up {age} years"
        ]

# ========== 2. Crawl ảnh ==========
def crawl_images_for_age(age, max_images=150):
    folder = f"images/age_{age}"
    os.makedirs(folder, exist_ok=True)

    keywords = get_keywords(age)
    per_keyword = max_images // len(keywords)

    for keyword in keywords:
        print(f"🔍 Crawling {per_keyword} images for: '{keyword}' (Tuổi: {age})")

        crawler = GoogleImageCrawler(storage={"root_dir": folder}, downloader_threads=4)
        crawler.crawl(keyword=keyword, max_num=per_keyword, file_idx_offset='auto')

        crawler = BingImageCrawler(storage={"root_dir": folder}, downloader_threads=4)
        crawler.crawl(keyword=keyword, max_num=per_keyword, file_idx_offset='auto', filters={"type": "photo"})

# ========== 3. Thống kê mô tả ==========
def analyze_and_plot_dataset(root="images"):
    age_dirs = sorted(os.listdir(root))
    image_counts = []
    avg_sizes = []

    for age_dir in age_dirs:
        folder = os.path.join(root, age_dir)
        count = 0
        sizes = []

        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            try:
                img = Image.open(path)
                sizes.append(img.size)
                count += 1
            except:
                continue

        image_counts.append(count)
        if sizes:
            avg_w = int(np.mean([s[0] for s in sizes]))
            avg_h = int(np.mean([s[1] for s in sizes]))
            avg_sizes.append((avg_w, avg_h))
        else:
            avg_sizes.append((0, 0))

    ages = [int(x.split('_')[-1]) for x in age_dirs]

    plt.figure(figsize=(15,5))
    sns.barplot(x=ages, y=image_counts, palette="viridis")
    plt.title("Số lượng ảnh theo độ tuổi")
    plt.xlabel("Tuổi")
    plt.ylabel("Số ảnh")
    plt.show()

# ========== 4. Làm sạch và chuẩn hóa ==========
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
    X = np.array(X).astype("float32") / 255.0  # Chuẩn hóa [0, 1]
    y = np.array(y)
    return X, y

# ========== 5. Giảm chiều và trực quan ==========
def reduce_and_visualize(X, y, n_samples=1000):
    X_flat = X.reshape(X.shape[0], -1)

    # PCA trước để giảm nhiễu
    pca = PCA(n_components=50)
    X_pca = pca.fit_transform(X_flat)

    # t-SNE
    X_tsne = TSNE(n_components=2, perplexity=30).fit_transform(X_pca[:n_samples])
    y_sample = y[:n_samples]

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=X_tsne[:,0], y=X_tsne[:,1], hue=y_sample, palette="Spectral", legend=False)
    plt.title("Biểu diễn dữ liệu sau khi giảm chiều bằng t-SNE")
    plt.xlabel("TSNE-1")
    plt.ylabel("TSNE-2")
    plt.show()

# ========== MAIN ==========
if __name__ == "__main__":
    # Bước 1: Crawl ảnh theo độ tuổi (chạy 1 lần đầu tiên, hoặc comment lại sau khi đã crawl xong)
    # for age in range(1, 71):
    #     crawl_images_for_age(age, max_images=150)

    # Bước 2: Phân tích thống kê dữ liệu ảnh
    analyze_and_plot_dataset()

    # Bước 3: Load ảnh, làm sạch, resize và chuẩn hoá
    X, y = load_clean_resize_images()

    # Bước 4: Giảm chiều và trực quan hoá dữ liệu
    reduce_and_visualize(X, y)
