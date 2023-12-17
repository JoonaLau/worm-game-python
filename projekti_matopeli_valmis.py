"""
COMP.CS.100
Tekijä: Joona Laukkanen, joona.o.laukkanen@tuni.fi
Opiskelijanumero: 150834359
Käyttöliittymäprojekti: matopeli. Tavoitteena kehittynyt versio.

Matopelin ohjeet: Peli alkaa siten, että madon pää ja omena on sijoitettu
sattumanvaraisiin koordinaatteihin. Madon pituus on aina aluksi yksi ruutu.
Kun ensimmäisen kerran painaa mitä tahansa nuolinäppäintä, mato alkaa
liikkumaan 0.1 sekunnin välein automaattisesti aina viimeisen nuolinäppäimen
määräämään suuntaan. Omenan syötyään madon pituus kasvaa yhdellä. Pelin
voittaa, kun pisteitä on saanut väh. 30. Peli loppuu, jos mato osuu seinään
tai itseensä.
Omenoiden lisäksi ruudukkoon ilmestyy kysymysmerkkejä. Uusi kysymysmerkki
ilmestyy aina 8-12 sekunnin jälkeen pelin aloittamisesta tai kysymysmerkin
keräämisestä.
Kysymysmerkki sisältää sattumanvaraisesti jonkin seuraavista ominaisuuksista:

Myrkytys: Mato menettää pituuttaan 3. Peli pysäytetään hetkeksi, että käyttäjä
ehtii lukemaan ja reagoimaan tämän johdosta luotuun ilmoitukseen.

Vauhdinlisäys: Madon nopeus kolminkertaistuu (liikkumisväli 100ms -> 33ms)
Peliä ei pysäytetä tai mitään ilmoitusta tehdä, jotta tämä efekti pysyisi
yllätyksellisenä. Voimassaoloaika 8 sekuntia.

Päinvastaiset käännökset: Tämän efektin aikana käyttäjän nuolinäppäimen
painallukset luetaan päinvastaisena. Peli pysäytetään hetkeksi, että
ilmoitukseen ehtii reagoida. Voimassaoloaika 8 sekuntia.

Haavoittumattomuus: Tämän efektin aikana mato voi kulkea seinien läpi
pelikentän toiselle puolella, eikä voi myöskään kuolla osuessa itseensä.
Tästä käyttäjä saa ilmoituksen, joka myös näyttää jäljellä olevan
voimassaoloajan. Voimassaoloaika 10 sekuntia.

Extra-kasvu: Tämän efektin aikana, aina kun omena syödään madon pituus kasvaa
yhden sijasta kahdella. Näkyviin tulee myös ilmoitus käyttäjälle.
Voimassaoloaika 10 sekuntia.
_______________________________________________________________________________
Tällä hetkellä itse testaamalla löydetyt bugit:
(1) Tietoa: Ohjelma ei anna madon kääntyä liikkumissuuntaan nähden
päinvastaiseen suuntaan.
Bugi: Kuitenkin jos yhden liikkumisvälin (0.1 sec) aikana ehtii kääntää suunnan
kahdella painalluksella päinvastaiseksi, on madon mahdollista törmätä itseensä.
Esim: Suunta vasen, 0.1 sec aikana nuolinäppäimen painallukset "alas","oikea".
Tämän voisi paremmalla ajalla korjata, muttä tällä kertaa ei ehtinyt.

(2) Bugi: Madon myrkyttyessä, jos pituutta on kertynyt riittävästi, hännän
poistaminen ei mene sulavasti, vaan poistettavan hännän väliin jää tyhjiä
ruutuja. Optimoidumpaan versioon tämän voisi korjata.
_______________________________________________________________________________
Käyttöliittymäkomponentti, johon tutuistuin itsenäisesti ja tässä ohjelmassa
käytin oli tkinter-kirjaston "Canvas". Lisäksi sain aikaan automaattisesti
liikkuvan madon, joka reagoin näppäintunnistimeen. Näiden ominaisuuksien ja
itse pelisisällön osalta tämä on perusteluni sille, että kyseessä on
kehittynyt käyttöliittymä.

_______________________________________________________________________________
Docstringeista: Tuo näppäimistönlukija oli minulle uusi opeteltava asia ja
koska en ole ehtinyt täysin perehtyä siihen, en osaa vielä kommentoida siihen
liittyviä parametrejä oikein. Lisäksi kun ohjelmassani on paljon lyhyitä
funktioita, niin olisi kysymys siihen liittyen: Mikä on käytäntönä ja tapana
:return: osan kommentointiin, jos funktio ei palauta mitään? Lisätäänkö silti
aina :return: None, vai voiko tämän jättää kokonaan lisäämättä?
_______________________________________________________________________________
Pelin resoluutio, liikkeet ja ruudut on suunniteltu siten, että ne skaalauvat
10 yksikön välein. Ohjelman on tarkoitus tällä hetkellä toimia vain 400x400
resoluutiolla, jotta kaikki muu toimii kuin pitää.
_______________________________________________________________________________
Viimeinen huomio: ajan mittaaminen pelissä sekuntien osalta ei ole täsmällisen
tarkka. Paremmalla ajalla ottaisin selvää time-kirjastosta ja loisin ohjelmaan
pelin sisäisen kellon, jonka avulla kaiken ajoittaminen olisi tismalleen
oikein. Nyt aika tarkistetaan lisäämällä jokaisella liikkumissyklillä sitä
vastaava arvo luokan aikatarkistimiin, joka ei tuota tarkkaa tulosta. (Oman
käsityksen mukaan siksi, että siinä ei voi ottaa huomioon komentojen
suorittamiseen kuluvaa aikaa.)
"""

import time
from tkinter import *
import random

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400


class Snakegame:
    """
    Tämä luokka määrittää kaikki kyseisen matopelin kannalta oleelliset
    ominaisuudet.
    """

    def __init__(self, width: int, height: int):
        # Luo tkinter-sovellusikkunan
        self.__window = Tk()
        self.__window.title("Matopeli")

        # Ikkunan koko, tyhjät ulkoreunat näyttävät (ainakin omasta mielestä)
        # paremmalta kuin 400x400 kokoinen ikkuna.
        self.__window.geometry("500x500")
        self.__window.update()  # Päivitä ikkuna

        # Canvaksen koon määrittäminen
        self.__canvas_width = width
        self.__canvas_height = height

        self.__move_interval = 100  # Madon liikkumisväli millisekunteina

        # Aika uuden kysymysmerkin ilmestymiseen
        self.__time_for_questionmark_to_appear = random.randint(8, 12)

        # Ajan seuraamiseen tarvittavat tiedot
        self.__time_from_any_effect = 0
        self.__timer_invulnerability = 0
        self.__timer_3x = 0

        # Kuvatiedoston lisääminen kysymysmerkkiä varten
        self.__questionmark_photo = PhotoImage(file="questionmark.png")
        # Sattumanvaraiset koordinaatit kysymysmerkille
        self.__questionmark_location = (self.generate_rand_coordinate("x"),
                                        self.generate_rand_coordinate("y"))

        # Tieto kysymysmerkin keräämisestä
        self.__questionmark_collected = False

        # Madon tila
        self.__status = None

        # Madon alustus, aloituspaikka sattumanvarainen
        self.__snake_head_x = self.generate_rand_coordinate("x")
        self.__snake_head_y = self.generate_rand_coordinate("y")
        self.__snake_body = [(self.__snake_head_x, self.__snake_head_y)]
        self.__snake_length = 1

        # Reunojen alustus
        self.__border_x = self.__canvas_width
        self.__border_y = self.__canvas_height

        # Suunta
        self.__direction = None

        # Omenan alustus, aloituspaikka sattumanvarainen
        self.__apple_x = self.generate_rand_coordinate("x")
        self.__apple_y = self.generate_rand_coordinate("y")

        # Luo pelialueen canvaksen
        self.__canvas = Canvas(self.__window, width=self.__canvas_width-11,
                               height=self.__canvas_height-11, border=10,
                               relief="solid")
        self.__canvas.pack()

        # Näppäimistönlukija
        self.__window.bind("<Key>", self.handle_key_press)

        # Pisteet
        self.__score = 0
        self.__score_to_win = 30

        # Inforuutu
        self.__info = Label(text="Press any arrow key to start")
        self.__info.pack(side="bottom")

        # Statusruutu
        self.__status_info = Label()

        # Pisteet-ruutu
        self.__score_info = Label(text=f"Score: {self.__score}")
        self.__score_info.pack(side="bottom")

    def draw_grid(self):
        """
        Piirtää canvakseen ruudukon.
        """
        for i in range(0, self.__canvas_width + 10, 10):
            self.__canvas.create_line([(i, 0), (i, self.__canvas_height)])
        for i in range(0, self.__canvas_width + 10, 10):
            self.__canvas.create_line([(0, i), (self.__canvas_width, i)])

    def start_game(self):
        """
        Aloittaa pelin. Luo pelialueen ja liikuttaa matoa "move_snake_auto"
        metodin määräämällä tavalla.
        """
        self.draw_game()
        self.move_snake_auto()
        self.__window.mainloop()

    def handle_key_press(self, event):
        """
        Määrittää madon liikkumissuunnan nuolinäppäinen painalluksen mukaan.
        Madon päinvastaisten käännösten tilaa varten myös oma määrittely.
        :param event: {keysym} (En tiedä, miten tätä parametriä pitäisi
                      kommentoida.)
        """
        key = event.keysym

        if self.__status != "inverse turns":
            if key == "Up" and self.__direction != "Down":
                self.__direction = "Up"
            elif key == "Down" and self.__direction != "Up":
                self.__direction = "Down"
            elif key == "Left" and self.__direction != "Right":
                self.__direction = "Left"
            elif key == "Right" and self.__direction != "Left":
                self.__direction = "Right"
        else:
            # Päinvastoin
            if key == "Up" and self.__direction != "Up":
                self.__direction = "Down"
            elif key == "Down" and self.__direction != "Down":
                self.__direction = "Up"
            elif key == "Left" and self.__direction != "Left":
                self.__direction = "Right"
            elif key == "Right" and self.__direction != "Right":
                self.__direction = "Left"

    def generate_rand_coordinate(self, x_or_y):
        """
        Luo sattumanvaraiset koordinaatit pelialueen sisällä.
        :param x_or_y: str, joko "x" tai "y" sen mukaan, kumman näistä akselin
                       koordinaatti halutaan luoda.
        :return: int, kokonaislukuarvo koordinaattia varten.
        """
        if x_or_y == "x":
            return random.randrange(10, self.__canvas_width - 9, 10)
        elif x_or_y == "y":
            return random.randrange(10, self.__canvas_height - 9, 10)
        else:
            pass

    def game_over(self):
        """
        Muokkaa kaikki pelin loppumisen kannalta oleelliset arvot takaisin
        oletusarvoihin. Lisäksi luo inforuudun saaduista pisteistä.
        """
        self.__info.destroy()
        self.__info = Label(text=f"Game over! Your score was: {self.__score}\n"
                                 f"Press any arrow key to start")
        self.__info.pack()
        self.reset_everything()

    def update_score(self):
        """
        Päivittää tulosnäkymän.
        """
        self.__score_info.destroy()
        self.__score_info = Label(text=f"Score: {self.__score}")
        self.__score_info.pack()

    def reset_everything(self):
        """
        Palauttaa oletusarvot. (Vain ne, mitkä on tarpeen nollata)
        """
        self.__direction = None
        self.__status = None
        self.__snake_head_x = self.generate_rand_coordinate("x")
        self.__snake_head_y = self.generate_rand_coordinate("y")
        self.__snake_body = [(self.__snake_head_x, self.__snake_head_y)]
        self.__snake_length = 1
        self.generate_new_apple()
        self.__score = 0
        self.update_score()
        self.__time_from_any_effect = 0
        self.__move_interval = 100
        self.__status_info.destroy()

    def update_apple_eaten(self, growth_amount):
        """
        Päivittää madon pituuden sen mukaan, mitä parametriksi "growth_amount"
        on annettu. Normaalisti se on yksi, mutta "extra growth" tilassa kaksi.
        Lisäksi pistenäkymä päivitetään.
        :param growth_amount: int, määrää kuinka paljon matoa ja pisteitä
                              kasvatetaan.
        """
        self.__snake_length += growth_amount
        self.__score += growth_amount
        self.update_score()
        self.generate_new_apple()

    def check_if_apple_eaten(self):
        """
        Tarkistaa, ovatko madon pään koordinaatit omenan koordinaattien
        kanssa samat. Jos on, kutsuu "update_apple_eaten"-metodia parametrinaan
        joko 1 tai 2 sen mukaan, onko madon tila "extra growth" vai jokin muu.
        """

        if self.__snake_head_x == self.__apple_x and \
                self.__snake_head_y == self.__apple_y:
            if self.__status != "extra growth":
                self.update_apple_eaten(1)
            else:
                self.update_apple_eaten(2)

    def generate_new_apple(self):
        """
        Luo uuden omenan sattumanvaraisin koordinaatein. Varmistaa myös,
        ettei omena päivity madon tai kysymysmerkin päälle.
        """

        self.__apple_x = self.generate_rand_coordinate("x")
        self.__apple_y = self.generate_rand_coordinate("y")

        for segment in self.__snake_body:
            if segment[0] == self.__apple_x and segment[1] == self.__apple_y:
                self.generate_new_apple()
                return

        if (self.__apple_x, self.__apple_y) == self.__questionmark_location:
            self.generate_new_apple()

    def check_collision_with_walls(self):
        """
        Tarkistaa tärmäyksen seinään, eli että madon pään koordinaatit ovat
        pelialueen sisällä.
        Jos ei ole, peli loppuu.
        """
        if self.__snake_head_x not in range(10, self.__border_x) or \
                self.__snake_head_y not in range(10, self.__border_y):
            self.game_over()

    def check_collision_with_itself(self):
        """
        Tarkistaa törmäyksen itseensä: Jos pään koordinaatit arvot ovat
        mikä tahansa "vartalon" koordinaateista, peli loppuu.
        """
        if (self.__snake_head_x, self.__snake_head_y) in self.__snake_body \
                and self.__snake_length > 1:
            self.game_over()

    def check_questionmark(self):
        """
        Tarkistaa, ovatko madon pään koordinaatit kysymysmerkin koordinaattien
        kanssa samat. Lisäksi aika viimeisen "efektin" (ts. kysymysmerkin)
        keräämisestä pitää olla suurempi, kuin aika kysymysmerkin
        ilmestymiselle. Tämä siksi, että kysymysmerkin koordinaatit on luotu jo
        aikaisemmin ja ovat olemassa, vaikka kysymysmerkki ei pelikentälle ole
        vielä ilmestynyt. Ehtojen täyttyessä lisätään uudet tiedot seuraavaa
        kysymysmerkkiä varten ja määritetään madolle uusi status.
        """
        if (self.__snake_head_x, self.__snake_head_y) == \
                self.__questionmark_location:

            if self.__time_from_any_effect > \
                    self.__time_for_questionmark_to_appear:

                self.__questionmark_location = \
                    (self.generate_rand_coordinate("x"),
                     self.generate_rand_coordinate("y"))
                self.__time_from_any_effect = 0
                self.__time_for_questionmark_to_appear = random.randint(8, 12)

                self.get_new_status()

    def get_new_status(self):
        """
        Määrittää madolle statuksen sattumanvaraisesti kaikista vaihtoehdoista.
        """
        rand_int = random.randint(1, 5)

        if rand_int == 1:
            self.__status = "poison"
        elif rand_int == 2:
            self.__status = "3xspeed"
        elif rand_int == 3:
            self.__status = "inverse turns"
        elif rand_int == 4:
            self.__status = "invulnerability"
        elif rand_int == 5:
            self.__status = "extra growth"

    def status_is_poison(self):
        """
        Tekee tarvittavat toimenpiteet madon tilan ollessa "poison".
        Päivittää tilaruudun.
        Pisteitä ja madon pituutta vähennetään kolmella. Madon vartalosta
        poistetaan viimeiset kolme alkiota.
        """
        self.__status_info.destroy()
        self.__status_info = Label(text=f"Oh no! You got poisoned :o",
                                   bg="red", width=30, height=3,
                                   relief="solid", font=("Arial", 13))
        self.__status_info.pack()
        self.__score -= 3
        self.update_score()
        self.__snake_length -= 3
        del self.__snake_body[-4:-1]

    def status_is_3xspeed(self):
        """
        Tekee tarvittavat toimenpiteet madon tilan ollessa "3xspeed".
        Tarkistaa, onko efektille annettu aikamääre (8 sec) täyttynyt ja jos
        on, tekee tarpeelliset muutokset.
        """
        if self.__timer_3x < 8:
            self.__move_interval = 33
        else:
            self.__move_interval = 100
            self.__status = None
            self.__timer_3x = 0

    def status_is_inverse(self):
        """
        Tekee tarvittavat toimenpiteet madon tilan ollessa "inverse turns".
        Päivittää tilaruudun.
        Tarkistaa, onko efektille annettu aikamääre (8 sec) täyttynyt ja jos
        on, tekee tarpeelliset muutokset.
        """
        self.__status_info.destroy()
        self.__status_info = Label(text=f"Be careful! Your turns are inverted"
                                        f"\nfor a while :s",
                                   bg="orange", width=30, height=3,
                                   relief="solid", font=("Arial", 13))
        self.__status_info.pack()

        if self.__time_from_any_effect > 8:
            self.__status = None
            self.__status_info.destroy()

    def status_is_invulnerability(self):
        """
        Tekee tarvittavat toimenpiteet madon tilan ollessa "invulnerability".
        Päivittää tilaruudun.
        Tarkistaa, onko efektille annettu aikamääre (10 sec) täyttynyt ja jos
        on, tekee tarpeelliset muutokset.
        """
        self.__status_info.destroy()
        self.__status_info = Label(text=f"You became invulnerable!( ಠ◡ಠ )\nBe"
                                        f" careful though:\nboost left for: "
                                   f"{(10.1-self.__timer_invulnerability):.1f}"
                                        f" seconds.",
                                   bg="purple", width=30, height=3,
                                   relief="solid", font=("Arial", 13))
        self.__status_info.pack()

        if self.__timer_invulnerability > 10:
            self.__status = None
            self.__status_info.destroy()
            self.__timer_invulnerability = 0

    def status_is_growth(self):
        """
        Tekee tarvittavat toimenpiteet madon tilan ollessa "extra growth"
        Päivittää tilaruudun.
        Tarkistaa, onko efektille annettu aikamääre (10 sec) täyttynyt ja jos
        on, tekee tarpeelliset muutokset.
        """
        self.__status_info.destroy()
        self.__status_info = Label(text=f"Powerup!\nNext apples you eat"
                                        f"\nwill make you grow double.",
                                   bg="purple", width=30, height=3,
                                   relief="solid", font=("Arial", 13))
        self.__status_info.pack()

        if self.__time_from_any_effect > 10:
            self.__status = None
            self.__status_info.destroy()

    def check_status(self):
        """
        Tarkistaa madon tilan. "poison" ei ole mahdollinen, jos mato on
        alle neljän pituinen. Kutsuu tarvittavia toimenpiteitä tekevää
        metodia sen mukaan, mikä madon tila on.
        """

        if self.__status == "poison":
            if self.__snake_length < 4:
                self.__status = "extra growth"
            else:
                self.status_is_poison()

        elif self.__status == "3xspeed":
            self.status_is_3xspeed()

        elif self.__status == "inverse turns":
            self.status_is_inverse()

        elif self.__status == "invulnerability":
            self.status_is_invulnerability()

        elif self.__status == "extra growth":
            self.status_is_growth()

    def check_direction(self):
        """
        Tarkistaa suunnan ja liikuttaa madon päätä sen mukaan.
        """

        if self.__direction == "Up":
            self.__snake_head_y -= 10
        elif self.__direction == "Down":
            self.__snake_head_y += 10
        elif self.__direction == "Left":
            self.__snake_head_x -= 10
        elif self.__direction == "Right":
            self.__snake_head_x += 10

    def check_winning_conditions(self):
        """
        Tarkistaa riittävätkö pisteet voittoon. Jos riittää, kutsuu
        "game_won" metodia.
        """
        if self.__score >= self.__score_to_win:
            self.game_won()

    def game_won(self):
        """
        Luo voittoilmoituksen ja resetoi pelin alkunäkymään.
        """
        self.__info.destroy()
        self.__info = Label(text=f"You won! Press any arrow key "
                                 f"to play again.", bg="green")
        self.__info.pack()

        self.reset_everything()
        time.sleep(0.35)

    def check_if_poison(self):
        """
        Tämä tarvitaan, koska madon liikkumistiheys on määritelty "poison"
        tilassa olevan 2500ms, jonka ansiosta käyttäjä ehtii reagoimaan ja
        lukemaan inforuudun. Tilan muuttaminen Noneen ansiosta tämä pidennetty
        aikaväli toistetaan vain kerran.
        """
        if self.__status == "poison":
            self.__status = None
            self.__status_info.destroy()

    def add_time_to_timers(self):
        """
        Lisää ajanseurantaa varten aikoja sen mukaan, missä tilassa mato on.
        Madon liikkumistiheys on 0.1 sec, jonka takia kaikissa muissa tiloissa
        paitsi "3xspeed" lisätään 0.1.
        """
        if self.__questionmark_collected is False and \
                self.__direction is not None:
            self.__time_from_any_effect += 0.1

        if self.__status == "3xspeed":
            # Tämä arvo lisäämällä tilan voimassaoloaika oli lähimpänä
            # haluttuja sekunteja, vaikka olettaisi arvon 0.033 toimivan
            # paremmin
            self.__timer_3x += 0.05

        if self.__status == "invulnerability":
            self.__timer_invulnerability += 0.1

    def move_snake_auto(self):
        """
        Sisältää kaikki tarvittavat metodit pelin toimintoja varten.
        Lopussa tämä metodi kutsuu uudestaan itseään tietyn aikavälin
        jälkeen riippuen madon tilasta.
        """

        # Muuttaa tilaksi None, jos se on "poison".
        self.check_if_poison()

        # Lisää ajastimeen aikaa
        self.add_time_to_timers()

        # Tarkistaa liikkumissuunnan ja liikuttaa matoa
        self.check_direction()

        # Poistaa aloitusnäkymästä ohjeen, kun mato on liikkeessä.
        if self.__direction is not None:
            self.__info.destroy()

        # Tarkistaa, osuuko mato omenaan ("extra growth" tilassa mato kasvaa
        # kahdella)
        self.check_if_apple_eaten()

        # Tarkistaa, riittävätkö pisteet voittoon
        self.check_winning_conditions()

        if self.__status != "invulnerability":
            # Tarkistetaan aina osumat seiniin ja itseensä
            self.check_collision_with_walls()
            self.check_collision_with_itself()
        else:
            # Haavoittumattomuus-statuksella tämä pitää toteuttaa toisin
            if self.__snake_head_x == 0:
                self.__snake_head_x += 390
            elif self.__snake_head_x == 400:
                self.__snake_head_x -= 390
            elif self.__snake_head_y == 400:
                self.__snake_head_y -= 390
            elif self.__snake_head_y == 0:
                self.__snake_head_y += 390

        # Tarkistaa, osuuko mato kysymysmerkkiin
        # Jos osuu niin mato saa uuden statuksen.
        self.check_questionmark()

        # Päivittää madon ruumiin koordinaatit
        self.__snake_body.append((self.__snake_head_x, self.__snake_head_y))

        # Pidetään madon pituus rajattuna.
        if len(self.__snake_body) > self.__snake_length:
            del self.__snake_body[0]

        # Päivittää pelialueen komponentit
        # (Mato, omena, kysymysmerkki, ruudukko)
        self.draw_game()

        # Tarkistaa tilan ja luo inforuudun sen mukaan.
        self.check_status()

        # Metodi kutsuu uudestaan itseään liikkumistiheyden määräämän aikavälin
        # jälkeen.
        if self.__status == "inverse turns":
            if self.__time_from_any_effect < 0.05:
                self.__window.after(2000, self.move_snake_auto)
            else:
                self.__window.after(self.__move_interval,
                                    self.move_snake_auto)
        elif self.__status == "poison":
            self.__window.after(2500, self.move_snake_auto)
        else:
            self.__window.after(self.__move_interval, self.move_snake_auto)

    def draw_game(self):
        """
        Päivittää pelialueelle madon, omenan,
        kysymysmerkin(jos ehdot täyttyvät) ja ruudukon.
        """
        # Tyhjentää pelialueelta kaiken uusia komponentteja varten.
        self.__canvas.delete("all")

        # Mato
        for segment in self.__snake_body:
            self.__canvas.create_rectangle(segment[0], segment[1],
                                           segment[0] + 10, segment[1] + 10,
                                           fill="green")
        # Omena
        self.__canvas.create_oval(self.__apple_x, self.__apple_y,
                                  self.__apple_x + 10, self.__apple_y + 10,
                                  fill="red")

        # Tarkistetaan, päivitetäänkö kysymysmerkki
        if self.__time_from_any_effect > \
                self.__time_for_questionmark_to_appear:

            self.__canvas.create_image(self.__questionmark_location,
                                       image=self.__questionmark_photo,
                                       anchor="nw")

        self.draw_grid()


def main():
    game = Snakegame(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    game.start_game()


if __name__ == "__main__":
    main()
