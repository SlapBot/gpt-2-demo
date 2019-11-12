model=$1

mkdir -p models/$model

# TODO: gsutil rsync -r gs://gpt-2/models/ models/
# Removed checkpoint below since we dont have permission to copy a directory
for filename in checkpoint, encoder.json hparams.json model.ckpt.data-00000-of-00001 model.ckpt.index model.ckpt.meta vocab.bpe; do
  gsutil.cmd cp gs://gpt-2/models/$model/$filename models/$model
done
