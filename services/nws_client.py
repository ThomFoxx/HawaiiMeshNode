import requests


BASE_URL = "https://api.weather.gov"

HEADERS = {
    "User-Agent": "HawaiiMeshNode/0.1",
    "Accept": "application/geo+json",
}


class NwsClient:
    def get_json(self, url):
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def get_point(self, latitude, longitude):
        url = f"{BASE_URL}/points/{latitude},{longitude}"

        return self.get_json(url)

    def get_recent_observations(self, station_url, limit=5):
        url = f"{station_url}/observations?limit={limit}"

        return self.get_json(url)