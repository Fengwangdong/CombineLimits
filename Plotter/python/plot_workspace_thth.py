import os, sys
import json

import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import CombineLimitsRunII.Plotter.CMS_lumi as CMS_lumi
import CombineLimitsRunII.Plotter.tdrstyle as tdrstyle

sys.path.append(r'/Users/chris/ModulesAndPackages')

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
tdrstyle.setTDRStyle()

isprelim = True
yvar = 'h'
h = 125
xVar = 'invMassMuMu'
yVar = 'visFourbodyMass'
#massRange = 'lowmass'
massRange = 'upsilon'
#massRange = 'highmass'
if massRange == 'lowmass':
    xRange = [2.5,8.5]
    xBinWidth = 0.1
    a = 5
elif massRange == 'upsilon':
    xRange = [6,14]
    xBinWidth = 0.1
    a = 11
elif massRange == 'highmass':
    xRange = [11,45]
    xBinWidth = 0.5
    a = 15

yRange = [0,1200]
yBinWidth = 10
blind = True
br = 0.0005
doPostfit = False

amasses = ['3p6','5','9','13','17','21']
colors = [ROOT.kBlue-4, ROOT.kCyan+1, ROOT.kGreen+1, ROOT.kOrange-3, ROOT.kRed+1, ROOT.kMagenta+1]

#jfile = 'fitParams/HaaLimits2D_unbinned_{}/with1DFits/background_PP.json'.format(yvar)
jfile = '../../HaaLimits/python/fitParams/HaaLimits2D_unbinned_{}/{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly/background_TauHadTauHad_V3_2018_PP.json'.format(yvar,massRange)
with open(jfile,'r') as f:
    results = json.load(f)

jfile_fakeUp = '../../HaaLimits/python/fitParams/HaaLimits2D_unbinned_{}/{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly/background_TauHadTauHad_V3_2018_PP_fakeUp.json'.format(yvar,massRange)
with open(jfile_fakeUp,'r') as f:
    results_fakeUp = json.load(f)

jfile_fakeDown = '../../HaaLimits/python/fitParams/HaaLimits2D_unbinned_{}/{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly/background_TauHadTauHad_V3_2018_PP_fakeDown.json'.format(yvar,massRange)
with open(jfile_fakeDown,'r') as f:
    results_fakeDown = json.load(f)

jfile_control = '../../HaaLimits/python/fitParams/HaaLimits2D_unbinned_{}/{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly/background_control_2018.json'.format(yvar,massRange)
with open(jfile_control,'r') as f:
    results_control = json.load(f)

#rfile = '../../HaaLimits/python/datacards_shape/MuMuTauTau/mmmt_mm_{}_parametric_unbinned_{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly.root'.format(yvar,massRange)
rfile = '../../HaaLimits/python/datacards_shape/MuMuTauTau/mmmt_mm_{}_parametric_unbinned_unblind_{}_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeJECFit_PPonly.root'.format(yvar,massRange)
tfile = ROOT.TFile.Open(rfile)

ws = tfile.Get('w')
ws.Print()

pdf_control = ws.pdf("bg_control_2018")
pdf_x = ws.pdf('bg_TauHadTauHad_V3_2018_PP_x')
pdf_y = ws.pdf('bg_TauHadTauHad_V3_2018_PP_y')

# override values
params = [
    # x
    'lambda_cont1_PP_x',
    'lambda_cont3_PP_x',
    'mean_jpsi1S',
    'sigma_jpsi1S',
    'width_jpsi1S',
    'mean_jpsi2S',
    'sigma_jpsi2S',
    'width_jpsi2S',
    'mean_upsilon1S',
    'sigma_upsilon1S',
    'width_upsilon1S',
    'mean_upsilon2S',
    'sigma_upsilon2S',
    'width_upsilon2S',
    'mean_upsilon3S',
    'sigma_upsilon3S',
    'width_upsilon3S',


    # y
    'lambda_conty1_PP_y',
    'erfShift_erf1_PP_y',
    'erfScale_erf1_PP_y',
]

def floatToText(x):
    s = '{:.1E}'.format(x).split('E')
    return '{} #times 10^{{{}}}'.format(int(float(s[0])),int(s[1]))

if doPostfit:
    jfile = 'impacts_mm_h_unbinned_with1DFits_125_7.json' # for now while the other is not working
    with open(jfile,'r') as f:
        postfit = json.load(f)

    postParams = {}
    for p in postfit['params']:
        postParams[p['name']] = p

    for p in params:
        param = ws.arg(p)
        val = postParams[p]['fit'][1]
        param.setVal(val)

data = ws.data('data_obs_TauHadTauHad_V3_2018_PP')
data_control = ws.data('data_obs')

mh = ws.var('MH')
mh.setVal(h)
ma = ws.var('MA')
ma.setVal(a)

sig_x = ws.pdf('ggH_haa_{}_TauHadTauHad_V3_2018_PP_x'.format(h))
sig_y = ws.pdf('ggH_haa_{}_TauHadTauHad_V3_2018_PP_y'.format(h))
sig_y_heavy = ws.pdf('ggH_haa_{}_TauHadTauHad_V3_2018_PP_y'.format(250))

integral = results['integral']
integral_fakeUp = results_fakeUp['integral']
integral_fakeDown = results_fakeDown['integral']

integral_control = results_control['integral']

print integral, integral_control

sigintegral = ws.function('fullIntegral_ggH_haa_{}_TauHadTauHad_V3_2018_PP'.format(h)).getVal() * br/0.001
sigintegral_heavy = ws.function('fullIntegral_ggH_haa_{}_TauHadTauHad_V3_2018_PP'.format(250)).getVal() * br/0.001 * 10.2/48.58

################################ control ######################################
x = ws.var('invMassMuMu_control_2018')
x.setUnit('GeV')
x.setPlotLabel('m(#mu#mu)')
x.SetTitle('m(#mu#mu)')


canvas = ROOT.TCanvas('c','c',800,800)
canvas.Divide(1,1)
canvas.cd()
padDown=ROOT.TPad("","",0,0,1,0.25)
padDown.SetTopMargin(0.035)
padDown.SetBottomMargin(0.4)
padDown.Draw()
canvas.cd()
padUp=ROOT.TPad("","",0,0.25,1,1)
padUp.SetBottomMargin(0.03)
padUp.SetTopMargin(0.07)
padUp.Draw()

xFrame = x.frame()


#pdf_control.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('Central'))
#pdf_control_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('cont'))

pdf_control.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('Central'))
#pdf_control_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('cont'))
#pdf_control_res.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_res),ROOT.RooFit.AddTo('cont'), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('central'))
data_control.plotOn(xFrame,ROOT.RooFit.Binning(int((xRange[1]-xRange[0])/0.001)))

pull = xFrame.pullHist()

padDown.cd()
padDown.SetGridy(1)
pull.Draw('ap')
#pull.GetXaxis().SetRangeUser(0,810)
pull.GetXaxis().SetLimits(8,12)
#pull.GetXaxis().SetMaximum(800)
pull.SetMaximum(2)
pull.SetMinimum(-2)
#pull.SetMarkerStyle(20)

pull.GetXaxis().SetTitleSize(0.16)
pull.GetXaxis().SetLabelSize(0.12)
pull.GetXaxis().SetTitleOffset(1)
pull.GetXaxis().SetTitle('m(#mu#mu) (GeV)')
pull.GetXaxis().SetNdivisions(510)
pull.GetXaxis().SetTickLength(0.09)

pull.GetYaxis().SetTitleSize(0.16)
pull.GetYaxis().SetLabelSize(0.12)
pull.GetYaxis().SetTitleOffset(0.4)
pull.GetYaxis().SetTitle('Pull')
pull.GetYaxis().SetNdivisions(502)

canvas.cd()
padUp.cd()

xFrame.Draw()
xFrame.GetYaxis().SetTitle('Events / {} GeV'.format(xBinWidth))

CMS_lumi.cmsText = 'CMS'
CMS_lumi.writeExtraText = isprelim
#CMS_lumi.extraText = 'Preliminary'
CMS_lumi.extraText = '#tau_{#mu}#tau_{h}'
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (59.8)
CMS_lumi.CMS_lumi(canvas,4,11)

if massRange == 'lowmass' or massRange == 'upsilon':
    xmax = xFrame.GetMaximum()
    xFrame.SetMaximum(xmax*100)
    xFrame.SetMinimum(1000)
xFrame.GetYaxis().SetTitleOffset(1.1)
xFrame.GetXaxis().SetLabelSize(0)

legend = ROOT.TLegend(0.45,0.55,0.92,0.88)
legend.SetTextFont(42)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0000)
#legend.SetNColumns(2)

for prim in reversed(padUp.GetListOfPrimitives()):
    #print prim.GetTitle()
    if 'data_obs' in prim.GetTitle():
        title = 'Predicted' if blind else 'Observed'
        legend.AddEntry(prim, title, 'ep')
    elif 'ggH' in prim.GetTitle():
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(h,a)
        legend.AddEntry(prim, title, 'l')
legend.AddEntry('central', 'Background Model', 'l')
#legend.AddEntry('Fake', 'Tight-to-Loose Ratio Uncertainty', 'l')
prim = padUp.GetListOfPrimitives()[-1]
prim.SetMarkerSize(0)
prim.SetLineColor(0)
title = 'B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}'.format(floatToText(br))
legend.AddEntry(prim, title, 'ep')

padUp.cd()
legend.Draw()

if massRange == 'lowmass' or massRange == 'upsilon':
    padUp.SetLogy()
canvas.RedrawAxis()

for ext in ['png']:
    canvas.Print('obs_mm_control_thth_{}.{}'.format(massRange,ext))


################################ x ######################################
x = ws.var(xVar)
x.setUnit('GeV')
x.setPlotLabel('m(#mu#mu)')
x.SetTitle('m(#mu#mu)')

canvas = ROOT.TCanvas('c','c',800,800)
canvas.Divide(1,1)
canvas.cd()
padDown=ROOT.TPad("","",0,0,1,0.25)
padDown.SetTopMargin(0.035)
padDown.SetBottomMargin(0.4)
padDown.Draw()
canvas.cd()
padUp=ROOT.TPad("","",0,0.25,1,1)
padUp.SetBottomMargin(0.03)
padUp.SetTopMargin(0.07)
padUp.Draw()

xFrame = x.frame()

uncert = ws.var('TauHadTauHad_V3_2018_fake')
uncert.setVal(-1)
pdf_x.plotOn(xFrame,ROOT.RooFit.Normalization(integral_fakeDown),ROOT.RooFit.LineColor(ROOT.kOrange+1), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('Fake'))
uncert.setVal(1)
pdf_x.plotOn(xFrame,ROOT.RooFit.Normalization(integral_fakeUp),ROOT.RooFit.LineColor(ROOT.kOrange+1), ROOT.RooFit.LineStyle(ROOT.kDashed))
sig_x.plotOn(xFrame,ROOT.RooFit.Normalization(sigintegral),ROOT.RooFit.LineColor(ROOT.kRed))#,ROOT.RooFit.NormRange("fullrange"),ROOT.RooFit.Range("range"))
uncert.setVal(0)
pdf_x.plotOn(xFrame,ROOT.RooFit.Normalization(integral),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('Central'))#,ROOT.RooFit.NormRange("fullrange"),ROOT.RooFit.Range("range"))
data.plotOn(xFrame,ROOT.RooFit.Binning(int((xRange[1]-xRange[0])/xBinWidth)))

pull = xFrame.pullHist()

padDown.cd()
padDown.SetGridy(1)
pull.Draw('ap')
pull.GetXaxis().SetLimits(*xRange)
pull.SetMaximum(2)
pull.SetMinimum(-2)

pull.GetXaxis().SetTitleSize(0.16)
pull.GetXaxis().SetLabelSize(0.12)
pull.GetXaxis().SetTitleOffset(1)
pull.GetXaxis().SetTitle('m(#mu#mu) (GeV)')
pull.GetXaxis().SetNdivisions(510)
pull.GetXaxis().SetTickLength(0.09)

pull.GetYaxis().SetTitleSize(0.16)
pull.GetYaxis().SetLabelSize(0.12)
pull.GetYaxis().SetTitleOffset(0.4)
pull.GetYaxis().SetTitle('Pull')
pull.GetYaxis().SetNdivisions(502)

canvas.cd()
padUp.cd()

xFrame.Draw()
xFrame.GetYaxis().SetTitle('Events / {} GeV'.format(xBinWidth))

CMS_lumi.cmsText = 'CMS'
CMS_lumi.writeExtraText = isprelim
#CMS_lumi.extraText = 'Preliminary'
CMS_lumi.extraText = '#tau_{h}#tau_{h}'
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (59.8)
CMS_lumi.CMS_lumi(canvas,4,11)

if massRange == 'lowmass':
    xmax = xFrame.GetMaximum()
    xFrame.SetMaximum(xmax*5)
    xFrame.SetMinimum(0.5)
elif massRange == 'upsilon':
    xFrame.SetMaximum(80)
xFrame.GetYaxis().SetTitleOffset(1.1)
xFrame.GetXaxis().SetLabelSize(0)

legend = ROOT.TLegend(0.45,0.55,0.92,0.88)
legend.SetTextFont(42)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0000)
#legend.SetNColumns(2)

for prim in reversed(padUp.GetListOfPrimitives()):
    if 'data_obs' in prim.GetTitle():
        title = 'Predicted' if blind else 'Observed'
        legend.AddEntry(prim, title, 'ep')
    #elif 'bg' in prim.GetTitle():
    #    legend.AddEntry(prim, 'Background Model', 'l')
    elif 'ggH' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(h,a)
        legend.AddEntry(prim, title, 'l')
legend.AddEntry('Central', 'Background Model', 'l')
legend.AddEntry('Fake', 'Tight-to-Loose Ratio Uncertainty', 'l')

prim = padUp.GetListOfPrimitives()[-1]
prim.SetMarkerSize(0)
prim.SetLineColor(0)
title = 'B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}'.format(floatToText(br))
legend.AddEntry(prim, title, 'ep')

padUp.cd()
legend.Draw()

if massRange == 'lowmass':
    padUp.SetLogy()
canvas.RedrawAxis()

for ext in ['png','pdf']:
    canvas.Print('obs_mm_TauHadTauHad_{}.{}'.format(massRange,ext))

################################ y ######################################
y = ws.var(yVar)
y.setUnit('GeV')
if yvar=='h':
    y.setPlotLabel('m(#mu#mu#tau_{#mu}#tau_{h})')
    y.SetTitle('m(#mu#mu#tau_{#mu}#tau_{h})')
else:
    y.setPlotLabel('m(#tau_{#mu}#tau_{h})')
    y.SetTitle('m(#tau_{#mu}#tau_{h})')
#y.setRange('fullrange',2.5,25)
y.setRange(*yRange)
y.setBins(int((yRange[1]-yRange[0])/yBinWidth))
#print y.getBinningNames()


canvas = ROOT.TCanvas('c','c',800,800)
canvas.Divide(1,1)
canvas.cd()
padDown=ROOT.TPad("","",0,0,1,0.25)
padDown.SetTopMargin(0.035)
padDown.SetBottomMargin(0.4)
padDown.Draw()
canvas.cd()
padUp=ROOT.TPad("","",0,0.25,1,1)
padUp.SetBottomMargin(0.03)
padUp.SetTopMargin(0.07)
padUp.Draw()

yFrame = y.frame()

uncert.setVal(-1)
pdf_y.plotOn(yFrame,ROOT.RooFit.Normalization(integral_fakeDown),ROOT.RooFit.LineColor(ROOT.kOrange+1), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('Fake'))
uncert.setVal(1)
pdf_y.plotOn(yFrame,ROOT.RooFit.Normalization(integral_fakeUp),ROOT.RooFit.LineColor(ROOT.kOrange+1), ROOT.RooFit.LineStyle(ROOT.kDashed))
sig_y.plotOn(yFrame,ROOT.RooFit.Normalization(sigintegral),ROOT.RooFit.LineColor(ROOT.kRed))#,ROOT.RooFit.NormRange("fullrange"),ROOT.RooFit.Range("range"))
sig_y_heavy.plotOn(yFrame,ROOT.RooFit.Normalization(sigintegral_heavy),ROOT.RooFit.LineColor(ROOT.kGreen+2))
uncert.setVal(0)
pdf_y.plotOn(yFrame,ROOT.RooFit.Normalization(integral),ROOT.RooFit.LineColor(ROOT.kBlue))#,ROOT.RooFit.NormRange("fullrange"),ROOT.RooFit.Range("range"))
data.plotOn(yFrame)

pull = yFrame.pullHist()

padDown.cd()
padDown.SetGridy(1)
pull.Draw('ap')
#pull.GetXaxis().SetRangeUser(0,810)
pull.GetXaxis().SetLimits(*yRange)
#pull.GetXaxis().SetMaximum(800)
pull.SetMaximum(2)
pull.SetMinimum(-2)
#pull.SetMarkerStyle(20)

pull.GetXaxis().SetTitleSize(0.16)
pull.GetXaxis().SetLabelSize(0.12)
pull.GetXaxis().SetTitleOffset(1)
pull.GetXaxis().SetTitle('m(#mu#muj) (GeV)')
pull.GetXaxis().SetNdivisions(510)
pull.GetXaxis().SetTickLength(0.09)

pull.GetYaxis().SetTitleSize(0.16)
pull.GetYaxis().SetLabelSize(0.12)
pull.GetYaxis().SetTitleOffset(0.4)
pull.GetYaxis().SetTitle('Pull')
pull.GetYaxis().SetNdivisions(502)

canvas.cd()
padUp.cd()
yFrame.Draw()
yFrame.GetYaxis().SetTitle('Events / {} GeV'.format(yBinWidth))
yFrame.GetXaxis().SetLimits(*yRange)

CMS_lumi.cmsText = 'CMS'
CMS_lumi.writeExtraText = isprelim
#CMS_lumi.extraText = 'Preliminary'
CMS_lumi.extraText = '#tau_{h}#tau_{h}'
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (59.8)
CMS_lumi.CMS_lumi(canvas,4,11)


ymax = yFrame.GetMaximum()
yFrame.SetMaximum(ymax*10)
yFrame.SetMinimum(0.1)
yFrame.GetYaxis().SetTitleOffset(1.1)
yFrame.GetXaxis().SetLabelSize(0)

legend = ROOT.TLegend(0.45,0.55,0.92,0.88)
legend.SetTextFont(42)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0000)
#legend.SetNColumns(2)

for prim in reversed(padUp.GetListOfPrimitives()):
    #print prim
    if 'data_obs' in prim.GetTitle():
        title = 'Predicted' if blind else 'Observed'
        legend.AddEntry(prim, title, 'ep')
    #elif 'bg' in prim.GetTitle():
    #    legend.AddEntry(prim, 'Background Model', 'l')
    elif 'ggH' in prim.GetTitle() and '125' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(h,a)
        legend.AddEntry(prim, title, 'l')
    elif 'ggH' in prim.GetTitle() and '250' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(250,a)
        legend.AddEntry(prim, title, 'l')
legend.AddEntry('Central', 'Background Model', 'l')
legend.AddEntry('Fake', 'Tight-to-Loose Ratio Uncertainty', 'l')

prim = padUp.GetListOfPrimitives()[-1]
prim.SetMarkerSize(0)
prim.SetLineColor(0)
title = 'B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}'.format(floatToText(br))
legend.AddEntry(prim, title, 'ep')

padUp.cd()
legend.Draw()

padUp.RedrawAxis()
padUp.SetLogy()

for ext in ['png','pdf']:
    canvas.Print('obs_{}_TauHadTauHad_{}.{}'.format(yvar,massRange,ext))

