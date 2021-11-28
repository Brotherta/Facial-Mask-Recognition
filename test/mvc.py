PRICE_PER_SONG = 1.20


# MODELS

class Song:
    """Modèle représentant un son."""

    def __init__(self, name, artist, genre, artwork):
        """Initialise les détails relatifs au son."""
        self.artist = artist
        self.name = name
        self.genre = genre
        self.artwork = artwork


class Library:
    """Modèle qui stocke les sons."""

    def __init__(self):
        """Initialise une liste de sons."""
        self.songs = []


class ServiceInfo:
    """Modèle qui gère la maintenance de la jukebox."""

    def __init__(self, status, engineer_name):
        """Initialise les détails du service."""
        self.status = status
        self.engineer = engineer_name


# VIEW
class Touchscreen:
    """Vue qui gère l'interface de la jukebox."""

    def select_song(self):
        """Sélectionne un son."""
        pass

    def prompt_for_next_song(self, songs):
        """Demande un nouveau son."""
        for song in songs:
            # affiche les sons
            pass
        return "Dark Chest of Wonders"


class Speakers:
    """Vue qui gère le son."""

    def __init__(self):
        """Initialise le volume."""
        self.volume = 5

    def get_louder(self):
        """Augmente le volume."""
        self.volume += 1

    def get_quieter(self):
        """Baisse le volume."""
        self.volume -= 1

    def play_song(self, song):
        """Joue la musique."""
        pass


class CoinSlot:
    """Vue qui gère la reception de l'argent."""

    def __init__(self, amount):
        """Initialise le montant."""
        self.amount = amount

    def request_money(self, amount):
        """Attend un montant de l'utilisateur."""
        # attend l'argent
        # donne le change
        self.amount += amount
        return True


# CONTROLLERS

class Controller:
    """Contrôleur principal."""

    def __init__(self):
        """Initialise les modèles et les vues."""
        self.bank = CoinSlot()
        self.library = Library()
        self.service_history = []

        self.ui = Touchscreen()
        self.audio_output = Speakers()

    def play_next_song(self):
        """Joue le prochain son."""
        songs_to_suggest = []
        for song in self.library:
            # filter logic
            songs_to_suggest.append(song)

        chosen_song = self.ui.prompt_for_next_song(songs_to_suggest)
        self.bank.request_money(PRICE_PER_SONG)
        self.audio_output.play_song(chosen_song)

    # Beaucoup plus de méthodes ici...
