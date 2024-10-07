import os, sys
import json

import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import CombineLimitsRunII.Plotter.CMS_lumi as CMS_lumi
import CombineLimitsRunII.Plotter.tdrStyle as tdrstyle

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
tdrstyle.setTDRStyle()

def floatToText(x):
    s = '{:.1E}'.format(x).split('E')
    return '{} #times 10^{{{}}}'.format(int(float(s[0])),int(s[1]))

isprelim = True
yvar = 'h'
#h = 1000
xVar = 'invMassMuMu'
yVar = 'visFourbodyMass'
#massRange = 'lowmass'
#massRange = 'upsilon'
#massRange = 'highmass'

#year = '2018'

massRange = sys.argv[1]
year = sys.argv[2]
h = sys.argv[3]

if year == '2018':
    lumi = 59.74
elif year == '2017':
    lumi = 41.53
elif year == '2016':
    lumi = 35.92

if massRange == 'lowmass':
    xRange = [3,8]
    xBinWidth = 0.1
    a = 5
elif massRange == 'upsilon':
    xRange = [8,12]
    xBinWidth = 0.1
    a = 11
elif massRange == 'highmass':
    xRange = [12,30]
    xBinWidth = 0.5
    a = 20
elif massRange == 'highmass2':
    xRange = [30,50]
    xBinWidth = 0.5
    a = 40

yRange = []
yBinWidth = 10
if h == "125":
    yRange = [80,150]
    yBinWidth = 5
elif h == "250":
    yRange = [130,280]
    yBinWidth = 5
elif h == "500":
    yRange = [250,600]
elif h == "750":
    yRange = [350,800]
elif h == "1000":
    #yRange = [450,1200]
    yRange = [150,1200]

blind = False
br = 0.0005
doPostfit = False

amasses = ['3p6','5','9','13','17','21']
colors = [ROOT.kBlue-4, ROOT.kCyan+1, ROOT.kGreen+1, ROOT.kOrange-3, ROOT.kRed+1, ROOT.kMagenta+1]

rfile = '../../HaaLimits/python/testPostFit/datacards_shape/MuMuTauTau/mmmt_mm_{}_parametric_unbinned_{}_H{}_TauMuTauHad_V2_{}_MVAMedium_DG_DoubleExpo_yRange_wFakeTauScale.root'.format(yvar,massRange,h,year)
tfile = ROOT.TFile.Open(rfile)
print rfile

ws = tfile.Get('w')
#ws.Print()
pdf_x = ws.pdf('bg_TauMuTauHad_V2_{}_PP_x'.format(year))
pdf_x_cont = ws.pdf('cont_TauMuTauHad_V2_{}_PP_x'.format(year))
if massRange == 'lowmass':
    pdf_x_res = ws.pdf('jpsi_TauMuTauHad_V2_{}_PP_x'.format(year))
elif massRange == 'upsilon':
    pdf_x_res = ws.pdf('upsilon_TauMuTauHad_V2_{}_PP_x'.format(year))
else:
    pdf_x_res = None
pdf_y = ws.pdf('bg_TauMuTauHad_V2_{}_PP_y'.format(year))


pdf_control = ws.pdf("bg_control_{}".format(year))
pdf_control_cont = ws.pdf("contpoly_control_{}".format(year))
if massRange == 'lowmass':
    pdf_control_res = ws.pdf("jpsi_control_{}".format(year))
elif massRange == 'upsilon':
    pdf_control_res = ws.pdf("upsilon_control_{}".format(year))
else:
    pdf_control_res = None


fpostfit = open('../../HaaLimits/python/testPostFit/Impacts_TauMuTauHad_{}_{}_h{}/fit.log'.format(massRange,year,h))
params={}
for line in fpostfit.readlines():
    txt = []
    if len(line.split()) > 3:
        txt = line.split()[3]
    if not '+/-' in txt: continue
    param = line.split()[0]
    val = line.split()[2]
    var = ws.var(param)

    if var:
        print param, val, float(val)
        var.setVal(float(val))
        params[param]=float(val)

data = ws.data('data_obs_TauMuTauHad_V2_{}_PP'.format(year))
data_control = ws.data('data_obs')

integral_postfit = data.sumEntries()

mh = ws.var('MH')
mh.setVal(float(h))
ma = ws.var('MA')
ma.setVal(a)

sig_x = ws.pdf('ggH_haa_{}_TauMuTauHad_V2_{}_PP_x'.format(h,year))
sig_y = ws.pdf('ggH_haa_{}_TauMuTauHad_V2_{}_PP_y'.format(h,year))
#sig_y1 = ws.pdf('ggH_haa_{}_TauMuTauHad_V2_{}_PP_y'.format(250,year))
#sig_y2 = ws.pdf('ggH_haa_{}_TauMuTauHad_V2_{}_PP_y'.format(500,year))

## if massRange == 'lowmass':
##     integral_postfit_cont = params['integral_cont1_TauMuTauHad_V2_2018_PP'] + params['integral_cont2_TauMuTauHad_V2_2018_PP']
## else:
##     integral_postfit_cont = params['integral_cont_TauMuTauHad_V2_2018_PP']
##
## if massRange == 'lowmass':
##     integral_postfit_res = params['integral_jpsi1S_TauMuTauHad_V2_2018_PP']+params['relNorm_jpsi2S_2018']*params['integral_jpsi1S_TauMuTauHad_V2_2018_PP']
## elif massRange == 'upsilon':
##     integral_postfit_res = params['integral_upsilon1S_TauMuTauHad_V2_2018_PP']+params['relNorm_upsilon2S_2018']*params['integral_upsilon1S_TauMuTauHad_V2_2018_PP']+params['relNorm_upsilon3S_2018']*params['integral_upsilon1S_TauMuTauHad_V2_2018_PP']
## else:
##     integral_postfit_res = 0
## integral_postfit = integral_postfit_cont+integral_postfit_res


integral_control_cont = 0
#if massRange == 'lowmass':
#    integral_control_cont = params['integral_contpoly_control_{}'.format(year)]
#    integral_control_res = params['integral_jpsi1S_control_{}'.format(year)]+params['relNorm_jpsi2S_{}'.format(year)]*params['integral_jpsi1S_control_{}'.format(year)]
#elif massRange == 'upsilon':
#    integral_control_cont = params['integral_contpoly_control_{}'.format(year)]
#    integral_control_res = params['integral_upsilon1S_control_{}'.format(year)]+params['relNorm_upsilon2S_{}'.format(year)]*params['integral_upsilon1S_control_{}'.format(year)]+params['relNorm_upsilon3S_{}'.format(year)]*params['integral_upsilon1S_control_{}'.format(year)]
#else:
#    integral_control_res = 0
integral_control_res = 0
integral_control = integral_control_cont+integral_control_res


sigintegral = ws.function('fullIntegral_ggH_haa_{}_TauMuTauHad_V2_{}_PP'.format(h,year)).getVal() * br/0.001
#sigintegral = -13.2224
#sigintegral = 0
#mh.setVal(250)
#sigintegral_heavy = ws.function('fullIntegral_ggH_haa_{}_TauMuTauHad_V2_2018_PP'.format(250)).getVal() * br/0.001
#mh.setVal(250)
#sigintegral_1 = ws.function('fullIntegral_ggH_haa_{}_TauMuTauHad_V2_{}_PP'.format(250,year)).getVal() * br/0.001
#mh.setVal(500)
#sigintegral_2 = ws.function('fullIntegral_ggH_haa_{}_TauMuTauHad_V2_{}_PP'.format(500,year)).getVal() * br/0.001

#print sigintegral,sigintegral_heavy
data.Print()
print integral_postfit
data_control.Print()
print integral_control

################################ control ######################################
x = ws.var('invMassMuMu_control_{}'.format(year))
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

#pdf_control.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('Central'))
if pdf_control_res:
    pdf_control_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('cont'))
    pdf_control_res.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_res),ROOT.RooFit.AddTo('cont'), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('central'))
else:
    pdf_control_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('cont'))

pdf_control.plotOn(xFrame,ROOT.RooFit.Normalization(integral_control),ROOT.RooFit.LineColor(ROOT.kBlue))
data_control.plotOn(xFrame,ROOT.RooFit.Binning(int((xRange[1]-xRange[0])/xBinWidth)))

pull = xFrame.pullHist()

padDown.cd()
padDown.SetGridy(1)
pull.Draw('ap')
#pull.GetXaxis().SetRangeUser(0,810)
pull.GetXaxis().SetLimits(6,14)
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
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (lumi)
CMS_lumi.CMS_lumi(canvas,4,11)

if massRange == 'lowmass':
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

#if massRange == 'lowmass' or massRange == 'upsilon':
#    padUp.SetLogy()
#canvas.RedrawAxis()

#for ext in ['png']:
#    canvas.Print('postfit_mm_control_{}_{}.{}'.format(massRange,year,ext))


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

## if pdf_x_res:
##     pdf_x_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_postfit_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('cont'))
##     pdf_x_res.plotOn(xFrame,ROOT.RooFit.Normalization(integral_postfit_res),ROOT.RooFit.AddTo('cont'),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('central'))
## else:
##     pdf_x_cont.plotOn(xFrame,ROOT.RooFit.Normalization(integral_postfit_cont),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('cont'))
sig_x.plotOn(xFrame,ROOT.RooFit.Normalization(sigintegral),ROOT.RooFit.LineColor(ROOT.kRed))

pdf_x.plotOn(xFrame,ROOT.RooFit.Normalization(integral_postfit),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name("central"))
data.plotOn(xFrame,ROOT.RooFit.Binning(int((xRange[1]-xRange[0])/xBinWidth)),ROOT.RooFit.Name("data_x"))

pull = xFrame.pullHist("data_x","central")
chi2_model_x = ROOT.TLatex(0.65,0.55, "#chi^{2} / NDF = " + "{:4.2f}".format(xFrame.chiSquare("central", "data_x")))
chi2_model_x.SetNDC()
chi2_model_x.SetTextSize(0.04)

padDown.cd()
padDown.SetGridy(1)
pull.Draw('ap')
#pull.GetXaxis().SetRangeUser(0,810)
pull.GetXaxis().SetLimits(*xRange)
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
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (lumi)
CMS_lumi.CMS_lumi(canvas,4,11)

if massRange == 'lowmass':
    xmax = xFrame.GetMaximum()
    xFrame.SetMaximum(xmax*5)
    xFrame.SetMinimum(0.5)
elif massRange == 'upsilon':
    xmax = xFrame.GetMaximum()
    xFrame.SetMaximum(xmax*1.3)
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
#legend.AddEntry(prim, title, 'ep')

padUp.cd()
legend.Draw()
chi2_model_x.Draw()

if massRange == 'lowmass':
    padUp.SetLogy()
canvas.RedrawAxis()

for ext in ['pdf']:
    canvas.Print('postfit_mm_TauMuTauHad_{}_{}_{}.{}'.format(massRange,year,h,ext))

################################ y ######################################
y = ws.var(yVar)
y.setUnit('GeV')
if yvar=='h':
    y.setPlotLabel('m(#mu#mu#mu#tau)')
    y.SetTitle('m(#mu#mu#mu#tau')
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

sig_y.plotOn(yFrame,ROOT.RooFit.Normalization(sigintegral),ROOT.RooFit.LineColor(ROOT.kRed))#,
#sig_y1.plotOn(yFrame,ROOT.RooFit.Normalization(sigintegral_1),ROOT.RooFit.LineColor(ROOT.kOrange-6))#,
#sig_y2.plotOn(yFrame,ROOT.RooFit.Normalization(sigintegral_2),ROOT.RooFit.LineColor(ROOT.kGreen+3))#,
pdf_y.plotOn(yFrame,ROOT.RooFit.Normalization(integral_postfit),ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Name('central_y'))

data.plotOn(yFrame,ROOT.RooFit.Name('data_y'))

pull = yFrame.pullHist('data_y','central_y')
chi2_model_y = ROOT.TLatex(0.65,0.55, "#chi^{2} / NDF = " + "{:4.2f}".format(yFrame.chiSquare('central_y', 'data_y')))
chi2_model_y.SetNDC()
chi2_model_y.SetTextSize(0.04)

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
pull.GetXaxis().SetTitle('m(#mu#mu#mu#tau) (GeV)')
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
CMS_lumi.extraText = '#tau_{#mu}#tau_{h}'
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (lumi)
CMS_lumi.CMS_lumi(canvas,4,11)


ymax = yFrame.GetMaximum()
yFrame.SetMaximum(ymax*1.3)
#yFrame.SetMaximum(ymax*10)
yFrame.SetMinimum(0.1)
yFrame.GetYaxis().SetTitleOffset(1.1)
yFrame.GetXaxis().SetLabelSize(0)

legend = ROOT.TLegend(0.45,0.55,0.92,0.88)
legend.SetTextFont(42)
legend.SetBorderSize(0)
legend.SetFillColor(0)
#legend.SetNColumns(2)

for prim in reversed(padUp.GetListOfPrimitives()):
    #print prim.GetTitle()
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
    elif 'ggH' in prim.GetTitle() and '500' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(500,a)
        legend.AddEntry(prim, title, 'l')
    elif 'ggH' in prim.GetTitle() and '750' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(750,a)
        legend.AddEntry(prim, title, 'l')
    elif 'ggH' in prim.GetTitle() and '1000' in prim.GetTitle():
        #title = '#splitline{{m_{{H}} = {} GeV, m_{{a}} = {} GeV}}{{B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}}}'.format(h,a,floatToText(br))
        title = 'm_{{H}} = {} GeV, m_{{a}} = {} GeV'.format(1000,a)
        legend.AddEntry(prim, title, 'l')
legend.AddEntry('central_y', 'Background Model', 'l')
#legend.AddEntry('Fake', 'Tight-to-Loose Ratio Uncertainty', 'l')
legend.SetFillStyle(0000)

prim = padUp.GetListOfPrimitives()[-1]
prim.SetMarkerSize(0)
prim.SetLineColor(0)
title = 'B(h #rightarrow aa #rightarrow #mu#mu#tau#tau) = {}'.format(floatToText(br))
#legend.AddEntry(prim, title, 'ep')

padUp.cd()
legend.Draw()
chi2_model_y.Draw()

#padUp.RedrawAxis()
#padUp.SetLogy()

for ext in ['pdf']:
    #canvas.Print('bg_{}_TauMuTauHad_Erfb_{}.{}'.format(yvar,massRange,ext))
    canvas.Print('postfit_{}_TauMuTauHad_{}_{}_{}.{}'.format(yvar,massRange,year,h,ext))

