# Парсер BS4-PARSER-PEP

# Стек технологий

- Python 3.10
- BeautifulSoup4
- lxml
- argparse
- logging
- GitHub Actions

# О проекте

Парсер собирает информацию о последних версиях документации Python и стандартах PEP, а затем отображает результаты парсинга в различных форматах по вашему выбору.

# Запуск проекта
Клонируйте репозиторий и перейдите в него в командной строке: 
```commandline
git clone git@github.com:Saida3232/bs4_parser_pep.git
cd bs4_parser_pep
```
Cоздайте и активируйте виртуальное окружение:
- для Windows
 ```commandline
python3 -m venv env
venv\Scripts\activate
  ```

- для Linux/MacOS
  ```commandline
  python -m venv venv
  source venv/bin/activate
  ```

Установите зависимости из файла requirements.txt: 
```commandline
pip install -r requirements.txt
```

# Использование

Функции программы и режимы парсера запускаются через аргументы командной строки. 
```commandline
python main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
```
Позиционный аргумент - один из режимов работы парсера (`whats-new`, `latest-versions`, `download`, `pep`)

- **whats-new**

  Парсинг последних обновлений 
  ```commandline
  python main.py whats-new <args>
  ```
  
- **latest-versions**

  Парсинг последних версий документации
  ```commandline
  python main.py latest_versions <args>
  ```
  
- **download**

  Загрузка и сохранение архива с документацией
  ```commandline
  python main.py download <args>
  ```
  
- **pep**

  Статусы PEP
  ```commandline
  python main.py pep <args>
  ```

`-h`, `-help` - вывести справочную информацию о парсере

`-c`, `--clear-cache` - очистка кэша 

`-o`, `--output` - вывод данных (`pretty` - в табличном формате в терминале или `file` - в CSV файл)

# Примеры запуска:

```
python main.py whats-new -o file 
python parser.py latest-versions --output pretty --clear-cache
python parser.py download
python parser.py pep -o file 
```

# Автор проекта:

[Саида Магомеддибирова](https://github.com/Saida3232)