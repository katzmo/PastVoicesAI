# Utility functions for processing Europeana API responses

# Get the preferred translation or any if the preferred one is not available
def get_lang_or_any(map, lang="en"):
    if map is None or len(map) == 0:
        return []
    return map.get(lang, next(iter(map.values())))


# Extract relevant data from the API response
def clean_data(item):
    return {
        "title": get_lang_or_any(item.get("dcTitleLangAware")) or ["???"],
        "creator": get_lang_or_any(item.get("edmAgentLabelLangAware"))
        or get_lang_or_any(item.get("dcCreatorLangAware")),
        "description": get_lang_or_any(item.get("dcDescriptionLangAware")),
        "concept": get_lang_or_any(item.get("edmConceptPrefLabelLangAware")),
        "place": get_lang_or_any(item.get("edmPlaceLabelLangAware")),
        "year": item.get("year")
        or get_lang_or_any(item.get("edmTimespanLabelLangAware")),
        "provider": item.get("dataProvider", []),
        "preview": item.get("edmPreview", []),
        "website": item.get("edmIsShownAt", []),
    }
