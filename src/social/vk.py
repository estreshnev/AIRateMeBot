# src/vk_parser.py

import httpx
from src.config import VK_API_VERSION, VK_ACCESS_TOKEN
from src.core.social_interface import SocialProfileProvider

API_URL = "https://api.vk.com/method"

class VKProfileProvider(SocialProfileProvider):
    async def get_profile(self, username: str) -> dict:
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(
                f"{API_URL}/users.get",
                params={
                    "user_ids": username,
                    "fields": "city,bdate,photo_200,followers_count",
                    "access_token": VK_ACCESS_TOKEN,
                    "v": VK_API_VERSION,
                }
            )
            data = user_resp.json()
            if "error" in data:
                raise ValueError(f"VK API error: {data['error']['error_msg']}")
            user_data = data["response"][0]

            wall_resp = await client.get(
                f"{API_URL}/wall.get",
                params={
                    "domain": username,
                    "count": 5,
                    "access_token": VK_ACCESS_TOKEN,
                    "v": VK_API_VERSION,
                }
            )
            wall_data = wall_resp.json()
            wall_items = wall_data.get("response", {}).get("items", [])
            posts = [item["text"] for item in wall_items if item.get("text")]

        name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
        city = user_data.get("city", {}).get("title", "Не указано")
        bdate = user_data.get("bdate", "")
        age = _parse_age(bdate) if bdate.count(".") == 2 else "Неизвестно"
        friends_count = user_data.get("followers_count", 0)

        return {
            "username": username,
            "name": name,
            "city": city,
            "age": age,
            "friends_count": friends_count,
            "posts": posts or ["Профиль без постов."],
        }

    async def get_group(self, group_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            group_resp = await client.get(
                f"{API_URL}/groups.getById",
                params={
                    "group_id": group_id,
                    "fields": "description,members_count",
                    "access_token": VK_ACCESS_TOKEN,
                    "v": VK_API_VERSION,
                }
            )
            data = group_resp.json()
            if "error" in data:
                raise ValueError(f"VK API error: {data['error']['error_msg']}")
            group_data = data["response"][0]

            wall_resp = await client.get(
                f"{API_URL}/wall.get",
                params={
                    "owner_id": f"-{group_id}",
                    "count": 5,
                    "access_token": VK_ACCESS_TOKEN,
                    "v": VK_API_VERSION,
                }
            )
            wall_data = wall_resp.json()
            wall_items = wall_data.get("response", {}).get("items", [])
            posts = [item["text"] for item in wall_items if item.get("text")]

        return {
            "group_id": group_id,
            "name": group_data.get("name", ""),
            "description": group_data.get("description", ""),
            "members_count": group_data.get("members_count", 0),
            "posts": posts or ["Группа без постов."],
        }

    async def get_entity(self, entity_id: str, entity_type: str) -> dict:
        if entity_type == "profile":
            return await self.get_profile(entity_id)
        elif entity_type == "group":
            return await self.get_group(entity_id)
        else:
            raise ValueError(f"Неизвестный тип сущности: {entity_type}")

def _parse_age(bdate: str) -> int:
    from datetime import datetime
    try:
        birth = datetime.strptime(bdate, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except:
        return "Неизвестно"

# Для обратной совместимости:
async def parse_vk_profile(username: str) -> dict:
    return await VKProfileProvider().get_profile(username)
