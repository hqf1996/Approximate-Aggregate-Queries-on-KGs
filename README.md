# Approximate Aggregate Queries on KGs

This repository contains the code used for the experiments described in the paper titled

_Aggregate Queries on Knowledge Graphs:Fast Approximation with Semantic-aware Sampling_

## Requirements

The experiments have been run on an CentOS Linux release 7.3.1611 computer with a 2.1 GHz Xeon processor and 64GB RAM. All programs are written with `java1.8` and make use of two external libraries [Apache Commons Math](http://commons.apache.org/proper/commons-math/download_math.cgi), [EJML](http://ejml.org/wiki/index.php?title=Main_Page).

## Input Data

[DBpedia input data](https://drive.google.com/drive/folders/1fQEbz7tmcbe8R3sTO_LwJ9LVBDtqlyph?usp=sharing), [Freebase input data](https://drive.google.com/drive/folders/1wZSbxF_x2DSJWiMf5sW9WnJ1NW_RR3IG?usp=sharing), [Yago input data](https://drive.google.com/drive/folders/1wZSbxF_x2DSJWiMf5sW9WnJ1NW_RR3IG?usp=sharing)

The experiment uses `QALD-4`, `WebQuestions`, and `Synthetic queries` as [benchmarks](https://drive.google.com/drive/folders/19T1Th9G4HcffIhAbaCHqOJPxeWElOy51?usp=sharing) for DBpedia, Freebase, and Yago datasets, respectively.

**Example of the input data (DBpedia)**

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

### Approximate Aggregate Queries

#### Our Method

Our proposed method, with a specific entity, a predicate and a type of target entity, can be run using the following command:

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entity-type>
```

For the query example, "How many software has been developed by organizations founded in California?", we can run with the following command:

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar California foundationPlace software
```

Output

For our method, it will output the following statistical results and running time. Here is the output of the above query example:

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
Response Time (ms) : 235ms
```

#### Baseline Method

To run the baseline algorithm, we need to run it using the following command:

```
java -jar BaseLineSGQ-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type>
java -jar BaseLineGraB-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type>
java -jar BaseLineQGA-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type>
python BaseLineEAQ.py <a-specific-entity> <target-entities-type>
```

For example:

```
java -jar BaseLineSGQ-jar-with-dependencies.jar California foundationPlace software
```

Output

For each method, it will output the following statistical results and running time respectively. Here is the output of SGQ for the above query example:

```
Ground-truth : 124
---------------------------------------------
Approximate result : 110
Relative error (%) : 11.29%
---------------------------------------------
Response Time (ms) : 405ms
```

### Effect of Each Phase

The effect of each phase on the performance (Section 8.3 of our paper) can be demonstrated using the command below(Use S1, S2 and S3 to represent each phase):

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type> <which-phase>
```

For example, we can specific \<which-phase\> as S1 to see the effect of S1 on our method for each query.

```
java -jar Approximate-Aggregation-Queries-jar-with-dependencies.jar California foundationPlace software S1
```

Output

For each phase, it will output the following statistical results and running time. Here is the output when we change S1 from our semantic-aware random walk smapling to CNARW:

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
Response Time (ms) : 501ms
```

### Parameter Sensitivity

As mentioned in Section 8.4 of our paper, we studied the sensitivity of our approach on some important parameters, including the user-specific error bound $e$, confidence level $1-\alpha$, repeat factor $r$, and desired sample ratio $\lambda$, we need to run it using the following command:

```
java -jar ParameterSensitivity-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type> <error-bound> <confidence-level> <repeat-factor> <desired-sample-ratio>
```

For example:

```
java -jar ParameterSensitivity-jar-with-dependencies.jar California foundationPlace software 0.01 0.95 3 0.3
```

Output

For each parameter, it will output the following statistical results and running time. Here is the output for user-specific error bound $e=0.01$, confidence level $1-\alpha=0.95$, repeat factor $r=3$, and desired sample ratio $\lambda=0.3$:

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
Response Time (ms) : 235ms
```

### Interactive Performance

We studied our interactive performance of our method by reducing the user-specific error bound during the query processing, we need to run it using the following command:

```
java -jar InteractivePerformance-jar-with-dependencies.jar <a-specific-entity> <a-predicate> <target-entities-type>
```

For example:

```
java -jar InteractivePerformance-jar-with-dependencies.jar California foundationPlace software
```

Output

For each reduction, it will output the following additional runtime. Here is the output of the above query example:

```
-------------------user-specific error bound reduce from 0.05 to 0.04-------------------
add time : 32ms
-------------------user-specific error bound reduce from 0.04 to 0.03-------------------
add time : 56ms
-------------------user-specific error bound reduce from 0.03 to 0.02-------------------
add time : 24ms
-------------------user-specific error bound reduce from 0.02 to 0.01-------------------
add time : 152ms
```

