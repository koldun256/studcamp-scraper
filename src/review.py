from dataclasses import dataclass

@dataclass
class Review:
    review_id: str
    review_body: str
    date: str
    rating: 1 | 2 | 3 | 4 | 5
    likes: int
    dislikes: int
    profile_name: str
    profile_url: str
    profile_image_url: str