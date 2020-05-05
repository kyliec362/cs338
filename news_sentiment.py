from google.cloud.language import enums
from google.cloud.language import types
import requests
bing_key = "24f21c96abbf401bac1b357a27840706"

def bing_query(query):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    for result in search_results['news']['value']:
        print(result['description'])


#TODO make working
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

#TODO make workiing
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
