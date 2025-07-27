import time
import requests
import json

def geocode(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1  # IMPORTANT: get structured address
        # IMPORTANT : obtenir une adresse structurée
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MyGeocoder/1.0; +http://yourdomain.com)'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return {'message': str(e)}

    if response.status_code != 200:
        return f'{response.status_code}: {response.text}'

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format!")
        # print("Erreur : la réponse n'est pas au format JSON !")
        print("Response content:", response.text)
        # print("Contenu de la réponse :", response.text)
        return None

    if not data:
        print("Nothing found.")
        # print("Aucun résultat trouvé.")
        return None

    address_data = data[0].get('address', {})
    print(json.dumps(data[0], indent = 6))
    # Universal way to get locality (city/town/village)
    # Méthode universelle pour obtenir la localité (ville/commune/village)
    locality = (
        address_data.get('city') or
        address_data.get('town') or
        address_data.get('village') or
        address_data.get('hamlet') or
        address_data.get('municipality') or
        ''
    )

    # Universal way to get street name
    # Méthode universelle pour obtenir le nom de la rue
    street = (
        address_data.get('road') or
        address_data.get('pedestrian') or
        address_data.get('path') or
        address_data.get('footway') or
        address_data.get('street') or
        ''
    )

    result = {
        'street': street,
        'house_number': address_data.get('house_number', ''),
        'zip_code': address_data.get('postcode', ''),
        'locality': locality,
        'region': address_data.get('state', ''),
        'country': address_data.get('country', ''),
        'country_code': address_data.get('country_code', '').upper(),
        'lat': data[0].get('lat', ''),
        'lon': data[0].get('lon', ''),
    }
    time.sleep(1)
    return result

if __name__ == '__main__':
    geocode()
