from django.db import models



class SignatureManager(models.Manager):
    def differential(self, ratio, pvalue):
        result = []
        signatures = self.models.objects.get.all()
        for signature in signatures:
            result.append(self.models.objects.differential(ratio, pvalue))# Might a good function for a custom manager.
        return result
