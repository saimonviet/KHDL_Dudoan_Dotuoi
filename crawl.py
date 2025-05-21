from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import os

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

def crawl_images_for_age(age, max_images=150):
    folder = f"images/age_{age}"
    os.makedirs(folder, exist_ok=True)

    keywords = get_keywords(age)
    per_keyword = max_images // len(keywords)

    for keyword in keywords:
        print(f"🔍 Crawling {per_keyword} images for: '{keyword}' (Tuổi: {age})")
        
        # Dùng Google (ưu tiên do icrawler hỗ trợ tốt hơn mặc định)
        crawler = GoogleImageCrawler(storage={"root_dir": folder}, downloader_threads=4)
        crawler.crawl(keyword=keyword, max_num=per_keyword, file_idx_offset='auto')

        # Nếu bạn muốn dùng Bing thay thế hoặc bổ sung:
        crawler = BingImageCrawler(storage={"root_dir": folder}, downloader_threads=4)
        crawler.crawl(keyword=keyword, max_num=per_keyword, file_idx_offset='auto',
                      filters={"type": "photo"})

# Danh sách độ tuổi (có thể thay bằng range nhỏ hơn nếu cần nhanh hơn)
age_list = range(1, 71)  # 1 đến 70 tuổi

for age in age_list:
    crawl_images_for_age(age, max_images=150)

print("✅ Hoàn tất tải dữ liệu hình ảnh.")
