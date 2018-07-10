## Cadence Optimization for AGN selection in LSST

This folder contains the notebooks demonstrating the workflow that we estbalished enroute to evaluate the quality of a particular cadence on AGN selection by flux variability. Some background information is also included in the notebooks alongside the code. To get a comprehensive understanding of the workflow, please start with the index notebook, where you can easily link to other two notebooks related different sections of the workflow. 

### Below is a brief summary:
- **index.ipynb**: Overview of the project and workflow. Mostly showing how I retrieve cadence information for OpSim database using MAF.
- **lc.ipynb**: How to generate CARMA mock light curve using [Kali](https://github.com/AstroVPK/kali) and how to downsample the original mock LC at LSST simulated cadence.
- **compare.ipynb**: Selecte three difference simulated cadence, estimate the CARMA parameters from LCs dowmsampled at these cadences using Kali, then compared the best-fit parameters with the parameters used to generate these mock LCs in a table. 

---
### Future work:
We will simulate multiple objects using a variaty of CARMA parameters (or timescales), select a few different locations on the sky within the LSST coverage, and then conduct a parameter space analysis based on different combination of parameters. Ideally we could draw some metrics out of the result of such analysis assuming our selection of parameters and coordinates are comprehensive and representive enough. 
