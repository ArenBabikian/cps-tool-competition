#!/bin/bash

current_date_time=$(date '+%d-%H-%M-%S')

# python competition.py \
#     --time-budget 1800 \
#     --executor beamng \
#     --beamng-home "C:\applications\BeamNG.tech.v0.26.2.0" \
#     --beamng-user "C:\applications\BeamNG.tech.v0.26.2.0_userpath" \
#     --map-size 200 \
#     --speed-limit 70 \
#     --oob-tolerance 0.85 \
#     --log-to "C:\git\cps-tool-competition\optangle\_log\\${current_date_time}.log" \
#     --module-path optangle \
#     --module-name  src.optangle \
#     --class-name OptAngleGenerator

# python competition.py \
#     --time-budget 1800 \
#     --executor dave2 \
#     --dave2-model "C:\git\cps-tool-competition\dave2\beamng-dave2.h5" \
#     --beamng-home "C:\applications\BeamNG.tech.v0.26.2.0" \
#     --beamng-user "C:\applications\BeamNG.tech.v0.26.2.0_userpath" \
#     --map-size 200 \
#     --speed-limit 25 \
#     --oob-tolerance 0.1 \
#     --log-to "C:\git\cps-tool-competition\optangle\_log\\${current_date_time}.log" \
#     --module-path optangle \
#     --module-name  src.optangle \
#     --class-name OptAngleGenerator
    
python competition.py \
    --time-budget 10 \
    --executor beamng \
    --beamng-home "C:\applications\BeamNG.tech.v0.26.2.0" \
    --beamng-user "C:\applications\BeamNG.tech.v0.26.2.0_userpath" \
    --map-size 200 \
    --module-name sample_test_generators.one_test_generator \
    --class-name OneTestGenerator
