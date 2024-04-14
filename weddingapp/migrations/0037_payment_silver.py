# Generated by Django 4.2.2 on 2024-04-13 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weddingapp', '0036_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_silver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('date_of_booking', models.DateField()),
                ('destination_selected', models.CharField(max_length=255)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('silver_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weddingapp.silverpackage')),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
