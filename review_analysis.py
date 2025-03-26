import json

positive_words = ['good','best', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'positive', 'happy', 'love']
negative_words = ['bad','risk', 'terrible', 'awful', 'horrible', 'negative', 'sad', 'hate', 'poor']

def analyze_sentiment(text):
    words = text.lower().split()
    
    positive_score = 0
    negative_score = 0
    
    for word in words:
        if word in positive_words:
            positive_score += 1
        elif word in negative_words:
            negative_score += 1
    
    if positive_score > negative_score:
        return 'positive'
    elif negative_score > positive_score:
        return 'negative'
    else:
        return 'neutral'

with open('merged_products.json', 'r') as file:
    data = json.load(file)

for product in data:
    reviews = product['reviews'].split(' | ')
    product['reviews'] = []
    for review_text in reviews:
        sentiment_label = analyze_sentiment(review_text)
        product['reviews'].append({'text': review_text, 'sentiment': sentiment_label})

with open('review_analysis.json', 'w') as file:
    json.dump(data, file, indent=4)
