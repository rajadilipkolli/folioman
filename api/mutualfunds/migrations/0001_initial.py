# Generated by Django 3.1.7 on 2021-04-02 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AMC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name': 'AMC',
                'verbose_name_plural': 'AMCs',
            },
        ),
        migrations.CreateModel(
            name='Folio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128, unique=True)),
                ('pan', models.CharField(blank=True, max_length=10, null=True)),
                ('kyc', models.BooleanField(default=False)),
                ('pan_kyc', models.BooleanField(default=False)),
                ('amc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mutualfunds.amc')),
            ],
        ),
        migrations.CreateModel(
            name='FolioScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=3, max_digits=20)),
                ('balance_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutualfunds.folio')),
            ],
        ),
        migrations.CreateModel(
            name='FundCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('EQUITY', 'Equity'), ('DEBT', 'Debt'), ('HYBRID', 'Hybrid'), ('OTHER', 'Other')], default='EQUITY', max_length=8)),
                ('subtype', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'FundCategory',
                'verbose_name_plural': 'Fund Categories',
            },
        ),
        migrations.CreateModel(
            name='FundScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('rta', models.CharField(blank=True, max_length=12, null=True)),
                ('plan', models.CharField(choices=[('REGULAR', 'Regular'), ('DIRECT', 'Direct')], default='REGULAR', max_length=8)),
                ('rta_code', models.CharField(max_length=32)),
                ('amc_code', models.CharField(db_index=True, max_length=32)),
                ('amfi_code', models.CharField(blank=True, db_index=True, max_length=8, null=True)),
                ('isin', models.CharField(db_index=True, max_length=16)),
                ('start_date', models.DateField(blank=True, db_index=True, null=True)),
                ('end_date', models.DateField(blank=True, db_index=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('amc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funds', to='mutualfunds.amc')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='funds', to='mutualfunds.fundcategory')),
            ],
            options={
                'verbose_name': 'Fund Scheme',
                'verbose_name_plural': 'Fund Schemes',
                'index_together': {('amc_id', 'rta_code'), ('rta', 'rta_code')},
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pan', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('order_type', models.CharField(choices=[('Buy', 'Buy'), ('Reinvest', 'Reinvest'), ('Redeem', 'Redeem'), ('Switch', 'Switch')], max_length=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('nav', models.DecimalField(decimal_places=4, max_digits=15)),
                ('units', models.DecimalField(decimal_places=3, max_digits=20)),
                ('invested', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('balance', models.DecimalField(decimal_places=3, max_digits=40)),
                ('avg_nav', models.DecimalField(decimal_places=8, default=0, max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='mutualfunds.folioscheme')),
            ],
        ),
        migrations.AddField(
            model_name='folioscheme',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mutualfunds.fundscheme'),
        ),
        migrations.AddField(
            model_name='folio',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folios', to='mutualfunds.portfolio'),
        ),
        migrations.CreateModel(
            name='SchemeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('invested', models.DecimalField(decimal_places=2, max_digits=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=30)),
                ('avg_nav', models.DecimalField(decimal_places=10, default=0.0, max_digits=30)),
                ('nav', models.DecimalField(decimal_places=4, max_digits=15)),
                ('balance', models.DecimalField(decimal_places=3, max_digits=20)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='mutualfunds.folioscheme')),
            ],
            options={
                'unique_together': {('scheme_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='PortfolioValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('invested', models.DecimalField(decimal_places=2, max_digits=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=30)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='mutualfunds.portfolio')),
            ],
            options={
                'unique_together': {('portfolio_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='NAVHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('nav', models.DecimalField(decimal_places=4, max_digits=15)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutualfunds.fundscheme')),
            ],
            options={
                'unique_together': {('scheme_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='FolioValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('invested', models.DecimalField(decimal_places=2, max_digits=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=30)),
                ('folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='mutualfunds.folio')),
            ],
            options={
                'unique_together': {('folio_id', 'date')},
            },
        ),
    ]
