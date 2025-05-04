import aiohttp
import os
import mimetypes
import re
import asyncio
from pathlib import Path
from uuid import uuid4
from typing import Optional
from PIL import Image

from .interfaces import IFileDownloader
from app.core.config import BASE_DIR


class FileDownloader(IFileDownloader):
    def __init__(self, base_storage_path: str = BASE_DIR):
        self.base_storage_path = Path(base_storage_path)
        self.base_storage_path.mkdir(parents=True, exist_ok=True)

    async def download_file(
        self, 
        url: str, 
        filename: Optional[str] = None,
        compress_image: bool = True,
        quality: int = 75
    ) -> str:

        folder_path = self.base_storage_path

        if filename is None:
            filename = f"{uuid4().hex}"

        file_path = None

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                extension = self._get_extension_from_response(response)
                filename += extension
                file_path = folder_path / filename

                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

        if compress_image and self._is_image(file_path):
            self._compress_image(file_path, quality)

        # relative_path = os.path.relpath(file_path, self.base_storage_path)
        return str(self.base_storage_path / file_path)

    def _is_image(self, file_path: Path) -> bool:
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def _compress_image(self, file_path: Path, quality: int):
        try:
            with Image.open(file_path) as img:
                img.save(file_path, optimize=True, quality=quality)
        except Exception as e:
            print(f"Ошибка при сжатии изображения {file_path.name}: {e}")

    def _get_extension_from_response(self, response, fallback_extension=".bin"):
        content_disposition = response.headers.get("Content-Disposition")
        
        if content_disposition:
            filename_match = re.findall('filename="(.+)"', content_disposition)
            if filename_match:
                filename = filename_match[0]
                return Path(filename).suffix

        content_type = response.headers.get("Content-Type")
        if content_type:
            extension = mimetypes.guess_extension(content_type)
            if extension:
                return extension

        return fallback_extension


async def main():
    file_loader = FileDownloader(Path(r'C:\projects\activity_monitor\backend\static\images'))
    f_path = await file_loader.download_file(
        r'https://99frank.bitrix24.ru/rest/crm.controller.item.getFile.json?auth=c3330d680073b32a001252ad00002e0d403807e6b9b968cd0a1b9a60395787dfe1403b&token=crm%7CYWN0aW9uPWNybS5jb250cm9sbGVyLml0ZW0uZ2V0RmlsZSZTSVRFX0lEPXMxJmVudGl0eVR5cGVJZD0xODgmaWQ9NDEmZmllbGROYW1lPVVGX0NSTV83M18xNzE0MDExMzY2JmZpbGVJZD04ODY0MDkmXz1HaGFCQWxGMXhXQmk4dVg4MUFrSm45OXZXaDB0Y1pvVw%3D%3D%7CImNybS5jb250cm9sbGVyLml0ZW0uZ2V0ZmlsZXxjcm18WVdOMGFXOXVQV055YlM1amIyNTBjbTlzYkdWeUxtbDBaVzB1WjJWMFJtbHNaU1pUU1ZSRlgwbEVQWE14Sm1WdWRHbDBlVlI1Y0dWSlpEMHhPRGdtYVdROU5ERW1abWxsYkdST1lXMWxQVlZHWDBOU1RWODNNMTh4TnpFME1ERXhNelkySm1acGJHVkpaRDA0T0RZME1Ea21YejFIYUdGQ1FXeEdNWGhYUW1rNGRWZzRNVUZyU200NU9YWlhhREIwWTFwdlZ3PT18YzMzMzBkNjgwMDczYjMyYTAwMTI1MmFkMDAwMDJlMGQ0MDM4MDdlNmI5Yjk2OGNkMGExYjlhNjAzOTU3ODdkZmUxNDAzYiI%3D.fmoyD7Y4GTcQT60j%2Fz3VnchXHEQGPyrJ%2BfaAhL5vyU8%3D',
    )
    print(f_path)


if __name__ == '__main__':
    asyncio.run(main())


# python -m app.infrastructure.file_downloader.file_downloader
# .\venv\Scripts\activate
