# QuestBoard 

Платформа для создания и выполнения ежедневных квестов и челленджей.

Пользователи создают доски с квестами, выполняют их и получают опыт (XP),
уровни и ачивки. Геймификация привычек — превращаем рутину в RPG.


## Фичи

- Доски с квестами (публичные и приватные)
- Отметка выполнения квестов
- Опыт, уровни, прогресс
- Ачивки за достижения
- Чат на доске (WebSocket)
- Вход через GitHub / VK (OAuth2)
- API + Swagger


## Стек

- Django 6.x + DRF
- PostgreSQL + Redis
- Django Channels
- Docker + GitHub Actions


## Запуск (локально, Windows PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver