from urllib.parse import urljoin
from constants import (
    BASE_DIR, MAIN_DOC_URL, PEP_REGUL, PEP_URL, EXPECTED_STATUS)
from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm
import re
import logging

from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import (
    get_response, find_tag, add_count, status_pep, is_status_tag)
from exceptions import PageNotFound


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')

    response = get_response(session, whats_new_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})

    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})

    result = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        href_join = urljoin(whats_new_url, href)
        response = get_response(session, href_join)
        if response is None:
            raise PageNotFound()

        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')

        dl = find_tag(soup, 'dl').text.replace('\n', ' ')

        result.append((href_join, h1, dl))

    return result


def latest_versions(session):
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise Exception('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    for o in a_tags:
        print(o.text)

    for a in a_tags:
        link = urljoin(MAIN_DOC_URL, a['href'])
        text = re.search(pattern, a.text)
        if text:
            version, status = text.groups()
        else:
            version = a.text
            status = ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    table = find_tag(soup, 'table', attrs={'class': 'docutils'})

    pdf_a4_tag = find_tag(table, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)

    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    pep_urls_tag = soup.find_all(
        'a', attrs={'class': 'pep reference internal',
                    'href': re.compile(PEP_REGUL)}, limit=5)

    results = []
    mismatched_data = []
    for pep_url in tqdm(pep_urls_tag):
        url = urljoin(PEP_URL, pep_url['href'])

        td = pep_url.parent.parent
        status_in_card = find_tag(td, 'td').text[1:]
        response = get_response(session, url)
        if response is None:
            return
        soup = BeautifulSoup(response.text, 'lxml')
        dd = soup.find(is_status_tag)
        status_tag = dd.find_next_sibling(
            'dd')
        status_in_pep_page = status_pep(status_tag.string)

        if status_in_card != '' and status_in_card != status_in_pep_page:
            mismatched_data.append({
                "url": url,
                "status_in_the_card": status_tag.string,
                "expected_status": EXPECTED_STATUS.get(
                    status_in_card, "Unknown")
            })

        results.append(status_in_pep_page)
    list_status = add_count(results, pep_urls_tag)

    if mismatched_data:
        logging.info("Несовпадающие статусы:")
        for item in mismatched_data:
            logging.info(f"URL: {item['url']}")
            logging.info(f"Статус в карточке: {item['status_in_the_card']}")
            logging.info(f"Ожидаемый статус: {item['expected_status']}")
    else:
        logging.info("Несовпадающих статусов не найдено.")

    return list_status


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'download': download,
    'latest-versions': latest_versions,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session=session)
    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
