# Generated by Django 4.1.3 on 2023-04-17 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('limits', '0002_alter_limit_name'),
        ('abonents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonent',
            name='limit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='abonents', to='limits.limit', verbose_name='Ограничения'),
            preserve_default=False,
        ),
    ]