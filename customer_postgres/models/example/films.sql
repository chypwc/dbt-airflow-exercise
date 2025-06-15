{{ config(materialized='table') }}

SELECT * FROM {{ source('destination_db', 'films') }}