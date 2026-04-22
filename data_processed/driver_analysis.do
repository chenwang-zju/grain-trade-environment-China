*******************************************************
* Script: 02_driver_analysis_and_sem.do
* Purpose:
*   Analyze socioeconomic and climate drivers of grain
*   production and related indicators using:
*   - two-way fixed effects regressions (reghdfe)
*   - subgroup regressions for northern and southern China
*   - structural equation modeling (SEM)
*
* Input:
*   paneldata240822.dta
*
* Notes:
*   - Local file paths should be updated by users.
*   - Cluster-robust standard errors are calculated at
*     the provincial level (PAC).
*******************************************************

clear all
set more off

*******************************************************
* 1. Set working directory
*******************************************************
cd "E:/OneDrive/stata/Grain_data"

*******************************************************
* 2. Example preprocessing: reshape irrigation variable
*    (run only if needed for the source dataset)
*******************************************************
* reshape long irri, i(PAC) j(year)

*******************************************************
* 3. Load panel dataset
*******************************************************
use paneldata240822.dta, clear

*******************************************************
* 4. Two-way fixed effects regressions
*    Main specification without climate controls
*******************************************************

* Key explanatory variables:
* lnMP     = mechanization / machinery-related variable
* lnAGE    = aging-related variable
* lnfa     = farm size
* lnUR     = urbanization rate
* lnpop    = population
* lnfer    = fertilizer input
* lnirri   = irrigation
*
* Dependent variables:
* lngr     = grain production
* lnri     = rice production
* lnwh     = wheat production
* lnma     = maize production
*
* Climate controls (in extended models):
* Tnew, Tnew2 = temperature and squared temperature
* Pnew, Pnew2 = precipitation and squared precipitation

*******************************************************
* 4.1 Baseline models without climate controls
*******************************************************

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri, ///
    absorb(year PAC) vce(cluster PAC)

reghdfe lnwh lnwha c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri, ///
    absorb(year PAC) vce(cluster PAC)

reghdfe lnma lnmaa c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri, ///
    absorb(year PAC) vce(cluster PAC)

*******************************************************
* 4.2 Subgroup regressions: North (ns==1) vs South (ns==2)
*******************************************************

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    if ns == 1, absorb(year PAC) vce(cluster PAC)

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    if ns == 2, absorb(year PAC) vce(cluster PAC)

*******************************************************
* 4.3 Extended models with climate controls
*******************************************************

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2, ///
    absorb(year PAC) vce(cluster PAC)

reghdfe lnri lnria c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2, ///
    absorb(year PAC) vce(cluster PAC)

reghdfe lnwh lnwha c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2, ///
    absorb(year PAC) vce(cluster PAC)

reghdfe lnma lnmaa c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2, ///
    absorb(year PAC) vce(cluster PAC)

*******************************************************
* 4.4 Subgroup regressions with climate controls
*******************************************************

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2 ///
    if ns == 1, absorb(year PAC) vce(cluster PAC)

reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
    c.Tnew c.Tnew2 c.Pnew c.Pnew2 ///
    if ns == 2, absorb(year PAC) vce(cluster PAC)

*******************************************************
* 5. Standardization for SEM
*******************************************************

foreach v in lngr lnMP lnAGE lnUR lnfa lnirri lnfer Tnew Pnew Tnew2 {
    capture drop z_`v'
    egen z_`v' = std(`v')
}

capture drop z_T z_P
egen z_T = std(Tnew)
egen z_P = std(Pnew)

*******************************************************
* 6. Structural equation model:
*    production-related pathway
*******************************************************

sem ///
    (z_lnMP    <- z_lnAGE z_lnfa z_lnirri) ///
    (z_lnirri  <- z_Tnew z_Pnew) ///
    (z_lngr    <- z_lnMP z_lnfa z_lnirri z_lnUR z_Pnew), ///
    method(ml) vce(robust)

* Goodness-of-fit statistics
estat eqgof
estat gof, stats(all)

* Direct, indirect, and total effects
estat teffects
estat teffects, by(ns)

*******************************************************
* 7. Structural equation model:
*    diet-production-surplus/deficit pathway
*******************************************************

sem ///
    (z_lndiet     <- z_lnUR z_lngr z_lnpop) ///
    (z_lngrSurDef <- z_lngr z_lndiet z_lnpop z_lnUR), ///
    method(ml) vce(robust)

* Effects and fit statistics
estat teffects
estat gof, stats(all)

* Modification indices
estat mindices, min(10)
