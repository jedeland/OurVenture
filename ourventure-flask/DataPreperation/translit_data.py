def transliterate_values(input_dict):
    #Latin-izes unicode values using the library unidecode
    #Extract key value from input dict (argument)
    for k, v in input_dict.items():
        #Type should be list with dicts in, which we will loop over
        #print(type(v))
        for sub_dict in v:
            #  Change name value to be latin readable, remove leading and trailing whitespace
            #  and replace whitespace with dashes
            #  This search matches to any basic latin, or extended latin letter usages in the right side values
            if re.search("[A-Za-z\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F]", sub_dict["name"]):
                pass
            else:
                sub_dict["name"] = unidecode.unidecode_expect_nonascii(sub_dict["name"]).strip().replace(" ", "-")
            # print(sub_dict)
        #After unidecode is done with iteration, reassign list to key in dictionary, use list comprehension to ensure no empty names after transliteration
        input_dict[k] = [i for i in v if not (i["name"] == "")]

        #current_dict = input_dict[k]
    print(input_dict["french"])
    print(input_dict["japanese"])

    print()