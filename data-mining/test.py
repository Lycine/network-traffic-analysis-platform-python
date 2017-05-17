# hostnames = ['abc123', 'def456', 'ghi789','ab123','1']  # normallist
# black_hostname_keyword = ['abc', '456','ab1']  # black
#
# for i, a_hostname in enumerate(hostnames):
#     print 'hostname: ' + a_hostname,
#     print ', ' + str(i)
#     for j, black_keyword in enumerate(black_hostname_keyword):
#         print '\tblack_keyword: ' + black_keyword,
#         print ', ' + str(j)
#         if black_keyword not in a_hostname:
#
#             print '\t\tdid not block: ' + a_hostname,
#             print j, len(black_hostname_keyword)
#             if j == len(black_hostname_keyword) - 1:
#                 print 'write'
#                 # break
#         else:
#             print '\t\tblock: ' + a_hostname
#             break




# hostnames = ['abc123', 'def456', 'ghi789','ab123','1']  # normallist
black_hostname_keyword = ['abc', '456','ab1']  # black
a_hostname = 'ac123'
print 'hostname: ' + a_hostname,

for j, black_keyword in enumerate(black_hostname_keyword):
    print '\tblack_keyword: ' + black_keyword,
    print ', ' + str(j)
    if black_keyword not in a_hostname:

        print '\t\tdid not block: ' + a_hostname,
        print j, len(black_hostname_keyword)
        if j == len(black_hostname_keyword) - 1:
            print 'write'
            # break
    else:
        print '\t\tblock: ' + a_hostname
        break
