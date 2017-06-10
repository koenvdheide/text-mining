# CoTextThen

### What we need to do:
* inserting the data in the database
* PYTHON: script to retrieve conditions + organisms + genes and convert this to a JSON (INCLUDING size = x)
* JAVASCRIPT: script that will execute the above script and uses the JSON to build the sunburst and tree.
* PYTHON: script that retrieves gene info, organism info or condition info based on the gene name, organism name and condtion name, respectively. 
* JAVASCRIPT that executes the above code when the user clicks on a certain item in the sunburst/tree to show more information.


### What you need:
* [BioPython](https://github.com/biopython/biopython)
*  [nltk](https://github.com/nltk/nltk) 
* [RetinaSDK](https://github.com/cortical-io/retina-sdk.py) 
* [BioC](https://github.com/2mh/PyBioC) 

For nltk to work properly the following code should be executed to download the "english" data:
```python
import nltk
nltk.download()
```



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


