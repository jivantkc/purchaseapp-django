from django.db import migrations

def rename_column(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "ALTER TABLE payroll_fixedexpense CHANGE expensecategory_id category_id INTEGER;"
        )

class Migration(migrations.Migration):
    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(rename_column),
    ]