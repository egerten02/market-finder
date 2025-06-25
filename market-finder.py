import requests
from geopy.distance import geodesic

# Konum
def get_current_location():
    default_location = (41.102660, 28.974830)
    return default_location

# Marketlerin konumunu bulma
def find_markets(location, market_names, radius):
    latitude, longitude = location
    markets = []
    for market_name in market_names:
        # Overpass API Sorgusu
        query = f"""[out:json]; node ["name"~"{market_name}"]
          (around:{radius},{latitude},{longitude}); out body;"""
        response = requests.post("http://overpass-api.de/api/interpreter", data=query)
        response.raise_for_status()
        data = response.json()
        for element in data['elements']:
            element['distance_km'] = geodesic(location, (element['lat'], element['lon'])).km
        markets.extend(data['elements'])

    # Marketleri mesafeye göre sıralar
    return sorted(markets, key=lambda x: x['distance_km'])[:5]

# En yakın marketlerin yol tarifi linklerini terminalde listeleme
def list_markets_with_directions(markets, location):
    for i, market in enumerate(markets, start=1):
        name = market.get('tags', {}).get('name', 'Market')
        distance_km = market['distance_km']
        market_lat = market['lat']
        market_lon = market['lon']

        directions_url = f"https://www.google.com/maps/dir/{location[0]},{location[1]}/{market_lat},{market_lon}"
        print(f"{i}. {name}: {distance_km:.2f} km - Yol Tarifi için: {directions_url}")

# Kullanıcının konumu
location = get_current_location()
print(f"Konumunuz: {location}")

# Aranacak market isimleri
market_names = ["Migros", "Macrocenter", "CarrefourSA"]

radius = int(input("Metre cinsinden aranacak maksimum mesafeyi yazın: "))
print("Yakınınızdaki marketler aranıyor...")
markets = find_markets(location, market_names, radius)

# En yakın marketleri mesafe ve yol tarifi ile terminalde gösterir
if markets:
    print(f"\nSize en yakın {len(markets)} market:")
    list_markets_with_directions(markets, location)  # Terminalde yol tarifi linklerini listele
else:
    print("Yakınınızda market bulunamadı. Arama mesafesini genişletip tekrar deneyebilirsiniz.")