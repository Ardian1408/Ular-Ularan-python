import pygame
import random
import json

# Inisialisasi pygame
pygame.init()

# Ukuran layar
lebar_layar = 800
tinggi_layar = 600

# Warna
warna_hitam = (0, 0, 0)
warna_putih = (255, 255, 255)
warna_merah = (255, 0, 0)

# Ukuran ular
ukuran_blok = 20

# Membuat layar permainan
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Permainan Ular-Ularan")

# Mengatur kecepatan permainan
clock = pygame.time.Clock()
kecepatan_permainan = 15

# Musik latar belakang
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.2)  # Mengatur volume musik (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Mengulang musik latar belakang secara terus-menerus

# Fungsi untuk menggambar ular
def gambar_ular(ukuran_blok, ular):
    for blok in ular:
        pygame.draw.rect(layar, warna_merah, [blok[0], blok[1], ukuran_blok, ukuran_blok])

# Fungsi untuk menampilkan menu awal
def tampilkan_menu_awal():
    menu_selesai = False

    while not menu_selesai:
        layar.fill(warna_putih)
        font = pygame.font.Font(None, 40)

        teks_start_game = font.render("Start Game", True, warna_hitam)
        teks_pengaturan = font.render("Pengaturan", True, warna_hitam)
        teks_selesai = font.render("Selesai", True, warna_hitam)

        posisi_teks_start_game = (lebar_layar / 2 - teks_start_game.get_width() / 2, tinggi_layar / 2 - 50)
        posisi_teks_pengaturan = (lebar_layar / 2 - teks_pengaturan.get_width() / 2, tinggi_layar / 2)
        posisi_teks_selesai = (lebar_layar / 2 - teks_selesai.get_width() / 2, tinggi_layar / 2 + 50)

        layar.blit(teks_start_game, posisi_teks_start_game)
        layar.blit(teks_pengaturan, posisi_teks_pengaturan)
        layar.blit(teks_selesai, posisi_teks_selesai)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if posisi_teks_start_game[0] <= mouse_pos[0] <= posisi_teks_start_game[0] + teks_start_game.get_width() and \
                        posisi_teks_start_game[1] <= mouse_pos[1] <= posisi_teks_start_game[1] + teks_start_game.get_height():
                    permainan_ular()
                elif posisi_teks_pengaturan[0] <= mouse_pos[0] <= posisi_teks_pengaturan[0] + teks_pengaturan.get_width() and \
                        posisi_teks_pengaturan[1] <= mouse_pos[1] <= posisi_teks_pengaturan[1] + teks_pengaturan.get_height():
                    tampilkan_pengaturan()
                elif posisi_teks_selesai[0] <= mouse_pos[0] <= posisi_teks_selesai[0] + teks_selesai.get_width() and \
                        posisi_teks_selesai[1] <= mouse_pos[1] <= posisi_teks_selesai[1] + teks_selesai.get_height():
                    pygame.quit()

# Fungsi untuk menampilkan pengaturan
def tampilkan_pengaturan():
    pengaturan_selesai = False
    kecepatan_pergerakan = kecepatan_permainan

    while not pengaturan_selesai:
        layar.fill(warna_putih)
        font = pygame.font.Font(None, 40)

        teks_kecepatan = font.render("Kecepatan Pergerakan: " + str(kecepatan_pergerakan), True, warna_hitam)
        teks_kembali = font.render("Kembali", True, warna_hitam)

        posisi_teks_kecepatan = (lebar_layar / 2 - teks_kecepatan.get_width() / 2, tinggi_layar / 2 - 50)
        posisi_teks_kembali = (lebar_layar / 2 - teks_kembali.get_width() / 2, tinggi_layar / 2)

        layar.blit(teks_kecepatan, posisi_teks_kecepatan)
        layar.blit(teks_kembali, posisi_teks_kembali)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if posisi_teks_kecepatan[0] <= mouse_pos[0] <= posisi_teks_kecepatan[0] + teks_kecepatan.get_width() and \
                        posisi_teks_kecepatan[1] <= mouse_pos[1] <= posisi_teks_kecepatan[1] + teks_kecepatan.get_height():
                    kecepatan_pergerakan += 1
                    if kecepatan_pergerakan > 30:
                        kecepatan_pergerakan = 1
                elif posisi_teks_kembali[0] <= mouse_pos[0] <= posisi_teks_kembali[0] + teks_kembali.get_width() and \
                        posisi_teks_kembali[1] <= mouse_pos[1] <= posisi_teks_kembali[1] + teks_kembali.get_height():
                    pengaturan_selesai = True

        clock.tick(10)

    # Menyimpan pengaturan ke file JSON
    simpan_pengaturan(kecepatan_pergerakan)
    tampilkan_menu_awal()

# Fungsi untuk menyimpan pengaturan ke file JSON
def simpan_pengaturan(kecepatan):
    pengaturan = {
        "kecepatan_pergerakan": kecepatan
    }
    with open("pengaturan.json", "w") as file:
        json.dump(pengaturan, file)

# Fungsi untuk memuat pengaturan dari file JSON
def muat_pengaturan():
    try:
        with open("pengaturan.json", "r") as file:
            pengaturan = json.load(file)
            return pengaturan["kecepatan_pergerakan"]
    except FileNotFoundError:
        return kecepatan_permainan

# Fungsi untuk menjalankan permainan
def permainan_ular():
    game_over = False
    game_selesai = False

    # Mengatur posisi awal ular
    x_ular = lebar_layar / 2
    y_ular = tinggi_layar / 2

    # Mengatur perubahan posisi awal ular
    perubahan_x = 0
    perubahan_y = 0

    # Membuat ular sebagai list
    ular = []
    panjang_ular = 1

    # Mengatur posisi makanan
    posisi_makanan = [random.randrange(1, lebar_layar // ukuran_blok) * ukuran_blok,
                      random.randrange(1, tinggi_layar // ukuran_blok) * ukuran_blok]

    # Memuat pengaturan kecepatan pergerakan
    kecepatan_permainan = muat_pengaturan()

    while not game_over:
        while game_selesai:
            layar.fill(warna_putih)
            font = pygame.font.Font(None, 40)
            teks = font.render("Permainan selesai, tekan R untuk bermain lagi atau Q untuk keluar", True, warna_hitam)
            layar.blit(teks, (lebar_layar / 2 - teks.get_width() / 2, tinggi_layar / 2 - teks.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        permainan_ular()
                    if event.key == pygame.K_q:
                        game_over = True
                        game_selesai = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    perubahan_x = -ukuran_blok
                    perubahan_y = 0
                elif event.key == pygame.K_RIGHT:
                    perubahan_x = ukuran_blok
                    perubahan_y = 0
                elif event.key == pygame.K_UP:
                    perubahan_y = -ukuran_blok
                    perubahan_x = 0
                elif event.key == pygame.K_DOWN:
                    perubahan_y = ukuran_blok
                    perubahan_x = 0

        # Mengubah posisi ular
        x_ular += perubahan_x
        y_ular += perubahan_y

        # Mengecek jika ular keluar dari layar
        if x_ular >= lebar_layar or x_ular < 0 or y_ular >= tinggi_layar or y_ular < 0:
            game_selesai = True

        # Membuat tampilan layar permainan
        layar.fill(warna_putih)
        pygame.draw.rect(layar, warna_merah, [posisi_makanan[0], posisi_makanan[1], ukuran_blok, ukuran_blok])

        # Menambahkan kepala ular ke list ular
        kepala_ular = []
        kepala_ular.append(x_ular)
        kepala_ular.append(y_ular)
        ular.append(kepala_ular)

        # Mengecek jika panjang ular lebih dari panjang yang ditentukan, hapus ekor ular
        if len(ular) > panjang_ular:
            del ular[0]

        # Mengecek jika ular menabrak tubuhnya sendiri
        for blok in ular[:-1]:
            if blok == kepala_ular:
                game_selesai = True

        # Menggambar ular
        gambar_ular(ukuran_blok, ular)

        # Mengupdate layar permainan
        pygame.display.update()

        # Mengecek jika ular makan makanan
        if x_ular == posisi_makanan[0] and y_ular == posisi_makanan[1]:
            posisi_makanan = [random.randrange(1, lebar_layar // ukuran_blok) * ukuran_blok,
                              random.randrange(1, tinggi_layar // ukuran_blok) * ukuran_blok]
            panjang_ular += 1

        # Mengatur kecepatan permainan
        clock.tick(kecepatan_permainan)

    pygame.quit()

# Memulai permainan
tampilkan_menu_awal()
