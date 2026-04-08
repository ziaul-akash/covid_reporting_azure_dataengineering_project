AZURE DATA LAKE GEN 2 STORAGE ACCOUNT
----------------------------------------

Container : 
      --> lookup
              --> dim_country
              --> dim_date
      --> processed
              --> "All processed files"
              
      --> raw 
          -->ecdc
                |--> cases_deaths --> csv file
                |--> country_response --> csv file
                |--> hospital_admissions --> csv file
                |--> testing --> csv file
                |--> case_deaths_uk_ind_only.csv
          -->population
                |-->population_by_age.tsv
