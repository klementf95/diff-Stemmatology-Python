# diff-Stemmatology-Python

SE - Computational Methods for Text Stemmatology

Univ.-Prof. Dr Tara L Andrews, Dott.ssa.mag. Elisabetta Magnanti

Florian Klement & David Siegl

**Difference Matrices and Leitfehler-detection: The longest common subsequence and measures of uniqueness**

**Converting and Adapting Dieter Bachmann's & Philipp Roelli's Perl Script to Python**

**Introduction:**

The algorithm diff, created by Ned Konz, on which the works of Roelli and Bachmann build upon is not based on phylogenetic tools, yet it shares the same caveats in its application, and struggles with inconsistencies and lacunae. Diff operates on the basis of pairwise juxtaposition, whereas each manuscript is compared with each other in order to compute a quantitative relatedness of the whole corpus. The basic notion of mathematical distance calculation is expressed via the so-called 'edit distance', referring to a given difference between two strings expressed in the number of edits or basic operations necessary to transform the first text into the second or vice versa. This distance metric can in the most general sense be applied on a character level but, as Roelli and Bachmann also point out, when it comes to stemmatological analysis, it seems more plausible to operate on a word level. - i. e. different manuscripts are considered as ordered lists of words in order to compare them. In a more practical sense the edit distance should therefore reflect the number of deletions or insertions made by a scribe, while the final result of the edit distance computation should in the end return the measure of distance connecting any two manuscripts in the shape of a matrix.

Among others, Roelli's & Bachmann's implementation added to it further adaptations in order to bring the algorithm closer in line with the practices of scribal transmission and general features for the preprocessing of natural language textual witnesses. They introduced a parameter for the adaptation of the weight subsequent mistakes carry, as is the case for a whole missing line or syntactical transposition, furthermore providing a method of extracting candidates for Leitfehler. (Cf. Roelli & Bachmann, 2010, 315-317)

Given that the implementation by Roelli & Bachmann is written in Perl, a scripting language that has fallen out of favor with the scientific community in recent years, and that its usage was mainly intended for comparing Latin texts, we decided to convert the script into the more versatile and - by today's standards - more popular language Python. This approach offers more flexibility in terms of implementing additional features, like a parameterized version of the letters or terms to be substituted for one another, within the normalization and general preprocessing steps. This could be provided by the user in the form of a dictionary as input. It will also allow the fitting of the existing script's core components into a wider array of possible use cases by making use of Python's rich ecosystem and community.

As the aforementioned diff algorithm lies at the core of the original Perl script, which imports it as a module, it is also necessary to find a working alternative within Python. Luckily since the diff algorithm was already developed for UNIX in the 1970s most programming languages of today - including Python - offer a working solution within their core utilities. Here we most likely would opt for making use of the library _difflib_, which contains different functions for comparing sequences of texts and can be directly imported into the working Python code. (Cf. Python Foundation, n.d.) Another important aspect which has to be taken into consideration is the heavy dependence on the native Regex functionality available within Perl which also has to be translated into Python syntax. Fortunately we can here again make use of another core Python library named _re_ which offers all the Regex functionality one can wish for.

In order to evaluate the quality of the modified script compared to its original implementation, we will make use of some of the benchmarking metrics laid out by Roos & Heikkilä in connection with their set of evaluation methods of the artificially created Heinrichi dataset as well as alternative state of the art methods, like parsimony or data compression. (Cf. Roos & Heikkilä, 2009)

The aim of this project can be summarized as follows: In order to increase the availability of Bachmann's and Roelli's script _lf\_new4.pl_ for a broader audience of digital researchers from different backgrounds and empower them to adapt the quality of their results via individual adjustments fitting for their respective language of research and tradition it appears to be beneficial to translate the script into a more modern scripting language and apply some adjustments to it in the process. Moving forward we hope to bring the project closer to the intended synthesis proposed by the original creators which pertains to the idea of "a happy marriage of our human philological judgment with the computing power of our algorithm".(Roelli & Bachmann, 2010, 32)

**Description:**

The adapted Python Script _lf\_new5.py_ provides the detection of Leitfehlers from a given text collation.

The point of diff was to align the texts, and there are two things that make it obsolete:

- We have better tools for text alignment, such as CollateX

- Many scholars will already have aligned the texts and won't want their collations to be disregarded.

The leitfehlers are pasted into a separate text document named "leitfehler\_list.txt". Additionally it produces a lower-triangular distance matrix which can then be further used as input for PHYLIP and its various functionalities. The script starts by reading in the input, which consists of tabular data (in either .csv or .txt format) with its columns containing labels for the manuscripts followed by a line for every word in each manuscript. The script standardized the input by removing punctuation; it also stores the labels and contents of the manuscripts. Optionally the user can provide the script also with a file of regex or other substitution terms which are then parsed through the preprocessing pipeline as an additional step.The function called dodiff takes two arrays of words in an input and returns the numeric difference between the two arrays. For this it compares the contents of each manuscript to the contents of every other manuscript that precedes it in the array. The actual leitfehler calculation is done by counting the number of times each word appears in each manuscript and comparing these counts between pairs of manuscripts. Two rating functions iterater over each term for each pairing of texts, to see if either, both, or neither of the words is included in a manuscript. The script calculates a score for each word in the manuscripts based on the number of manuscripts in which it appears and its global frequency in the manuscripts. The scores are normalized by dividing them by the number of occurrences of each leitfehler candidate in the manuscripts.

**Parameters:**

For making the handling of our script compliant with the UNIX-Standards, we made use of the standard Python library argparse in order to implement a number of parameters which can directly be called and modified by the end user via a CLI. The different parameters are as follows:

_-h / --help:_ This standard parameter provides the user with an overview documentation of the script and its different parameters.

_-f /--file:_ This parameter is required and denotes the filepath to the text collation in a tabular data format (either .csv or .txt).

_-c / -_-_cut:_ This parameter is optional and functions as a cut off threshold for the leitfehler detection score. Its default value = 0. Noticeable effect starts at roughly 400. For larger datasets, like Heinrichi, it is advisable to set a value preemptively to decrease the runtime considerably.

_-d / --debug:_ This parameter is optional and can take either the binary value of 0 or 1. If the value = 0 then the script will print out only the matrix of the computed diff scores and if the value = 1 then the script will also create a separate text file called _leitfehler\_list.txt_ which contains potential leitfehlers and their scores.

_-delim / --delim:_ This parameter is optional and takes as an input the separator of the collated input file. Its default value = comma but it can also handle other common delimiters such as tab.

_-e / --encoding:_ This parameter is optional and denotes the textual encoding of the input file. Its default value = 'utf-8', for other encoding options and for the explicit format please refer to the base Python function open().

_-r / --regex:_ This parameter is optional and provides the user the option to specify an additional filepath with regex expressions which will then be applied to the collated text within the preprocessing pipeline. The expected format of the regex file:

every substitution expression consisting of two lines where

first line = matching pattern

second line = substitution pattern

_-sm / --scoremax_: This parameter is optional and makes it possible the finetune the probability of the leitfehler detection. The expected input is of the type integer while its default value = 1.

_-v / --verbose_: This parameter is optional and can take either the binary value of 0 or 1. If the value = 0 then the script will print out only the standard text file _leitfehler\_list.txt_ with its diff scores and if the value = 1 then the script will also create an additional text file called _leitfehler\_vote.txt_ which contains another leitfehler list with the relevance for each manuscript.

**Some benchmarks and comparisons:**

Generally speaking the Python implementation outperformed its Perl ancestor by a moderate margin, especially in the case of the use of the Heinrichi text, where the difference is capable of accumulating more noticeable margins as the runtime goes up. In terms of the difference matrices, some subtle differences within the results can be seen, most notably due to our added preprocessing steps, as well as the subtle tweaks in the ranking of differences and our substitution of the diff algorithm with a simpler, more streamlined measure of comparison, entirely from within the base packages of python.

The following pictures show side by side comparisons of the lower half distance matrices of the Perl and Python scripts, as well as their runtime. Additionally we provide a visual comparison of a PHYLIP stemma created from the respective output, these were generated with the help of the trex-online tool of the Université du Québec à Montréal. ([http://www.trex.uqam.ca/index.php?action=phylip](http://www.trex.uqam.ca/index.php?action=phylip))

The texts we used were chosen from the normalized and edited selection of datasets made available by the Helsinki Institute for Information Technology on their website for the Computer-Assisted Stemmatology Challenge. ([https://www.cs.helsinki.fi/u/ttonteri/casc/data.html](https://www.cs.helsinki.fi/u/ttonteri/casc/data.html))

![](RackMultipart20230129-1-qm5hn8_html_5d441eab66ee3261.png)

![](RackMultipart20230129-1-qm5hn8_html_93d25cd7904c75eb.png)

![](RackMultipart20230129-1-qm5hn8_html_ce1ad87b91268b32.png)

![](RackMultipart20230129-1-qm5hn8_html_9b9224c7f47b3f2e.png)

![](RackMultipart20230129-1-qm5hn8_html_736540a2677c17aa.png)

![](RackMultipart20230129-1-qm5hn8_html_c2b42e45289b51ae.png)

Python Output für Harzival

![](RackMultipart20230129-1-qm5hn8_html_bea48fa49c3287e2.png)

Perl Output

![](RackMultipart20230129-1-qm5hn8_html_2c248c62daf24bc7.png)

Python Heinrichi ![](RackMultipart20230129-1-qm5hn8_html_df44d8f4396ac782.png)

Perl

![](RackMultipart20230129-1-qm5hn8_html_2a2789173b670266.png)

Python Bison/Bezos

![](RackMultipart20230129-1-qm5hn8_html_79be478a5be7a4da.png)

Perl

![](RackMultipart20230129-1-qm5hn8_html_81c75257cb1b02f.png)

**References**

Baret et al., P. (2006). Testing Methods on an Artificially Created Textual Tradition. In _In The Evolution of Texts. Confronting Stemmatological and Genetical Methods_ (Vol. XXIV–XXV., pp. 255-283). Istituti Editoriali e Poligrafici Internazionali.

Christiansen, T., Foy, B., Wall, L., & Orwant, J. (2012). _Programming Perl: Unmatched Power for Text Processing and Scripting_. O'Reilly Media, Incorporated.

Homolog\_us. (n.d.). Move Seamlessly between PERL and Python Move Seamlessly between PERL and Python. Retrieved 12 8, 2022, from https://leanpub.com/perl2python/read

Howe et al., C. J. (2012). Responding to Criticisms of Phylogenetic Methods in Stemmatology. _Studies in English Literature 1500-1900_, _52_(1), 51-67.

Hunt, J. W., & McIlroy, M. D. (1976). An Algorithm for Differential File Comparison. _Bell Laboratories_, _41_, 1-8.

PerlPhrasebook. (2012, 4 26). PerlPhrasebook - Python Wiki. Retrieved 12 8, 2022, from https://wiki.python.org/moin/PerlPhrasebook

Roelli, P., & Bachmann, D. (2010). Towards Generating A Stemma Of Complicated Manuscript Traditions. Petrus Alfonsi's Dialogus. _Revue d'histoire des textes_, _5_, 307-321.

Roos, T., & Heikkilä, T. (2009). Evaluating Methods for Computer-Assisted Stemmatology Using Artificial Benchmark Data Sets. _Literary and Linguistic Computing_, _24_(4), 417-433.

11 ![](RackMultipart20230129-1-qm5hn8_html_79be478a5be7a4da.png)
