from django import template
from django.templatetags.static import static
from io_app.consts import MediaConsts


register = template.Library()


@register.simple_tag(takes_context=True)
def get_icon_for_file(context, file):
    icons_prefix = "icons/"
    icon = "file_icon.svg"

    for ext_set in MediaConsts.ICONS_FOR_EXTENSIONS:
        if file.extension in ext_set["extensions"]:
            icon = ext_set["icon"]
            break

    return static(icons_prefix + icon)


@register.simple_tag(takes_context=True)
def can_file_be_previewed(context, file):
    return "true" if file.can_be_previewed() else "false"


@register.simple_tag(takes_context=True)
def is_media_file(context, file):
    media_extensions = MediaConsts.COMMON_AUDIO_EXTENSIONS + MediaConsts.COMMON_VIDEO_EXTENSIONS

    return "true" if file.extension in media_extensions else "false"

