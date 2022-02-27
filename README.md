# N-Gram Language Model
This is an implementation of N-Gram Language Model. This model is built from scratch, so it may not be optimal and has some bugs (one of them is the production of words that are repeated over and over again).

## Requirements
1. &nbsp;math
2. &nbsp;statistics
3. &nbsp;NumPy
4. &nbsp;Pandas
5. &nbsp;Swifter

## Text format
<div>The code accepts a text file in the form of a pandas dataframe. One row contains one sentence, as shown in the following figure:
</div>
<img src="https://github.com/vincentmichael089/NLP-Ngram-LM/blob/main/asset/disp-01.png" width="600" />
<br>

## Functions
<div>
  <b> 1. Train model: </b>
  To train the NGram Language Model, call the fit() function. the fit() function accepts 4 arguments:
  
  > 1. x = text that the model will use to train. Please follow the text format.
  > 2. n = the "n" of ngram. Larger values will take up more memory.
  > 3. smoothingType = smoothing for the ngram model. There are 3 options: no "non" smoothing; laplace smoothing "laplace"; and add-k smoothing "add-k".
  > 4. addk = value of k if smoothing is "add-k"
</div>
<br>
<img src="https://github.com/vincentmichael089/NLP-Ngram-LM/blob/main/asset/disp-02.png" width="600" />
<br>
<div>
  <b> 2. Entropy of text: </b>
  Call the entropy() function to find out the entropy of a text against the trained model. Please follow the text format.
</div>
<br>
<img src="https://github.com/vincentmichael089/NLP-Ngram-LM/blob/main/asset/disp-02.png" width="600" />
<br>
<div>
  <b> 3. Generate sentence: </b>
  Generate sentences by calling the generate() function. This function accepts 2 arguments:

  > 1. sentence = Initialization sentence to be continued by the model.
  > 2. limit = the length of the sentence you want to form.
</div>
<br>
<img src="https://github.com/vincentmichael089/NLP-Ngram-LM/blob/main/asset/disp-03.png" width="600" />
<br>
<hr>