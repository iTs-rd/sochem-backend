# Generated by Django 3.1.2 on 2020-11-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0015_auto_20201107_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumcomment',
            name='comment',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='forumpost',
            name='heading',
            field=models.CharField(max_length=500),
        ),
    ]
