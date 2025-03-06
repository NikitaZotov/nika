from bs4 import BeautifulSoup


def is_html(text: str) -> bool:
    """
    Check if the provided text contains HTML content.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text contains HTML; False otherwise.
    """
    return bool(BeautifulSoup(text, "html.parser").find())


def html_to_telegram_text(html: str) -> str:
    """
    Convert HTML content to a Telegram-friendly text format.

    If the input is not HTML, it returns the text as is.

    Args:
        html (str): The HTML string to convert.

    Returns:
        str: The converted text suitable for Telegram.
    """
    if not is_html(html):
        return html  # Return the original text if it is not HTML

    result_message = BeautifulSoup(html, 'html.parser')  # Parse the HTML content
    return process_list(result_message).strip()  # Process the parsed HTML and strip whitespace


def process_list(element) -> str:
    """
    Process a BeautifulSoup element containing a list (ordered or unordered)
    and convert it to a plain text format.

    Args:
        element: The BeautifulSoup element to process.

    Returns:
        str: The text representation of the list.
    """
    result = []  # Initialize an empty list to hold the formatted text

    for child in element.find_all(recursive=False):  # Iterate through direct children
        if child.name == 'li':  # Check if the child is a list item
            text = child.get_text(strip=True)  # Get the text of the list item
            nested = ""  # Initialize a variable for nested lists

            # Check for nested ordered or unordered lists
            if child.ol:
                nested = "\n" + process_list(child.ol)  # Process nested ordered list
                child.ol.decompose()  # Remove the nested list from the tree
            elif child.ul:
                nested = "\n" + process_list(child.ul)  # Process nested unordered list
                child.ul.decompose()  # Remove the nested list from the tree

            # Append the formatted list item to the result
            result.append(f"- {text}{nested}")
        elif child.name in ['ol', 'ul']:  # Check for other lists
            result.append(process_list(child))  # Process and append other lists

    return "\n".join(result)  # Join all formatted parts into a single string