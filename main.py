import pygame, sys
import os
pygame.font.init()
pygame.mixer.init()

#ustawienie ikony naszej gry
ikona = pygame.image.load(os.path.join('Assets','icon.jpeg'))
pygame.display.set_icon(ikona)

#stałe parametry
SZEROKOSC, DLUGOSC = 900, 600
SZEROKOSC_MARGINESU = 20
SZEROKOSC_OBIEKTU, DLUGOSC_OBIEKTU = 40, 40
PREDKOSC = 5
PREDKOSC_POCISKU = 7
MAX_POCISKOW = 3
FPS = 60

#event trafienia gracza
GRACZ1_TRAFIONY = pygame.USEREVENT + 1
GRACZ2_TRAFIONY = pygame.USEREVENT + 2

#obrazek na tło statku
ZOLTY_STATEK_OBRAZEK = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
CZERWONY_STATEK_OBRAZEK = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

#pygame.transform.rotate("co obracamy", "o jaki stopień obracamy")
ZOLTY_STATEK = pygame.transform.rotate(pygame.transform.scale(ZOLTY_STATEK_OBRAZEK, (SZEROKOSC_OBIEKTU, DLUGOSC_OBIEKTU)), 90)
CZERWONY_STATEK = pygame.transform.rotate(pygame.transform.scale(CZERWONY_STATEK_OBRAZEK, (SZEROKOSC_OBIEKTU, DLUGOSC_OBIEKTU)), 270)

#obrazek na tło planszy
GWIAZDY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (SZEROKOSC,DLUGOSC))

#dodajemy font do wyświetlania ilości żyć obu graczy
ZYCIA_FONT = pygame.font.SysFont("helvetica", 25)
AUTOR_FONT = pygame.font.SysFont("helvetica", 20)

#font do wyświetlania informacji o zwycięzcy. Helvetica - 50
ZWYCIEZCA_FONT = pygame.font.SysFont("helvetica", 90)

#zaimportować dźwięk do naszej gry
ODGLOS_STRZAL = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
ODGLOS_TRAFIENIE = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
ODGLOS_FANFARY = pygame.mixer.Sound(os.path.join('Assets','Ta-Dah.mp3'))

#załadowanie i odtwarzanie muzyki w tle
pygame.mixer.music.load(os.path.join('Assets','Pipe.mp3'))
pygame.mixer.music.play(-1,0.0)

#tworzymy nową klasę z naszą grą
class MojaGra:
    #tworzymy konstruktor
    def __init__(self):
        # inicjujemy pygame
        pygame.init()
        # tworzymy nasze okno gry
        self.okno = pygame.display.set_mode((SZEROKOSC, DLUGOSC))
        pygame.display.set_caption("Pierwsza gra Konrada!")

        self.gracz1 = pygame.Rect(100, 100, SZEROKOSC_OBIEKTU, DLUGOSC_OBIEKTU)
        self.gracz2 = pygame.Rect(700, 100, SZEROKOSC_OBIEKTU, DLUGOSC_OBIEKTU)

        self.pociski_gracz1 = []
        self.pociski_gracz2 = []

        self.granica = pygame.Rect(SZEROKOSC//2 - 5, 0, 10, DLUGOSC)

        self.zycia_gracz1 = self.zycia_gracz2 = 10

    def start(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            self.obslugaEventow()
            self.obslugaKlawiszy()
            self.obslugaPociskow()
            self.obslugaPunktow()
            self.obslugaEkranu()

    def obslugaPociskow(self):
        for pocisk in self.pociski_gracz1:
            pocisk.x += PREDKOSC_POCISKU
            # jeżeli pocisk uderzy w przeciwnika to znika z talbicy pociski_gracza
            if self.gracz2.colliderect(pocisk):
                #informacja, że gracz został trafiony
                pygame.event.post(pygame.event.Event(GRACZ2_TRAFIONY))
                #pocisk znika z tablicy pociski-gracza
                self.pociski_gracz1.remove(pocisk)
            # jeżeli pocisk wyleci poza ekran to znika z tablicy pociski_gracza
            elif pocisk.x > SZEROKOSC:
                self.pociski_gracz1.remove(pocisk)

        for pocisk in self.pociski_gracz2:
            pocisk.x -= PREDKOSC_POCISKU
            if self.gracz1.colliderect(pocisk):
                pygame.event.post(pygame.event.Event(GRACZ1_TRAFIONY))
                self.pociski_gracz2.remove(pocisk)
            elif pocisk.x < -10:
                self.pociski_gracz2.remove(pocisk)

    def obslugaPunktow(self):
        tekst_zwyciezca = ""
        #sprawdzamy, czy któryś z graczy ma mniej niż 1 punkt życia
        if self.zycia_gracz1 <= 0:
            tekst_zwyciezca = "Gracz 2 wygrał!"
        if self.zycia_gracz2 <= 0:
            tekst_zwyciezca = "Gracz 1 wygrał!"

        if tekst_zwyciezca:
            #duży napis na środku z tekstem tekst_zwyciezca
            #print(tekst_zwyciezca)
            zwyciezca = ZWYCIEZCA_FONT.render(tekst_zwyciezca, True, (200,200,200))
            self.okno.blit(zwyciezca, (SZEROKOSC/2 - zwyciezca.get_width()/2, DLUGOSC/2 - zwyciezca.get_height()/2))
            ODGLOS_FANFARY.play()
            pygame.display.update()
            pygame.time.delay(5000)
            self.__init__()

    def obslugaEkranu(self):
        self.okno.blit(GWIAZDY, (0,0))
        #rysujemy ile punktów życia ma gracz 1
        gracz1_zycie = ZYCIA_FONT.render("Życie: " + str(self.zycia_gracz1), True, (230,230,230))
        self.okno.blit(gracz1_zycie, (10,10))

        #rysujemy ile punktów życia ma gracz 2
        gracz2_zycie = ZYCIA_FONT.render("Życie:" + str(self.zycia_gracz2), True, (230,230,230))
        self.okno.blit(gracz2_zycie, (790,10))

        #podpis autora "Autor gry: IMIE, 2021 rok"
        #stworzyć nowy font: AUTOR_FONT: Helvetica. wielkość fontu: 12. umiejscowienie: prawy dolny róg ekranu. kolor: jasnoniebieski
        #ZYCIA_FONT = pygame.font.SysFont("helvetica", 25)
        copyright = AUTOR_FONT.render("Konrad, 2021 r.", True, (160, 200, 180))
        self.okno.blit(copyright, (780, 570))

        pygame.draw.rect(self.okno, (5, 5, 5), self.granica)
        self.okno.blit(ZOLTY_STATEK, (self.gracz1.x,self.gracz1.y))
        self.okno.blit(CZERWONY_STATEK, (self.gracz2.x,self.gracz2.y))

        for pocisk in self.pociski_gracz1:
            pygame.draw.rect(self.okno, (255,0,0), pocisk)
        for pocisk in self.pociski_gracz2:
            pygame.draw.rect(self.okno, (255,0,0), pocisk)

        pygame.display.flip()

    def obslugaKlawiszy(self):
        # wszystkie wcisniete klawisze
        klawisze = pygame.key.get_pressed()
        # poruszanie kwadratu lewo/prawo graczem 1
        if klawisze[pygame.K_RIGHT] and self.gracz1.x < self.granica.x - SZEROKOSC_OBIEKTU:
            self.gracz1.x += PREDKOSC
        elif klawisze[pygame.K_LEFT] and self.gracz1.x > SZEROKOSC_MARGINESU:
            self.gracz1.x -= PREDKOSC
        elif klawisze[pygame.K_UP] and self.gracz1.y > SZEROKOSC_MARGINESU:
            self.gracz1.y -= PREDKOSC
        elif klawisze[pygame.K_DOWN] and self.gracz1.y < DLUGOSC - SZEROKOSC_OBIEKTU - SZEROKOSC_MARGINESU:
            self.gracz1.y += PREDKOSC

        # poruszanie kwadratu lewo/prawo graczem 2
        if klawisze[pygame.K_d] and self.gracz2.x < SZEROKOSC - SZEROKOSC_OBIEKTU - SZEROKOSC_MARGINESU:
            self.gracz2.x += PREDKOSC
        elif klawisze[pygame.K_a] and self.gracz2.x > self.granica.x + self.granica.width:
            self.gracz2.x -= PREDKOSC
        elif klawisze[pygame.K_w] and self.gracz2.y > SZEROKOSC_MARGINESU:
            self.gracz2.y -= PREDKOSC
        elif klawisze[pygame.K_s] and self.gracz2.y < DLUGOSC - SZEROKOSC_OBIEKTU - SZEROKOSC_MARGINESU:
            self.gracz2.y += PREDKOSC

    def obslugaEventow(self):
        # nasłuchiwania akcji użytkowników
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            #obsługa strzelania pierwszego gracza jako event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m and len(self.pociski_gracz1) < MAX_POCISKOW:
                pocisk = pygame.Rect(self.gracz1.x + self.gracz1.width, self.gracz1.y + self.gracz1.height // 2, 10, 5)
                self.pociski_gracz1.append(pocisk)
                ODGLOS_STRZAL.play()

            #obsluga strzelania drugiego gracza jako event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and len(self.pociski_gracz2) < MAX_POCISKOW:
                pocisk = pygame.Rect(self.gracz2.x, self.gracz2.y + self.gracz2.height // 2, 10, 5)
                self.pociski_gracz2.append(pocisk)
                ODGLOS_STRZAL.play()

            #sprawdzenie czy event trafienia został wywołany
            if event.type == GRACZ1_TRAFIONY:
                self.zycia_gracz1 -= 1
                ODGLOS_TRAFIENIE.play()

            if event.type == GRACZ2_TRAFIONY:
                self.zycia_gracz2 -= 1
                ODGLOS_TRAFIENIE.play()

gierka = MojaGra()
gierka.start()