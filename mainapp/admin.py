from django.contrib import admin
from .models import (
    Rol, Users, Profil, Loyihalar,
    Faol_tarmoqlar, Sertifikat,
    Tadbirlar_va_yutuqlar, Ish_faoliyati
)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("nomi",)
    search_fields = ("nomi","tavsif")

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "rol", "user_holati", "qoshilgan_vaqt")
    list_filter = ("rol", "user_holati")
    search_fields = ("username", "email")

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ("ism", "familiya", "university", "kurs", "gpa", "tashriflar_soni")
    list_filter = ("university", "kurs", "fakultet")
    search_fields = ("ism", "familiya", "user__username")
    # Profil tahrirlanayotganda maydonlarni guruhlash (ixtiyoriy)
    fieldsets = (
        ("Shaxsiy ma'lumotlar", {
            'fields': ('user', 'ism', 'familiya', 'avatar', 'bio_text')
        }),
        ("O'qish ma'lumotlari", {
            'fields': ('university', 'fakultet', 'kurs', 'gpa')
        }),
        ("Qo'shimcha", {
            'fields': ('manzil', 'ish_sohasi', 'tashriflar_soni')
        }),
    )

@admin.register(Loyihalar)
class LoyihalarAdmin(admin.ModelAdmin):
    list_display = ("nomi", "profil", "status", "yaratilgan_sana", "korishlar_soni")
    list_filter = ("status", "yaratilgan_sana")
    search_fields = ("nomi", "profil__ism", "profil__familiya")
    date_hierarchy = "yaratilgan_sana" # Vaqt bo'yicha tezkor o'tish paneli

@admin.register(Faol_tarmoqlar)
class FaolTarmoqlarAdmin(admin.ModelAdmin):
    list_display = ("nomi", "profil", "manzil")
    list_filter = ("nomi",)
    search_fields = ("profil__ism", "nomi")

@admin.register(Sertifikat)
class SertifikatAdmin(admin.ModelAdmin):
    list_display = ("nomi", "profil", "bergan_tashkilot", "olingan_sana")
    list_filter = ("bergan_tashkilot", "olingan_sana")
    search_fields = ("nomi", "profil__ism")

@admin.register(Tadbirlar_va_yutuqlar)
class TadbirlarAdmin(admin.ModelAdmin):
    list_display = ("nomi", "profil", "roli", "bolib_otgan_sanasi")
    list_filter = ("roli", "bolib_otgan_sanasi")
    search_fields = ("nomi", "profil__ism")

@admin.register(Ish_faoliyati)
class IshFaoliyatiAdmin(admin.ModelAdmin):
    list_display = ("kompaniya", "profil", "lavozim", "boshlangan_sana", "tugatilgan_sana")
    list_filter = ("kompaniya", "boshlangan_sana")
    search_fields = ("kompaniya", "lavozim", "profil__ism")