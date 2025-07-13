import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os
import keyboard
from images import get_accept_trial_image, get_take_rewards_image, \
    get_ruin_stack_1_image, get_ruin_stack_2_image, get_ruin_stack_3_image, \
    get_ruin_stack_4_image, get_ruin_stack_5_image, get_ruin_stack_6_image
import pytesseract

# Global değişkenler
LOG_FILE = 'log.txt'
auto_clicking = False
click_count = 0

# Resim değişkenleri
accept_trial_image = None
take_rewards_image = None

ruin_stack_images = []
def load_images():
    """Gömülü resimleri yükle"""
    global accept_trial_image, take_rewards_image, ruin_stack_images
    
    try:
        log_message("📸 Resimler yükleniyor...")
        accept_trial_image = get_accept_trial_image()
        if accept_trial_image is not None:
            log_message(f"✅ Accept Trial resmi yüklendi.")
        else:
            log_message("❌ Accept Trial resmi yüklenemedi")
            
        take_rewards_image = get_take_rewards_image()
        if take_rewards_image is not None:
            log_message(f"✅ Take Rewards resmi yüklendi.")
        else:
            log_message("❌ Take Rewards resmi yüklenemedi")
            
            
        # Ruin stack rakam görsellerini sırayla yükle (1-6)
        ruin_stack_images = [
            get_ruin_stack_1_image(),
            get_ruin_stack_2_image(),
            get_ruin_stack_3_image(),
            get_ruin_stack_4_image(),
            get_ruin_stack_5_image(),
            get_ruin_stack_6_image(),
        ]
        if all(img is not None for img in ruin_stack_images):
            log_message("✅ Tüm ruin stack rakam görselleri yüklendi.")
        else:
            log_message("⚠️ Bazı ruin stack rakam görselleri yüklenemedi.")
            
        if accept_trial_image is not None and take_rewards_image is not None:
            log_message("✅ Tüm resimler başarıyla yüklendi")
        else:
            log_message("⚠️ Bazı resimler yüklenemedi")
    except Exception as e:
        log_message(f"❌ Resim yükleme hatası: {e}")

def setup_hotkeys():
    """Kısayol tuşlarını ayarla"""
    try:
        keyboard.add_hotkey('num 0', stop_clicking)
        log_message("⌨️ Num0 - Durdurma kısayolu aktif")
    except Exception as e:
        log_message(f"❌ Kısayol tuşu ayarlanamadı: {e}")

def find_take_rewards_button():
    """Take Rewards butonunu bulur"""
    if take_rewards_image is None:
        return None
    
    try:
        template_gray = cv2.cvtColor(take_rewards_image, cv2.COLOR_BGR2GRAY)
        tw, th = template_gray.shape[::-1]
        
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):
            return pt[0] + tw // 2, pt[1] + th // 2  # Butonun ortası
        return None
    except Exception as e:
        log_message(f"Take Rewards arama hatası: {e}")
        return None

def log_message(msg):
    """Log mesajı ekler"""
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}"
    log_text.config(state='normal')
    log_text.insert(tk.END, log_entry + '\n')
    log_text.see(tk.END)
    log_text.config(state='disabled')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def clear_logs():
    """Logları temizler"""
    log_text.config(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.config(state='disabled')
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('')
    log_message('Loglar temizlendi.')

def find_and_click_accept_trial():
    """Accept Trial butonunu bulur ve tıklar"""
    if accept_trial_image is None:
        log_message("❌ Accept Trial resmi yüklenmemiş")
        return False
    
    try:
        template_gray = cv2.cvtColor(accept_trial_image, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]
        
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        
        # Threshold değerini düşürerek daha esnek hale getir
        threshold = 0.6
        loc = np.where(res >= threshold)
        
        # En yüksek eşleşme değerini bul
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        for pt in zip(*loc[::-1]):
            try:
                x, y = pt[0] + w // 2, pt[1] + h // 2
                log_message(f"🎯 Accept Trial bulundu ve tıklanıyor: ({x}, {y})")
                pyautogui.moveTo(x, y, duration=0.1)
                
                # 3 kez tıkla
                for i in range(3):
                    pyautogui.click()
                    time.sleep(0.08)
                
                # 10 saniye bekle ve kontrol et
                for i in range(10):
                    time.sleep(1.0)
                    screenshot2 = pyautogui.screenshot()
                    screenshot2_gray = cv2.cvtColor(np.array(screenshot2), cv2.COLOR_RGB2GRAY)
                    res2 = cv2.matchTemplate(screenshot2_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                    if not np.any(res2 >= threshold):
                        log_message("✅ Accept Trial başarıyla tıklandı")
                        return True
                log_message("❌ Accept Trial tıklama başarısız")
                return False
            except Exception as e:
                log_message(f"❌ Tıklama hatası: {e}")
                return False
        
        
        return False
    except Exception as e:
        log_message(f"❌ Accept Trial arama hatası: {e}")
        return False

def auto_click():
    """Otomatik tıklama döngüsü"""
    global auto_clicking, click_count
    log_message("🔄 Otomatik tıklama döngüsü başladı")
    
    while auto_clicking:
        try:
            # Ruin kontrolü aktifse önce onu kontrol et
            if ruin_var.get():
                ruin_found, stack_num = find_ruin_and_stack()
                selected_stack = stack_var.get()
                if ruin_found:
                    log_message(f"🧨 Ruin stack: {stack_num} (seçili: {selected_stack})")
                    if stack_num is not None and stack_num >= selected_stack:
                        log_message(f"⚠️ Ruin stack {stack_num} >= {selected_stack}, Take Rewards tıklanıyor!")
                        pt = find_take_rewards_button()
                        if pt:
                            pyautogui.moveTo(pt[0], pt[1], duration=0.1)
                            pyautogui.click()
                            log_message("🏆 Take Rewards tıklandı!")
                            time.sleep(2.0)
                        else:
                            log_message("❌ Take Rewards butonu bulunamadı!")
                        time.sleep(1.0)
                        continue  # Bu turu atla, Accept Trial tıklama
            
            clicked = find_and_click_accept_trial()
            if clicked:
                click_count += 1
                click_label.config(text=f"Tıklama: {click_count}")
                log_message(f"📊 Toplam tıklama: {click_count}")
            
            time.sleep(1.0)  # 1 saniye bekle
        except Exception as e:
            log_message(f"❌ Otomatik tıklama hatası: {e}")
            time.sleep(2.0)  # Hata durumunda daha uzun bekle
    
    log_message("🛑 Otomatik tıklama döngüsü durduruldu")

def start_clicking():
    """Otomasyonu başlatır"""
    global auto_clicking
    if not auto_clicking:
        auto_clicking = True
        status_label.config(text="▶ Çalışıyor")
        log_message("🚀 Otomasyon başlatıldı")
        log_message("💡 Numpad 0 tuşu ile durdurabilirsin")
        threading.Thread(target=auto_click, daemon=True).start()

def stop_clicking():
    """Otomasyonu durdurur"""
    global auto_clicking
    auto_clicking = False
    status_label.config(text="⏸ Bekliyor")
    log_message("⏹ Otomasyon durduruldu")

def find_ruin_and_stack():
    """Ekranda ruin simgesi ve stack sayısı tespit eder. (template matching ile, tüm ekran)"""
    if not ruin_stack_images or any(img is None for img in ruin_stack_images):
        log_message("❌ Ruin stack rakam görselleri yüklenmemiş")
        return False, None
    try:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        stack_area = screenshot_np  # Tüm ekran
        best_score = 0
        best_stack = None
        threshold = 0.7  # Yükselttik!
        for idx, template in enumerate(ruin_stack_images):
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            area_gray = cv2.cvtColor(stack_area, cv2.COLOR_RGB2GRAY)
            res = cv2.matchTemplate(area_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # log_message(f"Stack {idx+1} için eşleşme skoru: {max_val:.3f}")
            if max_val > best_score:
                best_score = max_val
                best_stack = idx + 1
        if best_score > threshold:
            log_message(f"🧨 Ruin stack bulundu: {best_stack} (skor: {best_score:.3f})")
            return True, best_stack
        else:
            return False, None
    except Exception as e:
        log_message(f"❌ Ruin tespit hatası: {e}")
        return False, None

# Tkinter UI
root = tk.Tk()
root.title("Ultimatum Otomasyon v1.0.0")
root.geometry("380x280")
root.resizable(False, False)

# Ana frame
main_frame = tk.Frame(root)
main_frame.pack(padx=8, pady=8, fill='both', expand=True)

# Buton frame
button_frame = tk.Frame(main_frame)
button_frame.pack(fill='x', pady=(0, 3))

# Butonları yan yana yerleştir
start_btn = tk.Button(button_frame, text="▶ Başlat", command=start_clicking, 
                     bg='#28a745', fg='white', font=('Arial', 9, 'bold'),
                     width=10, height=1)
start_btn.pack(side='left', padx=(0, 3))

stop_btn = tk.Button(button_frame, text="⏹ Durdur", command=stop_clicking, 
                    bg='#dc3545', fg='white', font=('Arial', 9, 'bold'),
                    width=10, height=1)
stop_btn.pack(side='left', padx=(0, 3))

clear_log_btn = tk.Button(button_frame, text="🗑 Temizle", command=clear_logs, 
                         bg='#6c757d', fg='white', font=('Arial', 9),
                         width=10, height=1)
clear_log_btn.pack(side='left')

# Bilgi frame
info_frame = tk.Frame(main_frame)
info_frame.pack(fill='x', pady=(3, 5))

click_label = tk.Label(info_frame, text="Tıklama: 0", 
                      font=('Arial', 10, 'bold'), fg='#495057')
click_label.pack(side='left')

# Ruin kontrolü ve stack seçimi
ruin_var = tk.BooleanVar(value=False)
ruin_check = tk.Checkbutton(info_frame, text="Ruin kontrolü", variable=ruin_var, font=('Arial', 9))
ruin_check.pack(side='left', padx=(10, 2))

stack_var = tk.IntVar(value=6)
stack_spin = tk.Spinbox(info_frame, from_=1, to=6, width=2, textvariable=stack_var, font=('Arial', 9))
stack_spin.pack(side='left', padx=(2, 0))

# Status label
status_label = tk.Label(info_frame, text="⏸ Bekliyor", 
                       font=('Arial', 9), fg='#6c757d')
status_label.pack(side='right')

# Log frame
log_frame = tk.Frame(main_frame)
log_frame.pack(fill='both', expand=True)

# Log başlığı
log_title = tk.Label(log_frame, text="📋 Log Kayıtları", 
                    font=('Arial', 9, 'bold'), fg='#495057')
log_title.pack(anchor='w', pady=(0, 3))

# Log text
log_text = scrolledtext.ScrolledText(log_frame, width=45, height=10, 
                                   state='disabled', font=('Consolas', 8),
                                   bg='#f8f9fa', fg='#212529')
log_text.pack(fill='both', expand=True)

# Resimleri yükle
load_images()

# Kısayol tuşlarını ayarla
setup_hotkeys()

# Başlangıç mesajı
log_message("🚀 Ultimatum Otomasyon başlatıldı")
log_message("📱 UI compact modda çalışıyor")

root.mainloop()