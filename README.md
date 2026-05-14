# StudentFolio

Django asosidagi talaba portfolio platformasi.

## Render.com ga deploy qilish

### 1. PostgreSQL yaratish
Render Dashboard → New → PostgreSQL → yarating.
`DATABASE_URL` ni nusxa oling.

### 2. Cloudinary sozlash
https://cloudinary.com → bepul ro'yxatdan o'ting.
Dashboard → API Keys → 3 ta qiymatni oling.

### 3. Render Web Service — Environment Variables
| Variable | Qiymat |
|---|---|
| `SECRET_KEY` | Tasodifiy uzun satr |
| `DEBUG` | `False` |
| `DATABASE_URL` | Render PostgreSQL dan |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary dan |
| `CLOUDINARY_API_KEY` | Cloudinary dan |
| `CLOUDINARY_API_SECRET` | Cloudinary dan |

### 4. Build & Start
Render avtomatik `Procfile` ni o'qiydi:
```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application
```

## Local ishlatish
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
