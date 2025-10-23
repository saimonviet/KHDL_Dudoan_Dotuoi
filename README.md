Dự Án: Dự Đoán Độ Tuổi Từ Khuôn Mặt Bằng Deep Learning (KHDL_Dudoan_Dotuoi)
Giới Thiệu
Dự án này xây dựng một hệ thống dự đoán độ tuổi từ ảnh khuôn mặt (phạm vi 1-70 tuổi) sử dụng Deep Learning. Pipeline end-to-end bao gồm:

Thu thập dữ liệu: Crawl ảnh từ Google/Bing theo nhóm tuổi với từ khóa tiếng Việt/Anh, lọc ảnh không có khuôn mặt.
Xử lý dữ liệu: Làm sạch, resize (128x128), chuẩn hóa pixel [0,1], và trực quan hóa bằng PCA/t-SNE.
Huấn luyện mô hình: Sử dụng DenseNet tùy chỉnh trên TensorFlow/Keras, kết hợp dataset crawled (~150 ảnh/tuổi) và UKTFaces-IMDB-Wiki (downsampled 10-70 tuổi).
Kết quả: Đạt MAE ~46.84 trên tập validation, tập trung vào dữ liệu khuôn mặt Việt Nam.

Dự án phù hợp cho nghiên cứu Age Estimation trong sinh trắc học, với mã nguồn mở trên GitHub: https://github.com/saimonviet/KHDL_Dudoan_Dotuoi.
Mục Tiêu

Xây dựng dataset chất lượng cao (>10.000 ảnh đã lọc).
Phát triển mô hình DenseNet hiệu quả, tối ưu cho dữ liệu Việt Nam.
Hỗ trợ phân tích và trực quan hóa dữ liệu lớn.

Yêu Cầu Hệ Thống

Python 3.11+.
GPU khuyến nghị (NVIDIA Tesla T4 hoặc tương đương cho training).
Không gian lưu trữ: ~5-10GB cho dataset crawled.

Cài Đặt

Clone repository:
textgit clone https://github.com/saimonviet/KHDL_Dudoan_Dotuoi.git
cd KHDL_Dudoan_Dotuoi

Cài đặt dependencies (sử dụng virtual environment):
textpython -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

pip install -r requirements.txt

Chuẩn bị dataset:

Tải UKTFaces-IMDB-Wiki downsampled từ Kaggle: UKTFaces-IMDB-Wiki-10-70.
Đặt vào thư mục /data/ (hoặc chỉnh sửa đường dẫn trong densenet_KHDL.ipynb).



Hướng Dẫn Sử Dụng

Thu thập dữ liệu (chạy một lần):
textpython crawl.py

Crawl ~150 ảnh/tuổi (1-70) vào thư mục images/age_{age}.


Làm sạch và lọc khuôn mặt:
textpython data.py  # Lọc ảnh không có khuôn mặt trong dataset_crawled_v2
python clean.py  # Load, resize và chuẩn hóa vào X, y (NumPy arrays)

Phân tích và trực quan hóa:
textpython full.py  # Chạy toàn bộ: crawl (comment nếu đã có), analyze, clean, visualize

Tạo biểu đồ số lượng ảnh theo tuổi và t-SNE embedding.


Huấn luyện mô hình (sử dụng Jupyter Notebook):

Mở densenet_KHDL.ipynb trong Jupyter/Kaggle.
Chạy các cell để xử lý metadata, augmentation (ImageDataGenerator), train DenseNet (Adam optimizer, EarlyStopping).
Lưu mô hình: model.save('age_prediction_densenet.h5').


Dự đoán:
pythonfrom tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('age_prediction_densenet.h5')
img_path = 'path/to/test_image.jpg'
img = image.load_img(img_path, target_size=(128, 128))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)
predicted_age = model.predict(img_array)[0][0]
print(f"Tuổi dự đoán: {int(predicted_age)}")


Cấu Trúc Thư Mục
textKHDL_Dudoan_Dotuoi/
├── images/              # Dataset crawled (age_1/ ... age_70/)
├── dataset_crawled_v2/  # Dataset đã lọc
├── data/                # UKTFaces-IMDB-Wiki (downsampled)
├── scripts/
│   ├── crawl.py         # Crawl ảnh
│   ├── data.py          # Lọc khuôn mặt
│   ├── clean.py         # Resize và chuẩn hóa
│   └── full.py          # Pipeline đầy đủ
├── densenet_KHDL.ipynb  # Notebook huấn luyện DenseNet
├── requirements.txt     # Dependencies
└── README.md
Kết Quả & Đánh Giá

MAE: ~46.84 (validation set).
Dataset: >10.000 ảnh, lọc >90% ảnh hợp lệ có khuôn mặt.
Trực quan: Biểu đồ barplot số lượng ảnh/tuổi; t-SNE cho clustering độ tuổi.
