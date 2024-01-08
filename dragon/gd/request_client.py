from typing import Dict

import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": ""
}


def make(endpoint: str, data: Dict[str, any]):
    data["secret"] = "Wmfd2893gb7"

    response = requests.request(
        "POST",
        f"http://www.boomlings.com/database/{endpoint}.php",
        headers=headers,
        data=data
    )
    return response
