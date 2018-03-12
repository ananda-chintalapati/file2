from matilda_env.vz.onboarding import key_generator as kg

def test_kg_job():
    resp = kg.generate_keys('ABCD', 'ABCD_Policy.json')
    print 'Test response %r ' % resp

test_kg_job()