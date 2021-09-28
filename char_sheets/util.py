def make_head(subtitle=None, char=None):
    if subtitle:
        subtitle = ' - ' + subtitle
    else:
        subtitle = ''
    return {
        'title': "Para's Characters" + subtitle,
        'description': char['short_description'] if char else "An index of Parakoopa's TTRPG characters",
        'og_title': subtitle if subtitle else "Para's Characters",
        'og_site_name': "Para's Characters",
        'og_image': char.spec('general')['images'][0] if char else '/static/android-icon-192x192.png'
    }