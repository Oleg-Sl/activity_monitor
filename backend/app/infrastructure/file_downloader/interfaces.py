from typing import Protocol, Optional

class IFileDownloader(Protocol):
    async def download_file(
        self, 
        url: str, 
        filename: Optional[str] = None,
        compress_image: bool = False,
        quality: int = 85
    ) -> str:
        pass
