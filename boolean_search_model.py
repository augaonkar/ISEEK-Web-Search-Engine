from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from collections import defaultdict

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
#en_stop = get_stop_words('en')
en_stop=set(stopwords.words('english'))
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health." 

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

inverted_index=defaultdict()
for i in range (0,len(texts)):
    for j in range(len(texts[i])):
        #print (texts[i][j])
        inverted_index.setdefault(texts[i][j],set())
        if i not in inverted_index[texts[i][j]]:
            inverted_index[texts[i][j]].add(i)
print (inverted_index)

def query_handler():
    print("enter your query")
    query=input()
    result=set()
    print("Your query is:",query)
    query_tokens = tokenizer.tokenize(query)
    #for i in range(0,len(query_tokens)):
    flag = 0
    for i in range(0,len(query_tokens),+1):
        print(len(query_tokens))
        if "and" in query_tokens:
            if query_tokens[i] in inverted_index.keys():
                if flag==0 and (i!=len(query_tokens)-1):
                    result=inverted_index[query_tokens[i]]
                    flag=1
                result=inverted_index[query_tokens[i]].intersection(result)
        if "or" in query_tokens:
            if query_tokens[i] in inverted_index.keys():
                result=inverted_index[query_tokens[i]].union(result)
    print(result)
        
query_handler()
    
