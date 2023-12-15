from django.utils.text import slugify


class EmptySlugError(ValueError):
    pass


class SlugTooLongError(ValueError):
    pass


def create_unique_slug(instance, field_name="title", max_length=255):
    """
    Creates a unique slug for the given model instance.
    Args:
        instance (django.db.models.Model): Model instance for which the slug is to be created.
        field_name (str): Field name to be used for creating the slug.

    Returns:
        str: The generated unique slug.
    """
    # Define symbol_mapping
    symbol_mapping = (
        # symbols
        (" ", "-"),
        ("!", ""),
        ('"', ""),
        ("#", ""),
        ("$", ""),
        ("%", ""),
        ("&", "and"),
        ("'", ""),
        ("(", ""),
        (")", ""),
        ("*", ""),
        ("+", ""),
        (",", ""),
        ("-", ""),
        (".", ""),
        ("/", ""),
        (":", ""),
        (";", ""),
        ("<", ""),
        ("=", ""),
        (">", ""),
        ("?", ""),
        ("@", "at"),
        ("[", ""),
        ("\\", ""),
        ("]", ""),
        ("^", ""),
        ("_", ""),
        ("`", ""),
        ("{", ""),
        ("|", ""),
        ("}", ""),
        ("~", ""),
        ("№", "no"),
        # Azerbaijani alphabet
        ("ç", "c"),
        ('ə', 'e'),
        ('ğ', 'g'),
        ("ı", "i"),
        ('İ', 'I'),
        ('ö', 'o'),
        ('ş', 's'),
        ('ü', 'u'),
    )

    # Get the field value
    field_value = getattr(instance, field_name)

    # Replace symbols based on symbol_mapping
    for symbol, replacement in symbol_mapping:
        field_value = field_value.replace(symbol, replacement)

    # Apply slugify to the modified field value
    base_slug = slugify(field_value)
    unique_slug = base_slug
    counter = 1

    # Create a unique slug
    queryset = instance.__class__.objects.filter(slug=unique_slug)
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
        queryset = instance.__class__.objects.filter(slug=unique_slug)

    if not unique_slug:
        raise EmptySlugError("Generated unique slug is empty.")

    if len(unique_slug) > max_length:
        raise SlugTooLongError("Generated unique slug is too long.")

    return unique_slug
