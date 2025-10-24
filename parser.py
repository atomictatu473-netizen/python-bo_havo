import httpx
from bs4 import BeautifulSoup

class ObHavoClient:
    def __init__(self, city: str = "tashkent"):
        self.base_url = f"https://obhavo.uz/{city}"

    async def _fetch_html(self) -> str:
        """Asinxron tarzda sahifani yuklaydi."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.base_url)
            resp.raise_for_status()
            return resp.text

    def _parse_weather(self, html: str) -> dict:
        """HTML sahifadan kerakli ob-havo ma’lumotlarini ajratib oladi."""
        soup = BeautifulSoup(html, "html.parser")

        city = soup.find("h2").text.strip()
        date = soup.find("div", class_="current-day").text.strip()

        forecast_block = soup.find("div", class_="current-forecast")
        current_temp_day = forecast_block.find_all("span")[1].text.strip()
        current_temp_night = forecast_block.find_all("span")[2].text.strip()
        description = soup.find("div", class_="current-forecast-desc").text.strip()
        current_icon = forecast_block.find("img")["src"]

        forecast_day_div = soup.find("div", class_="current-forecast-day")
        time_blocks = forecast_day_div.find_all("div", class_=lambda x: x and x.startswith("col-"))

        times = {}
        for block in time_blocks:
            time_name = block.find("p", class_="time-of-day").text.strip()
            temp = block.find("p", class_="forecast").text.strip()
            icon = block.find("img")["src"]
            times[time_name] = {"temp": temp, "icon": icon}

        return {
            "city": city,
            "date": date,
            "current": {
                "temp_day": current_temp_day,
                "temp_night": current_temp_night,
                "description": description,
                "icon": current_icon
            },
            "times_of_day": times
        }

    async def get_weather(self) -> dict:
        """Bosh metod – sahifani yuklaydi va tayyor JSON ma’lumotni qaytaradi."""
        html = await self._fetch_html()
        data = self._parse_weather(html)
        return data