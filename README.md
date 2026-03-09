# QRKot --- Благотворительный фонд поддержки котиков

## Установка и запуск
1. Клонировать репозиторий
```
git clone https://github.com/collapsegamer/cat-charity-1.git
cd cat-charity
```
2. Установить зависимости
```
py -3.12 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
3. Применить миграции
```
alembic upgrade head
```
4. Запустить приложение
```
uvicorn app.main:app --reload
```