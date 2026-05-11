import requests
import time

from logger_config import (
    etl_logger,
    api_logger
)

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

REQUEST_DELAY = 0.5
MAX_RETRIES = 5
TIMEOUT = 15

session = requests.Session()

session.headers.update({
    "User-Agent": "CivitasETL/1.0"
})


def safe_request(url):
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = session.get(
                url,
                timeout=TIMEOUT
            )

            if response.status_code == 429:
                wait = 2 ** retries

                api_logger.warning(
                    f"429 Rate Limit | Waiting {wait}s"
                )

                time.sleep(wait)

                retries += 1
                continue

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            api_logger.error(f"Timeout: {url}")

        except requests.exceptions.ConnectionError:
            api_logger.error(f"Connection Error: {url}")

        except requests.exceptions.HTTPError as e:
            api_logger.error(
                f"HTTP Error {response.status_code}: {url}"
            )

        except Exception as e:
            api_logger.error(
                f"Unexpected Error: {str(e)}"
            )

        retries += 1

        wait = 2 ** retries

        time.sleep(wait)

    return None


def obter_lista_deputados():
    deputados = []

    url = f"{BASE_URL}/deputados?itens=100"

    while url:
        data = safe_request(url)

        if not data:
            break

        deputados.extend(data["dados"])

        etl_logger.info(
            f"Loaded page | total={len(deputados)}"
        )

        next_url = None

        for link in data.get("links", []):
            if link["rel"] == "next":
                next_url = link["href"]

        url = next_url

        time.sleep(REQUEST_DELAY)

    return deputados


def obter_detalhes_deputado(deputado_id):
    url = f"{BASE_URL}/deputados/{deputado_id}"

    data = safe_request(url)

    time.sleep(REQUEST_DELAY)

    if not data:
        return None

    return data.get("dados")