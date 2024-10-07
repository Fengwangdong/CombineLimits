# CombineLimits
Standalone limits to run with combine in the CMSSW framework

## Setup

ssh YOURUSERNAME@lxplus8.cern.ch

```bash
setenv SCRAM_ARCH cc8_amd64_gcc9
cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git cms-init
git clone https://github.com/Fengwangdong/CombineLimits.git -b feng-branch
./CombineLimits/recipe/recipe.sh
```

To produce prefit plots and datacards, follow the instruction when you run the script below (you will be directed to type in arguments inclusing H mass, final state, era, and M(#mu#mu) region): 
```
cd CombineLimitsRunII/HaaLimits/python/
./run_fit.csh
```
