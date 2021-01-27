# Approximate Aggregate Queries on KGs

This repository contains the code used for the experiments described in the paper titled

_Aggregate Queries on Knowledge Graphs: Fast Approximation with Semantic-aware Sampling_ by _Yuxiang Wang, Arijit Khan, Xiaoliang Xu, Jiahui Jin and Qifan Hong._

## Requirements

The experiments have been run on an CentOS Linux release 7.3.1611 computer with a 2.1 GHz Xeon processor and 64GB RAM. All programs are written with `java1.8` and make use of two external libraries [Apache Commons Math](http://commons.apache.org/proper/commons-math/download_math.cgi), [EJML](http://ejml.org/wiki/index.php?title=Main_Page).

## Datasets and Query Workloads

Datasets: [DBpedia dataset](https://drive.google.com/drive/folders/1fQEbz7tmcbe8R3sTO_LwJ9LVBDtqlyph?usp=sharing), [Freebase dataset](https://drive.google.com/drive/folders/1wZSbxF_x2DSJWiMf5sW9WnJ1NW_RR3IG?usp=sharing), [Yago dataset](https://drive.google.com/drive/folders/1Q35R1RImlZPYwTdBwXyvGSj-4aWIONb_?usp=sharing), each one consists of an `entity file` and an `edge file`.

The experiment uses `QALD-4`, `WebQuestions`, and `Synthetic queries` as [benchmarks](https://drive.google.com/drive/folders/19T1Th9G4HcffIhAbaCHqOJPxeWElOy51?usp=sharing) for DBpedia, Freebase, and Yago datasets, respectively.

**Example of the dataset (DBpedia)**

edge file

| entity1_id | entity2_id | entity1_name | predicate | entity2_name |
| :--------: | :--------: | :----------: | :-------: | :----------: |
|  3471751   |  1712537   | Porsche_944  | assembly  |   Germany    |

entity file

| entity_id | entity_name |    type    |
| :-------: | :---------: | :--------: |
|  3471751  | Porsche_944 | automobile |
|  1712537  |   Germany   |  country   |

## Usage

### Effectiveness and Efficiency Evaluation

#### Our Method

Our proposed method, with a specific entity, a predicate, a type of target entity and a aggregate function, can be run using the following command:

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar <specific-entity> <predicate> <target-entity-type> <aggregate-function>
```

For the query example, "How many software has been developed by organizations founded in California?", we can run with the following command:

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar California foundationPlace software COUNT
```

Output

For our method, we output the following statistical results and running time for each query round by round. Here is the output of the above query example:

```
Ground-truth : 124
-------------------Round 1-------------------
Approximate result : 115.23
Margin of error (MoE) : 1.52
Relative error (%) : 7.07%
-------------------Round 2-------------------
Approximate result : 124.58
Margin of error (MoE) : 0.71
Relative error (%) : 0.46%
---------------------------------------------
Response Time (ms) : 235 ms
```

#### Comparing Methods

We compare our method with different methods, that are, `EAQ`, `GraB`,`QGA` and `SGQ`. To run these algorithms, we need to run the following commands separately:

```
SGQ: java -jar BaseLineSGQ-jar-with-dependencies.jar <specific-entity> <predicate> <target-entities-type> <aggregate-function>
GraB: java -jar BaseLineGraB-jar-with-dependencies.jar <specific-entity> <predicate> <target-entities-type> <aggregate-function>
QGA: java -jar BaseLineQGA-jar-with-dependencies.jar <specific-entity> <predicate> <target-entities-type> <aggregate-function>
EAQ: python BaseLineEAQ.py <specific-entity> <target-entities-type> <aggregate-function>
```

For example:

```
java -jar BaseLineSGQ-jar-with-dependencies.jar California foundationPlace software COUNT
```

Output

For each method, we output the following statistical results and running time respectively. Here is the output of SGQ for the above query example:

```
Ground-truth : 124
---------------------------------------------
Approximate result : 110
Relative error (%) : 11.29%
---------------------------------------------
Response Time (ms) : 405 ms
```

### Effect of Each Step on the Performance

The effect of each step on the performance (Section 7.3 of our paper) can be demonstrated using the command below by specifying a certain step (we use S1, S2 and S3 to represent each step):

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar <specific-entity> <predicate> <target-entities-type> <aggregate-function> <which-phase>
```

For example, we can specific \<which-phase\> as S1 to see the effect of S1 on our method for each query.

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar California foundationPlace software COUNT S1
```

Output

For each step, we output the following statistical results and running time. Here is the output when we change S1 from our semantic-aware random walk smapling to CNARW:

```
Ground-truth : 124
-------------------Round 1-------------------
Approximate result : 108.21
Margin of error (MoE) : 2.21
Relative error (%) : 12.73%
-------------------Round 2-------------------
Approximate result : 113.51
Margin of error (MoE) : 0.98
Relative error (%) : 8.46%
---------------------------------------------
Response Time (ms) : 501 ms
```

### Interactive Performance

We study the interactive performance (Section 7.4)  of our method by reducing the user-specific error bound *e* during the query processing, we need to run it using the following command:

```
java -jar InteractivePerformance-jar-with-dependencies.jar <specific-entity> <predicate> <target-entities-type> <aggregate-function>
```

For example:

```
java -jar InteractivePerformance-jar-with-dependencies.jar California foundationPlace software COUNT
```

Output

For each reduction of *e*, we output the additional runtime required for our method. Here is the output of the above query example:

```
-------------------user-specific error bound reduce from 0.05 to 0.04-------------------
add time : 32 ms
-------------------user-specific error bound reduce from 0.04 to 0.03-------------------
add time : 56 ms
-------------------user-specific error bound reduce from 0.03 to 0.02-------------------
add time : 24 ms
-------------------user-specific error bound reduce from 0.02 to 0.01-------------------
add time : 152 ms
```

### Parameter Sensitivity

As mentioned in Section 7.5 of our paper, we study the sensitivity of our approach on some important parameters, including the user-specific error bound *e*, confidence level 1-*α*, repeat factor *r*, and desired sample ratio *λ*. We run this experiment through the following command by varying the values of parameters:

```
java -jar ParameterSensitivity-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type> <aggregate-function> <error-bound> <confidence-level> <repeat-factor> <desired-sample-ratio>
```

For example:

```
java -jar ParameterSensitivity-jar-with-dependencies.jar California foundationPlace software COUNT 0.01 0.95 3 0.3
```

Output

For each parameter, we output the following statistical results and running time. Here is the output for user-specific error bound *e*=0.01, confidence level 1-*α*=0.95, repeat factor *r*=3, and desired sample ratio *λ*=0.3:

```
Ground-truth : 124
-------------------Round 1-------------------
Approximate result : 115.23
Margin of error (MoE) : 1.52
Relative error (%) : 7.07%
-------------------Round 2-------------------
Approximate result : 124.58
Margin of error (MoE) : 0.71
Relative error (%) : 0.46%
---------------------------------------------
Response Time (ms) : 235 ms
```
