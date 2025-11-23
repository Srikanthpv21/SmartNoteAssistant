from django.db import models

class SummaryHistory(models.Model):
    original_text = models.TextField()
    summary_text = models.TextField()
    tone = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary created on {self.created_at.strftime('%Y-%m-%d %H:%M')}"