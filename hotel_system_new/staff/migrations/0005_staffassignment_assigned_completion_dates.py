import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_remove_staffassignment_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffassignment',
            name='assigned_date',
            field=models.DateField(default=datetime.date(2026, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffassignment',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
