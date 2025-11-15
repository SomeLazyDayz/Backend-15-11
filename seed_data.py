import random
from datetime import datetime, timedelta
from app import app, db, User, Hospital

# --- Dữ Liệu Mẫu (ĐÃ CÓ SẴN TỌA ĐỘ) ---
# Tọa độ đã được tính toán trước để không cần gọi API nữa.
ADDRESS_DATA = [
    {"address": "123 Nguyễn Huệ, Quận 5, TP.HCM", "lat": 10.7628, "lng": 106.6800},
    {"address": "456 Hồng Bàng, Quận 5, TP.HCM", "lat": 10.7570, "lng": 106.6575},
    {"address": "987 Trần Hưng Đạo, Quận 1, TP.HCM", "lat": 10.7643, "lng": 106.6883},
    {"address": "147 Nguyễn Thị Minh Khai, Quận 1, TP.HCM", "lat": 10.7758, "lng": 106.6923},
    {"address": "852 Lý Thái Tổ, Quận 3, TP.HCM", "lat": 10.7719, "lng": 106.6713},
    {"address": "246 Nguyễn Tri Phương, Quận 10, TP.HCM", "lat": 10.7635, "lng": 106.6669},
    {"address": "135 Sư Vạn Hạnh, Quận 10, TP.HCM", "lat": 10.7725, "lng": 106.6705},
    {"address": "444 Lũy Bán Bích, Quận 11, TP.HCM", "lat": 10.7702, "lng": 106.6346},
    {"address": "2001 Tây Sơn, Quận Tân Phú, TP.HCM", "lat": 10.8016, "lng": 106.6231},
    {"address": "321 Cách Mạng Tháng 8, Quận 3, TP.HCM", "lat": 10.7813, "lng": 106.6811},
    {"address": "654 Nguyễn Văn Cừ, Quận 5, TP.HCM", "lat": 10.7583, "lng": 106.6823},
    {"address": "258 Pasteur, Quận 1, TP.HCM", "lat": 10.7797, "lng": 106.6934},
    {"address": "579 Đường 3/2, Quận 10, TP.HCM", "lat": 10.7711, "lng": 106.6738},
    {"address": "3001 Tỉnh Lộ 10, Quận 12, TP.HCM", "lat": 10.8687, "lng": 106.6025},
    {"address": "4111 Trường Chinh, Quận Gò Vấp, TP.HCM", "lat": 10.8358, "lng": 106.6432}
]

HOSPITALS_DATA = [{"name": "Bệnh viện Chợ Rẫy", "lat": 10.7546, "lng": 106.6622}]
BLOOD_TYPES = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

def seed_database():
    """Xóa, tạo mới, và nạp dữ liệu mẫu vào database (không cần internet)."""
    with app.app_context():
        print("--- Bắt đầu quá trình Nạp Dữ Liệu vào Database (Offline) ---")
        db.drop_all()
        db.create_all()
        
        print("\n🏥 Đang thêm bệnh viện...")
        for h_data in HOSPITALS_DATA:
            db.session.add(Hospital(**h_data))
        print(" -> Xong.")

        print("\n👥 Đang thêm 100 người dùng với tọa độ có sẵn...")
        for i in range(1, 101):
            # Chọn ngẫu nhiên một địa chỉ đã có sẵn tọa độ
            location_data = random.choice(ADDRESS_DATA)
            
            days_ago = random.randint(30, 180)
            last_donation = datetime.now() - timedelta(days=days_ago)
            
            user = User(
                name=f"Người dùng {i}",
                phone=f"090{i:07d}",
                address=location_data["address"],
                lat=location_data["lat"],
                lng=location_data["lng"],
                blood_type=random.choice(BLOOD_TYPES),
                last_donation=last_donation.date()
            )
            db.session.add(user)

        db.session.commit()
        print("\n--- Nạp Dữ Liệu Hoàn Tất! ---")
        print(f"✅ Đã thêm {len(HOSPITALS_DATA)} bệnh viện và 100 người dùng.")
        print("--------------------------")

if __name__ == '__main__':
    seed_database()

