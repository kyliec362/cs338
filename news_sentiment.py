from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import requests
from azure.cognitiveservices.search.newssearch import NewsSearchClient
from msrest.authentication import CognitiveServicesCredentials
bing_key = "24f21c96abbf401bac1b357a27840706"
bing_client = NewsSearchClient(credentials=CognitiveServicesCredentials(bing_key), endpoint="https://cs338stockanalysis.cognitiveservices.azure.com/bing/v7.0")

#client = language.LanguageServiceClient.from_service_account_file('./key.json')

def old_bing_query(query):
    news_results = bing_client.news.search(query=query, market="en-us", count=5)
    if news_results.value:
        res = ""
        # return news_results.value[0].name
        for result in news_results.value[:5]:
            encoded_res = (result.name.encode('ascii', 'ignore').decode('ascii'))
            res += encoded_res + ". "
        return [res, news_results.value[:5]]
            # print("First news name: {}".format(result.name))
            # print("First news url: {}".format(result.url))
            # print("First news description: {}".format(result.description))

def bing_query(query):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    print(search_results)
    ##for result in search_results['news']:
      #  print(result['value']['description'])#['description'])

            
            
def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        print(sentence)
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0


def analyze(query):
    """Run a sentiment analysis request on text."""
    content, raw_news = bing_query(query)
    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    #annotations = client.analyze_sentiment(document=document)
    #return [annotations, raw_news]


if __name__ == '__main__':
    bing_query("$tsla")
