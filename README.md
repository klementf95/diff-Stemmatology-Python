# diff-Stemmatology-Python

SE - Computational Methods for Text Stemmatology

Univ.-Prof. Dr Tara L Andrews, Dott.ssa.mag. Elisabetta Magnanti

Florian Klement & David Siegl

Difference Matrices and Leitfehler-detection: The longest common subsequence and measures of uniqueness

Converting and Adapting Dieter Bachmann's & Philipp Roelli's Perl Script to Python

Introduction:

Our aim with this project was to contribute to the larger whole of the stemmatological community in a structural way that would continue to carry a lasting impact on the future approach of digital researchers, by promoting convenient and approachable practices to allow for a low-threshold of entry. The topic we chose, the script by Roelli and Bachmann, carries weight through the utility it offers practitioners since 2010, yet parts of its merits are marred by the constraints imposed on its users due to the language barrier they might see themselves confronted by when having to use Perl, a scripting language that has fallen out of favour with the scientific community in recent years. Thus, our main effort lies in being able to allow the implementation by Roelli & Bachmann, which was written for a specific project in mind (i. e. comparing Latin texts), to reach a much broader audience of digital researchers from different backgrounds and empower them to adapt the quality of their results via individual adjustments fitting for their respective language of research and tradition. Our realisation of it offers more flexibility in terms of implementing additional features, like a parameterized version of the letters or terms to be substituted for one another, within the normalisation and general preprocessing steps, as well as additional freedom of choice in substitutions and connectivity by making use of Python's rich ecosystem and community. It was especially important for us to streamline and standardise the procedure of generating I/O within the creation of digital stemmas and its surrounding analyses.

The algorithm diff, created by Ned Konz, on which the works of Roelli and Bachmann build upon shares caveats in its application with more commonly used methods of stemmatology, as well as those borrowed from phylogenetics and still struggles with inconsistencies and lacunae. Diff operates on the basis of pairwise juxtaposition, whereas each manuscript is compared with another in order to compute a quantitative relatedness of the whole corpus. The basic notion of mathematical distance calculation is expressed via the so-called 'edit distance', referring to a given difference between two strings expressed in the number of edits or basic operations necessary to transform the first text into the second or vice versa. This distance metric can in the most general sense be applied on a character level but, as Roelli and Bachmann also point out, when it comes to stemmatological analysis, it seems more plausible to operate on a word level. - i. e. different manuscripts are considered as ordered lists of words in order to compare them. In a more practical sense the edit distance should therefore reflect the number of deletions or insertions made by a scribe, while the final result of the edit distance computation should in the end return the measure of distance connecting any two manuscripts in the shape of a matrix.

Among others, Roelli's & Bachmann's implementation added to it further adaptations in order to bring the algorithm closer in line with the practices of scribal transmission and general features for the preprocessing of natural language textual witnesses. (Cf. Roelli & Bachmann, 2010, 315-317)

Our modification opted to drop diff altogether, given that the input format has been adapted from plain text, to the readily available shape of output automated collation tools like Collatex provide. In this shape, the alignment and standardisation of traditions is already taken care of and the act of comparison and weighting is a simpler procedure, which can do without requiring additional, external packages.

In order to evaluate the quality of the modified script compared to its original implementation, we selected several collated texts for comparison and made use of tools like the PHYLIP tree visualizer offered by Trex-online. More on this matter can be found in the following sections.

Description:

The adapted Python Script lf_new5.py provides the detection of Leitfehlers from a given text collation. The leitfehlers are pasted into a separate text document named "leitfehler_list.txt". Additionally it produces a lower-triangular distance matrix which can then be further used as input for PHYLIP and its various functionalities. The script starts by reading in the input, which consists of tabular data (in either .csv or .txt format) with its columns containing labels for the manuscripts followed by a line for every word in each manuscript. The script standardised the input by removing punctuation; it also stores the labels and contents of the manuscripts. Optionally the user can also provide the script with a file of regex or other substitution terms which are then parsed through the preprocessing pipeline as an additional step. The function called dodiff takes two arrays of words as an input and returns the numeric difference between the two arrays. For this it compares the contents of each manuscript to the contents of every other manuscript that precedes it in the array. The actual leitfehler calculation is done by counting the number of times each word appears in each manuscript and comparing these counts between pairs of manuscripts. Two rating functions iterate over each term for each pairing of texts, to see if either, both, or neither of the words is included in a manuscript. The script calculates a score for each word in the manuscripts based on the number of manuscripts in which it appears and its global frequency in the manuscripts. The scores are normalised by dividing them by the number of occurrences of each leitfehler candidate in the manuscripts.

Parameters:

For making the handling of our script compliant with the UNIX-Standards, we made use of the standard Python library argparse in order to implement a number of parameters which can directly be called and modified by the end user via a CLI. The different parameters are as follows:

-h / --help: This standard parameter provides the user with a documentation overview of the script and its different parameters.

-f /--file: This parameter is required and denotes the file path to the text collation in a tabular data format (either .csv or .txt).

-c / --cut: This parameter is optional and functions as a cut off threshold for the leitfehler detection score. Its default value = 0. A noticeable effect starts at roughly 400. For larger datasets, like Heinrichi, it is advisable to set a value preemptively to decrease the runtime considerably.

-d / --debug: This parameter is optional and can take either the binary value of 0 or 1. If the value = 0 then the script will print out only the matrix of the computed diff scores and if the value = 1 then the script will also create a separate text file called leitfehler_list.txt which contains potential leitfehlers and their scores.

-delim / --delim: This parameter is optional and takes as an input the separator of the collated input file. Its default value = comma but it can also handle other common delimiters such as tab.

-e / --encoding: This parameter is optional and denotes the textual encoding of the input file. Its default value = 'utf-8', for other encoding options and for the explicit format please refer to the base Python function open().

-r / --regex: This parameter is optional and provides the user the option to specify an additional filepath with regex expressions which will then be applied to the collated text within the preprocessing pipeline. The expected format of the regex file:

every substitution expression consisting of two lines where first line = matching pattern

second line = substitution pattern

-sm / --scoremax: This parameter is optional and makes it possible the finetune the probability of the leitfehler detection. The expected input is of the type integer while its default value = 1.

Some benchmarks and comparisons:

Generally speaking the Python implementation outperformed its Perl ancestor by a moderate margin, especially in the case of the use of the Heinrichi text, where the difference is capable of accumulating more noticeable headway as the runtime goes up. In terms of the difference matrices, some subtle changes within the results can be seen, most notably due to our added preprocessing steps, as well as the subtle tweaks in the ranking of differences and our substitution of the diff algorithm with a simpler, more streamlined measure of comparison, entirely from within the base packages of python.

The texts we used were chosen from the normalised and edited selection of datasets made available by the Helsinki Institute for Information Technology on their website for the Computer-Assisted Stemmatology Challenge. (Cf. Computer Assisted Stemmatology Challenge)

For detailed visualisations please refer to the PDF-file in the repository. These show side by side comparisons of the lower half distance matrices of the Perl and Python scripts, as well as their runtime. Additionally we provide a visual comparison of a PHYLIP stemma created from the respective output, these were generated with the help of the trex-online tool of the Université du Québec à Montréal. (Cf. Trex-online)


References

Baret et al., P. (2006). Testing Methods on an Artificially Created Textual Tradition. In The Evolution of Texts. Confronting Stemmatological and Genetical Methods (Vol. XXIV–XXV., pp. 255-283). Istituti Editoriali e Poligrafici Internazionali.

Christiansen, T., Foy, B., Wall, L., & Orwant, J. (2012). Programming Perl: Unmatched Power for Text Processing and Scripting. O'Reilly Media, Incorporated.

Computer-Assisted Stemmatology Challenge, https://www.cs.helsinki.fi/u/ttonteri/casc/data.html. Accessed 5 February 2023.

Howe et al., C. J. (2012). Responding to Criticisms of Phylogenetic Methods in Stemmatology. Studies in English Literature 1500-1900, 52(1), 51-67.

Hunt, J. W., & McIlroy, M. D. (1976). An Algorithm for Differential File Comparison. Bell Laboratories, 41, 1-8.

PerlPhrasebook. (2012, 4 26). PerlPhrasebook - Python Wiki. Retrieved 12 8, 2022, from https://wiki.python.org/moin/PerlPhrasebook

Roelli, P., & Bachmann, D. (2010). Towards Generating A Stemma Of Complicated Manuscript Traditions. Petrus Alfonsi's Dialogus. Revue d'histoire des textes, 5, 307-321.

Trex-online, http://www.trex.uqam.ca/index.php?action=phylip. Accessed 5 February 2023.

[![DOI](https://zenodo.org/badge/597797969.svg)](https://zenodo.org/badge/latestdoi/597797969)
