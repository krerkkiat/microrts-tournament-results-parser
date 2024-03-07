# MicroRTS TRP (Tournament Result Parser)



## Installation

```console
python -m pip install git+https://github.com/krerkkiat/microrts-trp.git@v0.1.2
```

## Usage

```console
python -m microrts_trp view map-folder/
```

Example of parsing one of the map folder from the [official result of the 2023 competition](https://github.com/rubensolv/MicroRTS2023Competition).

```console
$ git clone https://github.com/rubensolv/MicroRTS2023Competition.git
$ cd MicroRTS2023Competition/FourBWorkers8x8/tournament_2/
$ python -m microrts_trp view ./tournament.csv 
Map: maps/8x8/FourBasesWorkers8x8.xml
Number of AIs: 17
Total battles / bot: 34
| Bot                                     |   Win Rate |
|-----------------------------------------|------------|
| RAISocketAI                             |      91.18 |
| mayari{AStarPathFinding}                |      82.35 |
| ObiBotKenobi                            |      82.35 |
| NaiveMCTS(100, -1, 100,10,0.3, 1.0, ... |      76.47 |
| 2L                                      |      66.18 |
| MyMicroRtsBot(AStarPathFinding)         |      61.76 |
| Aggrobot(AStarPathFinding)              |      58.82 |
| POWorkerRush(AStarPathFinding)          |      55.88 |
| SaveTheBeesV4(AStarPathFinding)         |      51.47 |
| bRHEAdBot                               |      47.06 |
| myBot                                   |      38.24 |
| sophia                                  |      33.82 |
| POLightRush(AStarPathFinding)           |      32.35 |
| Ragnar                                  |      26.47 |
| RandomBiasedAI                          |      23.53 |
| NIlSiBot(GreedyPathFinding)             |      14.71 |
| Predator                                |       5.88 |
```
