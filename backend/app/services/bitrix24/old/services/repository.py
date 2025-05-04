
from app.bitrix24.client import Bitrix24Client
from app.models.bitrix_data import BitrixDeal
from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.db import async_session_maker


class Bitrix24Repository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.client = Bitrix24Client(api_url="https://your.bitrix.api", api_key="your_api_key")

    async def sync_deals(self):
        deals_data = await self.client.get_deals()
        for deal_data in deals_data:
            existing_deal = await self.session.execute(select(BitrixDeal).filter(BitrixDeal.bitrix_id == deal_data['id']))
            if existing_deal.scalar_one_or_none():
                await self.update_deal(deal_data)
            else:
                await self.add_deal(deal_data)

    async def add_deal(self, deal_data: dict):
        deal = BitrixDeal(**deal_data)
        self.session.add(deal)
        await self.session.commit()

    async def update_deal(self, deal_data: dict):
        deal = await self.session.execute(select(BitrixDeal).filter(BitrixDeal.bitrix_id == deal_data['id']))
        deal_instance = deal.scalar_one_or_none()
        if deal_instance:
            for key, value in deal_data.items():
                setattr(deal_instance, key, value)
            await self.session.commit()
