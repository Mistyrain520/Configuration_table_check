import file
import os


slot_dir = u'C:/Users/User/Desktop/log.tar(1)'
slot = file.File.get_file_dir(slot_dir, file_type="")
result = {}
result_count = {}
error_file = {}
find = "me is not defined"
for k in slot:
    # '\\006a29aa-7f4b-46ce-afc9-0ab7a2a36b6b', '\\game.log.2020-08-28.0.log'
    if "log" in k:
        continue
    # if "01d2be1c-58fd-4aef-b0dc-047552fa0234" not in i:
    #     continue
    full_path = slot_dir + k
    tag = []
    number = 0
    with open(full_path, encoding='utf-8', mode="r") as f:
        text = f.readlines()
    for i in range(len(text)):
        if find in text[i]:
            print(k)
        if "Error" in text[i]:
            tag.append(i)
            if text[i] in result_count.keys():
                result_count[text[i]] += 1
                error_file[text[i]] = list(set([k] + error_file[text[i]]))
            else:
                result_count[text[i]] = 1
                error_file[text[i]] = [k]
    # print(tag)
    for j in range(len(tag)):
        if j+1 >= len(tag):
            end = text[tag[j]:len(text)]
        else:
            end = text[tag[j]:tag[j+1]]
        if text[tag[j]] in result.keys():
            if len(end) < len(result[text[tag[j]]]):
                continue
        result[text[tag[j]]] = end
    f.close()
report = 0
name = "report"
filepath = 'C:/Users/User/Desktop/report/' + name + str(report) + '.txt'
while os.path.exists(filepath):
    report += 1
    filepath = 'C:/Users/User/Desktop/report/' + name + str(report) + '.txt'
# x[1] 表示第二个元素，即value
a1 = sorted(result_count.items(), key=lambda x: x[1], reverse=True)
fp = open(filepath, 'wb')
for i in a1:
    for j in result[i[0]]:
        fp.write(j.encode("utf-8"))
    fp.write("\n\n\n出现次数{}-----------------------------------------------\n\n\n".format(i[1]).encode("utf-8"))
    fp.write("\n出现文件-----------------------------------------------\n".encode("utf-8"))
    for m in error_file[i[0]]:
        fp.write(m.encode("utf-8"))
    fp.write("\n\n\nType分割-----------------------------------------------\n\n\n".encode("utf-8"))

fp.close()
# print(result)
# print(result_count)
