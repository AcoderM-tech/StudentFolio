from unittest import expectedFailure

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import registry
from django.shortcuts import render,redirect,get_object_or_404
from django.views import defaults
from django.contrib.auth import authenticate, login as auth_login # ism to'qnashmasligi uchun
from . import models
from .models import Profil, Loyihalar, Sertifikat, Tadbirlar_va_yutuqlar, Ish_faoliyati,TadbirRasmi
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
User=get_user_model()
# Create your views here.


def landing_view(request):
    return render(request, 'landing.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        login=request.POST.get('username')
        parol=request.POST.get('password')
        user=authenticate(request, username=login, password=parol)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': "Login yoki parol xato!"})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tasdiqlash=request.POST.get('password_confirm')
        email=request.POST.get('email')
        if not all([username, password, tasdiqlash, email]):
            return render(request, 'register.html', {'error': "Barcha maydonlarni to'ldiring!"})
        if User.objects.filter(username=username).exists():
            return render(request,'register.html',{'error':"Bu username allaqachon band!!",'email':email})
        if User.objects.filter(email=email).exists():
            return render(request,'register.html',{'error':"Bu email allaqachon band!!",'username':username})
        if password !=tasdiqlash:
            return render(request,'registry.html',{'error':"Parol va parol tasdig'i teng emas!!",'username':username,'password':password,'email':email})
        user = User.objects.create_user(username=username,password=password,email=email)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def about(request):
    return render(request, 'about.html')


@login_required(login_url='/login/')
def profil_form(request):
    profil = Profil.objects.filter(user=request.user).first()
    error = None

    if request.method == 'POST':
        ism = request.POST.get('ism')
        familiya = request.POST.get('familiya')
        university = request.POST.get('university')
        fakultet = request.POST.get('fakultet')
        kurs = request.POST.get('kurs')
        gpa = request.POST.get('gpa')
        avatar = request.FILES.get('avatar')

        if all([ism, familiya, university, fakultet, kurs, gpa]):
            profil, created = Profil.objects.update_or_create(
                user=request.user,
                defaults={
                    'ism': ism,
                    'familiya': familiya,
                    'university': university,
                    'fakultet': fakultet,
                    'kurs': kurs,
                    'gpa': float(gpa) if gpa else 0,
                }
            )
            if avatar:
                profil.avatar = avatar
                profil.save()

            return redirect('dashboard')
        else:
            error = "Iltimos, barcha maydonlarni to'ldiring!"
    context = {
        'profil': profil,
        'error': error
    }
    return render(request, 'dashboard/profil_form.html', context)
@login_required(login_url='/login/')
def dashboard(request):
    try:
      user_profil=Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
      return redirect('profil_form')

    s_soni = user_profil.sertifikat.count()
    t_soni = user_profil.tashriflar_soni
    loyihalar_list = user_profil.loyihalar.order_by('-id')
    context = {
        'profil':user_profil,
        's_soni':s_soni,
        't_soni':t_soni,
        'l_soni':loyihalar_list.count(),
        'loyihalar':loyihalar_list
    }
    return render(request,'dashboard/index.html',context)
@login_required(login_url='/login/')
def project_view(request):
     try:
        user_profil = Profil.objects.get(user=request.user)
     except Profil.DoesNotExist:
        return redirect('profil_form')

     loyihalar=Loyihalar.objects.filter(profil__user=request.user).order_by('-yaratilgan_sana')

     return render(request,'dashboard/projects.html',{'projects':loyihalar,'profil':user_profil})


@login_required(login_url='/login/')
def sertifikat_view(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    sertifikatlar=Sertifikat.objects.filter(profil__user=request.user).order_by('-yuklash_sanasi')
    return render(request,'dashboard/certificates.html',{'certificates':sertifikatlar,'profil':user_profil})


def logout_view(request):
    """Bu view foydalanuvchini asosiy sahifadan chiqarib yuboradi"""
    auth_logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def yutuqlar_view(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    yutuqlar=Tadbirlar_va_yutuqlar.objects.filter(profil__user=request.user).order_by('-yuklangan_sanasi')
    return render(request,'dashboard/achievements.html',{'achievements':yutuqlar,'profil':user_profil})
@login_required(login_url='/login/')
def ish_view(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    ishlar=Ish_faoliyati.objects.filter(profil__user=request.user).order_by('-yuklangan_sana')
    return render(request,'dashboard/experience.html',{'experiences':ishlar,'profil':user_profil})


@login_required(login_url='/login/')
def add_projects(request):
    user_profil = Profil.objects.get(user=request.user)
    if request.method == 'POST':
        nomi=request.POST['nomi']
        tavsif=request.POST['tavsif']
        avatar=request.FILES['avatar']
        status=request.POST['status']
        github_link=request.POST['github_link']
        live_link=request.POST['live_link']
        video_link=request.POST['video']

        if nomi and tavsif:
            loyiha = Loyihalar.objects.create(
                profil=user_profil,
                nomi=nomi,
                tavsif=tavsif,
                status=status,
                github_link=github_link,
                live_link=live_link,
                video=video_link
            )
            if avatar:
                 loyiha.avatar=avatar
                 loyiha.save()
            return redirect('projects')
        else:
            error = "Iltimos, loyiha nomi va tavsifini kiriting!"
            projects = Loyihalar.objects.filter(profil=user_profil)
            return render(request, 'dashboard/projects.html', {
                'projects': projects,
                'error': error
            })
    return redirect('projects')


@login_required(login_url='/login/')
def add_certificate(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    if request.method == 'POST':
        nomi = request.POST.get('nomi')
        bergan_tashkilot = request.POST.get('bergan_tashkilot')
        olingan_sana = request.POST.get('olingan_sana')
        fayl_isbot = request.FILES.get('fayl_isbot')
        if nomi and olingan_sana and fayl_isbot:
            Sertifikat.objects.create(
                profil=user_profil,
                nomi=nomi,
                bergan_tashkilot=bergan_tashkilot,
                olingan_sana=olingan_sana,
                fayl_isbot=fayl_isbot
            )
            return redirect('certificates')

    return redirect('certificates')


@login_required(login_url='/login/')
def add_achievement(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    if request.method == 'POST':
        tadbir = Tadbirlar_va_yutuqlar.objects.create(
            profil=user_profil,
            nomi=request.POST.get('nomi'),
            roli=request.POST.get('roli'),
            tavsif=request.POST.get('tavsif'),
            bolib_otgan_sanasi=request.POST.get('bolib_otgan_sanasi') or None
        )
        rasmlar = request.FILES.getlist('rasmlar')
        for rasm in rasmlar:
            TadbirRasmi.objects.create(
                tadbir=tadbir,
                rasm=rasm
            )

        return redirect('achievements')
    return redirect('achievements')
@login_required(login_url='/login/')
def add_ish(request):
    try:
        user_profil = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        return redirect('profil_form')
    if request.method == 'POST':
        ish=Ish_faoliyati.objects.create(
        profil=user_profil,
        kompaniya = request.POST.get('kompaniya'),
        lavozim= request.POST.get('lavozim'),
        ish_turi=request.POST.get('ish_turi'),
        boshlangan_sana=request.POST.get('boshlangan_sana'),
        tugatilgan_sana=request.POST.get('tugatilgan_sana') or None,
        tavsif=request.POST.get('tavsif')or None,
        )
        rasmlar = request.FILES.get('fotolavha')
        if rasmlar:
            ish.fotolavha=rasmlar
            ish.save()
            return redirect('experiences')
    return redirect('experiences')
from django.shortcuts import get_object_or_404, redirect
@login_required(login_url='/login/')
def edit_project(request, pk):
    project = get_object_or_404(Loyihalar, pk=pk, profil__user=request.user)
    if request.method == 'POST':
        project.nomi = request.POST.get('nomi')
        project.tavsif = request.POST.get('tavsif')
        project.status = request.POST.get('status')
        project.github_link = request.POST.get('github_link')
        project.live_link = request.POST.get('live_link')
        project.video = request.POST.get('video')
        avatar = request.FILES.get('avatar')
        if avatar:
            project.avatar = avatar
        project.save()
        return redirect('projects')
    return render(request, 'edit_project.html', {'project': project})
@login_required(login_url='/login/')
def del_project(request, pk):
    project = Loyihalar.objects.get(pk=pk, profil__user=request.user)
    project.delete()
    return redirect('projects')
@login_required(login_url='/login/')
def del_job(request, pk):
    job=Ish_faoliyati.objects.get(pk=pk, profil__user=request.user)
    job.delete()
    return redirect('experiences')

@login_required(login_url='/login/')
def edit_job(request, pk):
    job=Ish_faoliyati.objects.get(pk=pk, profil__user=request.user)
    if request.method == 'POST':
        job.kompaniya = request.POST.get('kompaniya')
        job.lavozim = request.POST.get('lavozim')
        job.ish_turi = request.POST.get('ish_turi')
        job.boshlangan_sana = request.POST.get('boshlangan_sana')
        tugash_sanasi = request.POST.get('tugatilgan_sana')
        if tugash_sanasi and tugash_sanasi.strip():
            job.tugatilgan_sana = tugash_sanasi
        else:
            job.tugatilgan_sana = None
        job.tavsif = request.POST.get('tavsif')
        rasm = request.FILES.get('fotolavha')
        if rasm:
            job.fotolavha=rasm
        job.save()
        return redirect('experiences')
    return render(request, 'edit_job.html', {'job': job})

@login_required(login_url='/login/')
def edit_achievement(request, pk):
    achievement = get_object_or_404(Tadbirlar_va_yutuqlar, pk=pk, profil__user=request.user)
    if request.method == 'POST':
        achievement.nomi = request.POST.get('nomi')
        achievement.roli = request.POST.get('roli')
        achievement.tavsif = request.POST.get('tavsif')
        sana = request.POST.get('bolib_otgan_sanasi')
        if sana and sana.strip():
            achievement.bolib_otgan_sanasi = sana
        else:
            achievement.bolib_otgan_sanasi = None
        achievement.save()
        yangi_rasmlar = request.FILES.getlist('rasmlar')
        if yangi_rasmlar:
            achievement.rasmlari.all().delete()
            for rasm in yangi_rasmlar:
                TadbirRasmi.objects.create(tadbir=achievement, rasm=rasm)
        return redirect('achievements')
    return redirect('achievements')

@login_required(login_url='/login/')
def delete_achievement(request, pk):
    achievement = get_object_or_404(Tadbirlar_va_yutuqlar, pk=pk, profil__user=request.user)
    achievement.delete()
    return redirect('achievements')
@login_required(login_url='/login/')
def edit_certificate(request, pk):
    cert = get_object_or_404(Sertifikat, pk=pk, profil__user=request.user)
    if request.method == "POST":
        cert.nomi = request.POST.get('nomi')
        cert.bergan_tashkilot = request.POST.get('bergan_tashkilot')
        cert.olingan_sana = request.POST.get('olingan_sana')
        yangi_fayl = request.FILES.get('fayl_isbot')
        if yangi_fayl:
            cert.fayl_isbot = yangi_fayl
        cert.save()
        return redirect('certificates')
    return redirect('certificates')
@login_required(login_url='/login/')
def delete_certificate(request, pk):
    cert = get_object_or_404(Sertifikat, pk=pk, profil__user=request.user)
    cert.delete()
    return redirect('certificates')
@login_required(login_url='/login/')
def cv_generator_page(request):
    profil = request.user.profil
    context = {
        'profil': profil,
        'projects': profil.loyihalar.all().order_by('-yaratilgan_sana'),
        'certificates': profil.sertifikat.all().order_by('-olingan_sana'),
        'experiences': profil.ishlari.all().order_by('-boshlangan_sana'),
        'achievements': profil.tadbirlar.all().order_by('-bolib_otgan_sanasi'),
    }
    return render(request, 'dashboard/cv_generator.html', context)




            



