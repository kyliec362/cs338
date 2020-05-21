from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import requests

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

def initialize_google_sentiment_service():
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])

    credentials.authorize(http)

    google_sentiment_service = discovery.build('language', 'v1beta1',
                              http=http, discoveryServiceUrl=DISCOVERY_URL)

    return google_sentiment_service

def get_sentiment(text, google_sentiment_service):
    service_request = google_sentiment_service.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text,
            }
        })
    response = service_request.execute()
    polarity = response['documentSentiment']['polarity']
    magnitude = response['documentSentiment']['magnitude']
    print('Description: ', text)
    print('Sentiment: polarity of %s with magnitude of %s \n' % (polarity, magnitude))

def get_article_sentiments():
    google_sentiment_service = initialize_google_sentiment_service()
    articles = get_news_for_stock("$tsla")['articles']
    for article in articles:
        get_sentiment(article['description'], google_sentiment_service)

if __name__ == '__main__':
    get_article_sentiments()
