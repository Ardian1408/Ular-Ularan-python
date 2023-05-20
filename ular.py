import pygame
import random

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

# Fungsi untuk menggambar ular
def gambar_ular(ukuran_blok, ular):
    for blok in ular:
        pygame.draw.rect(layar, warna_merah, [blok[0], blok[1], ukuran_blok, ukuran_blok])

# Fungsi untuk menjalankan permainan
def permainan_ular():
    game_over = False
    game_selesai = False

    # Koordinat awal ular
    x_ular = lebar_layar / 2
    y_ular = tinggi_layar / 2

    # Perubahan koordinat ular
    perubahan_x = 0
    perubahan_y = 0

    # Membuat ular
    ular = []
    panjang_ular = 1

    # Membuat makanan
    posisi_makanan = [random.randrange(1, lebar_layar // ukuran_blok) * ukuran_blok,
                      random.randrange(1, tinggi_layar // ukuran_blok) * ukuran_blok]

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
        pygame.display.update()

        # Mengecek jika ular memakan makanan
        if x_ular == posisi_makanan[0] and y_ular == posisi_makanan[1]:
            posisi_makanan = [random.randrange(1, lebar_layar // ukuran_blok) * ukuran_blok,
                              random.randrange(1, tinggi_layar // ukuran_blok) * ukuran_blok]
            panjang_ular += 1

        # Mengatur kecepatan permainan
        clock.tick(kecepatan_permainan)

    pygame.quit()

# Memulai permainan
permainan_ular()
