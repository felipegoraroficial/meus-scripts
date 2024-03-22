with markup as (
    select * ,
    first_value(custoimer_id)
    over(partition by company_name, contact_name
    order by company_namerows between unbounded preceding and undounded following) as result
    from {{source('sources','customers')}}
), removed as (
    select distinct result from markup
), final as  (
    select * from {{source('sources','customers')} where custoimer_id in (select result from removed)}
)
select * from final