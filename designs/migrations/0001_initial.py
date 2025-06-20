# Generated by Django 5.2.2 on 2025-06-07 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nome da Categoria')),
                ('slug', models.SlugField(help_text='Versão do nome otimizada para URLs.', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nome da Cor')),
                ('hex_code', models.CharField(help_text='Código Hexadecimal da cor. Ex: #FF5733', max_length=7, unique=True, verbose_name='Código Hex')),
            ],
            options={
                'verbose_name': 'Cor',
                'verbose_name_plural': 'Cores',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Design')),
                ('image', models.ImageField(upload_to='designs/', verbose_name='Imagem Principal')),
                ('available_variations', models.ManyToManyField(help_text='Selecione as variações de produto que podem ser usadas com este design.', related_name='designs', to='products.productvariation', verbose_name='Variações de Produto Disponíveis')),
                ('categories', models.ManyToManyField(related_name='designs', to='designs.category', verbose_name='Categorias')),
                ('colors', models.ManyToManyField(blank=True, related_name='designs', to='designs.color', verbose_name='Cores')),
            ],
            options={
                'verbose_name': 'Design',
                'verbose_name_plural': 'Designs',
            },
        ),
    ]
