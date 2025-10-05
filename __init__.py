from nodes.prompts import DOC_SaveImageAndAddToHistory


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DOC_Timestamp": DOC_SaveImageAndAddToHistory,
}

# This magic will use a property DISPLAY_NAME on each node to get the display name of the node for the UI
# This removees the need to define display names for all nodes in this file.
NODE_DISPLAY_NAME_MAPPINGS = {key: getattr(value, 'DISPLAY_NAME', None) for key, value in NODE_CLASS_MAPPINGS.items()}