import os
import sys
import logging
import itertools
import numpy as np
import argparse
import math
import errno

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()

import CombineLimits.Limits.Models as Models
from CombineLimits.Limits.Limits import Limits
from CombineLimits.Limits.utilities import *

from HaaLimits2DNew import *

XRANGE = [2.5, 30]
YRANGE = [0, 1200]
UPSILONRANGE = [8,11]
AMASSES = ['3p6',4,5,6,7,9,11,13,15,17,19,21]
HMASSES = [[125,300,750]
subdirectoryName='mumufourBody_SEP5_DG/'
name = 'mmmt_mm_parametric'
IFCONTROL = True

def getDataset(ds,weight='w',selection='1',xRange=[],yRange=[]):
   args = ds.get()
   if xRange: 
     args.find('x').setRange(*xRange)
   if args.find('y1'): 
     args.find('y1').SetName('y')     
     args.find('y').SetTitle('y')
   if yRange: 
     args.find('y').setRange(*yRange)
   ds = ROOT.RooDataSet(ds.GetName(),ds.GetTitle(),ds,args,selection,weight)
   return ds

def getTH1F(hist, dic, xMin=0, xMax=30, shift='', name='', region='PP'):
   width = hist.GetBinWidth(3)
   binedge = 0
   newHist = ROOT.TH1F(hist.GetName(), hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
   newHist.SetDirectory(0)
   newHist.AddDirectory(False)
   for i in range(hist.GetNbinsX() ):
      upperEdge = hist.GetBinCenter(i) + width/2
      lowerEdge = hist.GetBinCenter(i) - width/2
      if upperEdge > xMin and lowerEdge < xMax:
         newHist.SetBinContent(i, hist.GetBinContent(i) )
         newHist.SetBinError(i,   hist.GetBinError(i) )
      else:
         newHist.SetBinContent(i,0)
         newHist.SetBinError(i, 0)
   dic[region][shift][name] = newHist

def GetPPData(dictionary,xRange=[], yRange=[], rooDataSet=False):
   f_FRC = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/FINAL_RooDataSet_MiniAOD_SingleMu_MedIsoMu2_TauDMAntiMedIso_SEP2_AFromB_Plots.root")
   f_FRD = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/FINAL_RooDataSet_MiniAOD_SingleMu_MedIsoMu2_TauDMAntiMedIso_SEP2_AFromBDOWN_Plots.root")
   f_FRU = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/FINAL_RooDataSet_MiniAOD_SingleMu_MedIsoMu2_TauDMAntiMedIso_SEP2_AFromBUP_Plots.root")

   if rooDataSet:
      SingleMu_FakeRateCentral = f_FRC.Get("mumufourBodymass_dataset")
      SingleMu_FakeRateDOWN    = f_FRD.Get("mumufourBodymass_dataset")
      SingleMu_FakeRateUP      = f_FRU.Get("mumufourBodymass_dataset")
      SingleMu_FakeRateCentral = getDataset(SingleMu_FakeRateCentral, selection='x <= ' + str(XRANGE[1]) + ' && x >= ' + str(XRANGE[0]), xRange=xRange, yRange=yRange)
      SingleMu_FakeRateDOWN = getDataset(SingleMu_FakeRateDOWN,    selection='x <= ' + str(XRANGE[1]) + ' && x >= ' + str(XRANGE[0]), xRange=xRange, yRange=yRange)
      SingleMu_FakeRateUP = getDataset(SingleMu_FakeRateUP,      selection='x <= ' + str(XRANGE[1]) + ' && x >= ' + str(XRANGE[0]), xRange=xRange, yRange=yRange)
      dictionary['PP']['']['data']         = SingleMu_FakeRateCentral
      dictionary['PP']['FakeUp']['data']   = SingleMu_FakeRateUP
      dictionary['PP']['FakeDown']['data'] = SingleMu_FakeRateDOWN
      dictionary['PP']['']['dataNoSig']         = SingleMu_FakeRateCentral
      dictionary['PP']['FakeUp']['dataNoSig']   = SingleMu_FakeRateUP
      dictionary['PP']['FakeDown']['dataNoSig'] = SingleMu_FakeRateDOWN
   else:
      SingleMu_FakeRateCentral = f_FRC.Get("mumu_Mass")
      SingleMu_FakeRateDOWN    = f_FRD.Get("mumu_Mass")
      SingleMu_FakeRateUP      = f_FRC.Get("mumu_Mass")
      getTH1F(SingleMu_FakeRateCentral, xMin=XRANGE[0], xMax=XRANGE[1], shift='',         name='data', dic=dictionary, region='PP')
      getTH1F(SingleMu_FakeRateDOWN,    xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeDown', name='data', dic=dictionary, region='PP')
      getTH1F(SingleMu_FakeRateUP,      xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeUp',   name='data', dic=dictionary, region='PP')
      getTH1F(SingleMu_FakeRateCentral, xMin=XRANGE[0], xMax=XRANGE[1], shift='',         name='dataNoSig', dic=dictionary, region='PP')
      getTH1F(SingleMu_FakeRateDOWN,    xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeDown', name='dataNoSig', dic=dictionary, region='PP')
      getTH1F(SingleMu_FakeRateUP,      xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeUp',   name='dataNoSig', dic=dictionary, region='PP')

def GetPPSignal(dictionary,xRange=[],yRange=[], rooDataSet=False):
  f = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/FINAL_AllRooDataSet_MedIsoMu2_TauDMMedIso_SEP2.root")

  for hMass in HMASSES:
     if  hMass== 125: yRange = [20, 150]
     elif hMass== 300: yRange = [40,360]
     elif hMass== 750: yRange = [140,900]
     for aMass in AMASSES:
       if (str(hMass) == "300" or str(hMass) == "750") and (str(aMass) == "3p6" or str(aMass) == "4" or str(aMass) == "6"): continue
       h_Central    = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_Central_Plots_fourBody")
       h_IDDOWN     = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_IDDOWN_Plots_fourBody")
       h_IDUP       = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_IDUP_Plots_fourBody")
       h_IsoDOWN    = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_IsoDOWN_Plots_fourBody")
       h_IsoUP      = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_IsoUP_Plots_fourBody")
       h_PileupDOWN = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_PileupDOWN_Plots_fourBody")
       h_PileupUP   = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMMedIso_SEP2_PileupUP_Plots_fourBody")

       if not rooDataSet:
          getTH1F(h_Central,    xMin=0, xMax=30, shift='',           name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_IDDOWN,     xMin=0, xMax=30, shift='IDDown',     name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_IDUP,       xMin=0, xMax=30, shift='IDUp',       name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_IsoDOWN,    xMin=0, xMax=30, shift='IsoDown',    name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_IsoUP,      xMin=0, xMax=30, shift='IsoUp',      name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_PileupDOWN, xMin=0, xMax=30, shift='PileupDown', name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
          getTH1F(h_PileupUP,   xMin=0, xMax=30, shift='PileupUp',   name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='PP')
       else:
          h_Central   = getDataset(h_Central,    selection='', xRange=[0,30], yRange=yRange)
          h_IDDOWN    = getDataset(h_IDDOWN,     selection='', xRange=[0,30], yRange=yRange)
          h_IDUP      = getDataset(h_IDUP,       selection='', xRange=[0,30], yRange=yRange)
          h_IsoDOWN   = getDataset(h_IsoDOWN,    selection='', xRange=[0,30], yRange=yRange)
          h_IsoUP     = getDataset(h_IsoUP,      selection='', xRange=[0,30], yRange=yRange)
          h_PileupDOWN= getDataset(h_PileupDOWN, selection='', xRange=[0,30], yRange=yRange)
          h_PileupUP  = getDataset(h_PileupUP,   selection='', xRange=[0,30], yRange=yRange)
          dictionary['PP']['']["HToAAH" + str(hMass) + "A" + str(aMass)]           = h_Central
          dictionary['PP']['IDUp']["HToAAH" + str(hMass) + "A" + str(aMass)]       = h_IDUP
          dictionary['PP']['IDDown']["HToAAH" + str(hMass) + "A" + str(aMass)]     = h_IDDOWN
          dictionary['PP']['IsoUp']["HToAAH" + str(hMass) + "A" + str(aMass)]      = h_IsoUP
          dictionary['PP']['IsoDown']["HToAAH" + str(hMass) + "A" + str(aMass)]    = h_IsoDOWN
          dictionary['PP']['PileupUp']["HToAAH" + str(hMass) + "A" + str(aMass)]   = h_PileupUP
          dictionary['PP']['PileupDown']["HToAAH" + str(hMass) + "A" + str(aMass)] = h_PileupDOWN


def GetFPData(dictionary,xRange=[],yRange=[], rooDataSet=False):

   f_FakeRateRegionB = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/MiniAOD_SingleMu_MedIsoMu2_TauDMAntiMedIso_SEP2_BItself_Plots.root")
   if rooDataSet:
      SingleMu_RegionB = f_FakeRateRegionB.Get("mumufourBodymass_dataset")
      SingleMu_RegionB = getDataset(SingleMu_RegionB, selection='x <= ' + str(XRANGE[1]) + ' && x >= ' + str(XRANGE[0]), xRange=xRange, yRange=yRange)
      dictionary['FP']['']['data']         = SingleMu_RegionB
      dictionary['FP']['FakeUp']['data']   = SingleMu_RegionB
      dictionary['FP']['FakeDown']['data'] = SingleMu_RegionB
      dictionary['FP']['']['dataNoSig']         = SingleMu_RegionB
      dictionary['FP']['FakeUp']['dataNoSig']   = SingleMu_RegionB
      dictionary['FP']['FakeDown']['dataNoSig'] = SingleMu_RegionB
   else:
      SingleMu_RegionB = f_FakeRateRegionB.Get("mumu_Mass")
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='',         name='data', dic=dictionary, region='FP')
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeUp',   name='data', dic=dictionary, region='FP')
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeDown', name='data', dic=dictionary, region='FP')
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='',         name='dataNoSig', dic=dictionary, region='FP')
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeUp',   name='dataNoSig', dic=dictionary, region='FP')
      getTH1F(SingleMu_RegionB, xMin=XRANGE[0], xMax=XRANGE[1], shift='FakeDown', name='dataNoSig', dic=dictionary, region='FP')

def GetFPSignal(dictionary,xRange=[], yRange=[], rooDataSet=False):
  f = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/FINAL_AllRooDataSet_MedIsoMu2_TauDMAntiMedIso_SEP2.root")

  for hMass in HMASSES:
     if  hMass== 125: yRange = [20, 150]
     elif hMass== 300: yRange = [40,360]
     elif hMass== 750: yRange = [140,900]
     for aMass in AMASSES:
       if (str(hMass) == "300" or str(hMass) == "750") and (str(aMass) == "3p6" or str(aMass) == "4" or str(aMass) == "6"): continue
       h_Central    = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_Central_Plots_fourBody")
       h_IDDOWN     = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_IDDOWN_Plots_fourBody")
       h_IDUP       = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_IDUP_Plots_fourBody")
       h_IsoDOWN    = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_IsoDOWN_Plots_fourBody")
       h_IsoUP      = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_IsoUP_Plots_fourBody")
       h_PileupDOWN = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_PileupDOWN_Plots_fourBody")
       h_PileupUP   = f.Get("SIG_h" + str(hMass) + "a" + str(aMass) + "_MedIsoMu2_TauDMAntiMedIso_SEP2_PileupUP_Plots_fourBody")

       if not rooDataSet:
           getTH1F(h_Central,    xMin=0, xMax=30, shift='',           name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_IDDOWN,     xMin=0, xMax=30, shift='IDDown',     name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_IDUP,       xMin=0, xMax=30, shift='IDUp',       name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_IsoDOWN,    xMin=0, xMax=30, shift='IsoDown',    name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_IsoUP,      xMin=0, xMax=30, shift='IsoUp',      name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_PileupDOWN, xMin=0, xMax=30, shift='PileupDown', name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
           getTH1F(h_PileupUP,   xMin=0, xMax=30, shift='PileupUp',   name="HToAAH" + str(hMass) + "A" + str(aMass), dic=dictionary, region='FP')
       else:
          print hMass, aMass 
          h_Central    = getDataset(h_Central,    selection='', xRange=[0,30], yRange=yRange)
          h_IDDOWN     = getDataset(h_IDDOWN,     selection='', xRange=[0,30], yRange=yRange)
          h_IDUP       = getDataset(h_IDUP,       selection='', xRange=[0,30], yRange=yRange)
          h_IsoDOWN    = getDataset(h_IsoDOWN,    selection='', xRange=[0,30], yRange=yRange)
          h_IsoUP      = getDataset(h_IsoUP,      selection='', xRange=[0,30], yRange=yRange)
          h_PileupDOWN = getDataset(h_PileupDOWN, selection='', xRange=[0,30], yRange=yRange)
          h_PileupUP   = getDataset(h_PileupUP,   selection='', xRange=[0,30], yRange=yRange)
          dictionary['FP']['']["HToAAH" + str(hMass) + "A" + str(aMass)]           = h_Central
          dictionary['FP']['IDUp']["HToAAH" + str(hMass) + "A" + str(aMass)]       = h_IDUP
          dictionary['FP']['IDDown']["HToAAH" + str(hMass) + "A" + str(aMass)]     = h_IDDOWN
          dictionary['FP']['IsoUp']["HToAAH" + str(hMass) + "A" + str(aMass)]      = h_IsoUP
          dictionary['FP']['IsoDown']["HToAAH" + str(hMass) + "A" + str(aMass)]    = h_IsoDOWN
          dictionary['FP']['PileupUp']["HToAAH" + str(hMass) + "A" + str(aMass)]   = h_PileupUP
          dictionary['FP']['PileupDown']["HToAAH" + str(hMass) + "A" + str(aMass)] = h_PileupDOWN

if not IFCONTROL:
  dictionary = {'PP' : {
                   '' : {},
                   'IDUp' : {},
                   'IDDown' : {},
                   'PileupUp' : {},
                   'PileupDown' : {},
                   'IsoUp' : {},
                   'IsoDown' : {},
                   'FakeUp' : {},
                   'FakeDown' : {}
                       },
                'FP' : {
                   '' : {},
                   'IDUp' : {},
                   'IDDown' : {},
                   'PileupUp' : {},
                   'PileupDown' : {},
                   'IsoUp' : {},
                   'IsoDown' : {},
                   'FakeUp' : {},
                   'FakeDown' : {}
                       }
               }
else:
  dictionary = {'PP' : {
                   '' : {},
                   'IDUp' : {},
                   'IDDown' : {},
                   'PileupUp' : {},
                   'PileupDown' : {},
                   'IsoUp' : {},
                   'IsoDown' : {},
                   'FakeUp' : {},
                   'FakeDown' : {}
                       },
                'FP' : {
                   '' : {},
                   'IDUp' : {},
                   'IDDown' : {},
                   'PileupUp' : {},
                   'PileupDown' : {},
                   'IsoUp' : {},
                   'IsoDown' : {},
                   'FakeUp' : {},
                   'FakeDown' : {}
                       },
                'control': {'' :{} }
               }
  
  f = ROOT.TFile.Open("/eos/cms/store/user/ktos/ShapeDifferences/control.root")
  control = f.Get("mmMass")
  dictionary['control']['']['data'] = control
  dictionary['control']['']['dataNoSig'] = control




GetPPSignal(dictionary, xRange=XRANGE, yRange=YRANGE, rooDataSet=True)
GetPPData(dictionary,   xRange=XRANGE, yRange=YRANGE, rooDataSet=True)
GetFPData(dictionary,   xRange=XRANGE, yRange=YRANGE, rooDataSet=True)
GetFPSignal(dictionary, xRange=XRANGE, yRange=YRANGE, rooDataSet=True)

LimitsClass = HaaLimits2D(dictionary, tag='mumufourBody_SEP5_DG')
LimitsClass.YRANGE = YRANGE
LimitsClass.XRANGE = XRANGE
LimitsClass.UPSILONRANGE = UPSILONRANGE
LimitsClass.SHIFTS = ['Pileup','ID','Iso','Fake']
LimitsClass.BACKGROUNDSHIFTS = ['Fake']
LimitsClass.SIGNALSHIFTS = ['Pileup','ID','Iso']
LimitsClass.HMASSES = HMASSES
LimitsClass.REGIONS = ['FP','PP']
LimitsClass.AMASSES = AMASSES
LimitsClass.initializeWorkspace()

####################################
# Devin's code
####################################
if IFCONTROL: LimitsClass.addControlModels(voigtian=True)#, is2D=False)
LimitsClass.addBackgroundModels(voigtian=True,logy=False,fixAfterControl=IFCONTROL)

LimitsClass.XRANGE = [0,30]
LimitsClass.addSignalModels(fit=False, yFitFuncFP="DG", yFitFuncPP="DG",  isKinFit=False)
LimitsClass.XRANGE = XRANGE
if IFCONTROL: LimitsClass.addControlData()
LimitsClass.addData(asimov=True)

LimitsClass.setupDatacard(addControl=IFCONTROL)
LimitsClass.addSystematics(addControl=IFCONTROL)
LimitsClass.save(name=name, subdirectory=subdirectoryName)
