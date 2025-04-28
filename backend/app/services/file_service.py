import os
import asyncio
from pathlib import Path
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urlparse, parse_qs

from app.infrastructure.file_downloader.file_downloader import FileDownloader
from app.parameters.params import BASE_DIR, PATCH_TO_UPLOADS


class FileService:
    def __init__(self, file_downloader: FileDownloader, base_path: str):
        self.file_downloader = file_downloader
        self.base_path = base_path

    async def save_file_from_url(self, url: str, old_image_token: Optional[str], filename: Optional[str] = None) -> dict:
        image_token = self.get_image_token_from_url(url)
        if image_token == old_image_token:
            return None

        image_path = await self.file_downloader.download_file(url, filename)
        relative_image_path = str(Path(image_path).relative_to(self.base_path))

        return {
            "image_token": image_token,
            "image_path": relative_image_path
        }

    def get_image_token_from_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        token_value = query_params.get('token', [None])[0]
        return token_value


class FileServiceFactory:
    @staticmethod
    def create() -> FileService:
        base_path = Path(BASE_DIR)
        relative_path_to_images = PATCH_TO_UPLOADS
        file_downloader = FileDownloader(base_path / relative_path_to_images)
        return FileService(file_downloader, base_path)


async def main():
    file_service = FileServiceFactory.create()
    result = await file_service.save_file_from_url(
        url=r'https://99frank.bitrix24.ru/rest/crm.controller.item.getFile.json?auth=fcc10d680073b32a001252ad00002e0d4038072a38ef8a0e6df6e980b0183838c077f0&token=crm%7CYWN0aW9uPWNybS5jb250cm9sbGVyLml0ZW0uZ2V0RmlsZSZTSVRFX0lEPXMxJmVudGl0eVR5cGVJZD0xNjYmaWQ9MzQ5NyZmaWVsZE5hbWU9VUZfQ1JNXzIxXzE3NDUyNDg3MzkmZmlsZUlkPTkzMDc3NSZfPU44M3dxazRoRnNGYkN5NDgyZFIwMG5ZUnhiTThtRFc5%7CImNybS5jb250cm9sbGVyLml0ZW0uZ2V0ZmlsZXxjcm18WVdOMGFXOXVQV055YlM1amIyNTBjbTlzYkdWeUxtbDBaVzB1WjJWMFJtbHNaU1pUU1ZSRlgwbEVQWE14Sm1WdWRHbDBlVlI1Y0dWSlpEMHhOalltYVdROU16UTVOeVptYVdWc1pFNWhiV1U5VlVaZlExSk5Yekl4WHpFM05EVXlORGczTXprbVptbHNaVWxrUFRrek1EYzNOU1pmUFU0NE0zZHhhelJvUm5OR1lrTjVORGd5WkZJd01HNVpVbmhpVFRodFJGYzV8ZmNjMTBkNjgwMDczYjMyYTAwMTI1MmFkMDAwMDJlMGQ0MDM4MDcyYTM4ZWY4YTBlNmRmNmU5ODBiMDE4MzgzOGMwNzdmMCI%3D.hi7DJQfTlLC0zHZWzlq%2BHxzAdKPwre4Fgvp7dIJ%2FV5Q%3D',
        old_image_token='old_image_token',
        filename='test_file'
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())


# python -m app.services.file_service
# .\venv\Scripts\activate
