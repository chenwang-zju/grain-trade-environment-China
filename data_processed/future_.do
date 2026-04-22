*******************************************************
* Script: 04_future_projection_and_env_tax.do
* Purpose:
*   1) Estimate a historical fixed-effects model for grain production
*   2) Build a 2020 baseline by province
*   3) Import future SSP-climate projections (SSP1-2.6, SSP2-4.5, SSP5-8.5)
*   4) Predict future grain production changes relative to 2020
*   5) Reshape predicted outputs for downstream analysis
*   6) Calculate environmental tax indicators based on projected emissions
*
* Inputs:
*   - paneldata240822.dta
*   - future_panel_ssp126_245_585_to2060.csv
*
* Notes:
*   - Update local file paths before running.
*   - Variable definitions and units follow the manuscript
*     and Supplementary Information.
*******************************************************

clear all
set more off
capture log close

*******************************************************
* 1. Load historical panel data
*******************************************************
use "paneldata240822.dta", clear

*******************************************************
* 2. Check key identifiers
*******************************************************
capture confirm variable PAC
if _rc {
    di as error "Historical data are missing PAC."
    exit 198
}

capture confirm variable year
if _rc {
    di as error "Historical data are missing year."
    exit 198
}

*******************************************************
* 3. Harmonize historical variables
*******************************************************

* Generate logged demographic variables if absent
capture confirm variable lnpop
if _rc {
    gen lnpop = ln(pop)
}

capture confirm variable lnUR
if _rc {
    gen lnUR = ln(UR)
}

* Harmonize climate variables to Tnew / Pnew
capture confirm variable Tnew
if _rc {
    capture confirm variable tas_tmeanc
    if _rc {
        di as error "Historical data are missing both Tnew and tas_tmeanc."
        exit 198
    }
    gen Tnew = tas_tmeanc
}

capture confirm variable Pnew
if _rc {
    capture confirm variable pr_ptotal_mm
    if _rc {
        di as error "Historical data are missing both Pnew and pr_ptotal_mm."
        exit 198
    }
    gen Pnew = pr_ptotal_mm
}

* Generate nonlinear climate terms if absent
capture confirm variable Tnew2
if _rc gen Tnew2 = Tnew^2

capture confirm variable Pnew2
if _rc gen Pnew2 = Pnew^2

*******************************************************
* 4. Historical fixed-effects regression
*******************************************************
reghdfe lngr lngra c.lnMP##c.lnAGE lnfa lnUR lnpop lnfer lnirri ///
       c.Tnew c.Tnew2 c.Pnew c.Pnew2, ///
       absorb(year PAC) vce(cluster PAC)

estimates store M1

*******************************************************
* 5. Build provincial 2020 baseline
*******************************************************
preserve

keep if year == 2020

collapse (mean) lnpop lnUR Tnew Pnew Tnew2 Pnew2 lngr, by(PAC)

gen lnpop0 = lnpop
gen lnUR0  = lnUR
gen T0     = Tnew
gen P0     = Pnew
gen T0sq   = Tnew2
gen P0sq   = Pnew2
gen lngr0  = lngr

keep PAC lnpop0 lnUR0 T0 P0 T0sq P0sq lngr0
isid PAC

save "base2020.dta", replace
restore

*******************************************************
* 6. Import future SSP-climate panel data
*******************************************************
import delimited "future_panel_ssp126_245_585_to2060.csv", ///
    clear varnames(1) encoding(UTF-8)

* Trim variable names
foreach v of varlist _all {
    rename `v' `=strtrim("`v'")'
}

* Harmonize key identifiers
capture confirm variable pac
if !_rc rename pac PAC

capture confirm variable PAC
if _rc {
    di as error "Future data are missing PAC."
    exit 198
}

capture confirm variable year
if _rc {
    di as error "Future data are missing year."
    exit 198
}

capture confirm variable scenario
if _rc {
    di as error "Future data are missing scenario."
    exit 198
}

* Convert year to numeric and restrict time horizon
destring year, replace force
keep if year <= 2060

* Keep SSP1-2.6 / SSP2-4.5 / SSP5-8.5 only
replace scenario = lower(scenario)
keep if inlist(scenario, "ssp126", "ssp245", "ssp585")

*******************************************************
* 7. Harmonize future variables to model specification
*******************************************************

* Population and urbanization
capture confirm variable pop
if _rc {
    di as error "Future data are missing pop."
    exit 198
}

capture confirm variable ur
if _rc {
    di as error "Future data are missing ur."
    exit 198
}

gen lnpop = ln(pop)
gen lnUR  = ln(ur)

* Climate variables
capture confirm variable tas_tmeanc
if _rc {
    di as error "Future data are missing tas_tmeanc."
    exit 198
}

capture confirm variable pr_ptotal_mm
if _rc {
    di as error "Future data are missing pr_ptotal_mm."
    exit 198
}

gen Tnew  = tas_tmeanc
gen Pnew  = pr_ptotal_mm
gen Tnew2 = Tnew^2
gen Pnew2 = Pnew^2

*******************************************************
* 8. Merge 2020 baseline and calculate changes
*******************************************************
merge m:1 PAC using "base2020.dta", keep(match) nogen

gen d_lnpop = lnpop - lnpop0
gen d_lnUR  = lnUR  - lnUR0
gen d_Tnew  = Tnew  - T0
gen d_Tnew2 = Tnew2 - T0sq
gen d_Pnew  = Pnew  - P0
gen d_Pnew2 = Pnew2 - P0sq

*******************************************************
* 9. Predict future grain production changes
*    using estimated coefficients from M1
*******************************************************
estimates restore M1

gen d_lngr = ///
    _b[lnpop] * d_lnpop + ///
    _b[lnUR]  * d_lnUR  + ///
    _b[Tnew]  * d_Tnew  + ///
    _b[Tnew2] * d_Tnew2 + ///
    _b[Pnew]  * d_Pnew  + ///
    _b[Pnew2] * d_Pnew2

* Future log grain production = 2020 baseline + modeled change
gen lngr_hat = lngr0 + d_lngr
gen gr_hat   = exp(lngr_hat)

save "future_pred_to2060.dta", replace
export delimited using "future_pred_to2060.csv", replace

*******************************************************
* 10. Reshape projected outputs to wide format
*******************************************************
use "future_pred_to2060.dta", clear

isid PAC year scenario

keep PAC scenario year gr_hat lngr_hat
reshape wide gr_hat lngr_hat, i(PAC scenario) j(year)

save "future_pred_to2060_wide.dta", replace
export delimited using "future_pred_to2060_wide.csv", replace

*******************************************************
* 11. Environmental tax calculation
*
* Expected variable naming examples:
*   NH3_126_2030   NO_126_2030   NO3_126_2030   totC_126_2030net
*   NH3_245_2040   NO_245_2040   NO3_245_2040   totC_245_2040net
*   NH3_585_2060   NO_585_2060   NO3_585_2060   totC_585_2060net
*
* Tax calculation:
*   NH3, NO, NO3 in billion kg-equivalent scaling
*   net GHG = totC_*net, converted consistently
*******************************************************

* Tax parameters
local eq_nh3    0.95
local rate_nh3  6        // yuan/kg

local eq_nox    0.95
local rate_nox  8.55     // yuan/kg

local eq_nh4n   0.8
local rate_nh4n 4.8      // yuan/kg

local rate_ghg  0.09511  // yuan/kg

* Scenario IDs and years
local scen 126 245 585
local yrs  2030 2040 2050 2060

*******************************************************
* 12. Loop over scenarios and years to calculate tax
*******************************************************
foreach s of local scen {
    foreach y of local yrs {

        local vnh3 NH3_`s'_`y'
        local vno  NO_`s'_`y'
        local vno3 NO3_`s'_`y'
        local vghg totC_`s'_`y'net

        capture confirm variable `vnh3'
        if _rc {
            di as error "Missing variable: `vnh3' (skip scen=`s' year=`y')."
            continue
        }

        capture confirm variable `vno'
        if _rc {
            di as error "Missing variable: `vno' (skip scen=`s' year=`y')."
            continue
        }

        capture confirm variable `vno3'
        if _rc {
            di as error "Missing variable: `vno3' (skip scen=`s' year=`y')."
            continue
        }

        capture confirm variable `vghg'
        if _rc {
            di as error "Missing variable: `vghg' (skip scen=`s' year=`y')."
            continue
        }

        capture drop tax_`s'_`y'
        gen double tax_`s'_`y' = ///
            (`vnh3' * 1e9 * `eq_nh3'  * `rate_nh3'  + ///
             `vno'  * 1e9 * `eq_nox'  * `rate_nox'  + ///
             `vno3' * 1e9 * `eq_nh4n' * `rate_nh4n' + ///
             `vghg' * 1e9 * `rate_ghg') / 1e8

        label var tax_`s'_`y' "Environmental tax (scenario=`s', year=`y')"
    }
}

*******************************************************
* 13. Optional: save tax outputs
*******************************************************
* save "future_environmental_tax_outputs.dta", replace
