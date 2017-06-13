# CoTextThen
*made by Rick Beeloo, Koen van der Heide en Thomas Reinders*

### What you need:
* [BioPython](https://github.com/biopython/biopython)
*  [nltk](https://github.com/nltk/nltk) 
* [RetinaSDK](https://github.com/cortical-io/retina-sdk.py) 
* [BioC](https://github.com/yfpeng/bioc.git) (make sure to download this one from github ```pip install git+https://github.com/yfpeng/bioc.git```, oterwhise this won't work because the ```pip install bioc``` version is outdated.)


For nltk to work properly the following code should be executed to download the "english" data:
```python
import nltk
nltk.download()
```
### How to see results without the usage of the database?
Go to ```python main.py```
Comment out the database usages:
```from SQLConnector import SQLConnector```
```sqlconnect = SQLConnector(database='motor')```
And replace the insert call with a print call, so change:
```sqlconnect.insert_article(anno_article.to_dict())``` 
to:
```print(anno_article.to_dict())``` 
This will simply print something like this:
```python
{'Article': {'pubmed_id': '28550605', 'title': 'High-throughput SNP genotyping of modern and wild emmer wheat for yield and root morphology using a combined association and linkage analysis.', 'authors': ['Lucas SJ', 'Salantur A', 'Yazar S', 'Budak H']}, 'Gene': [], 'Organism': [{'taxonomy_id': '4565', 'name': 'Triticum aestivum', 'common_name': 'bread wheat', 'genus': 'Triticum'}, {'taxonomy_id': '4565', 'name': 'Triticum aestivum', 'common_name': 'bread wheat', 'genus': 'Triticum'}, {'taxonomy_id': '4565', 'name': 'Triticum aestivum', 'common_name': 'bread wheat', 'genus': 'Triticum'}, {'taxonomy_id': None, 'name': None, 'common_name': None, 'genus': None}], 'Condition': [{'name': '(1) stress', 'sentence': 'Using a combined linkage and association mapping approach, we generated a genetic map including 1345 SNP markers, and identified markers linked to 6 QTLs for coleoptile length (2), heading date (1), anthocyanin accumulation (1) and osmotic stress tolerance (2).', 'score': 0.573170731707317}, {'name': 'osmotic stress', 'sentence': 'Using a combined linkage and association mapping approach, we generated a genetic map including 1345 SNP markers, and identified markers linked to 6 QTLs for coleoptile length (2), heading date (1), anthocyanin accumulation (1) and osmotic stress tolerance (2).', 'score': 0.573170731707317}]}
```
Of course this could be printed more cleary by using the keys in the dictionary, e.g.: ```print(anno_article.to_dict()['Article']['title'])``` etc. 


### How it works  
Our application consist of five main parts:
* PubMed querying ([BioPython](https://github.com/biopython/biopython))
* Condition recognition
* Gene/Species extraction ([PubTator API](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/#RESTfulIntroduction))
* Data merge
* Database saving
* Data visualisation (see ``` tutorial.html``` for more details)


### Limitatons
**condition recognition**   
We have trained our CondtionSearcher using ~100 sentences, however this should be expanded much further in the futre. Further we didn't include a negative model (i.e. conditions in a certain context which should't be found)

**Gene/Species extraction**  
For this recognition we complelety rely on the ([PubTator API](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/#RESTfulIntroduction)). We have checked the articles, which are of our interest, on their quality and availablity. The quality is quite good, however some articles aren't annotated and therefore we miss some articles. We could overcome this using our own wirtten modules, but this will probably introduce false positives. 

### Experiencing problems?
 Call ```112``` 


