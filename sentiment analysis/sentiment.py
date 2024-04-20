from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Sentiment analysis using RoBERTa model from HuggingFace
MODEL = 'cardiffnlp/twitter-roberta-base-sentiment'
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)