# Ultimatum Otomasyon

Bu uygulama, oyunlarda "Accept Trial" butonlarını otomatik olarak tıklamak için geliştirilmiş bir otomasyon aracıdır.

## Özellikler

- Otomatik "Accept Trial" butonu tespiti ve tıklama
- "Take Rewards" butonu tespiti
- Gerçek zamanlı log sistemi
- Tıklama sayısı takibi
- Basit ve kullanıcı dostu arayüz

## Kullanım

### Exe Dosyası ile Çalıştırma (Önerilen)

1. `dist/ultimatum.exe` dosyasını çalıştırın
2. Uygulama arayüzü açılacaktır
3. "Başlat" butonuna tıklayarak otomasyonu başlatın
4. "Durdur" butonuna tıklayarak otomasyonu durdurun

### Python ile Çalıştırma

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```bash
   python ultimatum.py
   ```

## Gerekli Dosyalar

Uygulamanın çalışması için aşağıdaki PNG dosyaları gereklidir:
- `accept_trial.png` - Accept Trial butonunun şablon görseli
- `take_rewards.png` - Take Rewards butonunun şablon görseli
- `current_reward_box.png` - Ödül kutusu şablon görseli

## Ayarlar

- `ACCEPT_TRIAL_THRESHOLD = 0.75` - Accept Trial butonu tespit eşiği
- Tıklama aralığı: 0.5 saniye
- Bekleme süresi: 10 saniye (tıklama sonrası)

## Log Dosyası

Uygulama çalışırken `log.txt` dosyasına detaylı loglar kaydedilir.

## Notlar

- Uygulama çalışırken oyun penceresinin görünür olması gerekir
- PNG şablon dosyalarının güncel olması önemlidir
- Otomasyon sırasında fare ve klavye kullanımından kaçının

## Teknik Detaylar

- **Python 3.13** ile geliştirilmiştir
- **OpenCV** ile görsel tespit
- **PyAutoGUI** ile fare kontrolü
- **Tkinter** ile kullanıcı arayüzü
- **PyInstaller** ile exe oluşturma