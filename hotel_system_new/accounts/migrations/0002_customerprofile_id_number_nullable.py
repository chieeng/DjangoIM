from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='id_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
