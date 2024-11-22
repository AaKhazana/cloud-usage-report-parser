INSERT INTO unit_costs (
        resource_name,
        resource_description,
        profit_margin,
        unit_cost,
        unit_cost_margin,
        remarks
    )
VALUES (
        'vcores',
        'vCores',
        0.009530135,
        0.023825338,
        17.39249708,
        '-'
    ),
    (
        'ram',
        'RAM (GB)',
        0.000442471,
        0.001106176,
        0.807508793,
        '-'
    ),
    (
        'hdd-storage',
        'HDD Storage (GB)',
        1.64374e-05,
        4.10936e-05,
        0.029998292,
        'SATA Storage'
    ),
    (
        'ssd-storage',
        'SSD Storage (GB)',
        0.000164883,
        0.000412207,
        0.30091147,
        'SSD Storage - Recommended to quote'
    ),
    (
        'obj-storage',
        'OBS (GB)',
        1.08e-04,
        0.000270859,
        0.197726807,
        '-'
    ),
    (
        'backup-cap',
        'Backup Capacity (GB)',
        6.85399e-05,
        0.00017135,
        0.12508531,
        'Cost of licence only. Exact amout of OBS also need to be added while configuring backup service.'
    ),
    (
        'cce',
        'CCE - per (vCPU)',
        0.039371003,
        0.098427507,
        71.85208047,
        'For CCE pricing exact amount of worker nodes vCPU is required.'
    ),
    (
        'hss',
        'HSS (Per VM)',
        0.027438119,
        0.068595298,
        50.07456756,
        '-'
    ),
    (
        'csdr',
        'CSDR - (Per VM License)',
        0.003836734,
        0.009591836,
        7.002040417,
        "Cost is only for license. Resources need to add separately for both AZ's"
    ),
    (
        'cfw',
        'CFW - (Per vCPU)',
        0.002408784,
        0.00602196,
        4.396031115,
        'Per vCPU licence for all the protected ECS'
    ),
    -- TODO: update the first value to correct resource name
    (
        'cfw',
        'CFW - (Per vCPU)',
        0.001844328,
        0.00461082,
        3.365898483,
        'Per vCPU licence for all the protected ECS'
    ),
    (
        'waf',
        'WAF - (Per 100 Mbps)',
        2.139617309,
        5.349043272,
        3904.801589,
        '1 License support upto 100Mbps bandwidth protection per tenant. If protection requirement is more then 100Mbps, additional licenses need to be added.'
    ),
    (
        'dbaas',
        'DB as a Service',
        0.091894977,
        0.229737443,
        167.7083333,
        '-'
    ),
    (
        'hsm-kms',
        'HSM/KMS (per Key)',
        0.003369469,
        0.008423672,
        6.149280834,
        '-'
    ),
    (
        'eip-set',
        'EIP - Set',
        0.008680556,
        0.008219178,
        6,
        'These Prices are based on Khazana feedback and can be changed if required.'
    ),
    (
        'bandwidth',
        'Bandwidth - MB',
        0.010958904,
        0.010958904,
        8,
        'These Prices are based on Khazana feedback and can be changed if required.'
    );