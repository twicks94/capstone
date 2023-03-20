# -*- coding: utf-8 -*-
"""Capstone wOBA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13roTOEPV9kLyblFc0fI7xoCDyTplUCZ0
"""

import os
colab = 1

if colab == 1:
  from google.colab import drive
  drive.mount('/content/drive', force_remount = True)
  current_folder = 'Capstone'
  dest_folder = '/content/drive/My Drive/' + current_folder
  os.chdir(dest_folder)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def wobaYearWeight(year):
  if year == '2017':
    return (0.721409, 0.75488, 0.933841, 1.39309, 1.84695, 2.18011)

  elif year == '2018':
    return (0.729725, 0.758507, 0.941035, 1.41412, 1.82053, 2.19929)

  elif year == '2019':
    return (0.739806, 0.767695, 0.941771, 1.38062, 1.79559, 2.14158)

  elif year == '2020':
    return (0.756437, 0.781897, 0.955415, 1.39774, 1.81123, 2.1401)

  elif year == '2021':
    return (0.73817, 0.767148, 0.932931, 1.34641, 1.74889, 2.09657)

  elif year == '2022':
    return (0.738822, 0.765579, 0.92845, 1.34266, 1.71558, 2.0296)

def wOBACalc(file, playerName, pitchType, year, ubbFact = .738822, hbpFact = .765579, oneBFact = .92845, twoBFact = 1.34266, threeBFact = 1.71558, hrFact = 2.0296):

  bbFile = pd.read_csv(file)

  player = bbFile.loc[bbFile['Pitcher'] == playerName]

  if pitchType != 'None':
    
    player = player.loc[player['TaggedPitchType'] == pitchType]

  ubbFact, hbpFact, oneBFact, twoBFact, threeBFact, hrFact = wobaYearWeight(year)

  single = player.loc[player['PlayResult'] == 'Single']
  double = player.loc[player['PlayResult'] == 'Double']
  triple = player.loc[player['PlayResult'] == 'Triple']
  homerun = player.loc[player['PlayResult'] == 'HomeRun']
  hitbypitch = player.loc[player['PitchCall'] == 'HitByPitch']

  intentionalWalk = player.loc[player[ 'PitchCall'] == 'BallIntentional']
  unintentionalWalk = player.loc[player['KorBB'] == 'Walk']

  #Throw out undefined in playresult and add in results from korbb

  kbb = player.loc[player['KorBB'] != 'Undefined']
  play = player.loc[player['PlayResult'] != 'Undefined']


  sacrifice = player.loc[player['PlayResult'] == 'Sacrifice']

  sacrificefly = sacrifice.loc[sacrifice['TaggedHitType'] == 'FlyBall']
  sacrificehit = sacrifice.loc[sacrifice['TaggedHitType'] == 'Bunt']

  oneB = len(single)
  twoB = len(double)
  threeB = len(triple)
  hr = len(homerun)
  hbp = len(hitbypitch)
  ubb = len(unintentionalWalk) - len(intentionalWalk)
  ab = len(play) + len(kbb)
  sf = len(sacrificefly)
  sh = len(sacrificehit)


  if (((ab - sh) + ubb + sf + hbp) == 0):
    return 'UNDEFINED - DIVIDED BY ZERO'
    

  playerWOBA = (ubbFact * ubb + hbpFact * hbp + oneBFact * oneB + twoBFact * twoB + threeBFact * threeB + hrFact + hr) / ((ab - sh) + ubb + sf + hbp)

  return playerWOBA

def IndivwOBACalc(file, ubbFact = .738822, hbpFact = .765579, oneBFact = .92845, twoBFact = 1.34266, threeBFact = 1.71558, hrFact = 2.0296):

  ##print(bbFile.Pitcher.unique())

  playerName = input('\n Enter player name (Last, First): ')

  ##print('\n', bbFile.TaggedPitchType.unique())

  pitchType = input('\n Filter by pitch type(None, Fastball, etc.): ')

  year = input("\n Enter wOBA Factor Year: ")

  playerWOBA = wOBACalc(file, playerName, pitchType, year)

  if pitchType != 'None':
    print('\n' + playerName + "'s wOBA (for pitch type: " + pitchType + ") is: " + str(playerWOBA))

  else:
    print('\n' + playerName + "'s wOBA is: " + str(playerWOBA))

IndivwOBACalc('combined-all-fixed-names.csv')

inFile = pd.read_csv('combined-all-fixed-names.csv')

inFile.TaggedPitchType.unique()

graphWoba = pd.DataFrame(columns = ['Name', 'RelSpeed','VertRelAngle','HorzRelAngle','SpinRate','SpinAxis', 'RelHeight','RelSide','Extension','HorzBreak', 'PlateLocHeight', 
                                    'PlateLocSide','ZoneSpeed','VertApprAngle','HorzApprAngle','ZoneTime','EffectiveVelo','SpeedDrop', 'wOBA'])

playerName = inFile.Pitcher.unique()

file = 'combined-all-fixed-names.csv'

for i in playerName:

  woba = wOBACalc(file, i, 'None', '2022')

  player = inFile.loc[inFile['Pitcher'] == i]

  relSpeed = player["RelSpeed"].mean()

  vertAngle = player["VertRelAngle"].mean()

  horzAngle = player["HorzRelAngle"].mean()

  spinRate = player["SpinRate"].mean()

  spinAxis = player["SpinAxis"].mean()

  relHeight = player["RelHeight"].mean()

  relSide = player["RelSide"].mean()

  ext = player["Extension"].mean()

  horzBreak = player["HorzBreak"].mean()

  plateHeight = player["PlateLocHeight"].mean()

  plateSide = player["PlateLocSide"].mean()

  zoneSpeed = player["ZoneSpeed"].mean()

  vertAngle = player["VertApprAngle"].mean()

  horzAngle = player["HorzApprAngle"].mean()

  zoneTime = player["ZoneTime"].mean()

  effectVelo = player["EffectiveVelo"].mean()

  speedDrop = player["SpeedDrop"].mean()


  new_row = {'Name':i, 'RelSpeed':relSpeed, 'VertRelAngle':vertAngle,'HorzRelAngle':horzAngle,'SpinRate':spinRate,'SpinAxis':spinAxis, 'RelHeight':relHeight,'RelSide':relSide,'Extension':ext,
             'HorzBreak':horzBreak, 'PlateLocHeight':plateHeight, 'PlateLocSide':plateSide ,'ZoneSpeed':zoneSpeed, 'VertApprAngle':vertAngle, 'HorzApprAngle':horzAngle, 'ZoneTime':zoneTime,
             'EffectiveVelo':effectVelo, 'SpeedDrop':speedDrop, 'wOBA':woba}
  graphWoba = graphWoba.append(new_row, ignore_index=True)

graphWoba

import seaborn as sn
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(20, 10))

corr_matrix = graphWoba.corr()
sn.heatmap(corr_matrix, annot=True)

plt.show()

import plotly.express as px

fig = px.bar(graphWoba, x="Name", y="wOBA", color = "Name")
fig.show()

fig = px.bar(graphWoba, x="Name", y="wOBA", color = "RelHeight")
fig.show()

fig = px.bar(graphWoba, x="Name", y="wOBA", color = "SpinRate")
fig.show()