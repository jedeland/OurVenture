import re
from unihandecode import Unihandecoder
import unidecode
#Investigate: https://github.com/3aransia/3aransia


def transliterate_values(input_dict):
    #Latin-izes unicode values using the library unidecode
    #Each unicode decoder is created outside of the for loop to save on memory
    #The object is passed to the unihandle_utf function along with the name that is changed if not found to be latin
    ch_decode, kr_decode, ja_decode = Unihandecoder(lang="zh"), Unihandecoder(lang="kr"), Unihandecoder(lang="ja")
    #Extract key value from input dict (argument)
    
    for k, v in input_dict.items():
        #Type should be list with dicts in, which we will loop over
        #print(type(v))
        for sub_dict in v:
            #  Change name value to be latin readable, remove leading and trailing whitespace
            #  and replace whitespace with dashes
            #  This search matches to any basic latin, or extended latin letter usages in the right side values
            #  For asian languages, uses the unihandecode provided with the GNU licence 
            if re.search("[A-Za-z\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F]", sub_dict["name"]):
                pass
            #The possible language codes are: ["zh", "ja", "ka"]. See: https://github.com/miurahr/unihandecode/blob/master/src/unihandecode/__init__.py
            elif k.lower() == "chinese":
                sub_dict["name"] = unihande_utf(sub_dict["name"], ch_decode)
            elif k.lower() == "korean":
                sub_dict["name"] = unihande_utf(sub_dict["name"], kr_decode)
            elif k.lower() == "japanese":
                sub_dict["name"] = unihande_utf(sub_dict["name"], ja_decode)
            else:
                sub_dict["name"] = unidecode.unidecode_expect_nonascii(sub_dict["name"]).strip().replace(" ", "-")
                #If not translateable by unihande, then use unidecode
            #TODO: check arabic transliterations 
            # print(sub_dict)
        #After unidecode is done with iteration, reassign list to key in dictionary, use list comprehension to ensure no empty names after transliteration
        print("After the conversions ...")
        input_dict[k] = [i for i in v if not (i["name"] == "")]

        #current_dict = input_dict[k]
    return input_dict

def unihande_utf(name_value, decoder):
    return decoder.decode(name_value).strip().replace(" ", "-")