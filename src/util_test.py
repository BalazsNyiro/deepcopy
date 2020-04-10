def spirals_letter_e(): return {
    (1, 5): [(1, 5), (1, 6), (2, 6), (2, 5), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (2, 3), (1, 3)],
    (1, 9): [(1, 9), (1, 10), (0, 10), (0, 9), (0, 8), (1, 8), (2, 8), (2, 9), (2, 10), (2, 11), (1, 11)],
    (1, 12): [(1, 12), (2, 12), (2, 13)],
    (2, 1): [(2, 1), (3, 1), (3, 2), (2, 2), (1, 2)],
    (3, 9): [(3, 9), (3, 10)],
    (4, 12): [(4, 12), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (6, 14), (5, 14), (4, 14)],
    (5, 6): [(5, 6), (6, 6), (6, 7), (5, 7), (4, 7), (4, 6)],
    (6, 1): [(6, 1), (5, 1), (5, 2), (6, 2), (7, 2), (7, 1), (7, 0), (6, 0), (5, 0), (4, 0), (4, 1), (4, 2), (4, 3), (5, 3)],
    (7, 12): [(7, 12), (7, 13)],
    (7, 14): [(7, 14)],
    (8, 6): [(8, 6), (9, 6), (9, 7), (8, 7), (7, 7), (7, 6)],
    (9, 1): [(9, 1), (9, 2), (10, 2), (10, 1), (10, 0), (9, 0), (8, 0), (8, 1), (8, 2), (8, 3), (9, 3)],
    (9, 13): [(9, 13), (10, 13), (10, 12), (9, 12), (8, 12), (8, 13), (8, 14), (9, 14), (10, 14), (11, 14), (11, 13), (11, 12), (11, 11), (10, 11)],
    (11, 1): [(11, 1), (11, 2), (12, 2)],
    (12, 5): [(12, 5), (12, 6), (11, 6), (11, 5), (11, 4), (12, 4), (13, 4), (13, 5), (13, 6), (13, 7), (12, 7), (11, 7), (10, 7), (10, 6), (10, 5), (10, 4), (10, 3), (11, 3), (12, 3)],
    (12, 11): [(12, 11), (12, 12)],
    (12, 13): [(12, 13)]
}

def letter_e_string():
    return ( "    OOOOOOO   "
             "  OOOOOOOOOO  "
             " OOOOOOOOOOOO "
             " OOOOO  OOOOO "
             "OOOO      OOOO"
             "OOOO      OOOO"
             "OOOOOOOOOOOOOO"
             "OOOOOOOOOOOOOO"
             "OOO           "
             "OOOO          "
             "OOOO          "
             " OOOOOO   OOO "
             " OOOOOOOOOOOO "
             "  OOOOOOOOOOO "
             "    OOOOOOOO  ")


# https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method/39606065#39606065
def tearDown(Self, Prg):
    def list2reason(exc_list):
        if exc_list and exc_list[-1][0] is Self:
            return exc_list[-1][1]

    Result = Self.defaultTestResult()  # these 2 methods have no side effects
    Self._feedErrorsToResult(Result, Self._outcome.errors)
    Error = list2reason(Result.errors)
    Failure = list2reason(Result.failures)
    Ok = not Error and not Failure
    Prg["TestResults"].append({"status_ok": Ok, "Error": Error, "Failure": Failure})

def result_all(Prg):
    print("TestResults: ")
    for TestResult in Prg["TestResults"]:
        print(TestResult)
