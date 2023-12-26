from django.db import models
from django.db import models
from Game_app.models import GameMaker, device_frant
# Create your models here.

#    def __str__(self):
#     return f'{self.Game} {self.device}'


class category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    category_description = models.TextField(max_length=254)
    category_image = models.ImageField(
        upload_to='category_images', max_length=200)
    category_icon_upload = models.FileField(
        upload_to='category_icons', max_length=500)
    category_icon_url = models.URLField(max_length=200)
    active = models.BooleanField(default=True)
    category_subtitle = models.CharField(max_length=100)
    notes = models.CharField(max_length=254)

    def __str__(self):
        return self.category_name


class store_frant(models.Model):
    Game = models.ForeignKey(GameMaker, on_delete=models.CASCADE,
                             default=None, blank=True, related_name='store_game')
    device = models.ForeignKey(device_frant, on_delete=models.CASCADE,
                               default=None, blank=True, related_name='store_divice')
    category = models.ForeignKey(category, on_delete=models.CASCADE)


class Storemap(models.Model):
    GAME_TYPE_CHOICES = [
        ('HTML', 'HTML '),
        ('Cloud', 'Cloud'),
        ('Native', 'Native'),
    ]

    Game = models.ForeignKey(GameMaker, on_delete=models.CASCADE, default=1)
    device = models.ForeignKey(
        device_frant, on_delete=models.CASCADE, default=None, blank=True)
    Game_type = models.CharField(
        max_length=10, choices=GAME_TYPE_CHOICES, default='HTML')
    is_active = models.BooleanField(default=True)
    Play_url = models.URLField(max_length=200)
    Image_icon = models.FileField(upload_to='Image_icons', max_length=500)
    Banner_Image = models.ImageField(upload_to='Banner_images', max_length=200)
    Game_version = models.IntegerField()
    Game_size = models.IntegerField()
    Video_url = models.URLField(max_length=200)
    create_at = models.DateField(auto_now_add=False)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.Game} {self.device} {self.Game_type}'


class storefrontcategoryMapping(models.Model):
    id = models.AutoField(primary_key=True)
    storemap = models.ForeignKey(
        Storemap, on_delete=models.CASCADE, related_name="sfcategory")
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=False)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.storemap} {self.category}'


# ye mobile es modal ka he
class Make_and_Models(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.make}-{self.model}'


# ye game es modal pr khela ja skta he
class make_and_Models_mapping(models.Model):
    id = models.AutoField(primary_key=True)
    Game = models.ForeignKey(GameMaker, on_delete=models.CASCADE, default=1)
    Make_and_modle = models.ForeignKey(
        Make_and_Models, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.Make_and_modle)

# Create your models here.
