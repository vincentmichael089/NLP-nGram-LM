class nGramModel:
  def __init__(self):
    self._n = None
    self._data = []
    self._selfData = []
    self._smoothingType = None
    
    self._countMatrix = []
    self._nmin1gramCounter = []
    self._ngramCounter = []
    self._nmin1gramCounterIndexer = []
    self._ngramCounterIndexer = []

    self._addk = None
    
  def tokenize(self, sentence):
    return sentence.split()

  def initiateMatrix(self, xAxis, yAxis):
    self._countMatrix.append([np.zeros((len(xAxis), len(yAxis)), dtype=float)])
    
  def endMarker(self, sentence):
    return sentence + str(" </S>")

  def nGramCounter(self, pandasSeriesOfSentence, n):
    words = (pandasSeriesOfSentence.str.split(' ').explode())
    tempGram = (words)
    for i in range(n-1):
      nextWord = words.groupby(level=0).shift(i*-1-1)
      tempGram = (tempGram + " " + nextWord)

    tempGram.dropna()
    return tempGram.value_counts()[:]

  def entropy(self, testData):
    listEntropy = []
    xContext = None
    yGram = None

    self._testData = testData.copy().apply(self.endMarker)
    for gram in range(self._n):
      if gram != 0: self._testData = '<S> ' + self._testData

    for sentence in self._testData:
      key = []
      sumProb = 0
      tokenized = sentence.split()
      
      if gram > 0:
        for i in range(len(tokenized)):
          key.append(tokenized[i])
          if len(key) == gram + 1:
            xgram = " ".join(key[:gram])
            ygram = " ".join(key[:])
            
            if xgram in self._nmin1gramCounterIndexer[gram][0] and ygram in self._ngramCounterIndexer[gram][0]:
              proba = self._countMatrix[gram][0][self._nmin1gramCounterIndexer[gram][0].index(xgram)][self._ngramCounterIndexer[gram][0].index(ygram)]
              sumProb = sumProb + proba * math.log2(proba)
            else: 
              proba = 0.75/len(self._nmin1gramCounterIndexer[gram][0])
              sumProb = sumProb + proba * math.log2(proba)
            key.pop(0)
      else:
        for i in range(len(tokenized)):
          if tokenized[i] in self._countMatrix[0][0]:
            proba = self._countMatrix[0][0][tokenized[i]]
            sumProb = sumProb + proba * math.log2(proba)  
          else: 
            proba = 0.75/len(self._countMatrix[0][0])
            sumProb = sumProb + proba * math.log2(proba)     
      
      listEntropy.append(-sumProb)

    return statistics.mean(listEntropy)

  def fit(self, x, n, smoothingType = 'non', addk = 0):
    self._n = n
    self._data = x.copy().swifter.apply(self.endMarker)
    self._smoothingType  = smoothingType
    self._addk = addk

    for gram in range(n):
      if gram == 0:
        self._ngramCounter.append([self.nGramCounter(self._data, gram+1)])
        self._nmin1gramCounter.append([])
        self._nmin1gramCounterIndexer.append([])
        self._ngramCounterIndexer.append([])
        self._countMatrix.append([self._ngramCounter[gram][0] / len(self._ngramCounter[gram][0])])
      else:
        self._data = '<S> ' + self._data
        self._nmin1gramCounter.append([self.nGramCounter(self._data, gram)])
        self._ngramCounter.append([self.nGramCounter(self._data, gram+1)])
        self._nmin1gramCounterIndexer.append([self._nmin1gramCounter[gram][0].index.to_list()])
        self._ngramCounterIndexer.append([self._ngramCounter[gram][0].index.to_list()])
        self.initiateMatrix(self._nmin1gramCounter[gram][0], self._ngramCounter[gram][0])

        for sentence in self._data:
          key = []

          tokenized = sentence.split()
          for i in range(len(tokenized)):
            key.append(tokenized[i])
            if len(key) == gram + 1:
              xgram = " ".join(key[:gram])
              ygram = " ".join(key[:])
              #print(xgram)
              #print(ygram)
              #print("=====")
              self._countMatrix[gram][0][self._nmin1gramCounterIndexer[gram][0].index(xgram)][self._ngramCounterIndexer[gram][0].index(ygram)] += 1
              key.pop(0)

        if self._smoothingType == 'non':
          for i in range(len(self._countMatrix[gram][0])):
            self._countMatrix[gram][0][i] = self._countMatrix[gram][0][i] / self._nmin1gramCounter[gram][0][i]
        elif self._smoothingType == 'laplace':
          for i in range(len(self._countMatrix[gram][0])):
            self._countMatrix[gram][0][i] = (self._countMatrix[gram][0][i] + 1) / (self._nmin1gramCounter[gram][0][i] + len(self._nmin1gramCounter[gram][0]))
        elif self._smoothingType == 'add-k':
          for i in range(len(self._countMatrix[gram][0])):
            self._countMatrix[gram][0][i] = (self._countMatrix[gram][0][i] + self._addk) / (self._nmin1gramCounter[gram][0][i] + (self._addk * len(self._nmin1gramCounter[gram][0])))
    
    print("done! entropy on train corpus: ", self.entropy(self._data))
  
  def generate(self, sentence, limit = 0):
    if self._n is 1:
      print("can't use 1-gram to generate sentence.")
    elif len(sentence) < self._n:
      print("please provide a sentence with at least ", self._n - 1 , "in length.")
    else:
      generatedSentence = self.tokenize(sentence)

      cont = True
      while cont:
        lastNWord = " ".join(generatedSentence[-(self._n-1):])
        indexNextWord = np.argmax(self._countMatrix[self._n-1][0][ng._nmin1gramCounterIndexer[self._n-1][0].index(lastNWord)])
        nextWord = self.tokenize(self._ngramCounterIndexer[self._n-1][0][indexNextWord])
        generatedSentence.append(nextWord[-1])
        if generatedSentence[-1] == "</S>" or len(generatedSentence) == limit: cont = False
      
      print(' '.join(generatedSentence[:-1]))
