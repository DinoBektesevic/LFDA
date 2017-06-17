#!/bin/bash

##Copy the exact SDSS tree structure from boss onwards,
##somewhere on your machine and point BOSS to that address
export BOSS=/home/boss
export FITSDMP=/home/LFDS/fits_dump/

##change following env.var. at your own risk: 
export PHOTO_REDUX=$BOSS/photo/redux
export BOSS_PHOTOOBJ=$BOSS/photoObj
export BOSS_CAS=$BOSS/CAS

##Feel free to change your Python version
##not compatible to Python3
idle-python2.7&
