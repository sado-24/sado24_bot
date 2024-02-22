import os
import uuid


def get_channel_image_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("channel-images/", filename)


def get_podcast_image_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("podcast-images/", filename)


def get_collection_image_path(_, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("collection-images/", filename)
