# Generated by Django 4.2 on 2024-10-13 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Candidates", "0002_alter_candidate_id"),
        ("JobOffers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="joboffer",
            name="Id",
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "Id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Candidates.candidate",
                    ),
                ),
                (
                    "jobOffer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="JobOffers.joboffer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "Id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Candidates.candidate",
                    ),
                ),
                (
                    "jobOffer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="JobOffers.joboffer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="joboffer",
            name="candidate_application",
            field=models.ManyToManyField(
                related_name="applications",
                through="JobOffers.Application",
                to="Candidates.candidate",
            ),
        ),
        migrations.AddField(
            model_name="joboffer",
            name="candidate_match",
            field=models.ManyToManyField(
                related_name="matches",
                through="JobOffers.Match",
                to="Candidates.candidate",
            ),
        ),
    ]
