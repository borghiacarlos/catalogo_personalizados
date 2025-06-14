import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_embed_url')
def get_embed_url(video_url):
    """
    Transforma um URL normal do YouTube num URL de incorporação.
    Ex: https://www.youtube.com/watch?v=ABCDEFG -> https://www.youtube.com/embed/ABCDEFG
    """
    if not video_url:
        return ""
    
    # Usa expressões regulares para encontrar o ID do vídeo em vários formatos de URL
    regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = re.search(regex, video_url)
    
    if match:
        video_id = match.group(6)
        # Retorna o URL de incorporação correto e limpo
        return f"https://www.youtube.com/embed/{video_id}"
    
    # Se não for um URL do YouTube, retorna o URL original
    return video_url
