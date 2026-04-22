*******************************************************
* Script: 01_environmental_burden_calculation.do
* Purpose:
*   Calculate trade-embedded environmental burdens,
*   including:
*   - virtual cropland (VL)
*   - virtual blue and green water (VW_b, VW_g, VW)
*   - nitrogen-related emissions (NH3, NO, NO3, N2O)
*   - greenhouse gas emissions (CO2, CH4, N2O)
*
* Input:
*   grain_tran_analy2060_20251209.dta
*
* Notes:
*   - This script uses local input data and should be
*     adapted to the user's working directory.
*   - Units follow the conventions used in the manuscript.
*******************************************************

clear all
set more off

*******************************************************
* 1. Set working directory and load data
*******************************************************
cd "E:/OneDrive/stata/Grain_data"
use grain_tran_analy2060_20251209.dta, clear

*******************************************************
* 2. Define emission factors and constants
*******************************************************

* Nitrogen fertilizer production-related emission factors
local ef_N_prod   = 4.12      // kg N per t fertilizer
local ef_CO2_prod = 1.5       // t CO2 per t fertilizer

* Direct nitrogen loss factors (% of N input)
local EF_NH3    = 11.05
local EF_NO     = 0.53
local EF_leach  = 3.1
local EF_runoff = 6.2
local EF_N2O    = 0.69

* Global warming potentials
local GWP_N2O = 273
local GWP_CH4 = 27.9

* Straw-to-grain ratio
local straw_ratio = 1.1

* Agricultural machinery-related CO2 emissions
local EF_mech_CO2 = 0.0897    // t CO2 per t grain

* Soil respiration and carbon conversion
local soil_resp = 468.72
local C_to_CO2  = 44/12

*******************************************************
* 3. Define years for calculation
*******************************************************
local years 1980 1990 2000 2010 2020

*******************************************************
* 4. Loop over years and calculate environmental burdens
*******************************************************
foreach y of local years {

    di "===== Calculating environmental burdens for year `y' ====="

    * Open-field straw burning share (%)
    if `y' == 1980 local burn = 10
    else if `y' == 1990 local burn = 21
    else if `y' == 2000 local burn = 28
    else if `y' == 2010 local burn = 22
    else if `y' == 2020 local burn = 19

    ***************************************************
    * 4.1 Virtual land and water
    ***************************************************

    * Virtual cropland (million ha)
    gen VL`y' = t`y' * 10^4 * 10^3 / gra`y' / 10^6

    * Virtual blue water and green water (Gm^3)
    gen VW_b`y' = t`y' * 10^4 * 10^3 * wf_blue  / 10^9
    gen VW_g`y' = t`y' * 10^4 * 10^3 * wf_green / 10^9
    gen VW`y'   = VW_b`y' + VW_g`y'

    ***************************************************
    * 4.2 Fertilizer production-related emissions
    ***************************************************

    * NH3 emissions embodied in fertilizer production
    gen NH3_fert_prod`y' = (VL`y' * nrate_average) / 10^3 * ///
                           `ef_N_prod' / 10^3

    * CO2 emissions embodied in fertilizer production
    gen CO2_fert_prod`y' = (VL`y' * nrate_average) * ///
                           `ef_CO2_prod' / 10^3

    ***************************************************
    * 4.3 Direct nitrogen emissions
    ***************************************************

    * NH3 volatilization (Mt N)
    gen NH3_`y' = VL`y' * nrate_average * `EF_NH3' / 100 / 10^3

    * NO emissions (Mt N)
    gen NO_`y'  = VL`y' * nrate_average * `EF_NO' / 100 / 10^3

    * Nitrate-related losses (leaching + runoff, Mt N)
    gen NO3_`y' = VL`y' * nrate_average * ///
                  (`EF_leach' + `EF_runoff') / 100 / 10^3

    ***************************************************
    * 4.4 N2O and CH4 emissions
    ***************************************************

    * Direct N2O emissions converted to CO2-equivalent
    gen N2O_`y' = VL`y' * nrate_average * `EF_N2O' / 100 / 10^3 * `GWP_N2O'

    * Indirect N2O emissions from volatilization and leaching
    gen N2O_indirect`y' = (NH3_`y' * 0.01 + NO3_`y' * 0.0075) * `GWP_N2O'

    * CH4 emissions converted to CO2-equivalent
    gen CH4_`y' = VL`y' * 0.33 * ef_ch4 / 10^3 * `GWP_CH4'

    ***************************************************
    * 4.5 CO2 emissions from straw burning and machinery
    ***************************************************

    * CO2 emissions from open straw burning
    gen CO2bio`y' = t`y' * 10^4 * 10^3 * `straw_ratio' * ///
                    `burn' / 100 * 1342.6 / 10^12

    * CO2 emissions from agricultural machinery use
    gen CO2_mech`y' = t`y' * 10^4 * 10^3 * `EF_mech_CO2' / 10^9

    ***************************************************
    * 4.6 Soil carbon emissions and sink
    ***************************************************

    * Soil respiration-related CO2 emissions
    gen CO2_soilemi`y' = VL`y' / 10^3 * `soil_resp' * 10^7 / 10^6 * `C_to_CO2'

    * Soil carbon sequestration converted to CO2-equivalent
    gen CO2soilsink`y' = 129 * VL`y' / 10^3 * `C_to_CO2'

    ***************************************************
    * 4.7 Aggregate indicators
    ***************************************************

    * Total nitrogen-related emissions
    gen totN_`y' = NH3_`y' + NO_`y' + NO3_`y' + NH3_fert_prod`y'

    * Total gross greenhouse gas emissions
    gen totCemi_`y' = CO2_fert_prod`y' + N2O_`y' + N2O_indirect`y' + ///
                      CH4_`y' + CO2_mech`y' + CO2bio`y'

    * Net greenhouse gas emissions after subtracting soil sink
    gen totC_`y'net = totCemi_`y' - CO2soilsink`y'
}

*******************************************************
* 5. Keep core output variables if needed
*******************************************************
preserve

keep var1 ///
     VL* VW_b* VW_g* VW* ///
     totN_* totCemi_* totC_*net

* Optional: save processed output
* save "environmental_burden_outputs.dta", replace

restore
