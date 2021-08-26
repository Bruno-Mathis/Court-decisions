import sys
manual = sys.argv[1]    
auto = sys.argv[2]    
decisions_manual = []
manual_legal_references = []
auto_legal_references = []

with open(manual, encoding = 'utf-8') as f:
    content = f.read().splitlines()
    for line in content:
        first_semi_colon = line.find(";")
        identifier = line[0:first_semi_colon]
        decisions_manual.append(identifier)
        remainder = line[first_semi_colon+1:]
        second_semi_colon = remainder.find(";")
        article = remainder[0:second_semi_colon]
        instrument = remainder[second_semi_colon+1:]
        legal_reference = [identifier, article, instrument]
        manual_legal_references.append(legal_reference)

print("")
with open(auto, encoding = 'utf-8') as g:
    content = g.read().splitlines()
    for line in content:
        first_semi_colon = line.find(";")
        identifier = line[0:first_semi_colon]
        if identifier in decisions_manual:
            remainder = line[first_semi_colon+1:]
            second_semi_colon = remainder.find(";")
            article = remainder[0:second_semi_colon]
            instrument = remainder[second_semi_colon+1:]
            legal_reference = [identifier, article, instrument]
            auto_legal_references.append(legal_reference)

Correct       = 0
FalseNegative = 0
FalsePositive = 0

for reference in manual_legal_references:
    if reference in auto_legal_references:
    #if reference in auto_legal_references:
        Correct += 1
        print("Correct"+";"+reference[0]+";"+reference[1]+";"+reference[2])
    #else:
    if reference not in auto_legal_references:
        FalseNegative += 1
        print("False negative"+";"+reference[0]+";"+reference[1]+";"+reference[2])
print("")

for reference in auto_legal_references:
    if reference not in manual_legal_references:
            FalsePositive += 1
            print("False positive"+";"+reference[0]+";"+reference[1]+";"+reference[2])                

print("")
Recall = Correct / (Correct + FalseNegative)
Precision = Correct / (Correct + FalsePositive)
FMeasure = (2 * Precision * Recall) / (Precision + Recall)

print("Recall = %.4f" % Recall)
print("Precision = %.4f" % Precision)
print("F-Measure = %.4f" % FMeasure)