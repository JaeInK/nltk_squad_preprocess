import json
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle

#if there is encoding error. type 'export PYTHONIOENCODING=utf8' in console

#define tokenize by nltk
def tokenize(_context):
	sentContext = sent_tokenize(_context)
	words=[]
	for sent in sentContext:
		wordContext = word_tokenize(sent)
		for word in wordContext:
			words.append(word)
	return words

#load json file
dict = json.load(open('train-v2.0.json'))

titleArray=[]
contextArray=[]
questionArray=[]
answerArray=[]
isImpossibleArray=[]

contextIndex=-1
#parsing alltogether
titleNum = len(dict['data'])
for i in range(titleNum):
	titleArray.append(dict['data'][i]['title'])
	paragraphNum = len(dict['data'][i]['paragraphs'])
	for j in range(paragraphNum):
		contextIndex += 1
		context = dict['data'][i]['paragraphs'][j]['context']
		contextArray.append([tokenize(context),i]) #context is saved as [wordsList, titleNum]
		qasNum = len(dict['data'][i]['paragraphs'][j]['qas'])
		for k in range(qasNum):
			question = dict['data'][i]['paragraphs'][j]['qas'][k]['question']
			answersList = dict['data'][i]['paragraphs'][j]['qas'][k]['answers']
			if len(answersList)==0: #there is no answer, is_impossible=True
				answerText=''
				wordPosition=-1
			else: #there is answer, is_impossible=False
				answerText = dict['data'][i]['paragraphs'][j]['qas'][k]['answers'][0]['text']
				charPosition = dict['data'][i]['paragraphs'][j]['qas'][k]['answers'][0]['answer_start']
				startPosition = len(tokenize(dict['data'][0]['paragraphs'][0]['context'][:charPosition]))
				tokenizedAnswer = tokenize(answerText)
				endPosition = startPosition + len(tokenizedAnswer)-1
			isImpossible = dict['data'][i]['paragraphs'][j]['qas'][k]['is_impossible']
			questionArray.append([tokenize(question),i,contextIndex]) # question is saved as [wordList, titleNum, contextNum]
			answerArray.append([tokenizedAnswer, startPosition, endPosition, i, contextIndex]) #answer is saved as [wordList, startPosition, titleNum, contextNum]
			isImpossibleArray.append([isImpossible, i, contextIndex]) #is_impossible is saved as [is_impossble, titleNum, contextNum] 
				
#check if list are not 2d
#Train has only one answer, Dev has multiple answers????!!!!
			
print(titleArray[0])
print(contextArray[4])
print(questionArray[30])
print(answerArray[30])
print(contextArray[0][0][answerArray[1][1]])
print(contextArray[0][0][answerArray[1][2]])
print(isImpossibleArray[1])

with open('title.pickle', 'wb') as t:
    pickle.dump(titleArray, t, pickle.HIGHEST_PROTOCOL)
with open('context.pickle', 'wb') as c:
    pickle.dump(contextArray, c, pickle.HIGHEST_PROTOCOL)
with open('question.pickle', 'wb') as q:
    pickle.dump(questionArray, q, pickle.HIGHEST_PROTOCOL)
with open('answer.pickle', 'wb') as a :
    pickle.dump(answerArray, a, pickle.HIGHEST_PROTOCOL)
with open('isImpossible.pickle', 'wb') as i:
    pickle.dump(isImpossible, i, pickle.HIGHEST_PROTOCOL)
