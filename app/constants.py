DATABASE_URL = 'sqlite+aiosqlite:///./fastapi.db'
APP_TITLE = 'Благотворительный фонд поддержки котиков QRKot'
DESCRIPTION = 'Сервис для поддержки котиков'

PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_FULLY_INVESTED = 'Закрытый проект нельзя редактировать!'
PROJECT_EDIT_FULL_AMOUNT = 'Нельзя установить сумму меньше уже вложенной!'
DELETE_INVESTED_PROJECT = (
    'Нельзя удалить проект, в который уже были инвестированы средства.'
)
PROJECT_NAME_EXIST = 'Проект с таким названием уже существует!'