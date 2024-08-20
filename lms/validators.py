import re
from rest_framework.serializers import ValidationError


def validate_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    if not re.match(youtube_regex, url):
        raise ValidationError('Invalid URL! Only YouTube links are allowed.')
