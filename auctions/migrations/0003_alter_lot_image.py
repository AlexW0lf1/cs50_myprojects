# Generated by Django 4.1.5 on 2023-02-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_lot_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='image',
            field=models.ImageField(blank=True, upload_to='auctions/static/images/'),
        ),
    ]