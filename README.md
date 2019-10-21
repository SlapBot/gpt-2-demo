# gpt-2-demo

Refactored and Abstracted the GPT-2 model code while putting it beside a flask API and dockerized for easy deployment.

Code and samples from the paper ["Language Models are Unsupervised Multitask Learners"](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf).

See more details in [blog post](https://blog.openai.com/better-language-models/).

## Installation

Download the model data (needs [gsutil](https://cloud.google.com/storage/docs/gsutil_install)):

```
sh download_model.sh 117M
(In case it fails to download the models/117M/checkpoint file, just create one and add these lines:
model_checkpoint_path: "model.ckpt"
all_model_checkpoint_paths: "model.ckpt"
)
```

Build the docker image:

```
docker-compose build
```

Start the services

```
docker-compose up
```

visit the external IP/localhost to see the live demo.
