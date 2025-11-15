from datetime import datetime
from geopy.distance import geodesic

def calculate_distance(user_coords, hospital_coords):
    """Tính khoảng cách (km) giữa 2 tọa độ."""
    return geodesic(user_coords, hospital_coords).km

def calculate_ai_score(distance, user, radius_km):
    """
    Tính điểm phù hợp (0-1) cho người dùng dựa trên nhiều yếu tố.
    - 40% từ khoảng cách
    - 30% từ lịch sử hiến máu
    - 30% từ thời gian phù hợp
    """
    # 1. Điểm khoảng cách (càng gần điểm càng cao)
    distance_score = max(0, 1 - (distance / radius_km))
    
    # 2. Điểm lịch sử hiến máu (lần hiến cuối càng xa càng tốt)
    if user.last_donation:
        days_since_donation = (datetime.now().date() - user.last_donation).days
        # Cần đợi ít nhất 84 ngày (12 tuần)
        if days_since_donation < 84:
            history_score = 0
        else:
            # Điểm tăng dần đến 180 ngày
            history_score = min(1.0, (days_since_donation - 84) / (180 - 84))
    else:
        # Chưa hiến bao giờ = hoàn toàn sẵn sàng
        history_score = 1.0
    
    # 3. Điểm thời gian (giờ hành chính tốt hơn)
    current_hour = datetime.now().hour
    time_score = 1.0 if 8 <= current_hour < 20 else 0.5 # Từ 8h sáng đến 8h tối
    
    # Điểm tổng hợp cuối cùng
    final_score = (
        distance_score * 0.4 +
        history_score * 0.3 +
        time_score * 0.3
    )
    return final_score

def filter_nearby_users(hospital, users, radius_km=10):
    """
    Lọc danh sách người dùng dựa trên khoảng cách tới bệnh viện và tính điểm AI.
    """
    hospital_coords = (hospital.lat, hospital.lng)
    results = []
    
    for user in users:
        user_coords = (user.lat, user.lng)
        distance = calculate_distance(user_coords, hospital_coords)
        
        if distance <= radius_km:
            score = calculate_ai_score(distance, user, radius_km)
            results.append({
                'user': user,
                'distance': round(distance, 2),
                'ai_score': round(score, 3)
            })
    
    # Sắp xếp kết quả theo điểm AI giảm dần
    results.sort(key=lambda x: x['ai_score'], reverse=True)
    
    return results

