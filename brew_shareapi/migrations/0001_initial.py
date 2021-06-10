# Generated by Django 3.2.4 on 2021-06-10 20:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=50)),
                ('is_admin', models.BooleanField()),
                ('profile_image', models.ImageField(null=True, upload_to='user_pics/%Y/%m/%d')),
                ('current_coffee', models.CharField(blank=True, max_length=50)),
                ('current_brew_method', models.CharField(blank=True, max_length=50)),
                ('private', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BrewMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_image', models.ImageField(null=True, upload_to='coffee_pics/%Y/%m/%d')),
                ('website', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name': 'brewmethod',
                'verbose_name_plural': 'brewmethods',
            },
        ),
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coffee_image', models.ImageField(null=True, upload_to='coffee_pics/%Y/%m/%d')),
                ('roaster', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('process', models.CharField(max_length=50)),
                ('recommended_method', models.CharField(max_length=50)),
                ('tasting_notes', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='brew_shareapi.brewer')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grind_size', models.CharField(max_length=25)),
                ('title', models.CharField(max_length=50)),
                ('tasting_notes', models.CharField(max_length=50)),
                ('review', models.CharField(max_length=255)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('setup', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('water_temp', models.IntegerField()),
                ('water_volume', models.IntegerField()),
                ('private', models.BooleanField()),
                ('block', models.BooleanField()),
                ('recipe', models.BooleanField()),
                ('recommend', models.BooleanField()),
                ('coffee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='brew_shareapi.coffee')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='brew_shareapi.brewmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='RecommendRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('confirmer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='confirmer', to='brew_shareapi.brewer')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.entry')),
                ('recommender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='recommender', to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name': 'entryflag',
                'verbose_name_plural': 'entryflags',
            },
        ),
        migrations.CreateModel(
            name='RecipeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=255)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name': 'recipereview',
                'verbose_name_plural': 'recipereviews',
            },
        ),
        migrations.CreateModel(
            name='FavoriteEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name': 'favoriteentry',
                'verbose_name_plural': 'favoriteentries',
            },
        ),
        migrations.CreateModel(
            name='EntryStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_image', models.ImageField(null=True, upload_to='coffee_pics/%Y/%m/%d')),
                ('descriptor', models.CharField(max_length=30)),
                ('instruction', models.CharField(max_length=255)),
                ('seconds', models.IntegerField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.entry')),
            ],
        ),
        migrations.CreateModel(
            name='EntryFlag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='admin', to='brew_shareapi.brewer')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brew_shareapi.entry')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reporter', to='brew_shareapi.brewer')),
            ],
            options={
                'verbose_name': 'entryflag',
                'verbose_name_plural': 'entryflags',
            },
        ),
    ]
