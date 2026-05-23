from django.db import migrations, models


def remove_duplicate_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    ServiceCategory = apps.get_model('services', 'ServiceCategory')

    for model, field, pk in (
        (ServiceCategory, 'category_name', 'service_category_id'),
        (Service, 'service_name', 'service_id'),
    ):
        seen = set()
        for row in model.objects.order_by(pk):
            key = getattr(row, field).strip().lower()
            if key in seen:
                row.delete()
            else:
                seen.add(key)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_services, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='servicecategory',
            name='category_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
