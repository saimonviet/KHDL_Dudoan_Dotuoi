import os
import face_recognition
from PIL import Image

def filter_no_face_images(folder):
    print(f"🔍 Đang kiểm tra ảnh trong: {folder}")
    removed = 0

    for fname in os.listdir(folder):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        path = os.path.join(folder, fname)
        try:
            image = face_recognition.load_image_file(path)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                os.remove(path)
                print(f"❌ Không thấy khuôn mặt, đã xóa: {fname}")
                removed += 1
        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {fname}: {e}")
            os.remove(path)
            removed += 1

    print(f"✅ Đã xóa {removed} ảnh không có khuôn mặt.")

# Kiểm tra tất cả thư mục nhóm tuổi
for group in os.listdir("dataset_crawled_v2"):
    path = os.path.join("dataset_crawled_v2", group)
    if os.path.isdir(path):
        filter_no_face_images(path)
