# Generated by Django 4.2.7 on 2025-07-24 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('content', '0006_alter_searchlinks_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchlinks',
            name='title',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='search_links_title', to='translations.translation', verbose_name='Título'),
            preserve_default=False,
        ),
    ]
