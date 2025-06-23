from src.social.vk import VKProfileProvider
from src.core.utils import VK_PROFILE_REGEX, VK_GROUP_REGEX, parse_social_link

class SocialProviderFactory:
    @staticmethod
    def get_profile_provider_by_url(url: str):
        if VK_PROFILE_REGEX.match(url) or VK_GROUP_REGEX.match(url):
            return VKProfileProvider()
        # Здесь можно добавить другие соцсети (например, Telegram, Instagram)
        raise ValueError("Не удалось определить провайдера по ссылке")

    @staticmethod
    def get_profile_provider_by_username(username: str):
        # Можно добавить логику по username (например, если есть префиксы для других соцсетей)
        return VKProfileProvider()

    @staticmethod
    def get_entity_provider_by_url(url: str):
        parsed = parse_social_link(url)
        if not parsed:
            raise ValueError("Не удалось определить тип сущности по ссылке")
        provider = VKProfileProvider()  # Пока только VK
        return provider, parsed["entity_type"], parsed["entity_id"] 