INSERT INTO unit_costs (
        resource_desc,
        profit_margin,
        unit_cost,
        unit_cost_margin,
        appx_monthly_cost,
        remarks
    )
VALUES (
        'vCores',
        150,
        0.009530135,
        0.023825338,
        17.39249708,
        '-'
    ),
    (
        'RAM (GB)',
        150,
        0.000442471,
        0.001106176,
        0.807508793,
        '-'
    ),
    (
        'HDD Storage (GB)',
        150,
        1.64374e-05,
        4.10936e-05,
        0.029998292,
        'SATA Storage'
    ),
    (
        'SSD Storage (GB)',
        150,
        0.000164883,
        0.000412207,
        0.30091147,
        'SSD Storage - Recommended to quote'
    ),
    (
        'OBS (GB)',
        150,
        1.08e-04,
        0.000270859,
        0.197726807,
        '-'
    ),
    (
        'Backup Capacity (GB)',
        150,
        6.85399e-05,
        0.00017135,
        0.12508531,
        'Cost of licence only. Exact amout of OBS also need to be added while configuring backup service.'
    ),
    (
        'CCE - per (vCPU)',
        150,
        0.039371003,
        0.098427507,
        71.85208047,
        'For CCE pricing exact amount of worker nodes vCPU is required.'
    ),
    (
        'HSS (Per VM)',
        150,
        0.027438119,
        0.068595298,
        50.07456756,
        '-'
    ),
    (
        'CSDR - (Per VM License)',
        150,
        0.003836734,
        0.009591836,
        7.002040417,
        "Cost is only for license. Resources need to add separately for both AZ's"
    ),
    (
        'CFW - (Per vCPU)',
        150,
        0.002408784,
        0.00602196,
        4.396031115,
        'Per vCPU licence for all the protected ECS'
    ),
    -- TODO: update the first value to correct resource name
    (
        'CFW - (Per vCPU)',
        150,
        0.001844328,
        0.00461082,
        3.365898483,
        'Per vCPU licence for all the protected ECS'
    ),
    (
        'WAF - (Per 100 Mbps)',
        150,
        2.139617309,
        5.349043272,
        3904.801589,
        '1 License support upto 100Mbps bandwidth protection per tenant. If protection requirement is more then 100Mbps, additional licenses need to be added.'
    ),
    (
        'DB as a Service',
        150,
        0.091894977,
        0.229737443,
        167.7083333,
        '-'
    ),
    (
        'HSM/KMS (per Key)',
        150,
        0.003369469,
        0.008423672,
        6.149280834,
        '-'
    ),
    (
        'EIP - Set',
        150,
        0.008680556,
        0.008219178,
        6,
        'These Prices are based on Khazana feedback and can be changed if required.'
    ),
    (
        'Bandwidth - MB',
        150,
        0.010958904,
        0.010958904,
        8,
        'These Prices are based on Khazana feedback and can be changed if required.'
    );