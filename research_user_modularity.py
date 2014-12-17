from collections import defaultdict

years = range(2009, 2014)

if __name__ == "__main__":
    years_to_modules = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    with open("themes.csv", encoding="utf8") as themes_file:
        data = [x.strip("\n").split(",") for x in themes_file.readlines()]
        theme_ids_to_names = {int(x[0]): x[1] for x in data}
    # print(theme_ids_to_names)
    users_to_themes = defaultdict(lambda: defaultdict(int))
    for year in years:
        with open("ed/users{0}_edges.csv".format(year)) as connections_file:
            data = [x.strip("\n").split(",") for x in connections_file.readlines()]
            for elem in data:
                if elem[2] == "NULL":
                    continue
                users_to_themes[int(elem[0])][theme_ids_to_names[int(elem[2])]] += int(float(elem[3]))
                users_to_themes[int(elem[1])][theme_ids_to_names[int(elem[2])]] += int(float(elem[3]))
        # print(users_to_themes)
        modularity_to_ids = defaultdict(list)
        ids_to_modularity = {}

        with open("ed/users{0}_nodes.csv".format(year)) as nodes_file:
            data = [x.strip("\n").split(",") for x in nodes_file.readlines()]
            for elem in data:
                ids_to_modularity[int(elem[0])] = int(elem[1])
                modularity_to_ids[int(elem[1])].append(int(elem[0]))
        # print(ids_to_modularity)
        # print(modularity_to_ids)

        for module in modularity_to_ids.keys():
            for user_id in modularity_to_ids[module]:
                for user_topic, topic_count in users_to_themes[user_id].items():
                    years_to_modules[year][module][user_topic] += topic_count

    # print(years_to_modules)
    for year, modules in years_to_modules.items():
        print("YEAR: " + str(year))
        with open("user_modularity_{0}.csv".format(year), "w+", encoding="utf8") as output_file:
            for module, topics in modules.items():
                print("MODULE: " + str(module))
                tops = sorted(topics.items(), key = lambda tup: tup[1], reverse=True)
                print(tops)
                tops_names = [x[0] for x in tops]
                tops_counts = [str(x[1]) for x in tops]
                print(tops_names)
                print(tops_counts)
                output_file.write("\t".join(tops_names) + "\n")
                output_file.write("\t".join(tops_counts) + "\n")