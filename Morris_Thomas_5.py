def setup(): #apologies i could not generate a requirements.txt i spent hours trying but couldnt manage it inside jupyter or mac os terminal 

  import json #add all the relevant libraries
  from urllib.request import urlopen #to open the urls
  import requests
  from bs4 import BeautifulSoup #needed for parsing HTML
  import spacy #used for NLP
  from spacy import displacy #useful for jupyter
  import en_core_web_sm #small english trained model
  nlp = en_core_web_sm.load() #load this model as the nlp
  
def bbc_scraper(url):
    
  information = {} #set up empty dictionary to store data before saving as .json 
  information['Url Data'] = [] 

  html = urlopen(url)
  soup = BeautifulSoup(html, 'html.parser') #create a soup from the given url
  type(soup)
  url_location = soup.find('link', rel="canonical")
  url_name = url_location['href'] #get the url name from the soup (not needed as given but just for show)
  title = soup.title.text #only the text from the title        
  date_div = soup.find('div', class_='date date--v2') #this is where the article date stamp is
  date = date_div['data-datetime'] #specifically grab the date
    
  for span_tag in soup.findAll('span'): #remove the extra data which .text does not remove. More could be added if needed.
    span_tag.replace_with('')
  for scrip in soup.findAll('script'):
    scrip.replace_with('')   
  for lis in soup.findAll('li'): #remove the linked articles inside lists
    lis.replace_with('') 
  for anchor in soup.findAll('a'): #this was to get rid of some 'Reporter' and other random text
    anchor.replace_with('') 

  main_body = soup.find('div', class_='story-body__inner').text #now get the text after it has been cleaned up
      
  information['Url Data'].append({ #append the info from the url to the dictionary
      'Url': url_name,
      'Title': soup.title.text,
      'Date': date,
      'Contents': main_body
      })

  results_json = json.dumps(information, indent=4) #create a json object and make it more legible

  return results_json


def extract_entities(string):

  PERSON = [] #empty lists to hold entities before adding to dictionary
  ORG = []
  GPE = []

  doc = nlp(string) #pass the variable name from the function
  for word in doc.ents:
    if word.label_=='PERSON': #if the world label matches the required one then add it to the appropriate list
      tidy = str(word.text)
      tidy = tidy.replace('\\n'," ") #spacy fails to tidy up some of this so this was added to delete unwanted 
      tidy = tidy.replace('\\"'," ") #(cont) characters from the words and applied to all 3 labels
      tidy = tidy.replace('\\'," ")
      PERSON.append(tidy)
      PERSON = list(dict.fromkeys(PERSON))
    if word.label_=='ORG': #Organisations
      tidy = str(word.text)
      tidy = tidy.replace('\\n'," ")
      tidy = tidy.replace('\\"'," ")
      tidy = tidy.replace('\\'," ")
      ORG.append(tidy)
      ORG = list(dict.fromkeys(ORG))
    if word.label_=='GPE': #Places
      tidy = str(word.text)
      tidy = tidy.replace('\\n'," ")
      tidy = tidy.replace('\\"'," ")
      tidy = tidy.replace('\\'," ")
      GPE.append(tidy)
      GPE = list(dict.fromkeys(GPE))

  Processed_Data = { #dictionary to hold the processed entities 
    'People': PERSON,
    'Organisations': ORG,
    'Places': GPE }

  entities_json = json.dumps(Processed_Data, indent=4) #save dictionary to a json object and make it prettier

  return entities_json