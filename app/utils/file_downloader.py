import requests
import tempfile
from app.utils.logger import get_logger

logger = get_logger("file_downloader")

def download_file_from_url(url: str, suffix: str = ".pdf") -> str:
    """
    Downloads a file from the given URL and returns the local temporary path.
    Raises an HTTPError if the request fails.
    """
    logger.info(f"Downloading file from URL: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download file: {e}")
        raise

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(response.content)
        logger.info(f"File saved to temporary path: {tmp_file.name}")
        return tmp_file.name