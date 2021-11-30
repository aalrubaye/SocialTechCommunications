import pprint

__author__ = 'Abduljaleel'

# with open('all.txt') as f:
#     lines = [line.rstrip() for line in f]
#
# print (len(lines))
#
# res = []
# [res.append(x) for x in lines if x not in res]
#
# print (len(res))
#
# file = open("url_final.txt", "w")
#
# for element in res:
#     file.write(element + "\n")
# file.close()



with open('machine-learning.txt') as f:
    lines = [line.rstrip() for line in f]


with open('urls.txt') as fff:
    lines_url = [line_url.rstrip() for line_url in fff]

for l in lines :
    if l not in lines_url:
        print (l)



