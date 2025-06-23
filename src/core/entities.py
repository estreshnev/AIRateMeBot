from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SocialProfile:
    username: str
    name: str
    city: str
    age: str
    friends_count: int
    posts: List[str]

@dataclass
class SocialGroup:
    group_id: str
    name: str
    description: Optional[str]
    members_count: int
    posts: List[str] 