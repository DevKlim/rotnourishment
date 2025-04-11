2025-04-01 15:44

Status: #baby 

Tags: [[dsc102]], [[systems]]

# Computer Organization

#### Vector Store
> Manages and organizes vector embeddings by context

- Large datasets / multi-dim vectors, need to optimize for performance
- arranges to be retrieved quickly with algorithmic searching / parsing

Two types of embedding: **Word** and **Sentence** embedding

![[Pasted image 20250401184848.png]]

Convert text into numerical representation called embedding

Project to a vector space. Words which are close in real life into embeddings.

Unstructured data is found as text from internet -> LLM parse and reads them using transformer (converts text to series of numbers / vectors)

Software systems for Data Analytics / ML / AI, require optimization in many domains.

### Recommender Systems
> requires large (big) datasets and recommends via performant ML / DL / AI algorithms

Recommendations driven by machine learning. To accumulate data...
- Log user behaviors
	- views
	- clicks
	- pauses
	- etc.
- Apply ML models to Terabytes of data from **ALL** users
- Requires large computing power and money...

**Knowledge Base Construction** (KBC) extracts tabular / relational data from large amounts of text data.

A knowledge vault forms of all types of datatypes across internet...

### Vision...
- Build systems from user's perspective vs. traditional system implementers

Building scalable systems composed of...
1. **Systems**
	- Storing and efficiently compute large data in cloud settings
2. **Scalability**
	- Scale and parallelize these computations which more and more data / users
3. **Analytics**
	- Source: acquire data -> prep for ML
	- Build: model selection and dl systems
	- Deploy the pipeline

Popular stack choice include...
- python, scikit-learn, R, TensorFlow, PyTorch, Dask, Spark, Kubernates, AWS Services
- I like Dash, Streamlit, ...

The pipeline process include...
>Data acquisition -> Data prep
>Feature Engineering -> Training / Inference -> Model Selectiong
>Serving(Deploying) -> Monitoring

**ML Systems** is a data processing system for mathematically advanced data analysis operation.
- Choose inference or predictive-activity
- Statistical analysis; ML, DL;
- Choose for optimization for perfect library

**Orthogonal Dimensions of Categorizations** (does not overlap) are...
- **Scalability**: in-memory libraries vs scalable ML system (wants to develop modules that grow but optimize for less processing power; possibly reducing output size vs. input processing)
- **Target Workloads**: general ML libs vs Decision tree-oriented vs DL, etc.
	- will models clash or coallesce?
- **Implementation Reuse**: find businesses / industries that could be repurposed with similar framework to deploy multiple instances of value.

**Popular ML libraries**...
- In-memory: scikit-learn, R
- Disk-based: SAS, Dask
- RDBMS / Spark-based Layers: MADlib, Apache Spark, MLlib
- Cloud-native: Azure ML, Amazon SageMaker
- AutoML platforms: DataRobot, H$_2$Oai
- Decision tree-based: XGBoost, LightGBM

Concerns regarding ML...
- Accuracy
	- is real?
- Runtime Efficiency (length of algorithm runtime, depends on situation)
- Scalability (and efficiency for scale (can we reuse?))
	- given existing RAM, when tuning for larger datasets / models, current systems may brick or overheat current chips
- Usability
	- Is the interface readable for anyone to be used?
- Manageability
	- fine-tune or change for other systems of work?
- Developability
	- Possible to develop within scope and budget?
- Explainability
	- what value could be derived with this pipeline?
	- can higher management understand the value of this work?
As such, accuracy is a trade-off variable with all these practical concerns

**Conceptual Sys Stack...**
- Theory
- Program Formalism
- Prog Mod
- Exec Primitives
- HArdware

|                     | RDB Systems                                       | ML Systems                             |
| ------------------- | ------------------------------------------------- | -------------------------------------- |
| Theory              | First Order logic<br>Complexity Theory            | Learning Theory<br>Optimization Theory |
| Prog. Formalism     | Rel. Algebra                                      | Matrix alg, Grad desc                  |
| Prog. Specification | SQL                                               | TensorFlow? PyTorch?<br>scikit-learn?  |
| Prog Mod            | Query Optimization                                | ...? Fine-tune?                        |
| Exec Primitives     | Parallel Relational <br>Operator Dataflows        | Varies by ML Alg                       |
| Hardware            | CPU, GPU, Gate Arrays, <br>Node Version Managers, |                                        |

for example of real-world ML...

**Pareto Surfaces**: suppose ad click-through pred models A, B, C, and D with accuracies of 95%, 85%, 90%, and 85%. Which to select given...

![[Pasted image 20250401194457.png]]
Where *Pareto Frontier* is examined with a curved line through CEA.



[Slides](https://dsc-courses.github.io/dsc102-2023-sp/resources/lectures/Lec_01-Topic_1-Part_1a-CompOrg.pdf) | 

**Computer** is a programmable electronic device that can store / retrieve / process digital data

We split a computer into software and hardware...

![[Pasted image 20250403184022.png]]

**Hardware** includes...
- processors (CPU / GPU)
	- executes instructions to manipulate data specified by program
- main memory (DRAM aka *Dynamic Random Access Memory*)
	- store data and programs for fast location / retrieval; byte-level addressing
- disk (secondary storage like hard drives)
	- similar to memory but persistent, slower, and higher capacity-to-cost ratio; various addressing schemes
- network interface controller (NIC)
	- send data to / retrieve data over network of interconnected computers / devices

As such a computer will have these 4 working parts to
- retrieve and process via processor
- store data (and later quickly retrieve) with memory
- stores data for long term access in secondary storage
- then access internet or nearby devices with NIC

In a motherboard, ...
- RAM -> main memory
- CPU -> processor
- Ethernet Chip -> network
- SATA / PCI -> secondary storage

Working with software...
- **Instruction** is a command understood by hardware.
	- finite vocab between processor with Instruction Set Architecture (ISA)
	- bridge between hardware and software
- **Program** is code / collection of instructions for hardware to exec
- **Programming Lang** is human-readable formal language to write to a program
	- the language then compiles the abstracted message 
	- PL is higher level of abstraction than ISA
- **Application Programming Interface** (API)
	- set of functions or "interface" exposed by (single or set of) program(s) for use by humans / other programs
- **Data** is digital rep. of info stored, processed, displayed, retrieved, sent by program.

Types of programs include...
- **Firmware** which is read-only programs "baked into" device to offer basic hardware control functionalities
- **Operating System** (OS) is collections of related programs that work as platform to access application software
	- Utilizes hardware more easily
	- ex) Linux, Windows, MacOS
- **App Software** is program(s) that can manipulate data, interfaced for human use
	- ex) excel, chrome, postgres

Why learn low level systems?
>Data scientists need to scale applications for cost efficiently for Big Data

Data Scientist: Coined as a person with a most versatile skillset to perform all-in-one tasks such as...
- handling computationally any size of datasets 
- possessing statistical prowess and modeling skills 
- understanding and programming with databases 
- solving problems; visualize, communicate well 
- extracting business value from data

aka, jack of all trades...

In the future, there will be new data types, new hardware especially for LLM usage, evolving data file formats for cloud / clusters (Kubernates) and there is stronger/better storage hardware

Job roles...
- Statistician 
- Analyst
- Product DS 
- Half-stack DS 
- Full-stack DS 
- Machine Learning Engineer 
- Software Engineer, AI/ML (usually synonymous with MLE)

Which has hierarchy of...
- Associate Data Scientist 
- Data Scientist 
- Senior Data Scientist 
- Staff Data Scientist <-> Manager DS 
- (Senior Staff Data Scientist) <-> Senior Manager DS Principal 
- Data Scientist <-> Director DS, Sr Director, Or VP 
- (Senior Principal Data Scientist) 
- (Distinguished / Architect / etc) 
- (Chief AI Officer)

So what is **Data**?

## Digital Representation of Data
**Bits**: All data are sequences of 0 & 1 (binary)
- easily manip. to high-low/off-on electromagnetism
- layers of *abstraction* to interpret bit sequences that result in distinguishable outcomes
**Data type**: first layer of abstraction to interpret bit seq. with human-understandable category of info
- interpretation fixed by programming lang (PL)
- ex) Boolean, Byte, Int, float, char, str
**Data structure**: second layer abstraction to organize mult. instance of data types as complex objs.
- ex) array, linked list, tuple, graph, etc.
![[Pasted image 20250401163751.png]]

**Byte** is 8 bits and is basic unit of data types
Boolean -> T/F, Y/N, 1 bit needed but actual size is 1B (7 bits wasted)

Integer is 4 bytes and has many variants
- Java *int* represents -2^(31)



#### Reference