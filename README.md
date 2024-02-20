# microrts_trp

## Installation

```console
python -m pip install https://github.com/krerkkiat/microrts-tournament-results-parser.git
```

## Usage

```console
python -m microrts_trp map-folder/
```

Example of parsing one of the map folder from the [official result of the 2023 competition](https://github.com/rubensolv/MicroRTS2023Competition).

```console
$ git clone https://github.com/rubensolv/MicroRTS2023Competition.git
$ cd MicroRTS2023Competition
$ rm -rf ./FourBWorkers8x8/tournament_1  # since the it is not used in the official one.
$ python -m microrts_trp ./FourBWorkers8x8
Map: FourBWorkers8x8
Number of AIs: 17
| Bot                                     |   Win Rate |
|-----------------------------------------|------------|
| RAISocketAI                             |      90.00 |
| mayari{AStarPathFinding}                |      82.94 |
| ObiBotKenobi                            |      81.76 |
| NaiveMCTS(100, -1, 100,10,0.3, 1.0, ... |      75.59 |
| 2L                                      |      65.59 |
| Aggrobot(AStarPathFinding)              |      62.06 |
| MyMicroRtsBot(AStarPathFinding)         |      61.47 |
| POWorkerRush(AStarPathFinding)          |      60.00 |
| SaveTheBeesV4(AStarPathFinding)         |      51.76 |
| bRHEAdBot                               |      50.00 |
| myBot                                   |      38.24 |
| POLightRush(AStarPathFinding)           |      34.71 |
| sophia                                  |      32.94 |
| RandomBiasedAI                          |      28.24 |
| Ragnar                                  |      22.94 |
| NIlSiBot(GreedyPathFinding)             |      12.35 |
| Predator                                |       5.88 |
```

Note that in the `competitionDataPreparation.xlsx`, the number used is `160`, but since there are 17 bots we
are using `170`.
