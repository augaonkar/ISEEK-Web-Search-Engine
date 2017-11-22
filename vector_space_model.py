"""
Descrption: Search engine to illustrate the vector space model for documents.
It asks you to enter a search query, and then returns all documents
matching the query, in decreasing order of cosine similarity,
according to the vector space model.
"""
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
from functools import reduce
import math
import sys
from functools import partial
from collections import deque
from nltk.corpus import stopwords
from prettytable import PrettyTable
import re
import os

# We use a corpus of four documents.  Each document has an id, and these are the keys in the following dict.  The values are the
# corresponding filenames.
filesList = [f for f in os.listdir('F:\CS-609-DMEW\Project\VSM-master\KThatte') if f.endswith('.rtf')]
corpus_files = {}
courpusCounter = 0
for fCounter in filesList:
 corpus_files[courpusCounter]= fCounter
 courpusCounter+=1

N = len(corpus_files)
# dictionary: a set to contain all terms (i.e., words) in the document corpus.
dictionary = set()
tokenizer = RegexpTokenizer(r'\w+')

# postings: a defaultdict whose keys are terms, and whose  corresponding values are the so-called "postings list" for that
# term, i.e., the list of documents the term appears in.

postings = defaultdict(dict)

# document_frequency: a defaultdict whose keys are terms, with corresponding values equal to the number of documents which contain key
document_frequency = defaultdict(int)

# length: a defaultdict whose keys are document ids, with values equal
# to the Euclidean length of the corresponding document vector.
length = defaultdict(float)

# The list of characters (mostly, punctuation) we want to strip out of
# terms in the document.
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

def main():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
   
    while True:
      do_search()


def initialize_terms_and_postings():
    """Reads in each document in corpus_files, splits it into a list of terms (i.e., tokenizes it), 
    adds new terms to the global dictionary, and adds the document to the posting list for each
    term, with value equal to the frequency of the term in the
    document."""
    global dictionary, postings
    stop_words= set(stopwords.words('english'))

    for id in corpus_files:
        f = open(corpus_files[id],'r')
        document = f.read()
        f.close()
        
        terms = tokenize(document)    
        stopped_tokens = [i for i in terms if not i in stop_words]
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        unique_terms = set(stopped_tokens)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
           
            postings[term][id] = terms.count(term) # the value is the frequency of the term in the document
			#print(postings[term][id])

    #print(postings)                                                                                              
def tokenize(document):
    terms = document.lower().split()
    return [term.strip(characters) for term in terms]

def initialize_document_frequencies():
    
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    """Computes the length for each document."""
    global length
    for id in corpus_files:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)

def imp(term,id):
    """Returns the importance of term in document id.  If the term isn't in the document, then return 0."""
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    """Returns the inverse document frequency of term.  Note that if term isn't in the dictionary then it returns 0, by convention."""
    if term in dictionary:
    	if document_frequency[term] != 0 :
    		return math.log(N/document_frequency[term],2)
    	else:
        	return 0.0
    else:
        return 0.0

def do_search():
    t = PrettyTable(['Similarity Score', 'FileName'])
    query = tokenize((input("Enter Your Query:  ")))
    u_query= set(query)
    
    if u_query == (" "):
        sys.exit()

    result_doc_id = set()
    result_doc_id = intersection(
            [set(postings[term].keys()) for term in u_query])
    if not result_doc_id:
        print ("No documents matched all query terms.")
    else:
        scores = sorted([(id,similarity(u_query,id))
                         for id in result_doc_id],
                        key=lambda x: x[1],
                        reverse=True)
        for (id,score) in scores:
        	t.add_row([str(score), corpus_files[id].strip('.rtf')])
        print(t)
        pre_rec(u_query,result_doc_id)

def intersection(sets):
    """Returns the intersection of all sets in the list sets."""
    return reduce(set.union, [s for s in sets])

def similarity(query,id):
    """Returns the cosine similarity between query and document id."""
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    if length[id] != 0:
    	similarity = similarity / length[id]
    return similarity

def pre_rec(query,result_doc_id):    
    # Computes the Precision and Recall 
    t1 = PrettyTable(['Result For', 'Value'])
    t2 = PrettyTable(['EVALUATION']) 
    rd={}
    rd.setdefault("key",set())
    rd={"data courses mining":{1, 4, 6, 7, 12, 13, 15, 21, 22, 39, 41, 42}, "CS 609":{46}}
    q1= query
    
    a = ' '.join(q1)
    b = rd.keys()
    words_re = re.compile("|".join(a))
        
    r1= set()
    r1=result_doc_id
    for i in b:
        if words_re.search(i):
            precision= len(r1.intersection(rd[i]))/len(r1)
            recall= len(r1.intersection(rd[i]))/len(rd[i])
            if(precision != 0.0 or recall != 0.0):
                
                
                t1.add_row(["Precision",str(precision)])
                t1.add_row(["Recall",str(recall)])
    print(t2)
    print(t1)

if __name__ == "__main__":
    main()
