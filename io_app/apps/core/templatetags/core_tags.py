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
    disallowed_extensions = MediaConsts.COMMON_ARCHIVE_EXTENSIONS
    can_be_previewed = "true"

    if file.extension in disallowed_extensions:
        can_be_previewed = "false"

    return can_be_previewed
