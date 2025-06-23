import re

VK_PROFILE_REGEX = re.compile(r"(?:https?://)?vk\.com/([A-Za-z0-9_\.]+)")
VK_GROUP_REGEX = re.compile(r"(?:https?://)?vk\.com/(club|public)([0-9]+)")

def extract_vk_username(text: str):
    match = VK_PROFILE_REGEX.match(text.strip())
    return match.group(1) if match else None

def extract_vk_group_id(text: str):
    match = VK_GROUP_REGEX.match(text.strip())
    return match.group(2) if match else None

def parse_social_link(text: str):
    text = text.strip()
    match_group = VK_GROUP_REGEX.match(text)
    if match_group:
        return {"entity_type": "group", "entity_id": match_group.group(2)}
    match_profile = VK_PROFILE_REGEX.match(text)
    if match_profile:
        return {"entity_type": "profile", "entity_id": match_profile.group(1)}
    return None 