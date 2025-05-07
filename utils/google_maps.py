def get_maps_src(code: str) -> str:
    """
    Get the src attribute of the Google Maps iframe from the given code.

    Args:
        code (str): The HTML code containing the Google Maps iframe or src value

    Returns:
        str: The src attribute of the iframe, or an empty string if not found.
    """

    # Validate if the links its from google maps
    if "google.com/maps" not in code:
        raise ValueError(
            "El Src de Google Maps debe ser un iframe de Google Maps o Src"
        )

    # Extract src attribute from the iframe
    if "src=" in code:
        src_index = code.index("src=")
        src = code[src_index:]
        src = src.split('"')[1]
        return src

    # Return current src
    return code
