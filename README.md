# FancyWord

FancyWord is a Sublime Text 3 plugin that improves your word choice in writing.

# Motivation

As a non-native English speaker, I often feel frustrated when I'm writing something formal but can't think of a fancy word to replace a plain one.

A non-native English speaker may have a large vocabulary, he can recognize many words in reading and listening, but sometimes he can't recall and use those words appropriately when writing and speaking. This set of words is called passive vocabulary. [This post](https://eastasiastudent.net/study/active-passive-vocabulary/) has a clear explanation about it.

# Programmatically Find a Fancy Word

## Wordnet vs Word2Vec, which is robust?

To solve this problem, I look up the synonyms of a word in dictionary, programmatically I use `wordnet` in `nltk`. But wordnet can not give us synonyms in order of similarity, its result is just categorized by different part of speech. Besides, in many situations if there is no synonyms in dictionary, Wordnet will give nothing. To the contrast, Word2Vec also tells you the similarity between words so you can sort result, and it will always give you top N similar words as long as N is not larger than size of Word2Vec vocabulary. The nature of Word2Vec method is that the nearest words imply that they are used in most similar situation, they are not necessarily synonyms of each other, but they are related in some way, very likely not the lexical way.

## Space Required

Wordnet is part of `nltk` package, which takes about 11 MB on disk. Word2Vec is much bigger if you count its model in, for example the model trained by [Wikipedia Dependency](http://u.cs.biu.ac.il/~yogo/data/syntemb/deps.words.bz2) with 300 dimensions, 174,015 words is 860 MB, or 210 MB after converted to binary form, plus all packages required take another 110 MB, in total at least 320 MB.

## Funny Examples

Bellow is the outputs of Word2Vec and Wordnet when I look up the word 'beautiful'. Note that the output of Wordnet is unordered, I just take the first 10 it gives. We can see the results are both pretty good.

| Top 10 Output of Word2Vec | Top 10 Output of Wordnet |
|---------------------------|--------------------------|
| gorgeous                  | beauteous                |
| delightful                | bonny                    |
| glamorous                 | dishy                    |
| seductive                 | exquisite                |
| elegant                   | fine-looking             |
| adorable                  | glorious                 |
| stylish                   | gorgeous                 |
| sumptuous                 | lovely                   |
| wonderful                 | picturesque              |
| prettiest                 | pretty-pretty            |

'weirdo', of course I tested some informal words, we just got 3 synonyms from Wordnet, it seems that Wordnet take it too serious, LOL. Word2Vec gives us more various results, most of which are curses and some are off topic in some degree.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| crybaby            | creep             |
| klutz              | crazy             |
| cheater            |                   |
| voyeur             |                   |
| bummer             |                   |
| wanker             |                   |
| trekkie            |                   |
| lycanthrope        |                   |
| masochist          |                   |
| motherfucker       |                   |

'strengthen', I can't believe Wordnet just gives one output.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| entrench           | tone              |
| reinvigorate       |                   |
| enhance            |                   |
| democratize        |                   |
| solidify           |                   |
| deepen             |                   |
| bolster            |                   |
| modernise          |                   |
| weaken             |                   |
| decentralize       |                   |

'disgusting', Word2Vec wins this round.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| sickening          | disgust           |
| embarassing        | offensive         |
| horrifying         |                   |
| baffling           |                   |
| patronising        |                   |
| perplexing         |                   |
| nauseating         |                   |
| maddening          |                   |
| saddening          |                   |
| unsettling         |                   |

'door', still Wordnet gives too few output, and Word2Vec gives some interesting results.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| doors              | doorway           |
| doorway            |                   |
| window             |                   |
| gate               |                   |
| stairwell          |                   |
| stairway           |                   |
| jamb               |                   |
| balcony            |                   |
| entryway           |                   |
| vestibule          |                   |

'with', Wordnet gives zero result, while Word2Vec gives some prepositions and conjunctions and one of them is error starting with a single quote.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| for                |                   |
| without            |                   |
| after              |                   |
| despite            |                   |
| by                 |                   |
| 'without           |                   |
| whither            |                   |
| in                 |                   |
| eventhough         |                   |
| although           |                   |

'about', you should select really carefully from Word2Vec results.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| s750               | approximately     |
| measly             | active            |
| over               |                   |
| schilpp            |                   |
| approximately      |                   |
| 'without           |                   |
| than               |                   |
| ungodly            |                   |
| as                 |                   |
| particuarly        |                   |

'gently', I think most times Word2Vec works better than Wordnet.

| Output of Word2Vec | Output of Wordnet |
|--------------------|-------------------|
| softly             | lightly           |
| gracefully         |                   |
| neatly             |                   |
| awkwardly          |                   |
| loudly             |                   |
| silently           |                   |
| furiously          |                   |
| sharply            |                   |
| aggressively       |                   |
| endlessly          |                   |

# Drawback

Both Word2Vec and Wordnet can only deal with single word, you can't input or output a phrase for now.

# How to install?

+ Through Package Control
    + Package Control - First install Package Control
    + Search for the FancyWord package and install
+ From Source
    + From Source - Clone the repo to your Sublime Text packages folder.
    + `git clone https://github.com/easton042/FancyWord.git "~/Library/Application Support/Sublime Text 3/Packages/FancyWord"`

# Setup

For simplicity's sake, I will call both Word2Vec and Wordnet dictionary. Because of the huge size of Word2Vec pretrained model, I set Wordnet as your default dictionary, if you want to use the promising Word2Vec dictionary, you need to manually install Gensim: `pip install gensim`, download the pretrained model [here](https://drive.google.com/open?id=0Bz8u16o5sSTxSzVYVThGdUQ4Mjg) or [here](https://deg9gmdt8dxql.cloudfront.net/deps.words.bin), or you can find proper ones for yourself, but notice that pretrained model should be compatible with Gensim and be binary form. Last step, enable Word2Vec and set model file location in sublime-settings, then restart your SublimeText 3

# Usage 

`CMD K + CMD F` for popping the list of FancyWord, `CMD K + CMD D` for lookup up a word in Wordnet dictionary. For now, FancyWord only supports English.

Notice that the quality of Word2Vec result is determined by the pretrained model, you can download a model [here](https://deg9gmdt8dxql.cloudfront.net/deps.words.bin), which is trained by Wikipedia corpus and contains 300 dimensions and 174,015 words.

# License

This program is distributed under the terms of the GNU GPL v3. See the LICENSE file for more details.

# Credits

Thanks to contributors of Gensim, NLTK

Credit for pretrained Wikipedia Dependency model goes to [Yoav Goldberg](https://www.cs.bgu.ac.il/~yoavg/uni/)

Credit for word2vec-api code goes to [3Top](https://github.com/3Top/word2vec-api)

Credit for Anaconda code goes to [Oscar Campos](https://github.com/DamnWidget/anaconda)

Credit for KeyboardSpellCheck code goes to [jlknuth](https://github.com/jlknuth/KeyboardSpellCheck).
