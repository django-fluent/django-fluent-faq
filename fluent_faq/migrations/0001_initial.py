# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import fluent_faq.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_keywords', models.CharField(default=b'', help_text='When this field is not filled in, the the tags will be used.', max_length=255, verbose_name='keywords', blank=True)),
                ('meta_description', models.CharField(default=b'', help_text='When this field is not filled in, the contents or intro text will be used.', max_length=255, verbose_name='description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='last modification')),
                ('order', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent_site', models.ForeignKey(default=fluent_faq.models._get_current_site, editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('order', 'creation_date'),
                'verbose_name': 'FAQ Category',
                'verbose_name_plural': 'FAQ Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='fluent_faq.FaqCategory', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'fluent_faq_faqcategory_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'FAQ Category Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_keywords', models.CharField(default=b'', help_text='When this field is not filled in, the the tags will be used.', max_length=255, verbose_name='keywords', blank=True)),
                ('meta_description', models.CharField(default=b'', help_text='When this field is not filled in, the contents or intro text will be used.', max_length=255, verbose_name='description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='last modification')),
                ('order', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('category', models.ForeignKey(related_name='questions', verbose_name='Category', to='fluent_faq.FaqCategory')),
                ('parent_site', models.ForeignKey(default=fluent_faq.models._get_current_site, editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('order', 'creation_date'),
                'verbose_name': 'FAQ Question',
                'verbose_name_plural': 'FAQ Questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqQuestionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='fluent_faq.FaqQuestion', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'fluent_faq_faqquestion_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'FAQ Question Translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='faqquestiontranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='faqcategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
