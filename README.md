# CombineLimits
Standalone limits to run with combine in the CMSSW final state analysis framework.

## Setup

```
ssh YOURUSERNAME@lxplus8.cern.ch
```

Add this line into your ``.bashrc`` of your lxplus:
```
export X509_USER_PROXY=$HOME/tmp/x509up
```

Then initialize your grid proxy (for submitting condor jobs, need to run this regularly):
```
voms-proxy-init --voms cms --valid 192:0
```

Create your working directory and enter it:
```
cd YOURWORKDIRECTORY
```

```bash
setenv SCRAM_ARCH cc8_amd64_gcc9
cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git cms-init
git clone https://github.com/Fengwangdong/CombineLimits.git -b feng-branch
./CombineLimits/recipe/recipe.sh
```

## Pref-fit and Produce datacards
To produce prefit plots and datacards, follow the instruction when you run the script below (you will be directed to type in arguments inclusing H mass, final state, era, and M(mm) region): 
```
cd CombineLimitsRunII/HaaLimits/python/
csh run_fit.csh
```

You will find the pre-fit plots in the directory of ``figures/HaaLimits2D_unbinned_h/``, which can be downloaded and inspected for the fit quality. 
Some parameters may show anomalously huge uncertainty, most likely to be associated with M(mmtt). You will have to tune the fit constaints in 
this file: ``HaaLimits2DNew.py`` (Line 226 and 234). Then this step has to be redone for the specific region, final state, era or H mass.

The datacard can be found in ``datacards_shape/MuMuTauTau``. If you need to combine datacards, you can use this script:
```
csh run_combine.csh
```
And follow the instructions from the script. Your default order should be: first combine 3 years' datacards for each final state, second combine 
all the final states together.

## Run Asymptotic limits
You may make a new directory called testLimits, and copy the datacard directory that the previous step created for you into this work directory.
Before submit condor jobs, you should test one asymptotic limit using this script, NOTE that you need to modify the path in this script to your 
working directory path before running it as below:
```
bash test_example.sh
```

If it works well, you can prepare to submit condor jobs:
```
mkdir condorOut # This directory will contain the output files from condor jobs for you to inspect if there is any problem

sh submit_condor_lxplus.sh # Follow the instruction when you are running this script to provide the proper arguments
```

You may check the files named ``*.stderr`` which contains error information of each job (if failed), and check the files named ``*.stdout`` which 
contains the output (also limits) of the job (ONLY if succeeded).

If success, you have find the output limit files in these directories below:
``H125``, ``H250``, ``H500``, ``H750``, ``H1000``.

To produce the upper limit plots, this script does the work for you:  ``plot_limit_haa_multi.py`` You can dispatch it with another script:
```
bash run_plot.sh # Follow the instruction to provide the arguments for this script like final state, era, H mass etc.
```

It will create a directory for you to collect limit plots: ``plots/Limits/pdf/haa/`` 
Among the sub-directories, you can find the relevant plots eg:  ``*br_log.pdf`` 
