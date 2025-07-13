# Ultimatum Otomasyon v1.1.0

Bu uygulama, oyunlarda "Accept Trial" butonlarını otomatik olarak tıklamak ve ruin kontrolü yapmak için geliştirilmiş gelişmiş bir otomasyon aracıdır.

## 🆕 Yeni Özellikler (v1.1.0)

- **🧨 Ruin Kontrolü**: Otomatik ruin stack tespiti ve kontrolü
- **🏆 Akıllı Take Rewards**: Ruin stack belirlenen eşiği geçtiğinde otomatik ödül alma
- **📸 Gömülü Görseller**: Artık harici PNG dosyalarına ihtiyaç yok
- **⌨️ Kısayol Tuşları**: Numpad 0 ile hızlı durdurma
- **📊 Gelişmiş Log Sistemi**: Daha detaylı ve renkli log mesajları
- **⚙️ Ayarlanabilir Stack Eşiği**: 1-6 arası stack seviyesi seçimi

## Özellikler

- ✅ Otomatik "Accept Trial" butonu tespiti ve tıklama
- ✅ "Take Rewards" butonu tespiti ve akıllı tıklama
- ✅ Ruin stack sayısı tespiti (1-6 arası)
- ✅ Gerçek zamanlı log sistemi
- ✅ Tıklama sayısı takibi
- ✅ Basit ve kullanıcı dostu arayüz
- ✅ Kısayol tuşları desteği
- ✅ Gömülü görsel şablonları

## Kullanım

### Exe Dosyası ile Çalıştırma (Önerilen)

1. `dist/ultimatum.exe` dosyasını çalıştırın
2. Uygulama arayüzü açılacaktır
3. **Ruin Kontrolü** kutusunu işaretleyin (isteğe bağlı)
4. **Stack** değerini ayarlayın (1-6 arası)
5. "Başlat" butonuna tıklayarak otomasyonu başlatın
6. "Durdur" butonuna tıklayarak veya **Numpad 0** tuşuna basarak otomasyonu durdurun

### Python ile Çalıştırma

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```bash
   python ultimatum.py
   ```

## Ruin Kontrolü Nasıl Çalışır?

1. **Ruin Kontrolü** kutusunu işaretleyin
2. **Stack** değerini belirleyin (örn: 4)
3. Uygulama sürekli olarak ekranda ruin stack sayısını kontrol eder
4. Stack sayısı belirlenen değere ulaştığında otomatik olarak "Take Rewards" butonuna tıklar
5. Bu sayede ruin riskini minimize edersiniz

## Kısayol Tuşları

- **Numpad 0**: Otomasyonu durdur
- **Başlat/Durdur Butonları**: Manuel kontrol

## Ayarlar

- **Accept Trial Threshold**: 0.6 (esnek tespit için düşürüldü)
- **Take Rewards Threshold**: 0.8
- **Ruin Stack Threshold**: 0.7
- **Tıklama aralığı**: 1 saniye
- **Bekleme süresi**: 10 saniye (tıklama sonrası)

## Log Dosyası

Uygulama çalışırken `log.txt` dosyasına detaylı loglar kaydedilir:
- 📸 Resim yükleme durumu
- 🎯 Buton tespit ve tıklama işlemleri
- 🧨 Ruin stack tespitleri
- 🏆 Take Rewards işlemleri
- ❌ Hata mesajları

## Teknik İyileştirmeler

- **Gömülü Görseller**: Base64 formatında gömülü şablon görselleri
- **Gelişmiş Hata Yönetimi**: Daha detaylı hata mesajları
- **Performans Optimizasyonu**: Daha hızlı görsel tespit
- **Bellek Optimizasyonu**: Daha az RAM kullanımı

## Notlar

- Uygulama çalışırken oyun penceresinin görünür olması gerekir
- Ruin kontrolü aktifken daha dikkatli olun
- Otomasyon sırasında fare ve klavye kullanımından kaçının
- Stack eşiğini oyun stratejinize göre ayarlayın

## Teknik Detaylar

- **Python 3.13** ile geliştirilmiştir
- **OpenCV** ile görsel tespit
- **PyAutoGUI** ile fare kontrolü
- **Tkinter** ile kullanıcı arayüzü
- **PyInstaller** ile exe oluşturma
- **Base64** ile gömülü görseller

## Sürüm Geçmişi

### v1.1.0 (Güncel)
- 🆕 Ruin kontrolü eklendi
- 🆕 Akıllı Take Rewards sistemi
- 🆕 Gömülü görsel şablonları
- 🆕 Kısayol tuşları
- 🆕 Ayarlanabilir stack eşiği
- 🔧 Gelişmiş hata yönetimi
- 🔧 Performans optimizasyonları

### v1.0.0
- İlk sürüm
- Temel Accept Trial otomasyonu
- Basit kullanıcı arayüzü