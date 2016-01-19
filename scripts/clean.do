*******************************************************************************
*																			*
* PROJECT: 	CAG																* 
*																			*
* PURPOSE: Construct Useable Dataset for 								    *
*																			*
* DATE: January 14th, 2016												    *
*																			*
* AUTHOR:  Raahil Madhok 													*
*																				
********************************************************************************

********************************************************************************
*1. SET ENVIRONMENT
********************************************************************************

// Settings
clear all
pause on
cap log close
set more off

//Set Directory
/*---------------------------------------------------------------------------
Sets path directory for each users computer so program can run on any device.
Toggle local value when switching user
----------------------------------------------------------------------------*/
local RAAHIL 1
local OTHER  0

if `RAAHIL' {
	local ROOT /Users/rmadhok/Dropbox (CID)/CAG/
	local DATA `ROOT'/data
	}

if `OTHER' {
	local ROOT
	local DATA
	//[INSERT LOCALS FOR FILE PATHS]
	}


********************************************************************************
*2. CLEAN DATA
********************************************************************************
//Import Data into Stata
import delimited using "`DATA'/raw/state_cag.csv", clear

//clean questions
replace v1 = subinstr(v1,".", "",.) 

//Input district names
gen district = v2 if regexm(v2,"Key Indicators")
order district, first
replace district = subinstr(district, "- Key Indicators", "", .)
replace v2 = regexr(v2, "- Key Indicators", "")
replace district = trim(district)
replace v2 = trim(v2)
carryforward district, replace

//clean vars
drop if inlist(v1, "", "Villages covered", "Health Facilities covered", ///
	"Health programmes at village level", "Accessibility of health facility (%)", ///
	"Availability of Health Infrastructure, Staff and Services at (%)", ///
	"1Health programmes at village level")
drop if inlist(v1, "Sub Divisional Hospital (SDH)", "District Hospital (DH)", ///
	"Community Health Centre (CHC)", "Sub-Health Centre", "Primary Health Centre (PHC)")
drop if regexm(v1, "Out of")
drop if regexm(v1, "out of")
drop if v1 == "Indicators"
replace v3 = "" if district == "Chandigarh"
replace v3 = v4 if district == "Chandigarh"
replace v4 = v5 if district == "Chandigarh"
replace v5 = "" if district == "Chandigarh"
drop v5
replace v4 = v3 if district == "Chamba"
replace v3 = v2 if district == "Chamba"
replace v2 = "" if district == "Chamba"
egen v1_ = concat(v1 v2)
drop v1 v2
ren v1_ v1
replace v1 = subinstr(v1, ".", "",.)
drop if v1 == "5"
drop if v1 == "Availability of Health Infrastructure, Staff and Services (%)"
replace v3 = "571" if v1 == "Villages with Sub-Health Centre within 3 km  571"
replace v1 = "Villages with Sub-Health Centre within 3 km" ///
	if v1 == "Villages with Sub-Health Centre within 3 km  571"
replace v1 = "SDHs having Ultrasound facility" if ///
	v1 == "NA SDHs having Ultrasound facility" | v1 == "NASDHs having Ultrasound facility"

//prepare reshape
order district v1 v3 v4
encode district, gen(dist_id)
sort dist_id v1
bys dist_id: gen question = _n
ren v3 dlhs4_
ren v4 dlhs3_ 

//outsheet variable list
preserve
keep question v1
bys question: keep if _n==1
export delimited using "`DATA'/raw/variable_list.csv", replace
restore

//reshape
drop v1
reshape wide dlhs3 dlhs4, i(dist_id) j(question)


//Prepare for analysis
foreach var of varlist dlhs* {
	replace `var' = "" if inlist(`var', "NA", "na", "N.A.", "N.A", "N A", ///
	"Na", "-", "--", "-----")
	destring `var', replace
	}

//get state names
tempfile temp
save "`temp'"
import delimited using "`DATA'/raw/state_names.csv", clear
drop in 1
ren v1 district
ren v2 state
duplicates drop district, force
merge 1:1 district using "`temp'"
keep if _merge == 2 | _merge == 3

//outsheet and save
save "`DATA'/clean/district_dlhs.dta", replace
export delimited using "`DATA'/clean/district_dlhs.csv", replace











