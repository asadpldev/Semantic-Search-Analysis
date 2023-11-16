from django.db import models
from accounts.models import User
from accounts.mixins import TimeStampMixin
from django.db.models import Avg
from django.db.models import Count, Case, When, Value, CharField, F
class TVShow(TimeStampMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()

    def get_sentiments(self):
        #  Assuming 'self' refers to a specific TVShow instance
        tv_show_sentiment_analysis = SentimentAnalysis.objects.filter(tv_show=self).aggregate(
            positive_count=Count(
                Case(
                    When(analysis='Positive', then=Value(1)),
                    default=None,
                    output_field=CharField()
                )
            ),
            negative_count=Count(
                Case(
                    When(analysis='Negative', then=Value(1)),
                    default=None,
                    output_field=CharField()
                )
            ),
            neutral_count=Count(
                Case(
                    When(analysis='Neutral', then=Value(1)),
                    default=None,
                    output_field=CharField()
                )
            )
        )

        # Calculate the total counts
        total_counts = tv_show_sentiment_analysis['positive_count'] + tv_show_sentiment_analysis['negative_count'] + tv_show_sentiment_analysis['neutral_count']

        # Calculate the percentages
        positive_percentage = tv_show_sentiment_analysis['positive_count'] / total_counts if total_counts > 0 else 0
        negative_percentage = tv_show_sentiment_analysis['negative_count'] / total_counts if total_counts > 0 else 0
        neutral_percentage = tv_show_sentiment_analysis['neutral_count'] / total_counts if total_counts > 0 else 0

        # Determine the majority sentiment
        if positive_percentage > negative_percentage and positive_percentage > neutral_percentage:
            majority_sentiment = 'Positive'
        elif negative_percentage > positive_percentage and negative_percentage > neutral_percentage:
            majority_sentiment = 'Negative'
        else:
            majority_sentiment = 'Neutral'

        print(f"TV Show Sentiment Analysis - Majority Sentiment: {majority_sentiment}")
        return majority_sentiment
    
class Comment(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    comment_text = models.TextField()

class SentimentAnalysis(TimeStampMixin):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE,blank= True,null=True)
    comment_text = models.ForeignKey(Comment, on_delete=models.CASCADE)
    analysis = models.CharField(max_length=100)
    
