from django.db import models
from django.contrib.postgres import search
from pgvector.django import VectorField
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance

T = SentenceTransformer("distiluse-base-multilingual-cased-v1") # 539M download from huggingface

class Item(models.Model):
    content = models.TextField()
    price = models.IntegerField(db_default=10)
    in_stock = models.BooleanField(db_default=True)

    # SQL:
    # ADD COLUMN "vector" tsvector GENERATED ALWAYS AS (
    # to_tsvector('english'::regconfig, COALESCE("content", ''))
    # ) STORED;
    vector = models.GeneratedField(
        db_persist=True,
        expression=search.SearchVector("content", config="english"),
        output_field=search.SearchVectorField()
    )

    # SQL:
    # ADD COLUMN "embedding" vector(512)
    embedding = VectorField(dimensions=512, editable=False,
                            null=True # this was needed for the initial migration
                            )

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
      self.embedding = T.encode(self.content)
      super().save(*args, **kwargs)

    @classmethod
    def search(cls, q, dmax=0.5):
      distance = CosineDistance("embedding", T.encode(q)) # SQL: <=> operator
      return (
        cls.objects.alias(distance=distance)
        .filter(distance__lt=dmax)
        .order_by(distance)
      )