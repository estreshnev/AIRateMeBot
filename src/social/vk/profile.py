import httpx
from src.config import VK_API_VERSION, VK_ACCESS_TOKEN
from src.core.social_interface import SocialProfileProvider
from typing import Optional

API_URL = "https://api.vk.com/method"

async def fetch_user_data(client, username: str) -> dict:
    resp = await client.get(
        f"{API_URL}/users.get",
        params={
            "user_ids": username,
            "fields": "city,bdate,photo_200,followers_count",
            "access_token": VK_ACCESS_TOKEN,
            "v": VK_API_VERSION,
        }
    )
    data = resp.json()
    if "error" in data:
        raise ValueError(f"VK API error: {data['error']['error_msg']}")
    return data["response"][0]

async def fetch_wall_data(client, username: str, count: int = 10) -> list:
    resp = await client.get(
        f"{API_URL}/wall.get",
        params={
            "domain": username,
            "count": count,
            "access_token": VK_ACCESS_TOKEN,
            "v": VK_API_VERSION,
        }
    )
    data = resp.json()
    return data.get("response", {}).get("items", [])

def parse_profile_data(user_data: dict) -> dict:
    name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
    city = user_data.get("city", {}).get("title", "Не указано")
    bdate = user_data.get("bdate", "")
    age = _parse_age(bdate) if bdate.count(".") == 2 else None
    friends_count = user_data.get("followers_count", 0)
    has_avatar = bool(user_data.get("photo_200"))
    return {
        "name": name,
        "city": city,
        "bdate": bdate,
        "age": age,
        "friends_count": friends_count,
        "has_avatar": has_avatar,
    }

def parse_wall_data(wall_items: list) -> dict:
    posts = []
    reposts = 0
    likes_total = 0
    for item in wall_items:
        if "copy_history" in item:
            reposts += 1
        if text := item.get("text"):
            posts.append(text)
        likes_total += item.get("likes", {}).get("count", 0)
    return {
        "posts": posts,
        "reposts": reposts,
        "likes_total": likes_total,
    }

def build_meta_summary(profile: dict, wall: dict) -> tuple[str, str, str]:
    age = profile["age"]
    age_group = (
        "18–25" if isinstance(age, int) and age < 26 else
        "26–35" if isinstance(age, int) and age < 36 else
        "36+" if isinstance(age, int) else "неизвестно"
    )
    engagement_level = (
        "высокий" if wall["likes_total"] > 50 else "средний" if wall["likes_total"] > 10 else "низкий"
    )
    meta_summary = (
        f"Возраст: {age if age is not None else 'Неизвестно'} ({age_group})\n"
        f"Город: {profile['city']}\n"
        f"Аватарка: {'есть' if profile['has_avatar'] else 'нет'}\n"
        f"Постов: {len(wall['posts'])}, репостов: {wall['reposts']}, лайков: {wall['likes_total']}\n"
        f"Активность: {engagement_level}, Подписчиков: {profile['friends_count']}"
    )
    return age_group, engagement_level, meta_summary

def _parse_age(bdate: str) -> Optional[int]:
    from datetime import datetime
    try:
        birth = datetime.strptime(bdate, "%d.%m.%Y")
        today = datetime.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except Exception:
        return None

class VKProfileProvider:
    async def get_profile(self, username: str) -> dict:
        async with httpx.AsyncClient() as client:
            user_data = await fetch_user_data(client, username)
            wall_items = await fetch_wall_data(client, username, count=10)
        profile = parse_profile_data(user_data)
        wall = parse_wall_data(wall_items)
        age_group, engagement_level, meta_summary = build_meta_summary(profile, wall)
        return {
            "username": username,
            "name": profile["name"],
            "city": profile["city"],
            "age": profile["age"] if profile["age"] is not None else "Неизвестно",
            "age_group": age_group,
            "has_avatar": profile["has_avatar"],
            "friends_count": profile["friends_count"],
            "posts": wall["posts"] or ["Профиль без постов."],
            "engagement_level": engagement_level,
            "meta_summary": meta_summary,
        }

    async def get_entity(self, entity_id: str, entity_type: str) -> dict:
        if entity_type == "profile":
            return await self.get_profile(entity_id)
        else:
            raise ValueError(f"Неизвестный тип сущности: {entity_type}") 