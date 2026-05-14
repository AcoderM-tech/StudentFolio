from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
#Rollar jadvali
class Rol(models.Model):
    nomi=models.CharField(max_length=100,unique=True)
    tavsif=models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return self.nomi
#Userlar jadvali
class Users(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    qoshilgan_vaqt=models.DateTimeField(auto_now_add=True)
    user_holati=models.BooleanField(default=True)
    oxirgi_faollik=models.DateTimeField(auto_now=True)
    email_tasdiqlanganmi=models.BooleanField(default=False)

    def __str__(self):
        return self.username

#Profil jadvali
class Profil(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ism=models.CharField(max_length=20)
    familiya=models.CharField(max_length=20)
    avatar=models.ImageField(upload_to='avatar',default='avatar/default.png')
    university = models.CharField(max_length=200, blank=True)
    fakultet = models.CharField(max_length=200, blank=True)
    kurs = models.PositiveSmallIntegerField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, blank=True, null=True)
    manzil=models.CharField(max_length=200, blank=True)
    bio_text=models.TextField(blank=True,null=True)
    ish_sohasi=models.CharField(max_length=200, blank=True,null=True)
    tashriflar_soni=models.PositiveIntegerField( blank=True,null=True,default=0)

    def __str__ (self):
        return f"{self.ism} {self.familiya}"

#Foydalanuvchi faol bo'lgan ijtimoiy tarmoqlari
class Faol_tarmoqlar(models.Model):
    nomi=models.CharField(max_length=100,blank = True,null = True)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='tarmoqlari')
    manzil = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.profil.ism}ning {self.nomi}dagi faolligi"
    class  Meta:
        verbose_name_plural = "Ijtimoiy tarmoqlar"

#Foydalanuvchi loyihalari jadvali

class Loyihalar(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending'
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE,related_name='loyihalar')
    nomi=models.CharField(max_length=255)
    tavsif=models.TextField(max_length=500,blank=True,null=True)
    avatar=models.ImageField(upload_to='projectpicture',default='projectpicture/default.png')
    github_link=models.URLField(blank=True,null=True)
    live_link=models.URLField(blank=True,null=True)
    yaratilgan_sana=models.DateTimeField(auto_now_add=True)
    status=models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    video=models.URLField(blank=True,null=True)
    korishlar_soni=models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.profil.ism}ning {self.nomi} loyihasi"

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ["yaratilgan_sana"]

#Foydalanuvchining sertifikatlari

class Sertifikat(models.Model):
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE,related_name='sertifikat')
    nomi=models.CharField(max_length=100)
    bergan_tashkilot=models.CharField(blank=True,null=True,max_length=100)
    fayl_isbot=models.FileField(upload_to='fayl_isbot/%Y/%m/')
    olingan_sana=models.DateTimeField()
    yuklash_sanasi=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profil.ism}|| {self.nomi}"

    class Meta:
        verbose_name = "Sertifikatlar"
        verbose_name_plural = "Sertifikatlar"
        ordering = ["yuklash_sanasi"]

#Foydalanuvchi qatnashgan tadbirlari va yutuqlari

class Tadbirlar_va_yutuqlar(models.Model):
    class Rolchoices(models.TextChoices):
        GOLIB = 'golib', "G'olib"
        ISHTIROKCHI = 'ishtirokchi', 'Ishtirokchi'
        SPIKER = 'spiker', 'Spiker'
        TASHKILOTCHI = 'tashkilotchi', 'Tashkilotchi'
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE,related_name='tadbirlar')
    nomi=models.CharField(max_length=100)
    roli=models.CharField(
        max_length=100,
        choices=Rolchoices.choices,
        default=Rolchoices.ISHTIROKCHI
    )
    yuklangan_sanasi=models.DateTimeField(auto_now_add=True)
    bolib_otgan_sanasi=models.DateTimeField(blank=True, null=True)
    tavsif=models.TextField(max_length=500,blank=True,null=True)
    def __str__(self):
        return f"{self.profil.ism}||{self.nomi}"
    class Meta:
        verbose_name = "Tadbirlar va yutuqlar"
        verbose_name_plural = "Tadbirlar/Yutuqlar"
        ordering = ["yuklangan_sanasi"]
class TadbirRasmi(models.Model):
    tadbir = models.ForeignKey(Tadbirlar_va_yutuqlar, on_delete=models.CASCADE, related_name='rasmlari')
    rasm = models.ImageField(upload_to='tadbir_rasmlari/')
#Foydalanuvchining ish faoliyati

class Ish_faoliyati(models.Model):
    class IshTuriChoices(models.TextChoices):
        STAJIROVKA = 'stajirovka', 'Stajirovka (Internship)'
        FRILANS = 'frilans', 'Frilans'
        FULL_TIME = 'full_time', 'To\'liq stavka (Full-time)'
        PART_TIME = 'part_time', 'Yarim stavka (Part-time)'
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='ishlari')
    kompaniya = models.CharField(max_length=200)
    lavozim = models.CharField(max_length=200)
    ish_turi = models.CharField(
        max_length=50,
        choices=IshTuriChoices.choices,
        default=IshTuriChoices.STAJIROVKA
    )
    tavsif = models.TextField(blank=True, null=True)
    boshlangan_sana = models.DateField()
    tugatilgan_sana = models.DateField(blank=True, null=True)
    yuklangan_sana = models.DateTimeField(auto_now_add=True)
    fotolavha = models.ImageField(upload_to='ishdanlavha', default='ishdanlavha/default.png')
    def __str__(self):
        return f"{self.profil.ism} | {self.kompaniya} - {self.lavozim}"
    class Meta:
        verbose_name = "Ish faoliyati"
        verbose_name_plural = "Ish faoliyatlari"
        ordering = ["yuklangan_sana"]
