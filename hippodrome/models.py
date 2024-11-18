from django.db import models

# Modèle pour représenter un jockey
class Jockey(models.Model):
    name = models.CharField(max_length=100)  # Nom du jockey
    age = models.PositiveIntegerField()  # Âge du jockey
    experience = models.PositiveIntegerField(help_text="Expérience en années")  # Années d'expérience
    photo = models.ImageField(upload_to='jockeys/', blank=True, null=True)  # Photo du jockey

    def __str__(self):
        return self.name

class Ecurie(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    max_chevaux = models.PositiveIntegerField(default=10)
    logo = models.ImageField(upload_to='ecurie_logo/', blank=True, null=True)

    def __str__(self):
        return self.name

# Modèle pour représenter un cheval
class Cheval(models.Model):
    name = models.CharField(max_length=100)  # Nom du cheval
    age = models.PositiveIntegerField()  # Âge du cheval
    race_type = models.CharField(
        max_length=50,
        choices=[
            ('Sprint', 'Sprint'),
            ('Obstacle', 'Obstacle'),
            ('Endurance', 'Endurance'),
        ]
    )
    jockey = models.ForeignKey(
        Jockey, on_delete=models.SET_NULL, null=True, blank=True
    )
    ecurie = models.ForeignKey(Ecurie, on_delete=models.SET_NULL, null=True, blank=True, related_name='chevaux')
    photo = models.ImageField(upload_to='chevaux/', blank=True, null=True)  # Photo du cheval

    def __str__(self):
        return f"{self.name} ({self.race_type})"

# Modèle pour représenter une course
class Course(models.Model):
    name = models.CharField(max_length=100)  # Nom de la course
    date = models.DateTimeField()  # Date et heure de la course
    location = models.CharField(max_length=200)  # Lieu de la course
    chevaux = models.ManyToManyField(Cheval, related_name="courses")  # Chevaux participant à la course

    def __str__(self):
        return self.name  # Affiche le nom dans les listes


class Zone(models.Model):
    ZONE_TYPES = [
        ('Nettoyage', 'Nettoyage'),
        ('Soins Médicaux', 'Soins Médicaux'),
        ('Entraînement', 'Entraînement'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ZONE_TYPES)
    cheval = models.OneToOneField(Cheval, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='image_zone/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

    def is_occupied(self):
        return self.cheval is not None