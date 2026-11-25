
import requests
def get_race_results(year, round_number):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_number}/results/"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "F1IntelligenceLab/0.1.0"},
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.RequestException as error:
        print(f"Error al recuperar los datos: {error}")
        return None


def parse_race_results(data):
    races = data["MRData"]["RaceTable"]["Races"]

    if not races:
        return []

    race = races[0]
    parsed_results = []

    for result in race["Results"]:
        driver = result["Driver"]

        driver_data = {
            "driver_id": driver["driverId"],
            "driver_name": (
                driver["givenName"] + " " + driver["familyName"]
            ),
            "constructor": result["Constructor"]["name"],
            "position": int(result["position"]),
            "grid": int(result["grid"]),
            "points": float(result["points"]),
            "status": result["status"]
        }

        parsed_results.append(driver_data)

    return parsed_results





if __name__ == "__main__":
    data = get_race_results(2026, 2)

    if data is None:
        print("Failed to retrieve race data.")

    else:
        results = parse_race_results(data)

        print("Number of results:", len(results))

        for driver in results:
            print(
                driver["position"],
                driver["driver_name"],
                driver["constructor"],
                driver["points"]
            )
