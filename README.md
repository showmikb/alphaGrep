# alphaGrep

#Goal : Implementing a python based rule engine
## Request Validator
Takes input a file inputs.csv which contains request entries. The main.py generates an output validating the request against the rule engine. As mentioned
in the problem statement, the rule engine may generate multiple responses for a particular request. Deny rules take precidence over all other rules.

##CSV Matcher
Takes a file1.csv (Golden response) and validates the response of file2.csv for each request that matches.
