# Generated by Django 2.1 on 2020-05-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0006_board_board_image_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply_info',
            name='apply_info_reg_date',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
