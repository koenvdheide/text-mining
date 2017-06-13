# CoTextThen


### What you need:
* [BioPython](https://github.com/biopython/biopython)
*  [nltk](https://github.com/nltk/nltk) 
* [RetinaSDK](https://github.com/cortical-io/retina-sdk.py) 
* [BioC](https://github.com/yfpeng/bioc.git) (make sure to download this one from github ```pip install git+https://github.com/yfpeng/bioc.git```, oterwhise this won't work because the ```pip install bioc``` version is outdated.)
* 

For nltk to work properly the following code should be executed to download the "english" data:
```python
import nltk
nltk.download()
```
### Printing some results?(Text-mining)
To view the results before saving them in the database, which happens in ```python main.py```: ```pythonsqlconnect.insert_article(anno_article.to_dict())``` the results could also be printed beforehand using ```print(anno_article.to_dict())```


### How it works  
Our application consist of five main parts:
* PubMed querying ([BioPython](https://github.com/biopython/biopython))
* Condition recognition
* Gene/Species extraction ([PubTator API](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/#RESTfulIntroduction))
* Data merge
* Database saving

### Code example
(Just for a nice lay-out)
```python
#let's search
    ids = NCBISearcher.search("anthocyanin","pubmed",50)
    annotated_articles = []
    for article in NCBISearcher.fetch_articles(ids):
        title = article.get("TI",None)
        abstract = article.get("AB", None)
        authors = article.get("AU",None)
        pmid = article.get("PMID",None)

```


### Limitatons
**condition recognition**   
We have trained our CondtionSearcher using ~100 sentences, however this should be expanded much further in the futre. Further we didn't include a negative model (i.e. conditions in a certain context which should't be found)

**Gene/Species extraction**  
For this recognition we complelety rely on the ([PubTator API](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/#RESTfulIntroduction)). We have checked the articles, which are of our interest, on their quality and availablity. The quality is quite good, however some articles aren't annotated and therefore we miss some articles. We could overcome this using our own wirtten modules, but this will probably introduce false positives. 




