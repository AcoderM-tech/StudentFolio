# StudentFolio

Django asosidagi talaba portfolio platformasi.

## Render.com ga deploy qilish

### 1. PostgreSQL yaratish
* Render Dashboard → **New** → **PostgreSQL** orqali yangi baza yarating.
* Yaratilgan bazaning `Internal Database URL` yoki `External Database URL` manzilini (`DATABASE_URL`) nusxalab oling.

### 2. Supabase S3 Storage sozlash
* [Supabase](https://supabase.com) platformasida loyiha yarating.
* **Storage** bo'limiga kirib, rasmlar uchun yangi **Public Bucket** oching (masalan: `student-media`).
* **Project Settings** → **Storage** bo'limidan S3 aloqasi uchun zarur bo'lgan Endpoint va API kalitlarini (Access Key va Secret Key) oling.

### 3. Render Web Service — Environment Variables
Render panelida loyihangiz sozlamalariga kirib (**Settings** → **Environment Variables**), quyidagi o'zgaruvchilarni tartib bilan kiriting:

| Kalit (Key) | Qiymat (Value) |
| :--- | :--- |
| `PYTHON_VERSION` | `3.12.8` *(Majburiy: Barqaror ishlash uchun)* |
| `SECRET_KEY` | *Tasodifiy uzun xavfsiz satr* |
| `DEBUG` | `False` |
| `DATABASE_URL` | *Render PostgreSQL'dan olingan havola* |
| `SUPABASE_BUCKET` | *Supabase'da ochilgan bucket nomi (masalan: student-media)* |
| `SUPABASE_S3_ENDPOINT` | `https://<project-ref>.supabase.co/storage/v1/s3` |
| `SUPABASE_S3_ACCESS_KEY` | *Supabase'dan olingan Access Key* |
| `SUPABASE_S3_SECRET_KEY` | *Supabase'dan olingan Secret Key* |

---

### 4. Build & Start Commands
Render panelida sozlamalar quyidagicha bo'lishi kerak:

* **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
