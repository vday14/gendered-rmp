import math
import json
import urllib
import sys
import os

doc_counts = {}

def indexDocument(terms_dict, invertedIndex, docId):

    docId = int(docId)

    for word in terms_dict:

        if docId not in doc_counts:

            doc_counts[docId] = int(terms_dict[word])

        else:
            doc_counts[docId] += int(terms_dict[word])

        if word not in invertedIndex:

            invertedIndex[word] = {}
            invertedIndex[word][docId] = int(terms_dict[word])

        else:

            invertedIndex[word][docId] = int(terms_dict[word])


def retrieveDocuments(query_dict, invertedIndex, numDocs):

    relevantDocs = {}

    cosine_sim = {}
    query_sum = 0

    for word in query_dict:

        if word not in invertedIndex:
            continue

        idf = math.log10(numDocs / len(invertedIndex[word]))

        normalized_query_tf = float(query_dict[word]) / len(query_dict)

        query_tfidf = idf * normalized_query_tf

        query_sum += pow(query_tfidf, 2)

        for doc in invertedIndex[word]:

            normalized_tf = float(invertedIndex[word][doc]) / doc_counts[doc]
            tfidf = idf * normalized_tf

            if doc in cosine_sim:

                cosine_sim[doc]["dot_product"] += tfidf * query_tfidf
                cosine_sim[doc]["doc_sums"] += pow(tfidf, 2)

            else:
                cosine_sim[doc] = {}
                cosine_sim[doc]["dot_product"] = tfidf * query_tfidf
                cosine_sim[doc]["doc_sums"] = pow(tfidf, 2)


    for doc in cosine_sim:

        cosine_sim_calc = cosine_sim[doc]["dot_product"] / (math.sqrt(cosine_sim[doc]["doc_sums"]) * math.sqrt(query_sum))

        relevantDocs[doc] = cosine_sim_calc


    return relevantDocs



def main():


    correct_genders = {}
    prof_names = {}
    prof_terms = {}
    prof_ids = []
    num_docs = 0
    num_correct = 0

    with open('profTerms.json') as data_file:
        json_obj = json.load(data_file)

        num_docs = len(json_obj)
        print(num_docs)


        for prof_id in json_obj:

            correct_genders[int(prof_id)] = int(json_obj[prof_id]["gender"])

            prof_names[int(prof_id)] = json_obj[prof_id]["name"]

            prof_terms[int(prof_id)] = json_obj[prof_id]["terms"]

            prof_ids.append(int(prof_id))

    profs = {}

    for query in prof_ids:

        invertedIndex = {}

        for prof_id in prof_ids:

            if (prof_id != query):

                indexDocument(prof_terms[prof_id], invertedIndex, prof_id)

        rt = retrieveDocuments(prof_terms[query], invertedIndex, num_docs)

        print(prof_names[int(query)] + " " + str(correct_genders[int(query)]) + "\n")

        top = 1
        top_10 = {}
        top_gender = -1

        num_female = 0
        num_male = 0

        for k in sorted(rt, key=rt.get, reverse=True):

            top_10[k] = rt[k]
            if top == 1:
                top_gender = correct_genders[k]

            if correct_genders[k] == 0:
                num_male += 1
            else:
                num_female += 1

            print(str(top) + " " + prof_names[k] + " " + str(correct_genders[k]) + " " + str(rt[k]) + "\n")
            if top == 10:
                break

            top += 1

        prof = {"name": prof_names[int(query)],
                "gender": correct_genders[int(query)],
                "predicted_gender": top_gender,
                "top_10": top_10
                }

        profs[query] = prof

        if num_male > num_female:
            top_gender = 0
        else:
            top_gender = 1

        if (correct_genders[int(query)] == top_gender):
            num_correct += 1

        print("NUMBER CORRECT: " + str(num_correct))

    profs["accuracy"] = num_correct / num_docs
    profs["num_correct"] = num_correct

    output = json.dumps(profs, indent=4)
    f = open("profQueries.json", "w")
    f.write(output)


if __name__ == "__main__":
    main()