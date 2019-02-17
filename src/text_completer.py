import json
import os
import numpy as np
import tensorflow as tf

from src import model, sample, encoder



class TextCompleter:
    def __init__(self):
        self.model_name = '117M'
        self.seed = None
        self.nsamples = 1
        self.batch_size = 1
        self.length = None
        self.temperature = 1
        self.top_k = 0
        np.random.seed(self.seed)
        tf.set_random_seed(self.seed)
        self.encoder = self.get_encoder()

    def get_encoder(self):
        return encoder.get_encoder(self.model_name)

    def get_session(self):
        sess = tf.Session()
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', self.model_name))
        saver.restore(sess, ckpt)
        return sess

    def complete(self, text):
        hparams = model.default_hparams()
        with open(os.path.join('models', self.model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if self.length is None:
            self.length = hparams.n_ctx // 2
        elif self.length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

        with tf.Session(graph=tf.Graph()) as sess:
            context = tf.placeholder(tf.int32, [self.batch_size, None])
            output = sample.sample_sequence(
                hparams=hparams, length=self.length,
                context=context,
                batch_size=self.batch_size,
                temperature=self.temperature, top_k=self.top_k
            )

            saver = tf.train.Saver()
            ckpt = tf.train.latest_checkpoint(os.path.join('models', self.model_name))
            saver.restore(sess, ckpt)
            context_tokens = self.encoder.encode(text)
            out = sess.run(output, feed_dict={context: [context_tokens]})[:, len(context_tokens):]
            generated_text = self.encoder.decode(out[0])
            return generated_text

if __name__ == "__main__":
    import time
    tc = TextCompleter()
    start = time.time()
    new_result = tc.complete("We've trained a large-scale unsupervised language model which generates coherent paragraphs of text, achieves state of the art performance on many language modelling benchmarks, and performs rudimentary reading comprehension, machine translation, question answering and summarization - all without task specific training.")
    end = time.time()
    print("First result took: {0}".format(str(end-start)))
