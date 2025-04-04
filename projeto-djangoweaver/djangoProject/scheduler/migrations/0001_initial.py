# Generated by Django 5.1.1 on 2024-10-15 10:07

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import scheduler.models
import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, unique=True)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('delivery', models.CharField(choices=[('PERIODIC', 'Periodic'), ('REQUEST', 'On Request')], max_length=200)),
                ('email_text', models.CharField(blank=True, default='', max_length=2000, null=True)),
                ('endpoint', models.URLField()),
                ('delivery_endpoint', models.CharField(blank=True, help_text="Optional: Should be set for 'On Request' delivery type. Provides a callable internal endpoint. Ex.: 'https://www.(domain).com/services/api/(delivery_endpoint)/", max_length=20, null=True, unique=True)),
                ('last_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('input_data_type', models.CharField(choices=[('JSON', 'JSON'), ('XML', 'XML'), ('CSV', 'CSV'), ('TEXT', 'Text')], max_length=200)),
                ('output_type', models.CharField(choices=[('JSON', 'JSON'), ('XML', 'XML'), ('HTML', 'HTML'), ('EMAIL', 'Email'), ('PDF', 'PDF'), ('EMAIL_ATTACHMENT', 'Email w/ attachment')], max_length=200)),
                ('pdf_transformer', models.CharField(choices=[('default', 'Default'), ('pae', 'PAE')], default='default', max_length=10)),
                ('pdf_template', models.FileField(blank=True, help_text="Optional: PDF file to serve as template for the data output. 'Output Type' must be PDF, should only contain 1 page.", null=True, storage=scheduler.models.OverwriteStorage(), upload_to=scheduler.models.upload_location, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('cron_update_interval', models.CharField(blank=True, default='* * * * *', help_text="Here you can specify an interval for updates, following the use of Cron expressions, valid examples are '* 12 * * ?', or '* * L * *'.", max_length=100, null=True, validators=[utils.validators.validate_crontab])),
                ('archive_time', models.DurationField(default=datetime.timedelta(days=30), help_text="This field specifies for how long data should be kept. Ex.: '30 00:00:00' corresponds to 30 days, following the time representation D HH:MM:SS.")),
                ('mapping', models.JSONField(blank=True, default=scheduler.models.get_default_mapping, help_text='This mapping relates the response from this Service the possible outputs, letting you customize the output.', null=True, validators=[scheduler.models.validate_mapping])),
                ('response_mapping', models.TextField(blank=True, help_text='placeholder', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authentication_handler', models.CharField(choices=[('DEFAULT', 'Default'), ('PAE', 'PAE')], default='default', max_length=10)),
                ('authentication_type', models.CharField(choices=[('NONE', 'No Auth'), ('BASIC', 'Basic Auth'), ('TOKEN', 'Basic PAEToken'), ('DIGEST', 'Digest Auth'), ('OAUTH1', 'OAuth 1.0'), ('OAUTH2', 'OAuth 2.0')], default='NONE', max_length=20)),
                ('auth_user', models.CharField(blank=True, help_text='Basic Auth + Digest Auth', max_length=255, null=True)),
                ('auth_pass', models.CharField(blank=True, help_text='Basic Auth + Digest Auth', max_length=255, null=True)),
                ('auth_token', models.CharField(blank=True, help_text='Basic PAEToken Auth', max_length=255, null=True)),
                ('client_key', models.CharField(blank=True, help_text='OAuth 1.0', max_length=255, null=True)),
                ('resource_owner_key', models.CharField(blank=True, help_text='OAuth 1.0', max_length=255, null=True)),
                ('resource_owner_secret', models.CharField(blank=True, help_text='OAuth 1.0', max_length=255, null=True)),
                ('client_id', models.CharField(blank=True, help_text='OAuth 2.0', max_length=100, null=True)),
                ('client_secret', models.CharField(blank=True, help_text='OAuth 1.0 + OAuth 2.0', max_length=100, null=True)),
                ('access_token_url', models.CharField(blank=True, help_text='OAuth 2.0', max_length=100, null=True)),
                ('redirect_uri', models.CharField(blank=True, help_text='OAuth 2.0', max_length=100, null=True)),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheduler.service')),
            ],
        ),
    ]
