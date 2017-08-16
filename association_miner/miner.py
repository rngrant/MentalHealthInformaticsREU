import associations
import datetime
import sys

support_vals = [35,30,25,20]
confidence_vals  = [95,90,85,80]

import os
directories = ['association_rules', 'itemsets']
for dirname in directories:
    if not os.path.exists(dirname):
        os.makedirs(dirname)


for support_val in support_vals:
    for confidence_val in confidence_vals:
        print("starting with support: ",support_val," confidence:", confidence_val,"at ",datetime.datetime.now())
        sys.stdout.flush()

        try:
            print("trying")
            sys.stdout.flush()
            associations.mine_associations("PTSD_model",100,support_val,confidence_val)
            print("didn't error")
            sys.stdout.flush()
        except:
            print("support: ",support_val ," and confidence: ",confidence_val," failed")
            sys.stdout.flush()
        print("finished at :",datetime.datetime.now())
        sys.stdout.flush()


