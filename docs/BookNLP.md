# Tips for using BookNLP

In Elalytics, we use **Lucy's version of BookNLP**. You can install it using

- `pip install git+https://github.com/lucy3/booknlp`
- `python -m spacy download en_core_web_sm`

**Do not use the original version of BookNLP.**

## For Windows Users

Windows users require additional steps to install BookNLP properly. Please follow the instructions below:

- Just follow this video. Relevant instructions start from 14:20: [https://www.youtube.com/watch?v=3l5ERF3QX0M]
- Basically, we need to have the following models properly in the relevant directory:
  - entities [https://huggingface.co/google/bert_uncased_L-6_H-768_A-12]
  - coref [https://huggingface.co/google/bert_uncased_L-12_H-768_A-12]
  - speaker [https://huggingface.co/google/bert_uncased_L-12_H-768_A-12]
