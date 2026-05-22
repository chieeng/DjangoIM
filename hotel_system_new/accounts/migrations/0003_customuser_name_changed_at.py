from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customerprofile_id_number_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name_changed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
