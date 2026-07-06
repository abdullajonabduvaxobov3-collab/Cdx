import os
import sys
import json
import datetime
from pathlib import Path
import mimetypes
import shutil
import stat

class TelefonFaylBoshqaruv:
    def __init__(self):
        self.davom_etish = True
        self.foydalanuvchi = os.getenv("USER", "Telefon foydalanuvchisi")
        self.joriy_papka = "/storage/emulated/0"  # Android asosiy saqlash papkasi
        self.tarix_fayli = os.path.join(self.joriy_papka, ".fayl_boshqaruv_tarix.json")
        self.kutubxonalar = [
            "/storage/emulated/0",  # Asosiy saqlash
            "/storage/emulated/0/Download",  # Yuklab olishlar
            "/storage/emulated/0/Documents",  # Hujjatlar
            "/storage/emulated/0/Pictures",  # Rasmlar
            "/storage/emulated/0/Music",  # Musiqa
            "/storage/emulated/0/Movies",  # Videolar
            "/storage/emulated/0/DCIM",  # Kamera
        ]
        
        # Ruxsatlar rangi
        self.ranglar = {
            'papka': '\033[94m',    # Ko'k
            'fayl': '\033[0m',       # Oddiy
            'python': '\033[92m',    # Yashil
            'txt': '\033[93m',       # Sariq
            'image': '\033[95m',     # Binafsha
            'music': '\033[96m',     # Moviy
            'video': '\033[91m',     # Qizil
            'archive': '\033[33m',   # To'q sariq
            'reset': '\033[0m'       # Rangni tiklash
        }
        
        # Buyruqlar ro'yxati
        self.buyruqlar = {
            "yordam": "Barcha buyruqlar ro'yxati",
            "chiqish": "Dasturdan chiqish",
            "pwd": "Joriy papkani ko'rsatish",
            "ls": "Fayllar ro'yxatini ko'rsatish",
            "cd": "Papka o'zgartirish",
            "mkdir": "Yangi papka yaratish",
            "touch": "Yangi fayl yaratish",
            "rm": "Fayl yoki papkani o'chirish",
            "rmdir": "Bo'sh papkani o'chirish",
            "cp": "Faylni nusxalash",
            "mv": "Faylni ko'chirish yoki nomini o'zgartirish",
            "cat": "Fayl mazmunini ko'rsatish",
            "edit": "Fayl mazmunini tahrirlash (txt fayllar)",
            "find": "Fayl yoki papka qidirish",
            "info": "Fayl yoki papka haqida ma'lumot",
            "size": "Papka hajmini hisoblash",
            "tree": "Papka tuzilishini ko'rsatish",
            "storage": "Telefon saqlash imkoniyatlarini ko'rsatish",
            "goto": "Muhim papkalarga tez o'tish",
            "search": "Fayl ichida matn qidirish",
            "backup": "Fayl yoki papkani nusxasini olish",
            "permissions": "Fayl ruxsatlarini o'zgartirish"
        }
        
        # Fayl kengaytmalari va ularning turlari
        self.fayl_turlari = {
            '.txt': 'txt', '.py': 'python', '.java': 'java', '.js': 'javascript',
            '.html': 'html', '.css': 'css', '.json': 'json', '.xml': 'xml',
            '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
            '.mp3': 'music', '.wav': 'music', '.ogg': 'music',
            '.mp4': 'video', '.avi': 'video', '.mkv': 'video',
            '.zip': 'archive', '.rar': 'archive', '.tar': 'archive',
            '.pdf': 'document', '.doc': 'document', '.docx': 'document',
            '.xls': 'document', '.xlsx': 'document', '.ppt': 'document', '.pptx': 'document'
        }
    
    def ekranni_tozalash(self):
        """Ekran tozalash"""
        os.system('clear')
        print(f"{self.ranglar['papka']}╔══════════════════════════════════════════════════╗{self.ranglar['reset']}")
        print(f"{self.ranglar['papka']}║    TELEFON FAYL BOSHQARUV TIZIMI              ║{self.ranglar['reset']}")
        print(f"{self.ranglar['papka']}║    Foydalanuvchi: {self.foydalanuvchi:<30}║{self.ranglar['reset']}")
        print(f"{self.ranglar['papka']}╚══════════════════════════════════════════════════╝{self.ranglar['reset']}")
        return True
    
    def fayl_rangi_aniqlash(self, fayl_nomi):
        """Fayl turiga qarab rang aniqlash"""
        if os.path.isdir(os.path.join(self.joriy_papka, fayl_nomi)):
            return self.ranglar['papka']
        
        kengaytma = os.path.splitext(fayl_nomi)[1].lower()
        tur = self.fayl_turlari.get(kengaytma, 'fayl')
        
        if tur == 'txt':
            return self.ranglar['txt']
        elif tur == 'python':
            return self.ranglar['python']
        elif tur in ['image', 'music', 'video']:
            return self.ranglar[tur]
        elif tur == 'archive':
            return self.ranglar['archive']
        else:
            return self.ranglar['fayl']
    
    def ls_buyrugi(self, argumentlar=None):
        """Fayllar ro'yxatini ko'rsatish"""
        try:
            fayllar = os.listdir(self.joriy_papka)
            if not fayllar:
                print(f"{self.ranglar['txt']}📂 Papka bo'sh{self.ranglar['reset']}")
                return True
            
            # Saralash
            papkalar = []
            fayl_list = []
            
            for element in fayllar:
                element_yoli = os.path.join(self.joriy_papka, element)
                if os.path.isdir(element_yoli):
                    papkalar.append(element)
                else:
                    fayl_list.append(element)
            
            papkalar.sort()
            fayl_list.sort()
            
            print(f"\n{self.ranglar['papka']}📁 PAPKALAR ({len(papkalar)}){self.ranglar['reset']}")
            print(f"{self.ranglar['papka']}═{'═'*50}{self.ranglar['reset']}")
            
            for papka in papkalar:
                try:
                    ichidagi = len(os.listdir(os.path.join(self.joriy_papka, papka)))
                    print(f"{self.ranglar['papka']}📁 {papka}/ {' '*(40-len(papka))} ({ichidagi} ta){self.ranglar['reset']}")
                except:
                    print(f"{self.ranglar['papka']}📁 {papka}/ {' '*(40-len(papka))} (ruxsat yo'q){self.ranglar['reset']}")
            
            print(f"\n{self.ranglar['fayl']}📄 FAYLLAR ({len(fayl_list)}){self.ranglar['reset']}")
            print(f"{self.ranglar['fayl']}═{'═'*50}{self.ranglar['reset']}")
            
            for fayl in fayl_list:
                fayl_yoli = os.path.join(self.joriy_papka, fayl)
                try:
                    hajm = os.path.getsize(fayl_yoli)
                    hajm_str = self.hajmni_formatlash(hajm)
                    rang = self.fayl_rangi_aniqlash(fayl)
                    print(f"{rang}📄 {fayl} {' '*(40-len(fayl))} {hajm_str}{self.ranglar['reset']}")
                except:
                    rang = self.fayl_rangi_aniqlash(fayl)
                    print(f"{rang}📄 {fayl} {' '*(40-len(fayl))} (ma'lumot yo'q){self.ranglar['reset']}")
            
            print(f"\n{self.ranglar['txt']}Jami: {len(papkalar)} papka, {len(fayl_list)} fayl{self.ranglar['reset']}")
            return True
            
        except PermissionError:
            print(f"{self.ranglar['video']}❌ Ruxsat yo'q! Ushbu papkaga kirish mumkin emas.{self.ranglar['reset']}")
            return False
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def hajmni_formatlash(self, baytlar):
        """Hajmni qulay formatda ko'rsatish"""
        for birlik in ['B', 'KB', 'MB', 'GB', 'TB']:
            if baytlar < 1024.0:
                return f"{baytlar:.1f} {birlik}"
            baytlar /= 1024.0
        return f"{baytlar:.1f} PB"
    
    def cd_buyrugi(self, yangi_papka):
        """Papka o'zgartirish"""
        if not yangi_papka:
            print(f"{self.ranglar['txt']}ℹ️ Joriy papka: {self.joriy_papka}{self.ranglar['reset']}")
            return True
        
        # Maxsus belgilar
        if yangi_papka == "..":
            yangi_yol = os.path.dirname(self.joriy_papka)
        elif yangi_papka == ".":
            return True
        elif yangi_papka == "~":
            yangi_yol = "/storage/emulated/0"
        else:
            # Nisbiy yoki mutlaq yol
            if os.path.isabs(yangi_papka):
                yangi_yol = yangi_papka
            else:
                yangi_yol = os.path.join(self.joriy_papka, yangi_papka)
        
        try:
            if os.path.exists(yangi_yol) and os.path.isdir(yangi_yol):
                os.chdir(yangi_yol)
                self.joriy_papka = os.getcwd()
                print(f"{self.ranglar['txt']}✅ Papka o'zgartirildi: {self.joriy_papka}{self.ranglar['reset']}")
                return True
            else:
                print(f"{self.ranglar['video']}❌ Papka topilmadi: {yangi_papka}{self.ranglar['reset']}")
                return False
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def mkdir_buyrugi(self, papka_nomi):
        """Yangi papka yaratish"""
        if not papka_nomi:
            print(f"{self.ranglar['video']}❌ Papka nomi kiritilmadi!{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ Misol: mkdir yangi_papka{self.ranglar['reset']}")
            return False
        
        yangi_papka_yoli = os.path.join(self.joriy_papka, papka_nomi)
        
        try:
            os.makedirs(yangi_papka_yoli, exist_ok=True)
            print(f"{self.ranglar['txt']}✅ Papka yaratildi: {papka_nomi}{self.ranglar['reset']}")
            return True
        except PermissionError:
            print(f"{self.ranglar['video']}❌ Ruxsat yo'q! Papka yarata olmaysiz.{self.ranglar['reset']}")
            return False
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def touch_buyrugi(self, fayl_nomi):
        """Yangi fayl yaratish"""
        if not fayl_nomi:
            print(f"{self.ranglar['video']}❌ Fayl nomi kiritilmadi!{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ Misol: touch yangi_fayl.txt{self.ranglar['reset']}")
            return False
        
        fayl_yoli = os.path.join(self.joriy_papka, fayl_nomi)
        
        try:
            # Fayl mavjud bo'lsa, vaqtni yangilash
            if os.path.exists(fayl_yoli):
                os.utime(fayl_yoli, None)
                print(f"{self.ranglar['txt']}✅ Fayl vaqti yangilandi: {fayl_nomi}{self.ranglar['reset']}")
            else:
                # Yangi fayl yaratish
                with open(fayl_yoli, 'w', encoding='utf-8') as f:
                    f.write(f"# {fayl_nomi}\n# Yaratilgan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"{self.ranglar['txt']}✅ Fayl yaratildi: {fayl_nomi}{self.ranglar['reset']}")
            return True
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def rm_buyrugi(self, nishon):
        """Fayl yoki papkani o'chirish"""
        if not nishon:
            print(f"{self.ranglar['video']}❌ O'chirish uchun nom kiritilmadi!{self.ranglar['reset']}")
            return False
        
        nishon_yoli = os.path.join(self.joriy_papka, nishon)
        
        if not os.path.exists(nishon_yoli):
            print(f"{self.ranglar['video']}❌ Fayl yoki papka topilmadi: {nishon}{self.ranglar['reset']}")
            return False
        
        try:
            if os.path.isdir(nishon_yoli):
                # Papkani o'chirish
                if len(os.listdir(nishon_yoli)) > 0:
                    tasdiq = input(f"{self.ranglar['video']}⚠️ Papka bo'sh emas! Barcha ichki narsalar bilan o'chirilsinmi? (ha/yoq): {self.ranglar['reset']}")
                    if tasdiq.lower() != 'ha':
                        print(f"{self.ranglar['txt']}❌ Bekor qilindi.{self.ranglar['reset']}")
                        return False
                    shutil.rmtree(nishon_yoli)
                else:
                    os.rmdir(nishon_yoli)
                print(f"{self.ranglar['txt']}✅ Papka o'chirildi: {nishon}{self.ranglar['reset']}")
            else:
                # Faylni o'chirish
                tasdiq = input(f"{self.ranglar['video']}⚠️ {nishon} faylini o'chirishni tasdiqlaysizmi? (ha/yoq): {self.ranglar['reset']}")
                if tasdiq.lower() == 'ha':
                    os.remove(nishon_yoli)
                    print(f"{self.ranglar['txt']}✅ Fayl o'chirildi: {nishon}{self.ranglar['reset']}")
                else:
                    print(f"{self.ranglar['txt']}❌ Bekor qilindi.{self.ranglar['reset']}")
            return True
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def cat_buyrugi(self, fayl_nomi):
        """Fayl mazmunini ko'rsatish"""
        if not fayl_nomi:
            print(f"{self.ranglar['video']}❌ Fayl nomi kiritilmadi!{self.ranglar['reset']}")
            return False
        
        fayl_yoli = os.path.join(self.joriy_papka, fayl_nomi)
        
        if not os.path.exists(fayl_yoli):
            print(f"{self.ranglar['video']}❌ Fayl topilmadi: {fayl_nomi}{self.ranglar['reset']}")
            return False
        
        if os.path.isdir(fayl_yoli):
            print(f"{self.ranglar['video']}❌ Bu papka! Fayl emas.{self.ranglar['reset']}")
            return False
        
        try:
            # Fayl hajmini tekshirish
            fayl_hajmi = os.path.getsize(fayl_yoli)
            if fayl_hajmi > 1024 * 1024:  # 1MB dan katta bo'lsa
                tasdiq = input(f"{self.ranglar['video']}⚠️ Fayl juda katta ({self.hajmni_formatlash(fayl_hajmi)}). Ko'rsatishni davom ettirishni istaysizmi? (ha/yoq): {self.ranglar['reset']}")
                if tasdiq.lower() != 'ha':
                    return False
            
            # Fayl turini aniqlash
            kengaytma = os.path.splitext(fayl_nomi)[1].lower()
            
            if kengaytma in ['.txt', '.py', '.json', '.xml', '.html', '.css', '.js', '.md']:
                # Matnli fayllar
                with open(fayl_yoli, 'r', encoding='utf-8', errors='ignore') as f:
                    print(f"\n{self.ranglar['txt']}📖 {fayl_nomi} mazmuni:{self.ranglar['reset']}")
                    print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
                    
                    satrlar = f.readlines()
                    for idx, satr in enumerate(satrlar[:1000]):  # Faqat 1000 ta satr
                        print(f"{self.ranglar['txt']}{idx+1:4}: {satr.rstrip()}{self.ranglar['reset']}")
                    
                    if len(satrlar) > 1000:
                        print(f"{self.ranglar['txt']}... ({len(satrlar)-1000} satr qisqartirildi){self.ranglar['reset']}")
                    
                    print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
                    print(f"{self.ranglar['txt']}Jami {len(satrlar)} satr{self.ranglar['reset']}")
            else:
                # Binar fayllar
                print(f"{self.ranglar['video']}⚠️ Bu binar fayl. Matn sifatida ko'rsatib bo'lmaydi.{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}ℹ️ Fayl turi: {mimetypes.guess_type(fayl_yoli)[0] or 'Noma\'lum'}{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}ℹ️ Hajmi: {self.hajmni_formatlash(fayl_hajmi)}{self.ranglar['reset']}")
            
            return True
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def edit_buyrugi(self, fayl_nomi):
        """Fayl mazmunini tahrirlash (txt fayllar uchun)"""
        if not fayl_nomi:
            print(f"{self.ranglar['video']}❌ Fayl nomi kiritilmadi!{self.ranglar['reset']}")
            return False
        
        fayl_yoli = os.path.join(self.joriy_papka, fayl_nomi)
        kengaytma = os.path.splitext(fayl_nomi)[1].lower()
        
        # Faqat matnli fayllar uchun
        if kengaytma not in ['.txt', '.py', '.json', '.xml', '.html', '.css', '.js', '.md', '']:
            print(f"{self.ranglar['video']}❌ Bu turdagi faylni tahrirlab bo'lmaydi.{self.ranglar['reset']}")
            return False
        
        try:
            # Fayl mavjud bo'lsa, mazmunini o'qish
            mazmun = ""
            if os.path.exists(fayl_yoli):
                with open(fayl_yoli, 'r', encoding='utf-8') as f:
                    mazmun = f.read()
            
            print(f"\n{self.ranglar['txt']}✏️ {fayl_nomi} faylini tahrirlash{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}⚠️ Yangi mazmunni kiriting. Tugatish uchun alohida qatorda '--SAVE--' deb yozing.{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}⚠️ Bekor qilish uchun alohida qatorda '--CANCEL--' deb yozing.{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            
            if mazmun:
                print(f"{self.ranglar['txt']}Hozirgi mazmun:{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}{mazmun}{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            
            print(f"{self.ranglar['txt']}Yangi mazmun:{self.ranglar['reset']}")
            
            # Yangi mazmunni o'qish
            yangi_satrlar = []
            while True:
                try:
                    satr = input()
                    if satr == "--SAVE--":
                        break
                    elif satr == "--CANCEL--":
                        print(f"{self.ranglar['txt']}❌ Bekor qilindi.{self.ranglar['reset']}")
                        return False
                    yangi_satrlar.append(satr)
                except EOFError:
                    break
                except KeyboardInterrupt:
                    print(f"{self.ranglar['txt']}❌ Bekor qilindi.{self.ranglar['reset']}")
                    return False
            
            # Faylni saqlash
            with open(fayl_yoli, 'w', encoding='utf-8') as f:
                f.write('\n'.join(yangi_satrlar))
            
            print(f"{self.ranglar['txt']}✅ Fayl saqlandi: {fayl_nomi}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ {len(yangi_satrlar)} satr saqlandi{self.ranglar['reset']}")
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def cp_buyrugi(self, manba, nusha):
        """Faylni nusxalash"""
        if not manba or not nusha:
            print(f"{self.ranglar['video']}❌ Manba va nusha nomlari kiritilmadi!{self.ranglar['reset']}")
            return False
        
        manba_yoli = os.path.join(self.joriy_papka, manba)
        nusha_yoli = os.path.join(self.joriy_papka, nusha)
        
        if not os.path.exists(manba_yoli):
            print(f"{self.ranglar['video']}❌ Manba topilmadi: {manba}{self.ranglar['reset']}")
            return False
        
        try:
            if os.path.isdir(manba_yoli):
                # Papkani nusxalash
                if os.path.exists(nusha_yoli):
                    tasdiq = input(f"{self.ranglar['video']}⚠️ Nusha allaqachon mavjud. Ustiga yozilsinmi? (ha/yoq): {self.ranglar['reset']}")
                    if tasdiq.lower() != 'ha':
                        return False
                    shutil.rmtree(nusha_yoli)
                shutil.copytree(manba_yoli, nusha_yoli)
            else:
                # Faylni nusxalash
                shutil.copy2(manba_yoli, nusha_yoli)
            
            print(f"{self.ranglar['txt']}✅ Nusxalandi: {manba} → {nusha}{self.ranglar['reset']}")
            return True
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def mv_buyrugi(self, eski_nom, yangi_nom):
        """Faylni ko'chirish yoki nomini o'zgartirish"""
        if not eski_nom or not yangi_nom:
            print(f"{self.ranglar['video']}❌ Eski va yangi nomlar kiritilmadi!{self.ranglar['reset']}")
            return False
        
        eski_yol = os.path.join(self.joriy_papka, eski_nom)
        yangi_yol = os.path.join(self.joriy_papka, yangi_nom)
        
        if not os.path.exists(eski_yol):
            print(f"{self.ranglar['video']}❌ Fayl yoki papka topilmadi: {eski_nom}{self.ranglar['reset']}")
            return False
        
        try:
            if os.path.exists(yangi_yol):
                tasdiq = input(f"{self.ranglar['video']}⚠️ {yangi_nom} allaqachon mavjud. Ustiga yozilsinmi? (ha/yoq): {self.ranglar['reset']}")
                if tasdiq.lower() != 'ha':
                    return False
                if os.path.isdir(yangi_yol):
                    shutil.rmtree(yangi_yol)
                else:
                    os.remove(yangi_yol)
            
            shutil.move(eski_yol, yangi_yol)
            print(f"{self.ranglar['txt']}✅ Ko'chirildi: {eski_nom} → {yangi_nom}{self.ranglar['reset']}")
            return True
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def find_buyrugi(self, qidirish_nomi):
        """Fayl yoki papka qidirish"""
        if not qidirish_nomi:
            print(f"{self.ranglar['video']}❌ Qidirish uchun nom kiritilmadi!{self.ranglar['reset']}")
            return False
        
        topilganlar = []
        
        try:
            for ildiz, papkalar, fayllar in os.walk(self.joriy_papka):
                # Papkalarni qidirish
                for papka in papkalar:
                    if qidirish_nomi.lower() in papka.lower():
                        toliq_yol = os.path.join(ildiz, papka)
                        nisbiy_yol = os.path.relpath(toliq_yol, self.joriy_papka)
                        topilganlar.append(('📁', nisbiy_yol + '/', os.path.getsize(toliq_yol) if os.path.exists(toliq_yol) else 0))
                
                # Fayllarni qidirish
                for fayl in fayllar:
                    if qidirish_nomi.lower() in fayl.lower():
                        toliq_yol = os.path.join(ildiz, fayl)
                        nisbiy_yol = os.path.relpath(toliq_yol, self.joriy_papka)
                        hajm = os.path.getsize(toliq_yol) if os.path.exists(toliq_yol) else 0
                        topilganlar.append(('📄', nisbiy_yol, hajm))
                
                # Ko'p natijalarni oldini olish
                if len(topilganlar) > 100:
                    break
            
            if topilganlar:
                print(f"\n{self.ranglar['txt']}🔍 '{qidirish_nomi}' uchun topilganlar ({len(topilganlar)}):{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
                
                for tur, nom, hajm in topilganlar[:50]:  # Faqat 50 tasini ko'rsatish
                    hajm_str = f"{self.hajmni_formatlash(hajm):>10}" if hajm > 0 else " " * 10
                    print(f"{self.ranglar['txt']}{tur} {nom:40} {hajm_str}{self.ranglar['reset']}")
                
                if len(topilganlar) > 50:
                    print(f"{self.ranglar['txt']}... va yana {len(topilganlar)-50} ta{self.ranglar['reset']}")
            else:
                print(f"\n{self.ranglar['txt']}🔍 '{qidirish_nomi}' uchun hech narsa topilmadi{self.ranglar['reset']}")
            
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def info_buyrugi(self, nishon):
        """Fayl yoki papka haqida ma'lumot"""
        if not nishon:
            print(f"{self.ranglar['video']}❌ Ma'lumot olish uchun nom kiritilmadi!{self.ranglar['reset']}")
            return False
        
        nishon_yoli = os.path.join(self.joriy_papka, nishon)
        
        if not os.path.exists(nishon_yoli):
            print(f"{self.ranglar['video']}❌ Topilmadi: {nishon}{self.ranglar['reset']}")
            return False
        
        try:
            stat_info = os.stat(nishon_yoli)
            path_obj = Path(nishon_yoli)
            
            print(f"\n{self.ranglar['txt']}📊 {nishon} haqida ma'lumot:{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            
            # Asosiy ma'lumotlar
            print(f"{self.ranglar['txt']}To'liq yo'l: {nishon_yoli}{self.ranglar['reset']}")
            
            if path_obj.is_dir():
                print(f"{self.ranglar['txt']}Turi: 📁 Papka{self.ranglar['reset']}")
                try:
                    ichidagi = len(os.listdir(nishon_yoli))
                    print(f"{self.ranglar['txt']}Ichidagi elementlar: {ichidagi} ta{self.ranglar['reset']}")
                except:
                    print(f"{self.ranglar['txt']}Ichidagi elementlar: Ruxsat yo'q{self.ranglar['reset']}")
            else:
                print(f"{self.ranglar['txt']}Turi: 📄 Fayl{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}Kengaytmasi: {path_obj.suffix or 'Yo\'q'}{self.ranglar['reset']}")
                mime_turi = mimetypes.guess_type(nishon_yoli)[0] or 'Noma\'lum'
                print(f"{self.ranglar['txt']}MIME turi: {mime_turi}{self.ranglar['reset']}")
            
            # Hajm
            if path_obj.is_file():
                hajm = os.path.getsize(nishon_yoli)
                print(f"{self.ranglar['txt']}Hajmi: {self.hajmni_formatlash(hajm)} ({hajm} bayt){self.ranglar['reset']}")
            else:
                # Papka hajmini hisoblash
                try:
                    umumiy_hajm = 0
                    for ildiz, papkalar, fayllar in os.walk(nishon_yoli):
                        for fayl in fayllar:
                            fayl_yoli = os.path.join(ildiz, fayl)
                            try:
                                umumiy_hajm += os.path.getsize(fayl_yoli)
                            except:
                                pass
                    print(f"{self.ranglar['txt']}Umumiy hajmi: {self.hajmni_formatlash(umumiy_hajm)}{self.ranglar['reset']}")
                except:
                    print(f"{self.ranglar['txt']}Umumiy hajmi: Hisoblash mumkin emas{self.ranglar['reset']}")
            
            # Vaqt ma'lumotlari
            yaratilgan = datetime.datetime.fromtimestamp(stat_info.st_ctime)
            ozgartirilgan = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            
            print(f"{self.ranglar['txt']}Yaratilgan: {yaratilgan.strftime('%Y-%m-%d %H:%M:%S')}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}O'zgartirilgan: {ozgartirilgan.strftime('%Y-%m-%d %H:%M:%S')}{self.ranglar['reset']}")
            
            # Ruxsatlar
            try:
                ruxsatlar = stat.filemode(stat_info.st_mode)
                print(f"{self.ranglar['txt']}Ruxsatlar: {ruxsatlar}{self.ranglar['reset']}")
            except:
                print(f"{self.ranglar['txt']}Ruxsatlar: Noma'lum{self.ranglar['reset']}")
            
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def size_buyrugi(self, papka_nomi=None):
        """Papka hajmini hisoblash"""
        if papka_nomi:
            papka_yoli = os.path.join(self.joriy_papka, papka_nomi)
            if not os.path.exists(papka_yoli) or not os.path.isdir(papka_yoli):
                print(f"{self.ranglar['video']}❌ Papka topilmadi: {papka_nomi}{self.ranglar['reset']}")
                return False
        else:
            papka_yoli = self.joriy_papka
        
        try:
            print(f"\n{self.ranglar['txt']}📊 {papka_yoli} hajmini hisoblash...{self.ranglar['reset']}")
            
            fayllar_soni = 0
            papkalar_soni = 0
            umumiy_hajm = 0
            
            for ildiz, papkalar, fayllar in os.walk(papka_yoli):
                papkalar_soni += len(papkalar)
                fayllar_soni += len(fayllar)
                
                for fayl in fayllar:
                    fayl_yoli = os.path.join(ildiz, fayl)
                    try:
                        umumiy_hajm += os.path.getsize(fayl_yoli)
                    except:
                        pass
            
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}📁 Papkalar: {papkalar_soni} ta{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}📄 Fayllar: {fayllar_soni} ta{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}💾 Umumiy hajm: {self.hajmni_formatlash(umumiy_hajm)}{self.ranglar['reset']}")
            
            # Hajm taqsimoti
            if fayllar_soni > 0:
                o_rtacha_hajm = self.hajmni_formatlash(umumiy_hajm / fayllar_soni)
                print(f"{self.ranglar['txt']}📈 O'rtacha fayl hajmi: {o_rtacha_hajm}{self.ranglar['reset']}")
            
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def tree_buyrugi(self, daraja=3):
        """Papka tuzilishini ko'rsatish"""
        try:
            print(f"\n{self.ranglar['txt']}🌳 {self.joriy_papka} papka tuzilishi:{self.ranglar['reset']}")
            
            def chop_etish(ildiz, prefiks="", daraja_qolgan=daraja):
                if daraja_qolgan < 0:
                    return
                
                try:
                    elementlar = sorted(os.listdir(ildiz))
                except PermissionError:
                    print(f"{prefiks}└── 📁 [Ruxsat yo'q]")
                    return
                
                for i, element in enumerate(elementlar):
                    element_yoli = os.path.join(ildiz, element)
                    oxirgi = (i == len(elementlar) - 1)
                    
                    if os.path.isdir(element_yoli):
                        belgi = "└── " if oxirgi else "├── "
                        print(f"{prefiks}{belgi}{self.ranglar['papka']}📁 {element}/{self.ranglar['reset']}")
                        
                        if not oxirgi:
                            yangi_prefiks = prefiks + "│   "
                        else:
                            yangi_prefiks = prefiks + "    "
                        
                        chop_etish(element_yoli, yangi_prefiks, daraja_qolgan-1)
                    else:
                        belgi = "└── " if oxirgi else "├── "
                        rang = self.fayl_rangi_aniqlash(element)
                        print(f"{prefiks}{belgi}{rang}📄 {element}{self.ranglar['reset']}")
            
            chop_etish(self.joriy_papka)
            print()
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def goto_buyrugi(self, kutubxona_nomi):
        """Muhim papkalarga tez o'tish"""
        kutubxonalar_royxati = {
            "asosiy": "/storage/emulated/0",
            "yuklab": "/storage/emulated/0/Download",
            "hujjat": "/storage/emulated/0/Documents",
            "rasm": "/storage/emulated/0/Pictures",
            "musiqa": "/storage/emulated/0/Music",
            "video": "/storage/emulated/0/Movies",
            "kamera": "/storage/emulated/0/DCIM",
            "telegram": "/storage/emulated/0/Telegram",
            "whatsapp": "/storage/emulated/0/WhatsApp",
            "python": "/storage/emulated/0/Pydroid3",
        }
        
        if not kutubxona_nomi:
            print(f"\n{self.ranglar['txt']}📂 Muhim papkalar ro'yxati:{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            
            for nom, yol in kutubxonalar_royxati.items():
                mavjud = "✅" if os.path.exists(yol) else "❌"
                print(f"{self.ranglar['txt']}{nom:15} → {yol} {mavjud}{self.ranglar['reset']}")
            
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ Misol: goto yuklab{self.ranglar['reset']}")
            return True
        
        if kutubxona_nomi in kutubxonalar_royxati:
            yangi_yol = kutubxonalar_royxati[kutubxona_nomi]
            if os.path.exists(yangi_yol):
                return self.cd_buyrugi(yangi_yol)
            else:
                print(f"{self.ranglar['video']}❌ Bu papka mavjud emas: {yangi_yol}{self.ranglar['reset']}")
                return False
        else:
            print(f"{self.ranglar['video']}❌ Noma'lum kutubxona: {kutubxona_nomi}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ 'goto' buyrug'ini argument siz ishlating{self.ranglar['reset']}")
            return False
    
    def search_buyrugi(self, matn, fayl_nomi="*.txt"):
        """Fayl ichida matn qidirish"""
        if not matn:
            print(f"{self.ranglar['video']}❌ Qidirish uchun matn kiritilmadi!{self.ranglar['reset']}")
            return False
        
        import fnmatch
        
        try:
            print(f"\n{self.ranglar['txt']}🔍 '{matn}' matnini qidirish...{self.ranglar['reset']}")
            topilganlar = []
            
            for ildiz, papkalar, fayllar in os.walk(self.joriy_papka):
                for fayl in fayllar:
                    if fnmatch.fnmatch(fayl, fayl_nomi):
                        fayl_yoli = os.path.join(ildiz, fayl)
                        try:
                            with open(fayl_yoli, 'r', encoding='utf-8', errors='ignore') as f:
                                satrlar = f.readlines()
                                for satr_raqam, satr in enumerate(satrlar, 1):
                                    if matn.lower() in satr.lower():
                                        nisbiy_yol = os.path.relpath(fayl_yoli, self.joriy_papka)
                                        topilganlar.append((nisbiy_yol, satr_raqam, satr.strip()))
                        except:
                            continue
                
                if len(topilganlar) > 50:
                    break
            
            if topilganlar:
                print(f"{self.ranglar['txt']}Topildi ({len(topilganlar)} ta):{self.ranglar['reset']}")
                print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
                
                for fayl, satr_raqam, satr in topilganlar[:30]:  # Faqat 30 tasini ko'rsatish
                    print(f"{self.ranglar['txt']}📄 {fayl}:{satr_raqam}{self.ranglar['reset']}")
                    print(f"{self.ranglar['txt']}   {satr[:80]}{'...' if len(satr) > 80 else ''}{self.ranglar['reset']}")
                
                if len(topilganlar) > 30:
                    print(f"{self.ranglar['txt']}... va yana {len(topilganlar)-30} ta{self.ranglar['reset']}")
            else:
                print(f"{self.ranglar['txt']}❌ Hech qanday faylda '{matn}' matni topilmadi{self.ranglar['reset']}")
            
            print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
            return True
            
        except Exception as e:
            print(f"{self.ranglar['video']}❌ Xatolik: {e}{self.ranglar['reset']}")
            return False
    
    def yordam_buyrugi(self):
        """Barcha buyruqlar ro'yxatini ko'rsatish"""
        print(f"\n{self.ranglar['txt']}📖 YORDAM: Barcha buyruqlar ro'yxati{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
        
        for buyruq, tavsif in self.buyruqlar.items():
            print(f"{self.ranglar['txt']}{buyruq:15} - {tavsif}{self.ranglar['reset']}")
        
        print(f"\n{self.ranglar['txt']}📋 MISOLLAR:{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}ls                    - Fayllar ro'yxati{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}cd Downloads          - Downloads papkasiga o'tish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}mkdir yangi_papka     - Yangi papka yaratish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}touch yangi.txt       - Yangi fayl yaratish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}edit yangi.txt        - Faylni tahrirlash{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}cat yangi.txt         - Fayl mazmunini ko'rsatish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}cp eski.txt yangi.txt - Faylni nusxalash{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}find *.mp3            - MP3 fayllarni qidirish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}goto yuklab           - Yuklab olishlar papkasiga o'tish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}tree                  - Papka tuzilishini ko'rsatish{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}═{'═'*50}{self.ranglar['reset']}")
        return True
    
    def buyruqni_bajarish(self, kirish):
        """Foydalanuvchi buyrug'ini bajarish"""
        if not kirish.strip():
            return True
        
        qismlar = kirish.strip().split()
        buyruq = qismlar[0].lower()
        argumentlar = qismlar[1:] if len(qismlar) > 1 else []
        
        # Chiqish
        if buyruq in ["chiqish", "exit", "quit", "q"]:
            self.davom_etish = False
            print(f"\n{self.ranglar['txt']}👋 Xayr! Dasturdan chiqildi.{self.ranglar['reset']}")
            return False
        
        # Yordam
        elif buyruq in ["yordam", "help", "h"]:
            return self.yordam_buyrugi()
        
        # Joriy papka
        elif buyruq == "pwd":
            print(f"\n{self.ranglar['txt']}📁 {self.joriy_papka}{self.ranglar['reset']}")
            return True
        
        # Fayllar ro'yxati
        elif buyruq == "ls":
            return self.ls_buyrugi(argumentlar)
        
        # Papka o'zgartirish
        elif buyruq == "cd":
            papka_nomi = " ".join(argumentlar) if argumentlar else ""
            return self.cd_buyrugi(papka_nomi)
        
        # Papka yaratish
        elif buyruq == "mkdir":
            papka_nomi = " ".join(argumentlar) if argumentlar else ""
            return self.mkdir_buyrugi(papka_nomi)
        
        # Fayl yaratish
        elif buyruq in ["touch", "new"]:
            fayl_nomi = " ".join(argumentlar) if argumentlar else ""
            return self.touch_buyrugi(fayl_nomi)
        
        # O'chirish
        elif buyruq in ["rm", "del", "delete"]:
            nishon = " ".join(argumentlar) if argumentlar else ""
            return self.rm_buyrugi(nishon)
        
        # Fayl mazmuni
        elif buyruq in ["cat", "type", "show"]:
            fayl_nomi = " ".join(argumentlar) if argumentlar else ""
            return self.cat_buyrugi(fayl_nomi)
        
        # Tahrirlash
        elif buyruq in ["edit", "nano", "vi"]:
            fayl_nomi = " ".join(argumentlar) if argumentlar else ""
            return self.edit_buyrugi(fayl_nomi)
        
        # Nusxalash
        elif buyruq == "cp":
            if len(argumentlar) >= 2:
                return self.cp_buyrugi(argumentlar[0], argumentlar[1])
            else:
                print(f"{self.ranglar['video']}❌ Manba va nusha nomlari kerak!{self.ranglar['reset']}")
                return False
        
        # Ko'chirish
        elif buyruq == "mv":
            if len(argumentlar) >= 2:
                return self.mv_buyrugi(argumentlar[0], argumentlar[1])
            else:
                print(f"{self.ranglar['video']}❌ Eski va yangi nomlar kerak!{self.ranglar['reset']}")
                return False
        
        # Qidirish
        elif buyruq in ["find", "search"]:
            nishon = " ".join(argumentlar) if argumentlar else ""
            return self.find_buyrugi(nishon)
        
        # Ma'lumot
        elif buyruq in ["info", "stat"]:
            nishon = " ".join(argumentlar) if argumentlar else ""
            return self.info_buyrugi(nishon)
        
        # Hajm
        elif buyruq == "size":
            papka_nomi = " ".join(argumentlar) if argumentlar else None
            return self.size_buyrugi(papka_nomi)
        
        # Daraxt
        elif buyruq == "tree":
            daraja = 3
            if argumentlar and argumentlar[0].isdigit():
                daraja = int(argumentlar[0])
            return self.tree_buyrugi(daraja)
        
        # Tez o'tish
        elif buyruq == "goto":
            kutubxona = " ".join(argumentlar) if argumentlar else ""
            return self.goto_buyrugi(kutubxona)
        
        # Matn qidirish
        elif buyruq == "search":
            if len(argumentlar) >= 1:
                matn = argumentlar[0]
                fayl_nomi = argumentlar[1] if len(argumentlar) > 1 else "*.txt"
                return self.search_buyrugi(matn, fayl_nomi)
            else:
                print(f"{self.ranglar['video']}❌ Qidirish uchun matn kerak!{self.ranglar['reset']}")
                return False
        
        # Tozalash
        elif buyruq in ["clear", "cls"]:
            self.ekranni_tozalash()
            return True
        
        else:
            print(f"{self.ranglar['video']}❌ Noma'lum buyruq: {buyruq}{self.ranglar['reset']}")
            print(f"{self.ranglar['txt']}ℹ️ 'yordam' buyrug'i bilan barcha buyruqlarni ko'ring{self.ranglar['reset']}")
            return False
    
    def ishga_tushirish(self):
        """Terminalni ishga tushirish"""
        self.ekranni_tozalash()
        
        print(f"{self.ranglar['txt']}📱 Telefon Fayl Boshqaruv Tizimiga xush kelibsiz!{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}💡 'yordam' buyrug'i bilan barcha imkoniyatlarni ko'ring{self.ranglar['reset']}")
        print(f"{self.ranglar['txt']}⚠️  Ehtiyot bo'ling! Noto'g'ri buyruqlar ma'lumotlar yo'qolishiga olib kelishi mumkin.{self.ranglar['reset']}\n")
        
        while self.davom_etish:
            try:
                # Buyruq satrini kiritish
                prompt = f"{self.ranglar['papka']}[{self.foydalanuvchi}@{os.path.basename(self.joriy_papka)}]{self.ranglar['reset']}$ "
                kirish = input(prompt)
                
                # Buyruqni bajarish
                self.buyruqni_bajarish(kirish)
                
            except KeyboardInterrupt:
                print(f"\n{self.ranglar['txt']}\n⚠️  Ctrl+C bosildi. Chiqish uchun 'chiqish' deb yozing.{self.ranglar['reset']}")
            except EOFError:
                print(f"\n{self.ranglar['txt']}")
                break
            except Exception as e:
                print(f"{self.ranglar['video']}❌ Kutilmagan xatolik: {e}{self.ranglar['reset']}")

def main():
    """Asosiy funksiya"""
    terminal = TelefonFaylBoshqaruv()
    terminal.ishga_tushirish()

if __name__ == "__main__":
    main()