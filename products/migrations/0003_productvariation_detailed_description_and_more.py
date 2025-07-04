# Generated by Django 5.2.2 on 2025-06-09 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_specification_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='detailed_description',
            field=models.TextField(blank=True, help_text='Explique em detalhes sobre o produto, papel, acabamentos, etc.', verbose_name='Descrição Detalhada'),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='video_url',
            field=models.URLField(blank=True, help_text="Cole aqui o link 'embed' do vídeo.", verbose_name='URL do Vídeo (YouTube, Vimeo)'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery/', verbose_name='Imagem')),
                ('alt_text', models.CharField(blank=True, max_length=255, verbose_name='Texto Alternativo (SEO)')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.productvariation', verbose_name='Variação de Produto')),
            ],
            options={
                'verbose_name': 'Imagem do Produto',
                'verbose_name_plural': 'Imagens do Produto',
            },
        ),
    ]
