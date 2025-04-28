from typing import Protocol

class IFileDownloader(Protocol):
    async def download_file(
        self, 
        url: str, 
        filename: str | None = None,
        compress_image: bool = False,
        quality: int = 85
    ) -> str:
        pass
