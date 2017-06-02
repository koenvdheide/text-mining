# CoTextThen

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


### The Name?
Cohen (a god) + Text + Go then = GoTexThen
```python
#python told us
>>>Cohen == God
True

```


