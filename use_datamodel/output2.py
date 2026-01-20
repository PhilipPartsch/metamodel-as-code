needs_schema_definitions_from_json = "output2.schema.json"

needs_types = [
    dict(directive='aou', title='Assumption of Use', prefix='AOU__', color='#FF0000', style='node'),
    dict(directive='asreq', title='assumed requirement', prefix='ASREQ__', color='#FFA500', style='node'),
    dict(directive='datatype', title='Datatype', prefix='DATATYPE__', color='#FFA500', style='node'),
    dict(directive='parameter', title='Parameter', prefix='PORT__', color='#FFA500', style='node'),
    dict(directive='port', title='Port', prefix='PORT__', color='#FFA500', style='node'),
    dict(directive='sw_arch_dec', title='Software Architecture Decision', prefix='ARCH_DEC__', color='#FFA500', style='node'),
    dict(directive='sw_arch_dia', title='Software Architecture Diagram', prefix='ARCH_DIA__', color='#FFA500', style='node'),
    dict(directive='swreq', title='sw requirement', prefix='SWREQ__', color='#FFA500', style='node'),
    dict(directive='sysreq', title='sys requirement', prefix='SYSREQ__', color='#FFA500', style='node'),
    dict(directive='test_specification', title='test_specification', prefix='TESTSPEC__', color='#00FF00', style='node'),
    dict(directive='unit', title='Unit', prefix='UNIT__', color='#FFA500', style='node'),
]

needs_extra_options = [
    dict(name='safety', description='safety level', schema=dict(type='string', enum=['QM', 'ASIL-A', 'ASIL-B', 'ASIL-C', 'ASIL-D'])),
    dict(name='security', description='security level', schema=dict(type='string', enum=['No', 'Yes'])),
]

needs_extra_links = [
    dict(option='covered_by', incoming='covers', outgoing='covered by', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='covers', incoming='covered by', outgoing='covers', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='datatype', incoming='datatype of', outgoing='datatype', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='provided', incoming='provided by', outgoing='provided', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='required', incoming='required by', outgoing='required', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='satisfies', incoming='satisfied by', outgoing='satisfies', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='verifies', incoming='verified by', outgoing='verifies', copy=True, style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
]

