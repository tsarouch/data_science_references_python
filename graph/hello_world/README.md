### Hello World example
Find details here:
https://neo4j.com/docs/operations-manual/current/tutorial/import-tool/
</br>
This is a simple example of importing .csv files in the neo4j DB
</br>

### Install
from here: https://neo4j.com/download-center/
- download the community edition
- unzip
- declare top dir as $NEO4J_HOME
- Change directory to: $NEO4J_HOME
- Run ./bin/neo4j console
  - in case jvm is not yet installed, try to donwload & install it with https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
  - jre is not enough, we need to install jdk too https://www.oracle.com/technetwork/pt/java/javase/downloads/jdk8-downloads-2133151.html
- Stop the server by typing Ctrl-C in the console.
(When Neo4j runs in console mode, logs are printed to the terminal)


### Import Shell cmd (for fast DB population)
> $NEO4J_HOME/bin/neo4j-admin import --nodes data/movies.csv --nodes data/actors.csv --relationships data/roles.csv
We expect to see something like
```
IMPORT DONE in 991ms. 
Imported:
  6 nodes
  9 relationships
  15 properties
Peak memory usage: 1.00 GB
```

### Run console
> $NEO4J_HOME/bin/neo4j console
We wxpect to see something lke:
```
2019-01-27 15:25:31.233+0000 INFO  Starting...
^[[B2019-01-27 15:25:43.969+0000 INFO  Bolt enabled on 127.0.0.1:7687.
2019-01-27 15:25:45.908+0000 INFO  Started.
2019-01-27 15:25:46.945+0000 INFO  Remote interface available at **http://localhost:7474/**
```