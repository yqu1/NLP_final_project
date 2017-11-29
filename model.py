from keras.models import Model
from keras.layers import Dense, Input, Dropout, MaxPooling1D, Conv1D
from keras.layers import LSTM, Lambda
from keras.layers import TimeDistributed, Bidirectional
from keras.layers.normalization import BatchNormalization

def CL_LSTM(max_sentences, maxlen):
  filter_length = [5, 3, 3]
  nb_filter = [196, 196, 256]
  pool_length = 2
  # document input
  document = Input(shape=(max_sentences, maxlen), dtype='int64')
  # sentence input
  in_sentence = Input(shape=(maxlen,), dtype='int64')
  # char indices to one hot matrix, 1D sequence to 2D 
  embedded = Lambda(binarize, output_shape=binarize_outshape)(in_sentence)
  # embedded: encodes sentence
  for i in range(len(nb_filter)):
      embedded = Conv1D(filters=nb_filter[i],
                        kernel_size=filter_length[i],
                        padding='valid',
                        activation='relu',
                        kernel_initializer='glorot_normal',
                        strides=1)(embedded)

      embedded = Dropout(0.1)(embedded)
      embedded = MaxPooling1D(pool_size=pool_length)(embedded)

  bi_lstm_sent = \
      Bidirectional(LSTM(128, return_sequences=False, dropout=0.15, recurrent_dropout=0.15, implementation=0))(embedded)

  # sent_encode = merge([forward_sent, backward_sent], mode='concat', concat_axis=-1)
  sent_encode = Dropout(0.3)(bi_lstm_sent)
  # sentence encoder
  encoder = Model(inputs=in_sentence, outputs=sent_encode)

  encoded = TimeDistributed(encoder)(document)
  # encoded: sentences to bi-lstm for document encoding 
  b_lstm_doc = \
      Bidirectional(LSTM(128, return_sequences=False, dropout=0.15, recurrent_dropout=0.15, implementation=0))(encoded)

  output = Dropout(0.3)(b_lstm_doc)
  output = Dense(128, activation='relu')(output)
  output = Dropout(0.3)(output)
  output = Dense(1, activation='sigmoid')(output)

  model = Model(inputs=document, outputs=output)
  return model
