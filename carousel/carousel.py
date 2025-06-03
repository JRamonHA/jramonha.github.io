import yaml


def nav_button(target_id: str, btn_type: str, text: str) -> str:
    return f'''
    <button class="carousel-control-{btn_type}" type="button" data-bs-target="#{target_id}" data-bs-slide="{btn_type}">
      <span class="carousel-control-{btn_type}-icon" aria-hidden="true"></span>
      <span class="visually-hidden">{text}</span>
    </button>
    '''.strip()


def carousel_item(image: str, index: int, interval: int) -> dict:
    """
    Generate the HTML for a carousel item and its associated indicator.

    Parameters:
    - image: path or URL of the image.
    - index: position of the item within the carousel (0-based).
    - interval: interval in milliseconds for this slide (data-bs-interval).

    Returns:
    - A dictionary with two keys:
        "button" -> the HTML for the indicator <button> for this slide.
        "item"   -> the HTML for the <div class="carousel-item"> corresponding to this slide.
    """
    # Indicator button
    if index == 0:
        button = f'''
        <button type="button"
                data-bs-target="#gallery-carousel"
                data-bs-slide-to="{index}"
                class="active"
                aria-current="true"
                aria-label="Slide {index + 1}">
        </button>
        '''.strip()
    else:
        button = f'''
        <button type="button"
                data-bs-target="#gallery-carousel"
                data-bs-slide-to="{index}"
                aria-label="Slide {index + 1}">
        </button>
        '''.strip()
    
    # Carousel item
    active_class = " active" if index == 0 else ""
    item = f'''
    <div id="gallery-carousel-item-{index}"
         class="carousel-item{active_class}"
         data-bs-interval="{interval}">
      <img src="{image}" class="d-block mx-auto border" alt="Slide {index + 1}">
    </div>
    '''.strip()

    return {
        "button": button,
        "item": item
    }


def carousel(id: str, duration: int, items: list) -> str:
    """
    Build the complete HTML for the carousel, including indicators, slides, and navigation controls.

    Parameters:
    - id: unique identifier for the main <div> of the carousel.
    - duration: default interval (in milliseconds) for each slide.
    - items: list of dictionaries, each containing:
        {
          "image": str
        }

    Returns:
    - A string with the complete HTML for the carousel.
    """
    # Generate each carousel_item with its indicator
    rendered_items = []
    for idx, itm in enumerate(items):
        ci = carousel_item(
            image=itm["image"],
            index=idx,
            interval=duration
        )
        rendered_items.append(ci)

    # Indicators section
    indicators_html = '<div class="carousel-indicators">\n'
    for ci in rendered_items:
        indicators_html += ci["button"] + "\n"
    indicators_html += '</div>'

    # Items section
    inner_html = '<div class="carousel-inner">\n'
    for ci in rendered_items:
        inner_html += ci["item"] + "\n"
    inner_html += '</div>'

    # Navigation buttons
    prev_button = nav_button(id, "prev", "Previous")
    next_button = nav_button(id, "next", "Next")

    # Compose the main container
    html = f'''
    <div id="{id}" class="carousel carousel-dark slide" data-bs-ride="carousel">
      {inner_html}
      {indicators_html}
      {prev_button}
      {next_button}
    </div>
    '''.strip()
    return html


def load_items_from_yaml(yaml_path: str) -> list:
    """
    Read the YAML file and return a list of dictionaries
    with key 'image'.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data
