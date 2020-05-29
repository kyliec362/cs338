import requests
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


DISCOVERY_URL = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')

google_sentiment_service = ""

def get_news_for_stock(stock):
    query = 'q=' + stock + '&'
    NEWS_URL = ('http://newsapi.org/v2/everything?'
                + query +
                'from=2020-05-21&'
                'sortBy=popularity&'
                'apiKey=fae0fb9f9ec04ab7a007c4dd3b1ea220')
    response = requests.get(NEWS_URL)
    return response.json()

def print_news_result_descriptions(stock):
    articles = get_news_for_stock(stock)['articles']
    for article in articles:
        print(article['description'])

def get_sentiment(text, google_sentiment_service):
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Description: {}'.format(text))
    print('Sentiment score: {}, magnitude: {}'.format(sentiment.score, sentiment.magnitude))


def get_article_sentiments():
    # google_sentiment_service = initialize_google_sentiment_service()
    articles = get_news_for_stock("$tsla")['articles']
    for article in articles:
        get_sentiment(article['description'], google_sentiment_service)

if __name__ == '__main__':
    get_article_sentiments()
