# Railway-Scheduling

## About

This project uses Anser Set Programming (ASP), specifically [clingo](https://potassco.org/clingo/), to solve train scheduling problems. As an framework for instance generation and testing we use [flatland](https://flatland.aicrowd.com/intro.html).

## Directory Structure
- './encodinds/' contains all ASP related files used for the scheduling
- './instances/' contains all instances used for testing
- './tools/' contains all tools and scripts, e.g. for instance generation

## Encodings
- contains prototyp solver

## Instances
- 'test' our minimal instance with a 2x3 grid and one agent
- 'testing' is a randomly generated instance with two agents
- '5_5_1a' is a bigger(5x5) intance with one agent
- '5_5_2a_crossing' is a instance with a crossing in the middle that 2 agents need to pass
- '5_5_2a_switches' is a 5x5 grid with 2 agents a multiple switches
- '7_7_4a_circle' is a instance with 4 agents that need to move in a circle
- '7_7_4a_wait' is a instance with 4 agents where 2 agents need to wait in order for all agents to reach their target

## Tools
- 'instance_gen.py' is a script used to generate and visulize custom maps with randomly palced agents
- 'generation.py' is a script to generate completly random maps with randomly placed agents
