# Finding Similar Documents with MinHash and LSH

Nearest-neighbor search in a document collection, comparing **brute force**, **MinHash signatures** and **Locality Sensitive Hashing (LSH)** on two real "bag-of-words" datasets (Enron emails and NIPS papers).

Coursework for **MYE047 – Algorithms for Big Data** (Lab 1), Department of Computer Science & Engineering, University of Ioannina, academic year 2021–22. Pure Python, standard library only.

---

## The problem

Given a collection of `D` documents and a document `X`, find the `K` documents most similar to `X`. Comparing every pair costs `D·(D−1)/2` similarity computations, which is about **794 million pairs** for the 39,861 Enron emails, so it does not scale. This project measures how much speed MinHash and LSH buy, and what they cost in quality.

Each document is represented by the **set of words** it contains (word counts are ignored), and similarity is measured in two ways:

| Metric | Definition |
|---|---|
| **Jaccard similarity** (`JacSim`) | `\|A ∩ B\| / \|A ∪ B\|` computed on the two word sets. Used as the ground truth. |
| **Signature similarity** (`SigSim`) | Fraction of MinHash signature rows on which two documents agree. It estimates the Jaccard similarity. |

Four ways of finding the nearest neighbors are compared:

| Method | What it does |
|---|---|
| **Brute force + Jaccard** | Jaccard similarity for every pair of documents |
| **Brute force + MinHash** | Signature similarity for every pair of documents |
| **LSH + Jaccard** | LSH selects candidate pairs, Jaccard is computed only for them |
| **LSH + MinHash** | LSH selects candidate pairs, signature similarity is computed only for them |

Quality is reported as **AvgSim**, the average similarity of the neighbors found, and speed as **ExecTime**, the execution time in seconds.

## Datasets

Two bag-of-words collections are used. They are **not included** in this repository. They appear to correspond to the *Bag of Words* data set of the UCI Machine Learning Repository, and the course provided them under the names below.

| File | Collection | Documents | Distinct words |
|---|---|---|---|
| `DATA_1-docword.enron.txt` | Enron emails | 39,861 | 28,102 |
| `DATA_2-docword.nips.txt` | NIPS papers | 1,500 | – |

Place both files in the **same folder as `LAB1.py`**. Each file has the format:

```
D                              number of documents
W                              number of distinct words
NNZ                            number of non-zero counts
docID wordID wordCountInDocument
docID wordID wordCountInDocument
...
```

Only whether a word occurs in a document matters, so the count column is ignored.

## How it works

1. **Reading.** The first `numDocuments` documents are read and each one is stored as a `frozenset` of word IDs (a compact, immutable representation). Processing only a prefix of the collection keeps experiments fast.
2. **Jaccard similarity.** Two implementations are provided and can be timed against each other:
   - `MyJacSimWithSets`: compares the two sets with a double `for` loop, `O(|A|·|B|)`.
   - `MyJacSimWithOrderedLists`: sorts both sets and walks them with two pointers, `O(|A|+|B|)`. It is orders of magnitude faster.
3. **MinHash.** `K` random permutations of the word IDs are generated with the hash `h(x) = 1 + ((a·x + b) mod p) mod m`, with `p = 2³³ − 355` and `m = 2³² − 1`. For every permutation, a document's signature entry is the smallest permuted position among its words. The result is the `K × numDocuments` **signature matrix**. An inverted index (for each word, the documents that contain it) lets the matrix be built by scanning words instead of building the huge 0/1 characteristic matrix.
4. **Brute force.** Each document is compared with the documents that follow it in the collection, the distances `1 − Sim` are sorted, and the nearest ones are kept.
5. **LSH.** The signature matrix is split into `⌊K / rowsPerBand⌋` bands. In each band, every document's slice of rows is hashed to a bucket, documents are sorted by bucket, and documents that fall in the same bucket form **candidate pairs**. Only candidate pairs are then compared. Fewer rows per band means more candidates (closer to brute force); more rows per band means fewer candidates (faster, but neighbors may be missed).

### Where things are in the code

| Function | Role |
|---|---|
| `MyReadDataRoutine` | reads the file and builds the list of frozensets |
| `MyJacSimWithSets`, `MyJacSimWithOrderedLists` | the two Jaccard implementations |
| `create_random_hash_function` | random hash function used for permutations and LSH buckets |
| `hashFunction` | creates the `K` permutations and stores/loads them in `hashFunctions.csv` |
| `MyMinHash` | builds the signature matrix |
| `MySigSim` | signature similarity of two documents (first `numPermutations` rows) |
| `neighborsBF` | nearest neighbors of a document by brute force |
| `LSH`, `neighborsLSH` | candidate pairs and nearest neighbors via LSH |

## Running it

Requirements: **Python 3.9+**, no third-party packages.

```bash
python LAB1.py
```

The program is interactive and asks, in order:

| Prompt | Meaning |
|---|---|
| File (1 or 2) | Enron or NIPS |
| Number of documents | how many documents to process (from 1 up to the file's `D`) |
| Number of neighbors | neighbors to find per document (up to 10) |
| Number of permutations `K` | signature length; a power of 2 is suggested |
| Hash-function file | `1` create `hashFunctions.csv`, `2` delete and regenerate it, `3` reuse the existing one |
| Metric check *(optional)* | compute `JacSim` (with both implementations and timings) or `SigSim` for two documents of your choice |
| Similarity metric | Jaccard or Signature similarity |
| Method | Brute force or LSH |
| Rows per band *(LSH only)* | your own value, or the default (2) |
| Specific documents *(optional)* | print the neighbors of a chosen `docID` |

At the end it prints the **execution time** of the neighbor search and the **Average Similarity**. Reading the data and building the signature matrix are not included in the timing.

**About `hashFunctions.csv`.** The permutations are saved so that repeated runs use the same ones. Delete the file (or choose option `2`) whenever you change the number of permutations `K` or switch to the other dataset, because the saved permutations only fit the settings they were created with.

## Known limitations

This is a coursework implementation. Things to keep in mind when reading the results:

- The document reader stores document `d` at position `d` of the list and leaves position 0 as an empty set, so the last requested document is not loaded and the `docID` printed by the program refers to document `d − 1` of the input file.
- Neighbors of a document are searched only among documents that come after it (each pair is examined once), so `AvgSim` is not the average over all other documents.
- LSH candidate pairs are formed from *consecutive* documents inside a bucket, so a document may end up with fewer candidates than the requested number of neighbors. `AvgSim` is averaged over the neighbors actually found, and documents without candidates count as 0, which makes the LSH and brute-force values not directly comparable.
- If rows per band is not given, a fixed default of 2 is used; the program does not adapt it to guarantee enough candidates.
- The "neighbors of a specific document" option always uses signature similarity with brute force, and prints the raw candidate list with LSH.

## Repository layout

```
.
├── LAB1.py        # the whole program
├── README.md
└── .gitignore
```
