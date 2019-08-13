# markov-text-gen
Markov chain based sentence generator, written in Python 3.7.

## To run:

```
python3 text-gen.py [-h] [--sentences SENTENCES] [--limit LIMIT]
optional arguments:
  -h, --help            show this help message and exit
  --sentences SENTENCES, -s SENTENCES
                        Specify the number of sentences to be generated (> 1).
  --limit LIMIT, -l LIMIT
                        Specify the maximum word count of a sentence (> 1), or
                        enforce no limit (= 0)
                        
The program reads from stdin and writes to stdout,
error messages are written to stderr. Any file I/O
can be done through redirection.
```
