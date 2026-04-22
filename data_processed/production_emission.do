*******************************************************
* Script: 03_production_emission_calculation.do
* Purpose:
*   Calculate grain production-related environmental
*   burdens over 1980–2020, including:
*   - virtual cropland
*   - virtual blue water
*   - NH3, NO, and NO3 losses
*   - N2O, CH4, and CO2 emissions
*   - aggregated total N and total C indicators
*
* Notes:
*   - Local paths and input data should be adapted by users.
*   - Variable definitions and unit conventions follow the
*     manuscript and Supplementary Information.
*******************************************************

clear all
set more off

*******************************************************
* 1. Load data
*******************************************************
* Update to your local working directory before running
cd "E:/OneDrive/stata/Grain_data"

* Example:
* use production_input_data.dta, clear

*******************************************************
* 2. Calculate virtual cropland
*******************************************************
* Virtual cropland associated with grain production
* Formula follows grain production divided by yield

forvalues i = 1980/2020 {
    gen VL_grain`i' = grain`i' * 10^4 * 10^3 / gra`i'
}

*******************************************************
* 3. Calculate virtual blue water
*******************************************************
* Example shown for 1990 in the original workflow
* Water footprint unit conversion follows manuscript settings

gen VW1990 = t1990 * 10^4 * 10^3 / wf_blue / 10^3

*******************************************************
* 4. Fill missing emission factors
*******************************************************
* Carry forward missing emission factor values
* across observations where needed

foreach var of varlist ef_* {
    replace `var' = `var'[_n-1] if missing(`var')
}

*******************************************************
* 5. Nitrogen-related emissions from fertilizer use
*******************************************************

* NH3 emissions from fertilizer application
* ef_`i' is a time-varying annual emission factor
forvalues i = 1980/2020 {
    gen NH3_grain`i' = grain`i' * 1000 * nrate_average * ef_`i' / 10^9
}

* NO emissions from fertilizer application
* EF_NO = 0.53%
forvalues i = 1980/2020 {
    gen NO_grain`i' = grain`i' * 1000 * nrate_average * 0.53 / 100 / 10^9
}

* Nitrate-related losses from leaching and runoff
* Leaching = 3.1%, runoff = 6.2%
forvalues i = 1980/2020 {
    gen NO3_grain`i' = grain`i' * 1000 * nrate_average * ///
                       (3.1 + 6.2) / 100 / 10^9
}

*******************************************************
* 6. Greenhouse gas emissions from fertilizer use
*******************************************************

* N2O emissions from fertilizer application
* Emission factor = 0.69%, GWP = 273
forvalues i = 1980/2020 {
    gen N2O_grain`i' = grain`i' * 1000 * 0.33 * ///
                       nrate_average * 0.69 / 100 / 10^9 * 273
}

* CH4 emissions from grain production
* Provincial CH4 factor = efch4, GWP = 27.9
forvalues i = 1980/2020 {
    gen CH4_grain`i' = grain`i' * 1000 * 0.33 * ///
                       efch4 / 10^9 * 12 / 16 * 27.9
}

*******************************************************
* 7. CO2 emissions from straw burning
*******************************************************
* Straw-to-grain ratio = 1.1
* Open burning share = 19% (here fixed as in the original code)

forvalues i = 1980/2020 {
    gen CO2_grain`i' = grain_yield`i' * 10^4 * 10^3 * ///
                       1.1 * 19 / 100 * 12 / 44 / 10^9
}

*******************************************************
* 8. Aggregate total N and total C indicators
*******************************************************

* Total nitrogen-related emissions
forvalues i = 1980/2020 {
    gen totN_grain`i' = NH3_grain`i' + NO_grain`i' + NO3_grain`i'
}

* Total carbon-related / greenhouse gas emissions
forvalues i = 1980/2020 {
    gen totC_grain`i' = N2O_grain`i' + CH4_grain`i' + CO2_grain`i'
}

*******************************************************
* 9. Optional: keep or save output variables
*******************************************************
* keep PAC VL_grain* VW1990 NH3_grain* NO_grain* NO3_grain* ///
*      N2O_grain* CH4_grain* CO2_grain* totN_grain* totC_grain*

* save "production_emission_outputs.dta", replace
