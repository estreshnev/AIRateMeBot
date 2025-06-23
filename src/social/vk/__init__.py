from .profile import VKProfileProvider
from .group import VKGroupProvider

async def parse_vk_profile(username: str) -> dict:
    return await VKProfileProvider().get_profile(username)

async def parse_vk_group(group_id: str) -> dict:
    return await VKGroupProvider().get_group(group_id) 