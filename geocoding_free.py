"""
geocoding_free.py
Geocoding HOÀN TOÀN MIỄN PHÍ cho địa chỉ Việt Nam
"""

import requests
import time
from typing import Optional, Tuple


def geocode_photon(address: str) -> Optional[Tuple[float, float]]:
    """Sử dụng Photon API từ Komoot (miễn phí, nhanh)"""
    try:
        url = "https://photon.komoot.io/api/"
        params = {'q': f"{address}, Vietnam", 'limit': 1, 'lang': 'en'}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'features' in data and len(data['features']) > 0:
                coords = data['features'][0]['geometry']['coordinates']
                lng, lat = coords[0], coords[1]
                return (lat, lng)
        return None
    except:
        return None


def geocode_osm(address: str) -> Optional[Tuple[float, float]]:
    """Sử dụng OpenStreetMap Nominatim"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{address}, Vietnam",
            'format': 'json',
            'limit': 1,
            'countrycodes': 'vn'
        }
        headers = {'User-Agent': 'BloodDonationApp/1.0'}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lng = float(data[0]['lon'])
                return (lat, lng)
        return None
    except:
        return None


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Hàm chính - Geocode địa chỉ Việt Nam bằng nhiều phương pháp miễn phí
    
    Args:
        address: Địa chỉ cần geocode
        
    Returns:
        Tuple (lat, lng) hoặc None nếu không tìm thấy
    """
    if not address or not address.strip():
        print("❌ Địa chỉ rỗng")
        return None
    
    print(f"\n{'='*70}")
    print(f"🔍 GEOCODING MIỄN PHÍ")
    print(f"   Địa chỉ: '{address}'")
    print(f"{'='*70}")
    
    # Thử Photon trước
    print("\n🔍 [1/2] Đang thử Photon API...")
    result = geocode_photon(address)
    if result:
        lat, lng = result
        print(f"   ✅ THÀNH CÔNG!")
        print(f"   📍 Tọa độ: ({lat}, {lng})")
        print(f"{'='*70}\n")
        return result
    else:
        print(f"   ⚠️ Không tìm thấy")
    
    time.sleep(1)
    
    # Thử OpenStreetMap
    print("\n🔍 [2/2] Đang thử OpenStreetMap...")
    result = geocode_osm(address)
    if result:
        lat, lng = result
        print(f"   ✅ THÀNH CÔNG!")
        print(f"   📍 Tọa độ: ({lat}, {lng})")
        print(f"{'='*70}\n")
        return result
    else:
        print(f"   ⚠️ Không tìm thấy")
    
    print(f"\n❌ THẤT BẠI - Không tìm thấy tọa độ")
    print(f"{'='*70}\n")
    return None


# Test
if __name__ == "__main__":
    print("\n🧪 TEST GEOCODING\n")
    
    test_addresses = [
        "Bệnh viện Chợ Rẫy, TP.HCM",
        "Đại học Bách Khoa, TP.HCM"
    ]
    
    for addr in test_addresses:
        coords = geocode_address(addr)
        print(f"Kết quả: {coords}\n")
        time.sleep(2)