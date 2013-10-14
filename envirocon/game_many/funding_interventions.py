autoshocks = {
    'funding_interventions': {
        1: {'choices': set(['water-supply-low', 'sanitation-low',
                            'waste-low']),
            'text': (
                """At least 27 districts have been affected by cholera """
                """since January with 6,024 cases and 350 deaths recorded,"""
                """ according to the Ministry of Public Health. Poor """
                """ latrine coverage and unsafe drinking water are helping """
                """to fuel a cholera outbreak affecting many areas of the """
                """country. There is a higher concentration in refugee """
                """camps in the north.""")},

        2: {'choices': set(['timber-low']),
            'text': (
                """The head of the UN Security Council sanctions """
                """committee has praised the government of Nimpala for """
                """efforts to assess potential for regulatory targets in """
                """the timber trades that could lead to the lifting of """
                """sanctions. As part of efforts to exercise full control """
                """over the timber sector, the report suggests that the """
                """forestry sector could generate between $15 and $20 """
                """million a year and some 8,000 new jobs if brought """
                """under better management and formal sector jobs. The """
                """report also shows significant timber products """
                """continuing to flow into county B.""")},

        3: {'choices': set(['tenure-low']),
            'text': (
                """Leading reformists are worried the right mechanisms """
                """to address land rights are still not in place.Most """
                """lost their land deeds during the war, or had """
                """traditional verbal agreements that have since been """
                """broken. Land ownership requires an owner to have a """
                """land deed. But a parallel system of traditional law, """
                """based on verbal agreement, is also prevalent. The """
                """government established a Land Commission to suggest """
                """recommendations and responses to conflicts over land """
                """sales, insecure land tenure and to modernize the """
                """country's land laws - supported by international """
                """donors including the World Bank. But some say while """
                """progress is being made, others argue more needs to be """
                """done on a village-to-village basis.""")},

        4: {'choices': set(['tenure-high']),
            'text': (
                """Some 120 long-displaced farmers returned this week """
                """to a plantation in western Nimpala to reclaim land """
                """that was given up during the civil war. Fighting has """
                """been frequent as seen in one example of organized """
                """groups attacking conveys which were bring returnees to """
                """farms, according to the UN Office for the Coordination """
                """of Humanitarian Affairs (OCHA). The ambush and ensuing """
                """unrest, in which at least two people died, forced """
                """hundreds of people to flee their homes and take refuge """
                """in a local government building for several days. UN """
                """aid agencies provided food and other assistance to the """
                """displaced. Much of this unrest is attributed to recent """
                """government land reforms and resulting resettlement """
                """programs, with increased number of IDP's are returning """
                """quickly after the conflict to previously occupied """
                """lands.""")},

        5: {'choices': set(['nomadic-low']),
            'text': (
                """Amid deadly clashes with farmers and expulsion """
                """orders by state authorities, thousands of nomadic """
                """herders do not know where to turn. Tensions linked to """
                """pastoralist - farmer disputes have been mounting in """
                """recent months in several states. Local authorities """
                """expelled 700 pastoralists in the central and northern """
                """areas after national efforts were launched to shift """
                """track and control migratory paths. The livelihoods of """
                """some roughly estimated 15 million pastoralists in are """
                """threatened by decreasing access to water and """
                """pasture.""")},

        6: {'choices': set(['habitat-high']),
            'text': (
                """The results of a new monitoring system co-managed """
                """between the international community and the Nimpala """
                """government revealed that local regional councils in """
                """the north west continue the export of illegally """
                """harvested precious hardwoods from the remaining """
                """forested areas of the northern zones. The report found """
                """that the revenue is used to keep the local """
                """municipalities funded. An investigation by Global """
                """Witness (GW), which monitor the illegal exploitation """
                """and trade of natural resources, found that in the """
                """months after the announcement of tighter monitoring """
                """and regulation, that there was a significant increase """
                """in harvests and trade across the northern border. The """
                """report also identified charcoal profits are supporting """
                """militias and rebel groups around refugee camps in the """
                """northern border region.""")},

        7: {'choices': set(['capacity-high']),
            'text': (
                """The national government has cooperated with """
                """international agencies to increase the facilitate """
                """consultation, coordination and cooperation among """
                """stakeholders in order to mainstream environmental """
                """considerations within government strategies. They have """
                """also made progress contributing to the development and """
                """institutionalization of environmental laws and """
                """regulations through training and technical support in """
                """the development of an integrated environmental legal, """
                """regulatory and policy framework. An essential step """
                """throughout the development of this framework is an """
                """extensive public consultation process with national """
                """and international stakeholders and to """
                """institutionalization of Environmental Impact """
                """Assessment (EIA) and Pollution Control through """
                """training and technical support in the development and """
                """effective implementation of Environmental Impact """
                """Assessment policies, procedures and legislation.""")},
    },

    'donors_conference': {
        1: {'choices': set(['deforestation-med']),
            'text': (
                """Internally displaced people (IDPs) in Nimpala are set to """
                """enjoy greater protection under a national policy that """
                """also aims to prevent future displacement and to fulfil """
                """the country's obligations under international IDP law. """
                """The draft policy broadens the definition to cover """
                """displacement due to political and resource-based """
                """conflict and natural disasters, as well as development """
                """projects that force people from their homes without """
                """proper relocation.""")},

        2: {'choices': set(['tenure-med']),
            'text': (
                """With an increase in returning IDPs, the new legal """
                """framework has enabled the courts to address a far """
                """greater number of cases.""")},
    },
}


def funding_autoshocks(game, funded_interventions):
    choices = set(funded_interventions.keys())
    return "\n\n".join([shock['text']
                        for shock in autoshocks[game].values()
                        if shock['choices'].intersection(choices)])


# calculate points for funding choices (Funding Interventions and Donor
# Conference)
def funding_points(funded_interventions, week=4):
    value = {
        'water-supply-high': 1,
        'water-supply-med': 2,
        'water-supply-low': 3,

        'sanitation-high': 1,
        'sanitation-med': 2,
        'sanitation-low': 3,

        'waste-high': 2,
        'waste-med': 1,
        'waste-low': 3,

        'timber-high': 2,
        'timber-med': 2,
        'timber-low': 1,

        'deforestation-high': 2,
        'deforestation-med': 1,
        'deforestation-low': 3,

        'tenure-high': 6,
        'tenure-med': 3,
        'tenure-low': 1,

        'nomadic-high': 3,
        'nomadic-med': 2,
        'nomadic-low': 1,

        'agriculture-high': 2,
        'agriculture-med': 5,
        'agriculture-low': 1,

        'desertification-high': 3,
        'desertification-med': 2,
        'desertification-low': 1,

        'habitat-high': 3,
        'habitat-med': 2,
        'habitat-low': 1,

        'water-high': 3,
        'water-med': 1,
        'water-low': 6,

        'capacity-high': 1,
        'capacity-med': 2,
        'capacity-low': 6,
    }
    if week == 6:
        value['timber-med'] = 1
        value['timber-low'] = 3

        value['tenure-high'] = 3
        value['tenure-med'] = 1
        value['tenure-low'] = 2

        value['nomadic-high'] = 1
        value['nomadic-low'] = 3

        value['agricultural-med'] = 1
        value['agricultural-low'] = 3

        value['water-low'] = 3
        value['water-high'] = 2

        value['capacity-low'] = 3

        value['desertification-high'] = 2
        value['desertification-med'] = 1
        value['desertification-low'] = 3

    points = sum([value[intervention]
                 for intervention in funded_interventions])
    return points
