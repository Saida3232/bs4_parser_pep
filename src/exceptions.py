class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class PageNotFound(Exception):
    """Вызывается, когда не получается загрузить страницу."""
