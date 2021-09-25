class HasOglLikeInventoryTrait:
    """
    Must be an AbstractSpec with an 'inventory' with the following format:
    'inventory': {
        'on_hand': [DocReference(OglItem)],
        'stored': [DocReference(OglItem)],
    },
    """
