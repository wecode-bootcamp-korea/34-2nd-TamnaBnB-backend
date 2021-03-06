# Generated by Django 4.0.6 on 2022-07-06 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review_img',
            new_name='image_url',
        ),
        migrations.AlterField(
            model_name='review',
            name='ratings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
