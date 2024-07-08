import logging
from requests import RequestException
from exceptions import ParserFindTagException
from constants import EXPECTED_STATUS


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def status_pep(current_status):
    for short_status, status in EXPECTED_STATUS.items():
        if current_status in status:
            return short_status


def add_count(results, count):
    statuses = [('Статус', "Количество")]
    for i in EXPECTED_STATUS.keys():
        statuses.append((i, results.count(i)))
    statuses.append(('Total', len(count)))
    return statuses


def is_status_tag(tag):
    return tag.text == 'Status:'
